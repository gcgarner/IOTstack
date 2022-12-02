
## Resources

*   Search github [issues](https://github.com/SensorsIot/IOTstack/issues?q=).

    - Closed issues or pull-requests may also have valuable hints.

*   Ask questions on [IOTStack Discord](https://discord.gg/ZpKHnks). Or report
    how you were able to fix a problem.

*   There are over 40 gists about IOTstack. These address a diverse range of
    topics from small convenience scripts to complete guides. These are
    individual contributions that aren't reviewed.

    You can add your own keywords into the search:
    [https://gist.github.com/search?q=iotstack](https://gist.github.com/search?q=iotstack)

## FAQ

!!! danger "Breaking update"
    A change done 2022-01-18 will require [manual steps](
    ../Updates/migration-network-change.md)
    or you may get an error like:  
    `ERROR: Service "influxdb" uses an undefined network "iotstack_nw"`

## Device Errors

If you are trying to run IOTstack on non-Raspberry Pi hardware, you will probably get the following error from `docker-compose` when you try to bring up your stack for the first time:

```
Error response from daemon: error gathering device information while adding custom device "/dev/ttyAMA0": no such file or directory
```

> You will get a similar message about any device which is not known to your hardware.

The `/dev/ttyAMA0` device is the Raspberry Pi's built-in serial port so it is guaranteed to exist on any "real" Raspberry Pi. As well as being referenced by containers that can actually use the serial port, `ttyAMA0` is often employed as a placeholder.

Examples:

* Node-RED flows can use the `node-red-node-serialport` node to access the serial port. This is an example of "actual use";
* The Zigbee2MQTT container employs `ttyAMA0` as a placeholder. This allows the container to start. Once you have worked out how your Zigbee adapter appears on your system, you will substitute your adapter's actual device path. For example:

	``` yaml
	- "/dev/serial/by-id/usb-Texas_Instruments_TI_CC2531_USB_CDC___0X00125B0028EEEEE0-if00:/dev/ttyACM0"
	```

The simplest approach to solving "error gathering device information" problems is just to comment-out every device mapping that produces an error and, thereafter, treat the comments as documentation about what the container is expecting at run-time. For example, this is the devices list for Node-RED:

``` yaml
  devices:
    - "/dev/ttyAMA0:/dev/ttyAMA0"
    - "/dev/vcio:/dev/vcio"
    - "/dev/gpiomem:/dev/gpiomem"
```   

Those are, in turn, the Raspberry Pi's:

* serial port
* videoCore multimedia processor
* mechanism for accessing GPIO pin headers

If none of those is available on your chosen platform (the usual situation on non-Pi hardware), commenting-out the entire block is appropriate:

``` yaml
# devices:
#   - "/dev/ttyAMA0:/dev/ttyAMA0"
#   - "/dev/vcio:/dev/vcio"
#   - "/dev/gpiomem:/dev/gpiomem"
```

You interpret each line in a device map like this:

``` yaml
    - "«external»:«internal»"
```

The *«external»* device is what the platform (operating system plus hardware) sees. The *«internal»* device is what the container sees. Although it is reasonably common for the two sides to be the same, this is **not** a requirement. It is usual to replace the *«external»* device with the actual device while leaving the *«internal»* device unchanged.

Here is an example. On macOS, a CP2102 USB-to-Serial adapter shows up as:

```   
/dev/cu.SLAB_USBtoUART
```

Assume you are running the Node-RED container in macOS Docker Desktop, and that you want a flow to communicate with the CP2102. You would change the service definition like this:

``` yaml
  devices:
    - "/dev/cu.SLAB_USBtoUART:/dev/ttyAMA0"
#   - "/dev/vcio:/dev/vcio"
#   - "/dev/gpiomem:/dev/gpiomem"
```

In other words, the *«external»* (real world) device `cu.SLAB_USBtoUART` is mapped to the *«internal»* (container) device `ttyAMA0`. The flow running in the container is expecting to communicate with `ttyAMA0` and is none-the-wiser.

## Needing to use `sudo` to run docker commands

You should never (repeat **never**) use `sudo` to run docker or docker compose commands. Forcing docker to do something with `sudo` almost always creates more problems than it solves. Please see [What is sudo?](https://sensorsiot.github.io/IOTstack/Basic_setup/What-is-sudo/) to understand how `sudo` actually works.

If `docker` or `docker-compose` commands *seem* to need elevated privileges, the most likely explanation is incorrect group membership. Please read the [next section](#dockerGroup) about errors involving `docker.sock`. The solution (two `usermod` commands) is the same.

If, however, the current user *is* a member of the `docker` group *but* you still get error responses that *seem* to imply a need for `sudo`, it implies that something fundamental is broken. Rather than resorting to `sudo`, you are better advised to rebuild your system.

## Errors involving `docker.sock` { #dockerGroup }

If you encounter permission errors that mention `/var/run/docker.sock`, the most likely explanation is the current user (usually "pi") not being a member of the "docker" group.

You can check membership with the `groups` command:

``` console
$ groups
pi adm dialout cdrom sudo audio video plugdev games users input render netdev bluetooth lpadmin docker gpio i2c spi
```

In that list, you should expect to see both `bluetooth` and `docker`. If you do not, you can fix the problem like this:

``` console
$ sudo usermod -G docker -a $USER
$ sudo usermod -G bluetooth -a $USER
$ exit
```

The `exit` statement is **required**. You must logout and login again for the two `usermod` commands to take effect. An alternative is to reboot.

## System freezes or SSD problems

You should read this section if you experience any of the following problems:

* Apparent system hangs, particularly if Docker containers were running at the time the system was shutdown or rebooted;
* Much slower than expected performance when reading/writing your SSD; or
* Suspected data-corruption on your SSD.

### Try a USB2 port

Start by shutting down your Pi and moving your SSD to one of the USB2 ports. The slower speed will often alleviate the problem.

Tips:

1. If you don't have sufficient control to issue a shutdown and/or your Pi won't shut down cleanly:

	- remove power
	- move the SSD to a USB2 port
	- apply power again.

2. If you run "headless" and find that the Pi responds to pings but you can't connect via SSH:

	- remove power
	- connect the SSD to a support platform (Linux, macOS, Windows)
	- create a file named "ssh" at the top level of the boot partition
	- eject the SSD from your support platform
	- connect the SSD to a USB2 port on your Pi
	- apply power again.

### Check the `dhcpcd` patch

Next, verify that the [dhcpcd patch](https://sensorsiot.github.io/IOTstack/Basic_setup/#patch-1-restrict-dhcp) is installed. There seems to be a timing component to the deadlock which is why it can be *alleviated*, to some extent, by switching the SSD to a USB2 port.

If the `dhcpcd` patch was not installed but you have just installed it, try returning the SSD to a USB3 port.

### Try a quirks string

If problems persist even when the `dhcpcd` patch is in place, you *may* have an SSD which isn't up to the Raspberry Pi's expectations. Try the following:

1. If your IOTstack is running, take it down.
2. If your SSD is attached to a USB3 port, shut down your Pi, move the SSD to a USB2 port, and apply power.
3. Run the following command:

	``` console
	$ dmesg | grep "\] usb [[:digit:]]-"
	```
 
	In the output, identify your SSD. Example:

	```
	[    1.814248] usb 2-1: new SuperSpeed Gen 1 USB device number 2 using xhci_hcd
	[    1.847688] usb 2-1: New USB device found, idVendor=f0a1, idProduct=f1b2, bcdDevice= 1.00
	[    1.847708] usb 2-1: New USB device strings: Mfr=99, Product=88, SerialNumber=77
	[    1.847723] usb 2-1: Product: Blazing Fast SSD
	[    1.847736] usb 2-1: Manufacturer: Suspect Drives
	```

	In the above output, the second line contains the Vendor and Product codes that you need:

	* `idVendor=f0a1`
	* `idProduct=f1b2`

4. Substitute the values of *«idVendor»* and *«idProduct»* into the following command template:

	``` console
	sed -i.bak '1s/^/usb-storage.quirks=«idVendor»:«idProduct»:u /' /boot/cmdline.txt
	```

	This is known as a "quirks string". Given the `dmesg` output above, the string would be:

	``` console
	sed -i.bak '1s/^/usb-storage.quirks=f0a1:f1b2:u /' /boot/cmdline.txt
	```
	
	Make sure that you keep the <kbd>space</kbd> between the `:u` and `/'`. You risk breaking your system if that <kbd>space</kbd> is not there.

5. Run the command you prepared in step 4 using `sudo`:

	``` console
	$ sudo sed -i.bak '1s/^/usb-storage.quirks=f0a1:f1b2:u /' /boot/cmdline.txt
	```
	
	The command:
	
	- makes a backup copy of `/boot/cmdline.txt` as `/boot/cmdline.txt.bak`
	- inserts the quirks string at the start of `/boot/cmdline.txt`.

	You can confirm the result as follows:
	
	* display the original (baseline reference):

		```
		$ cat /boot/cmdline.txt.bak
		console=serial0,115200 console=tty1 root=PARTUUID=06c69364-02 rootfstype=ext4 fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
		```

	* display the modified version:

		```
		$ cat /boot/cmdline.txt
		usb-storage.quirks=f0a1:f1b2:u console=serial0,115200 console=tty1 root=PARTUUID=06c69364-02 rootfstype=ext4 fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
		```

6. Shutdown your Pi.
7. Connect your SSD to a USB3 port and apply power.

Note:

* If your Pi fails to boot and you suspect that the quirks string might be the culprit, don't forget that you can always mount the `boot` partition on a support host (Linux, macOS, Windows) where you can undo the change by replacing `cmdline.txt` with `cmdline.txt.bak`.

There is more information about this problem [on the Raspberry Pi forum](https://forums.raspberrypi.com/viewtopic.php?t=245931&sid=66012d5cf824004bbb414cb84874c8a4).

## Getting a clean slate

If you create a mess and can't see how to recover, try proceeding like this:

``` console
$ cd ~/IOTstack
$ docker-compose down
$ cd
$ mv IOTstack IOTstack.old
$ git clone https://github.com/SensorsIot/IOTstack.git IOTstack
```

In words:

1. Be in the right directory.
2. Take the stack down.
3. The `cd` command without any arguments changes your working directory to
   your home directory (variously known as `~` or `$HOME` or `/home/pi`).
4. Move your existing IOTstack directory out of the way. If you get a
   permissions problem:

    * Re-try the command with `sudo`; and
    * Read [a word about the `sudo` command](What-is-sudo.md). Needing `sudo`
      in this situation is an example of over-using `sudo`.

5. Check out a clean copy of IOTstack.

Now, you have a clean slate and can start afresh by running the menu:

``` console
$ cd ~/IOTstack
$ ./menu.sh
```

The `IOTstack.old` directory remains available as a reference for as long as
you need it. Once you have no further use for it, you can clean it up via:

``` console
$ cd
$ sudo rm -rf ./IOTstack.old # (1)
```

1. The `sudo` command is needed in this situation because some files and
   folders (eg the "volumes" directory and most of its contents) are owned by
   root.
