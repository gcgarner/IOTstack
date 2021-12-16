# Pi-hole
Pi-hole is a fantastic utility to reduce ads.

The interface can be found on `http://"your_ip":8089/admin` 

Default password is `IOtSt4ckP1Hol3`. This can be changed with:
```
docker exec pihole pihole -a -p myNewPassword
```

## Pi-hole as DNS server

In order for the Pi-hole to work, it needs to be defined as the DNS server.
This can either be done manually to each device or you can define it as a
DNS-nameserver for the whole LAN.

Assuming your pihole hostname is `raspberrypi` and has the IP `192.168.1.10`:

1. Go to the Pi-hole web interface: `http://raspberrypi.local:8089/admin` and Login
    * From Left menu: Select Local DNS -> DNS Records
    * Enter Domain: `raspberrypi.home.arpa` and IP Address: `192.168.1.10`. Press Add.
2. Go to your DHCP server, usually this is your Wireless Access Point / WLAN Router web interface.
    * Find where DNS servers are defined
    * Change all DNS fields to `192.168.1.10`.
3. All local machines have to be rebooted or have their DHCP leases released. Without this they will continue to use the old DNS setting from an old DHCP lease for quite some time.

Now you can use `raspberrypi.home.arpa` as the domain name for the Raspberry Pi in your whole local network.

For the Raspberry Pi itself to also use the Pi-hole DNS server, run:
```bash
echo "name_servers=127.0.0.1" | sudo tee -a /etc/resolvconf.conf
echo "name_servers_append=8.8.8.8" | sudo tee -a /etc/resolvconf.conf
echo "resolv_conf_local_only=NO" | sudo tee -a /etc/resolvconf.conf
sudo resolvconf -u # Ignore "Too few arguments."-complaint
```
Quick explanation: resolv_conf_local_only is disabled and a public nameserver is added, so that in case the Pi-hole container is stopped, the Raspberry won't lose DNS functionality. It will just fallback to 8.8.8.8.

### Testing & Troubleshooting

Install dig:
```
apt install dnsutils
```

Test that pi-hole is correctly configured (should respond 192.168.1.10):
```
dig raspberrypi.home.arpa @192.168.1.10
```

To test on your desktop if your network configuration is correct, and an ESP will resolve its DNS queries correctly, restart your desktop machine to ensure DNS changes are updated and then use:
```
dig raspberrypi.home.arpa
```
This should produce the same result as the previous command.

If this fails to resolve the IP, check that the server in the response is `192.168.1.10`.
If it's `127.0.0.xx` check `/etc/resolv.conf` begins with `nameserver 192.168.1.10`.

## Microcontrollers

If you want to avoid hardcoding your Raspberry Pi IP to your ESPhome devices,
you need a DNS server that will do the resolving. This can be done using the
Pi-hole container as described above.

## Why .home.arpa?

Instead of `.home.arpa` - which is the real standard, but a mouthful - you may use `.internal`.
Using `.local` would technically also work, but it should be reserved only for mDNS use.

Note: There is a special case for resolving `*.local` addresses. If you do a `ping raspberrypi.local` on your desktop linux or the RPI, it will first try using mDNS/bonjour to resolve the IP address raspberrypi.local. If this fails it will then ask the DNS server. Esphome devices can't use mDNS to resolve an IP address. You need a proper DNS server to respond to queries made by an ESP. As such, `dig raspberrypi.local` will fail, simulating ESPhome device behavior. This is as intended, and you should use raspberrypi.home.arpa as the address on your ESP-device.
