# x2go
x2go is an "alternative" to using VNC for a remote connection. It uses X11 forwarding over ssh to provide a desktop environment

Reason for using:
I have a Pi 4 and I didn't buy a micro hdmi cable. You can use VNC however you are limited to a 800x600 window.

## Installation

Install with `sudo apt install x2goserver`

x2go cant connect to the native Raspbian Desktop so you will need to install another with `sudo tasksel`

![image](https://user-images.githubusercontent.com/46672225/69007692-b4df0a00-0949-11ea-82d5-09a6833df186.png)

I chose Xfce because it is light weight.

Install the x2go client from their [website](https://wiki.x2go.org/doku.php/download:start)

Now I have a full-screen client 

![image](https://user-images.githubusercontent.com/46672225/69007780-0045e800-094b-11ea-9626-4947595a016e.png)

## YouTube tutorial
[Laurence systems](https://www.youtube.com/watch?v=oSuy1TS8FGs)