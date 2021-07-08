# Accessing your device from the internet

The challenge most of us face with remotely accessing our home networks is that our routers usually have a dynamically-allocated IP address on the public (WAN) interface.

From time to time the IP address that your ISP assigns changes and it's difficult to keep up. Fortunately, there is a solution: Dynamic DNS. The section below shows you how to set up an easy-to-remember domain name that follows your public IP address no matter when it changes.

Secondly, how do you get into your home network? Your router has a firewall that is designed to keep the rest of the internet out of your network to protect you. The solution to that is a Virtual Private Network (VPN) or "tunnel". 

## <a name="dynamicDNS"> Dynamic DNS </a>

There are two parts to a Dynamic DNS service:

1. You have to register with a Dynamic DNS service provider and obtain a domain name that is not already taken by someone else.
2. Something on your side of the network needs to propagate updates so that your chosen domain name remains in sync with your router's dynamically-allocated public IP address.

### <a name="registerDDNS"> Register with a Dynamic DNS service provider </a>

The first part is fairly simple and there are quite a few Dynamic DNS service providers including:

* [DuckDNS.org](https://www.duckdns.org)
* [NoIP.com](https://www.noip.com)

> You can find more service providers by Googling ["Dynamic DNS service"](https://www.google.com/search?q="Dynamic DNS service").

Some router vendors also provide their own built-in Dynamic DNS capabilities for registered customers so it's a good idea to check your router's capabilities before you plough ahead.

### <a name="propagateDDNS"> Dynamic DNS propagation </a>

The "something" on your side of the network propagating WAN IP address changes can be either:

* your router; or
* a "behind the router" technique, typically a periodic job running on the same Raspberry Pi that is hosting IOTstack and WireGuard.

If you have the choice, your router is to be preferred. That's because your router is usually the only device in your network that actually knows when its WAN IP address changes. A Dynamic DNS client running on your router will propagate changes immediately only will only transmit updates when necessary. More importantly, it will persist through network interruptions or Dynamic DNS service provider outages until it receives an acknowledgement that the update has been accepted.

Nevertheless, your router may not support the Dynamic DNS service provider you wish to use, or may come with constraints that you find unsatisfactory so any behind-the-router technique is always a viable option, providing you understand its limitations.

A behind-the-router technique usually relies on sending updates according to a schedule. An example is a `cron` job that runs every five minutes. That means any router WAN IP address changes won't be propagated until the next scheduled update. In the event of network interruptions or service provider outages, it may take some time before everything is back in sync. Moreover, given that WAN IP address changes are infrequent events, most scheduled updates will be sending information unnecessarily, contributing unnecessarily to server load.

> This seems to be a problem for DuckDNS which takes a beating because almost every person using it is sending an update bang-on five minutes.

### <a name="duckDNSclient"> DuckDNS client </a>

IOTstack provides a solution for DuckDNS. The best approach to running it is:

```bash
$ mkdir -p ~/.local/bin
$ cp ~/IOTstack/duck/duck.sh ~/.local/bin
```

Then edit `~/.local/bin/duck.sh` to add your DuckDNS domain name(s) and token:

```bash
DOMAINS="YOURS.duckdns.org"
DUCKDNS_TOKEN="YOUR_DUCKDNS_TOKEN"
```

Once your credentials are in place, test the result by running:

```bash
$ ~/.local/bin/duck.sh
ddd, dd mmm yyyy hh:mm:ss ±zzzz - updating DuckDNS
OK
```

The expected response is a timestamp followed by "OK". Check your work if you get any errors.

Next, assuming `dig` is installed on your Raspberry Pi (`sudo apt install dnsutils`), you can test propagation by sending a directed query to a DuckDNS name server. For example, assuming the domain name you registered was `downunda.duckdns.org`, you would query like this:

```bash
$ dig @ns1.duckdns.org downunda.duckdns.org +short
```

The expected result is the IP address of your router's WAN interface. It is a good idea to confirm that it is the same as you get from [whatismyipaddress.com](https://whatismyipaddress.com).

A null result indicates failure so check your work.

#### <a name="duckDNSauto"> Running the DuckDNS client automatically </a>

The recommended arrangement for keeping your Dynamic DNS service up-to-date is to invoke `duck.sh` from `cron` at five minute intervals.

If you are new to `cron`, see these guides for more information about setting up and editing your `crontab`:

* [raspberrytips.com](https://raspberrytips.com/schedule-task-raspberry-pi/)
* [pimylifeup.com](https://pimylifeup.com/cron-jobs-and-crontab/)

A typical `crontab` will look like this:

```bash
SHELL=/bin/bash
HOME=/home/pi
PATH=/home/pi/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

*/5	*	*	*	*	duck.sh >/dev/null 2>&1
```

The first three lines construct the runtime environment correctly and should be at the start of any `crontab`.

The last line means "run duck.sh every five minutes". See [crontab.guru](https://crontab.guru/#*/5_*_*_*_*) if you want to understand the syntax of the last line.

When launched in the background by `cron`, the script supplied with IOTstack adds a random delay of up to one minute to try to reduce the "hammering effect" of a large number of users updating DuckDNS simultaneously.

Standard output and standard error are redirected to `/dev/null` which is appropriate for jobs run by `cron`. Keep in mind that you can always run the `duck.sh` command from a terminal session, in which case you will see all the output.

If you wish to keep a log of `duck.sh` activity, the following will get the job done:

1. Make a directory to hold log files:

	```bash
	$ mkdir -p ~/Logs
	```

2. Edit the last line of the `crontab` like this:

	```bash
	*/5	*	*	*	*	duck.sh >>./Logs/duck.log 2>&1
	```

## Virtual Private Network

### WireGuard

WireGuard is supplied as part of IOTstack. See [WireGuard documentation](https://sensorsiot.github.io/IOTstack/Containers/WireGuard.html).

### PiVPN

pimylifeup.com has an excellent tutorial on how to install [PiVPN](https://pimylifeup.com/raspberry-pi-vpn-server/)

In point 17 and 18 they mention using noip for their dynamic DNS. Here you can use the DuckDNS address if you created one.

Don't forget you need to open the port 1194 on your firewall. Most people won't be able to VPN from inside their network so download OpenVPN client for your mobile phone and try to connect over mobile data. ([More info.](https://en.wikipedia.org/wiki/Hairpinning))

Once you activate your VPN (from your phone/laptop/work computer) you will effectively be on your home network and you can access your devices as if you were on the wifi at home.

I personally use the VPN any time I'm on public wifi, all your traffic is secure.

### Zerotier

https://www.zerotier.com/

Zerotier is an alternative to PiVPN that doesn't require port forwarding on your router. It does however require registering for their free tier service [here](https://my.zerotier.com/login). 

Kevin Zhang has written a how to guide [here](https://iamkelv.in/blog/2017/06/zerotier.html). Just note that the install link is outdated and should be:

```bash
curl -s 'https://raw.githubusercontent.com/zerotier/ZeroTierOne/master/doc/contact%40zerotier.com.gpg' | gpg --import && \
if z=$(curl -s 'https://install.zerotier.com/' | gpg); then echo "$z" | sudo bash; fi
```
