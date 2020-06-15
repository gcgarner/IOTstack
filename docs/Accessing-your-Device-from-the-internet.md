# Accessing your device from the internet
The challenge most of us face with remotely accessing your home network is that you don't have a static IP. From time to time the IP that your ISP assigns to you changes and it's difficult to keep up. Fortunately, there is a solution, a DynamicDNS. The section below shows you how to set up an easy to remember address that follows your public IP no matter when it changes.

Secondly, how do you get into your home network? Your router has a firewall that is designed to keep the rest of the internet out of your network to protect you. Here we install a VPN and configure the firewall to only allow very secure VPN traffic in. 

## DuckDNS
If you want to have a dynamic DNS point to your Public IP I added a helper script.
Register with duckdns.org and create a subdomain name. Then edit the `nano ~/IOTstack/duck/duck.sh` file and add your

```bash
DOMAINS="YOUR_DOMAINS"
DUCKDNS_TOKEN="YOUR_DUCKDNS_TOKEN"
```

first test the script to make sure it works `sudo ~/IOTstack/duck/duck.sh` then `cat /var/log/duck.log`. If you get KO then something has gone wrong and you should check out your settings in the script. If you get an OK then you can do the next step. 

Create a cron job by running the following command `crontab -e`

You will be asked to use an editor option 1 for nano should be fine
paste the following in the editor `*/5 * * * * sudo ~/IOTstack/duck/duck.sh >/dev/null 2>&1` then ctrl+s and ctrl+x to save

Your Public IP should be updated every five minutes

## PiVPN
pimylifeup.com has an excellent tutorial on how to install [PiVPN](https://pimylifeup.com/raspberry-pi-vpn-server/)

In point 17 and 18 they mention using noip for their dynamic DNS. Here you can use the DuckDNS address if you created one.

Don't forget you need to open the port 1194 on your firewall. Most people won't be able to VPN from inside their network so download OpenVPN client for your mobile phone and try to connect over mobile data. ([More info.](https://en.wikipedia.org/wiki/Hairpinning))

Once you activate your VPN (from your phone/laptop/work computer) you will effectively be on your home network and you can access your devices as if you were on the wifi at home.

I personally use the VPN any time I'm on public wifi, all your traffic is secure.

## Zerotier
https://www.zerotier.com/

Zerotier is an alternative to PiVPN that doesn't require port forwarding on your router. It does however require registering for their free tier service [here](https://my.zerotier.com/login). 

Kevin Zhang has written a how to guide [here](https://iamkelv.in/blog/2017/06/zerotier.html). Just note that the install link is outdated and should be:
```
curl -s 'https://raw.githubusercontent.com/zerotier/ZeroTierOne/master/doc/contact%40zerotier.com.gpg' | gpg --import && \
if z=$(curl -s 'https://install.zerotier.com/' | gpg); then echo "$z" | sudo bash; fi
```
