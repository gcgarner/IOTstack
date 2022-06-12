# Accessing your device from the internet

The challenge most of us face with remotely accessing our home networks is that our routers usually have a dynamically-allocated IP address on the public (WAN) interface.

From time to time the IP address that your ISP assigns changes and it's difficult to keep up. Fortunately, there is a solution: Dynamic DNS. The section below shows you how to set up an easy-to-remember domain name that follows your public IP address no matter when it changes.

Secondly, how do you get into your home network? Your router has a firewall that is designed to keep the rest of the internet out of your network to protect you. The solution to that is a Virtual Private Network (VPN) or "tunnel". 

## Dynamic DNS

There are two parts to a Dynamic DNS service:

1. You have to register with a Dynamic DNS service provider and obtain a domain name that is not already taken by someone else.
2. Something on your side of the network needs to propagate updates so that your chosen domain name remains in sync with your router's dynamically-allocated public IP address.

### Register with a Dynamic DNS service provider

The first part is fairly simple and there are quite a few Dynamic DNS service providers including:

* [DuckDNS.org](https://www.duckdns.org)
* [NoIP.com](https://www.noip.com)

> You can find more service providers by Googling ["Dynamic DNS service"](https://www.google.com/search?q=%22Dynamic%20DNS%20service%22).

Some router vendors also provide their own built-in Dynamic DNS capabilities for registered customers so it's a good idea to check your router's capabilities before you plough ahead.

### Dynamic DNS propagation

The "something" on your side of the network propagating WAN IP address changes can be either:

* your router; or
* a "behind the router" technique, typically a periodic job running on the same Raspberry Pi that is hosting IOTstack and WireGuard.

If you have the choice, your router is to be preferred. That's because your router is usually the only device in your network that actually knows when its WAN IP address changes. A Dynamic DNS client running on your router will propagate changes immediately and will only transmit updates when necessary. More importantly, it will persist through network interruptions or Dynamic DNS service provider outages until it receives an acknowledgement that the update has been accepted.

Nevertheless, your router may not support the Dynamic DNS service provider you wish to use, or may come with constraints that you find unsatisfactory so any behind-the-router technique is always a viable option, providing you understand its limitations.

A behind-the-router technique usually relies on sending updates according to a schedule. An example is a `cron` job that runs every five minutes. That means any router WAN IP address changes won't be propagated until the next scheduled update. In the event of network interruptions or service provider outages, it may take close to ten minutes before everything is back in sync. Moreover, given that WAN IP address changes are infrequent events, most scheduled updates will be sending information unnecessarily.

### DuckDNS container

The recommended and easiest solution is to install the Duckdns docker-container
from the menu. It includes the cron service and logs are handled by Docker.

For configuration see [Containers/Duck DNS]( ../Containers/Duckdns.md).

!!! note
    This is a recently added container, please don't hesitate to report any
    possible faults to Discord or as Github issues.

### DuckDNS client script { #duckdns-client }

!!! info
    This method will soon be deprecated in favor of the DuckDNS container.

IOTstack provides a solution for DuckDNS. The best approach to running it is:

``` console
$ mkdir -p ~/.local/bin
$ cp ~/IOTstack/duck/duck.sh ~/.local/bin
```

> The reason for recommending that you make a copy of `duck.sh` is because the "original" is under Git control. If you change the "original", Git will keep telling you that the file has changed and it may block incoming updates from GitHub.

Then edit `~/.local/bin/duck.sh` to add your DuckDNS domain name(s) and token:

```bash
DOMAINS="YOURS.duckdns.org"
DUCKDNS_TOKEN="YOUR_DUCKDNS_TOKEN"
```

For example:

```bash
DOMAINS="downunda.duckdns.org"
DUCKDNS_TOKEN="8a38f294-b5b6-4249-b244-936e997c6c02"
```

Note:

* The `DOMAINS=` variable can be simplified to just "YOURS", with the `.duckdns.org` portion implied, as in:

	```bash
	DOMAINS="downunda"
	```

Once your credentials are in place, test the result by running:

``` console
$ ~/.local/bin/duck.sh
ddd, dd mmm yyyy hh:mm:ss ±zzzz - updating DuckDNS
OK
```

The timestamp is produced by the `duck.sh` script. The [expected responses from the DuckDNS service](https://www.duckdns.org/spec.jsp) are:

* "OK" - indicating success; or
* "KO" - indicating failure.

Check your work if you get "KO" or any other errors.

Next, assuming `dig` is installed on your Raspberry Pi (`sudo apt install dnsutils`), you can test propagation by sending a directed query to a DuckDNS name server. For example, assuming the domain name you registered was `downunda.duckdns.org`, you would query like this:

``` console
$ dig @ns1.duckdns.org downunda.duckdns.org +short
```

The expected result is the IP address of your router's WAN interface. It is a good idea to confirm that it is the same as you get from [whatismyipaddress.com](https://whatismyipaddress.com).

A null result indicates failure so check your work.

Remember, the Domain Name System is a *distributed* database. It takes *time* for changes to propagate. The response you get from directing a query to ns1.duckdns.org may not be the same as the response you get from any other DNS server. You often have to wait until cached records expire and a recursive query reaches the authoritative DuckDNS name-servers.

#### Running the DuckDNS client automatically

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

Standard output and standard error are redirected to `/dev/null` which is appropriate in this instance. When DuckDNS is working correctly (which is most of the time), the only output from the `curl` command is "OK". Logging that every five minutes would add wear and tear to SD cards for no real benefit.

If you suspect DuckDNS is misbehaving, you can run the `duck.sh` command from a terminal session, in which case you will see all the `curl` output in the terminal window.

If you wish to keep a log of `duck.sh` activity, the following will get the job done:

1. Make a directory to hold log files:

	``` console
	$ mkdir -p ~/Logs
	```

2. Edit the last line of the `crontab` like this:

	```bash
	*/5	*	*	*	*	duck.sh >>./Logs/duck.log 2>&1
	```

Remember to prune the log from time to time. The generally-accepted approach is:

``` console
$ cat /dev/null >~/Logs/duck.log
```

## Virtual Private Network

### WireGuard

WireGuard is supplied as part of IOTstack. See [WireGuard documentation](../Containers/WireGuard.md).

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

``` console
$ curl -s 'https://raw.githubusercontent.com/zerotier/ZeroTierOne/master/doc/contact%40zerotier.com.gpg' | gpg --import && \
if z=$(curl -s 'https://install.zerotier.com/' | gpg); then echo "$z" | sudo bash; fi
```
