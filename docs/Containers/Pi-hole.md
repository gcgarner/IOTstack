# Pi-hole
Pi-hole is a fantastic utility to reduce ads.

The web interface can be found at `http://«your_ip»:8089/admin`  
where «your_ip» can be:

* The IP address of the Raspberry Pi running Pi-hole.
* The domain name of the Raspberry Pi running Pi-hole.
* The multicast DNS name (eg "raspberrypi.local") of the Raspberry Pi running
  Pi-hole.

Default password is random, it can be changed by running:
```
docker-compose exec pihole pihole -a -p myNewPassword
```

References:

* [Pi-hole on GitHub](https://github.com/pi-hole/docker-pi-hole)
* [Pi-hole on Dockerhub](https://hub.docker.com/r/pihole/pihole)

## Environment variables

Environment variables govern much of Pi-hole's behaviour. If you are running new
menu (master branch), the variables are inline in `docker-compose.yml`. If you
are running old menu, the variables will be in:
`~/IOTstack/services/pihole/pihole.env`

The first time Pi-hole is launched, it checks for the `WEBPASSWORD` environment
variable. If found, sets the initial password.

Pi-hole supports a [long list of environment
variables](https://github.com/pi-hole/docker-pi-hole#environment-variables).

## Using Pi-hole as your DNS resolver

In order for the Pi-hole to ad-block or resolve anything, it needs to be
defined as the DNS server.  This can either be done manually to each device or
you can define it as a DNS-nameserver for the whole LAN.

Note that using Pi-hole for clients on your network pretty much **requires** the
Raspberry Pi running Pi-hole to have a fixed IP address.

Assuming your RPi hostname is `raspberrypi` and has the static IP
`192.168.1.10`:

1. Go to your network's DHCP server, usually this is your Wireless Access Point
   / WLAN Router.
    * Login into its web-interface
    * Find where DNS servers are defined
    * Change all DNS fields to `192.168.1.10`
2. All local machines have to be rebooted. Without this they will continue to
   use the old DNS setting from an old DHCP lease for quite some time.

## Adding domain names

Login to the Pi-hole web interface: `http://raspberrypi.local:8089/admin`:

1. Select from Left menu: Local DNS -> DNS Records
2. Enter Domain: `raspberrypi.home.arpa` and IP Address: `192.168.1.10`. Press
   Add.

Now you can use `raspberrypi.home.arpa` as the domain name for the Raspberry Pi
in your whole local network. You can also add domain names for your other
devices, provided they too have static IPs.

The Raspberry Pi itself must also use be configured to use the Pi-hole DNS
server. This is especially important when you add your own domains names,
otherwise DNS may work differently on the Pi than on other devices. Configure
this by running:
```bash
echo "name_servers=127.0.0.1" | sudo tee -a /etc/resolvconf.conf
echo "name_servers_append=8.8.8.8" | sudo tee -a /etc/resolvconf.conf
echo "resolv_conf_local_only=NO" | sudo tee -a /etc/resolvconf.conf
sudo resolvconf -u # Ignore "Too few arguments."-complaint
```
Quick explanation: resolv_conf_local_only is disabled and a public nameserver
is added, so that in case the Pi-hole container is stopped, the Raspberry won't
lose DNS functionality. It will just fallback to 8.8.8.8.

### Testing & Troubleshooting

Install dig:
```
apt install dnsutils
```

Test that Pi-hole is correctly configured (should respond 192.168.1.10):
```
dig raspberrypi.home.arpa @192.168.1.10
```

To test on your desktop if your network configuration is correct, and an ESP
will resolve its DNS queries correctly, restart your desktop machine to ensure
DNS changes are updated and then use:
```
dig raspberrypi.home.arpa
```
This should produce the same result as the previous command.

If this fails to resolve the IP, check that the server in the response is
`192.168.1.10`. If it's `127.0.0.xx` check `/etc/resolv.conf` begins with
`nameserver 192.168.1.10`.

## Why .home.arpa?

Instead of `.home.arpa` - which is the real standard, but a mouthful - you may
use `.internal`. Using `.local` would technically also work, but it should be
reserved only for mDNS use.

## Microcontrollers

If you want to avoid hardcoding your Raspberry Pi IP to your ESPhome devices,
you need a DNS server that will do the resolving. This can be done using the
Pi-hole container as described above.

!!! info "`*.local` won't work for ESPhome"

    There is a special case for resolving `*.local` addresses. If you do a
    `ping raspberrypi.local` on your desktop linux or the RPI, it will first
    try using mDNS/bonjour to resolve the IP address raspberrypi.local. If this
    fails it will then ask the DNS server. Esphome devices can't use mDNS to
    resolve an IP address. You need a proper DNS server to respond to queries
    made by an ESP. As such, `dig raspberrypi.local` will fail, simulating
    ESPhome device behavior. This is as intended, and you should use
    raspberrypi.home.arpa as the address on your ESP-device.

