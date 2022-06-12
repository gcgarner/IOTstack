# Pi-hole

Pi-hole is a fantastic utility to reduce ads.

## References { #references }

* [Pi-hole on GitHub](https://github.com/pi-hole/docker-pi-hole)
* [Pi-hole on Dockerhub](https://hub.docker.com/r/pihole/pihole)
* [Pi-hole environment variables](https://github.com/pi-hole/docker-pi-hole#environment-variables)

## Environment variables  { #envVars }

In conjunction with controls in Pi-hole's web GUI, environment variables govern much of Pi-hole's behaviour. If you are running new menu (master branch), the variables are inline in `docker-compose.yml`. If you are running old menu, the variables will be in:

```
~/IOTstack/services/pihole/pihole.env
```

> There is nothing about old menu which *requires* the variables to be stored in the `pihole.env` file. You can migrate everything to `docker-compose.yml` if you wish.

Pi-hole's authoritative list of environment variables can be found [here](https://github.com/pi-hole/docker-pi-hole#environment-variables). Although many of Pi-hole's options can be set through its web GUI, there are two key advantages to using environment variables:

1. If you ever need to reset Pi-hole by [erasing its persistent storage area](#cleanSlate), configuration options set using environment variables will persist while those set through the GUI may be lost; and
2. On at least two occasions in its history, Pi-hole upgrades have had the effect of wiping configuration options set through the GUI, whereas options set using environment variables survived. 

### Admin password { #adminPassword }

The first time Pi-hole is launched, it checks for the `WEBPASSWORD` environment variable. If found, the right hand side becomes the administrative password.

You can set the value of `WEBPASSWORD` in the IOTstack menu by:

1. Placing the cursor on top of "pihole".
2. If Pi-hole is not already selected as a container, press <kbd>space</kbd> to select it.
3. Press the right arrow, and then
4. Choose "PiHole Password Options".

From there, you have the choice of:

* *Use default password for this build*

	Choosing this option results in:

	```yaml
	- WEBPASSWORD=IOtSt4ckP1Hol3
	```

* *Randomise password for this build*

	Choosing this option results in a randomly-generated password which you can find by inspecting your `docker-compose.yml`.

* *Do nothing*

	Choosing this option results in:

	```yaml
	- WEBPASSWORD=%randomAdminPassword%
	```

	which is a valid password string so "%randomAdminPassword%" will become the password.

Regardless of which option you choose, you can always edit your `docker-compose.yml` to change the value of the environment variable. For example:

```yaml
- WEBPASSWORD=mybigsecret
```

It is important to realise that `WEBPASSWORD` only has any effect on the very **first** launch. Once Pi-hole has been run at least once, the value of `WEBPASSWORD` is ignored and any changes you make will have no effect.

If `WEBPASSWORD` is **not** set on first launch, Pi-hole defaults to a randomly-generated password which you can discover after the first launch like this:

```console
$ docker logs pihole | grep random 
```

> Remember, docker logs are ephemeral so you need to run that command before the log disappears!

If you ever need to reset Pi-hole's admin password to a known value, use the following command:

```console
$ docker exec pihole pihole -a -p mybigsecret
```

> replacing "mybigsecret" with your choice of password.

### Other variables { #otherVars }

Most of Pi-hole's environment variables are self-explanatory but some can benefit from elaboration.

First, understand that there are two basic types of DNS query:

* *forward queries*:

	- question: "what is the IP address of fred.yourdomain.com?"
	- answer: 192.168.1.100

* *reverse queries*:

	- question: "what is the domain name for 192.168.1.100?"
	- answer: fred.yourdomain.com

Pi-hole has its own built-in DNS server which can answer both kinds of queries. The implementation is useful but doesn't offer all the features of a full-blown DNS server like BIND9. If you decide to implement a more capable DNS server to work alongside Pi-hole, you will need to understand the following Pi-hole environment variables:

* `REV_SERVER=`

	If you configure Pi-hole's built-in DNS server to be authoritative for your local domain name, `REV_SERVER=false` is appropriate, in which case none of the variables discussed below has any effect.

	Setting `REV_SERVER=true` allows Pi-hole to forward queries that it can't answer to a local upstream DNS server, typically running inside your network.

* `REV_SERVER_DOMAIN=yourdomain.com` (where "yourdomain.com" is an example)

	The Pi-hole documentation says:

	> *"If conditional forwarding is enabled, set the domain of the local network router".*

	The words "if conditional forwarding is enabled" mean "when `REV_SERVER=true`".

	However, this option really has little-to-nothing to do with the "domain of the local network **router**". Your router *may* have an IP address that reverse-resolves to a local domain name (eg gateway.mydomain.com) but this is something most routers are unaware of, even if you have configured your router's DHCP server to inform clients that they should assume a default domain of "yourdomain.com".

	This variable actually tells Pi-hole the name of your local domain. In other words, it tells Pi-hole to consider the possibility that an *unqualified* name like "fred" could be the fully-qualified domain name "fred.yourdomain.com".

* `REV_SERVER_TARGET=192.168.1.5` (where 192.168.1.5 is an example):

	The Pi-hole documentation says:

	> *"If conditional forwarding is enabled, set the IP of the local network router".*

	This option tells Pi-hole where to direct *forward queries* that it can't answer. In other words, Pi-hole will send a forward query for fred.yourdomain.com to 192.168.1.5.

	It *may* be appropriate to set `REV_SERVER_TARGET` to the IP address of your router (eg 192.168.1.1) but, unless your router is running as a DNS server (not impossible but uncommon), the router will likely just relay any queries to your ISP's DNS servers (or other well-known DNS servers like 8.8.8.8 or 1.1.1.1 if you have configured those). Those external DNS servers are unlikely to be able to resolve queries for names in your private domain, and won't be able to do anything sensible with reverse queries if your home network uses RFC1918 addressing (which most do: 182.168.x.x being the most common example).

	Forwarding doesn't guarantee that 192.168.1.5 will be able to answer the query. The DNS server at 192.168.1.5 may well relay the query to yet another server. In other words, this environment variable does no more than set the next hop.

	If you are planning on using this option, the target needs to be a DNS server that is authoritative for your local domain and that, pretty much, is going to be a local upstream DNS server inside your home network like another Raspberry Pi running BIND9.

* `REV_SERVER_CIDR=192.168.1.0/24` (where 192.168.1.0/24 is an example)

	The Pi-hole documentation says:

	> *"If conditional forwarding is enabled, set the reverse DNS zone (e.g. 192.168.0.0/24)".*

	This is correct but it lacks detail.

	The string "192.168.1.0/24" defines your local subnet using Classless Inter-Domain Routing (CIDR) notation. Most home subnets use a subnet-mask of 255.255.255.0. If you write that out in binary, it is 24 1-bits followed by 8 0-bits, as in:

	```
	   255  .   255  .   255  .   0
	11111111 11111111 11111111 00000000
	```

	Those 24 one-bits are where the `/24` comes from in `192.168.1.0/24`. When you perform a bitwise logical AND between that subnet mask and 192.168.1.0, the ".0" is removed (conceptually), as in:

	```
	192.168.1.0 AND 255.255.255.0 = 192.168.1
	```

	What it **means** is:

	1. The network *prefix* is "192.168.1".
	2. *This* host on the 192.168.1 network is the reserved address "192.168.1.0". It is better to think of this as "the network prefix followed by all-zero bits in the host portion". It is not common to see the .0 address used in practice. A device either knows its IP address or it doesn't. If it doesn't then it won't know its prefix so it will use 0.0.0.0 as a substitute for "this".
	3. The *range* of IP addresses available for allocation to hosts on this subnet is 192.168.1.1 through 192.168.1.254 inclusive.
	4. *All* hosts on the 192.168.1 network (ie broadcast) is the reserved address "192.168.1.255". It is better to think of this as "the network prefix followed by all-one bits in the host portion".

	When you set `REV_SERVER_CIDR=192.168.1.0/24` you are telling Pi-hole that *reverse queries* for the host range 192.168.1.1 through 192.168.1.254 should be sent to the `REV_SERVER_TARGET=192.168.1.5`.

## Pi-hole Web GUI { #webGUI }

### Connecting to the GUI { #connectGUI }

Point your browser to:

```
http://«your_ip»:8089/admin
```

where «your_ip» can be:

* The IP address of the Raspberry Pi running Pi-hole.
* The domain name of the Raspberry Pi running Pi-hole.
* The multicast DNS name (eg "raspberrypi.local") of the Raspberry Pi running Pi-hole.

### Adding local domain names { #localNames }

Login to the Pi-hole web interface: `http://raspberrypi.local:8089/admin`:

1. Select from Left menu: Local DNS -> DNS Records
2. Enter Domain: `raspberrypi.home.arpa` and IP Address: `192.168.1.10`.
3. Press Add.

Now you can use `raspberrypi.home.arpa` as the domain name for the Raspberry Pi
in your whole local network. You can also add domain names for your other
devices, provided they too have static IPs.

#### why .home.arpa? { #homeArpa }

Instead of `.home.arpa` - which is the real standard, but a mouthful - you may
use `.internal`. Using `.local` would technically also work, but it should be
reserved only for mDNS use.

## Configuring the Raspberry Pi running Pi-hole { #rpiConfig }

### Assign a fixed IP address { #rpiFixedIP }

If you want clients on your network to use Pi-hole for their DNS, the Raspberry Pi running Pi-hole **must** have a fixed IP address. It does not have to be a *static* IP address (in the sense of being hard-coded into the Raspberry Pi). The Raspberry Pi can still obtain its IP address from DHCP at boot time, providing your DHCP server (usually your home router) always returns the same IP address. This is usually referred to as a *static binding* and associates the Raspberry Pi's MAC address with a fixed IP address.

Keep in mind that many Raspberry Pis have both Ethernet and WiFi interfaces. It is generally prudent to establish static bindings for *both* network interfaces in your DHCP server.

You can use the following command to discover the MAC addresses for your Raspberry Pi's Ethernet and WiFi interfaces:

```console
$ for I in eth0 wlan0 ; do ip link show $I ; done
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether dc:a6:32:4c:89:f9 brd ff:ff:ff:ff:ff:ff
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether e5:4f:01:41:88:b2 brd ff:ff:ff:ff:ff:ff
```

In the above:

* The MAC address of the Ethernet interface is "dc:a6:32:4c:89:f9"
* The MAC address of the WiFi interface is "e5:4f:01:41:88:b2"

If a physical interface does not exist, the command returns "Device does not exist" for that interface. If you prefer, you can also substitute the `ifconfig` command for `ip link show`. It's just a little more wordy.

### Decide how the Raspberry Pi obtains its own DNS { #rpiDNS }

The Raspberry Pi itself does **not** have to use the Pi-hole container for its own DNS services. Some chicken-and-egg situations can exist if, for example, the Pi-hole container is down when another process (eg `apt` or `docker-compose`) needs to do something that depends on DNS services being available.

Nevertheless, if you configure Pi-hole to be [authoritative for local domain names](#localNames) (eg `raspberrypi.home.arpa`) then you will probably want to configure your Raspberry Pi to use the Pi-hole container in the first instance, and then fall back to an alternative if the container is down. Here is an example of how to do that:

```console
$ echo "name_servers=127.0.0.1" | sudo tee -a /etc/resolvconf.conf
$ echo "name_servers_append=8.8.8.8" | sudo tee -a /etc/resolvconf.conf
$ echo "resolv_conf_local_only=NO" | sudo tee -a /etc/resolvconf.conf
$ sudo resolvconf -u
```

In words:

1. `name_servers=127.0.0.1` instructs the Raspberry Pi to direct DNS queries to the loopback address. Port 53 is implied. If the Pi-hole container is running in:

	- non-host mode, Docker is listening to port 53 and forwards the queries to the Pi-hole container;
	- host mode, the Pi-hole container is listening to port 53.

2. `name_servers_append=8.8.8.8` instructs the Raspberry Pi to fail-over to 8.8.8.8 if Pi-hole does not respond. You can replace `8.8.8.8` (a Google service) with:

	* Another well-known public DNS server like `1.1.1.1` (Cloudflare).
	* The IP address(es) of your ISP's DNS hosts (generally available from your ISP's web site).
	* The IP address of another DNS server running in your local network (eg BIND9).
	* The IP address of your home router. Most home routers default to the ISP's DNS hosts but you can usually change your router's configuration to bypass your ISP in favour of public servers like 8.8.8.8 and 1.1.1.1.

	You need slightly different syntax if you want to add multiple fallback servers. For example, suppose your fallback hosts are a local server (eg 192.168.1.2) running BIND9 and 8.8.8.8. The command would be:

	```console
	$ echo 'name_servers_append="192.168.1.2 8.8.8.8"' | sudo tee -a /etc/resolvconf.conf
	```

3. `resolv_conf_local_only=NO` is needed so that 127.0.0.1 and 8.8.8.8 can coexist.
4. The `resolvconf -u` command instructs Raspberry Pi OS to rebuild the active resolver configuration. In principle, that means parsing `/etc/resolvconf.conf` to derive `/etc/resolv.conf`. This command can sometimes return the error "Too few arguments". You should ignore that error.

#### Example configuration { #rpiDNSExample }

Make these assumptions:

1. You have followed the instructions above to add these lines to `/etc/resolvconf.conf`:

	```
	name_servers=127.0.0.1
	name_servers_append=8.8.8.8
	resolv_conf_local_only=NO
	```

2. The Raspberry Pi running Pi-hole has the IP address 192.168.1.50 which it obtains as a static assignment from your DHCP server.
3. You have configured your DHCP server to provide 192.168.1.50 for client devices to use to obtain DNS services (ie, you are saying clients should use Pi-hole for DNS). 

The result of the configuration appears in `/etc/resolv.conf`:

```console
$ cat /etc/resolv.conf
# Generated by resolvconf
nameserver 127.0.0.1
nameserver 192.168.1.50
nameserver 8.8.8.8
```

Interpretation:

* `nameserver 127.0.0.1` is present because of `name_servers=127.0.0.1`
* `nameserver 192.168.1.50` is present because it was learned from DHCP
* `nameserver 8.8.8.8` is present because of `name_servers_append=8.8.8.8`

The fact that the Raspberry Pi is effectively represented twice (once as 127.0.0.1, and again as 192.168.1.50) does not matter. If the Pi-hole container stops running, the Raspberry Pi will bypass 192.168.1.50 and fail over to 8.8.8.8, failing back to 127.0.0.1 when the Pi-hole container starts again.

Notes:

* If you wish to prevent the Raspberry Pi from including the address(es) of DNS servers learned from DHCP, you can instruct the DHCP client running on the Raspberry Pi to ignore the information coming from the DHCP server:

	```console
	$ echo 'nooption domain_name_servers' | sudo tee -a /etc/dhcpcd.conf
	$ sudo service dhcpcd reload
	$ sudo resolvconf -u 
	```

* If you have followed the steps in [Adding local domain names](#localNames) to define names for your local hosts, you can inform the Raspberry Pi of that fact like this:

	```console
	$ echo 'search_domains=home.arpa' | sudo tee -a /etc/resolvconf.conf
	$ sudo resolvconf -u 
	```

	That will add the following line to `/etc/resolv.conf`:

	```
	search home.arpa
	```

	Then, when you refer to a host by a short name (eg "fred") the Raspberry Pi will also consider "fred.home.arpa" when trying to discover the IP address.

## Using Pi-hole as your DNS resolver { #piholePrimary }

In order for Pi-hole to block ads or resolve anything, clients need to be told to use it as their DNS server. You can either:

1. Adopt a whole-of-network approach and edit the DNS settings in your DHCP server so that all clients are given the IP address of the Raspberry Pi running Pi-hole to use for DNS services when a lease is issued.
2. Adopt a case-by-case (manual) approach where you instruct particular clients to obtain DNS services from the IP address of the Raspberry Pi running Pi-hole.

Option 1 (whole-of-network) is the simplest approach. Assuming your Raspberry Pi has the static IP `192.168.1.10`:

1. Go to your network's DHCP server. In most home networks, this will be your Wireless Access Point/WLAN Router:

	* Login into its web-interface
	* Find where DNS servers are defined (generally with DHCP controls)
	* Change all DNS fields to `192.168.1.10`

2. All local clients have to be rebooted. Without this they will continue to use the old DNS setting from an old DHCP lease for quite some time.

Option 2 (case-by-case) generally involves finding the IP configuration options for each host and setting the DNS server manually. Manual changes are usually effective immediately without needing a reboot.

### advanced configurations { #advancedConfig }

Setting up a combination of Pi-hole (for ad-blocking services), and/or a local upstream DNS resolver (eg BIND9) to be authoritative for a local domain and reverse-resolution for your local IP addresses, and decisions about where each DNS server forwards queries it can't answer (eg your ISP's DNS servers, or Google's 8.8.8.8, or Cloudflare's 1.1.1.1) is a complex topic and depends on your specific needs.

The same applies to setting up a DHCP server (eg DHCPD) which is capable of distinguishing between the various clients on your network (ie by MAC address) to make case-by-case decisions as to where each client should obtain its DNS services. 

If you need help, try asking questions on the [IOTstack Discord channel](https://discord.gg/ZpKHnks).

## Testing and Troubleshooting { #debugging }

Install dig:

```console
$ apt install dnsutils
```

Test that Pi-hole is correctly configured (should respond 192.168.1.10):

```console
$ dig raspberrypi.home.arpa @192.168.1.10
```

To test on your desktop if your network configuration is correct, and an ESP
will resolve its DNS queries correctly, restart your desktop machine to ensure
DNS changes are updated and then use:

```console
$ dig raspberrypi.home.arpa
```

This should produce the same result as the previous command.

If this fails to resolve the IP, check that the server in the response is
`192.168.1.10`. If it's `127.0.0.xx` check `/etc/resolv.conf` begins with
`nameserver 192.168.1.10`.

## Microcontrollers { #iotConfig }

If you want to avoid hardcoding your Raspberry Pi IP to your ESPhome devices,
you need a DNS server that will do the resolving. This can be done using the
Pi-hole container as described above.

### `*.local` won't work for ESPhome { #esp32mDNS }

There is a special case for resolving `*.local` addresses. If you do a `ping raspberrypi.local` on your desktop Linux or the Raspberry Pi, it will first try using mDNS/bonjour to resolve the IP address raspberrypi.local. If this fails it will then ask the DNS server. ESPhome devices can't use mDNS to resolve an IP address. You need a proper DNS server to respond to queries made by an ESP. As such, `dig raspberrypi.local` will fail, simulating ESPhome device behavior. This is as intended, and you should use raspberrypi.home.arpa as the address on your ESP-device.

## Getting a clean slate { #cleanSlate }

If Pi-hole misbehaves, you can always try starting from a clean slate by erasing Pi-hole's persistent storage area. Erasing the persistent storage area causes PiHole to re-initialise its data structures on the next launch. You will lose:

1. Any configuration options you may have set via the web GUI that are not otherwise reflected in [environment variables](#envVars).
2. Any whitelist, blacklist or local DNS records you entered.
3. All DNS resolution and blocking history.

Also note that your [administrative password](#adminPassword) will reset.

The recommended approach is:

1. Login to Pi-hole's web GUI and navigate to Settings » Teleporter.
2. Click the <kbd>Backup</kbd> button to download a backup.
3. Logout of the Web GUI.
4. Run the following commands:

	```console
	$ cd ~/IOTstack
	$ docker-compose rm --force --stop -v pihole
	$ sudo rm -rf ./volumes/pihole
	$ docker-compose up -d pihole
	```

5. Login to Pi-hole's web GUI and navigate to Settings » Teleporter.
6. Use the checkboxes to select the settings you wish to restore, and click the <kbd>Browse</kbd> and <kbd>Restore</kbd> buttons.
