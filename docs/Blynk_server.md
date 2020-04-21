# Blynk server
This is a custom implementation of Blynk Server

```yml
  blynk_server:
    build: ./services/blynk_server/.
    container_name: blynk_server
    restart: unless-stopped
    ports:
      - 8180:8080
      - 8441:8441
      - 9443:9443
    volumes:
      - ./volumes/blynk_server/data:/data
```

To connect to the admin interface navigate to `<your pis IP>:9443/admin`

I don't know anything about this service so you will need to read though the setup on the [Project Homepage](https://github.com/blynkkk/blynk-server)

When setting up the application on your mobile be sure to select custom setup [here](https://github.com/blynkkk/blynk-server#app-and-sketch-changes)

Writeup From @877dev

## Getting started
Log into admin panel at https://youripaddress:9443/admin
(Use your Pi's IP address, and ignore Chrome warning).

Default credentials:
user:admin@blynk.cc
pass:admin

## Change username and password
Click on Users > "email address" and edit email, name and password. 
Save changes
Restarting the container using Portainer may be required to take effect.

## Setup gmail
Optional step, useful for getting the auth token emailed to you.
(To be added once confirmed working....)

## iOS/Android app setup
Login the app as per the photos [HERE](https://github.com/blynkkk/blynk-server#app-and-sketch-changes)
Press "New Project"
Give it a name, choose device "Raspberry Pi 3 B" so you have plenty of [virtual pins](http://help.blynk.cc/en/articles/512061-what-is-virtual-pins) available, and lastly select WiFi.
Create project and the [auth token](https://docs.blynk.cc/#getting-started-getting-started-with-the-blynk-app-4-auth-token) will be emailed to you (if emails configured). You can also find the token in app under the phone app settings, or in the admin web interface by clicking Users>"email address" and scroll down to token.

## Quick usage guide for app
Press on the empty page, the widgets will appear from the right.
Select your widget, let's say a button.
It appears on the page, press on it to configure.
Give it a name and colour if you want. 
Press on PIN, and select virtual. Choose any pin i.e. V0
Press ok.
To start the project running, press top right Play button.
You will get an offline message, because no devices are connected to your project via the token.
Enter node red.....

## Node red
Install node-red-contrib-blynk-ws from pallette manager
Drag a "write event" node into your flow, and connect to a debug node
Configure the Blynk node for the first time:
```URL: wss://youripaddress:9443/websockets``` more info [HERE](https://github.com/gablau/node-red-contrib-blynk-ws/blob/master/README.md#how-to-use)
Enter your [auth token](https://docs.blynk.cc/#getting-started-getting-started-with-the-blynk-app-4-auth-token) from before and save/exit.
When you deploy the flow, notice the app shows connected message, as does the Blynk node.
Press the button on the app, you will notice the payload is sent to the debug node.

## What next?
Further information and advanced setup:
https://github.com/blynkkk/blynk-server

Check the documentation:
https://docs.blynk.cc/

Visit the community forum pages:
https://community.blynk.cc/

Interesting post by Peter Knight on MQTT/Node Red flows:
https://community.blynk.cc/t/my-home-automation-projects-built-with-mqtt-and-node-red/29045

Some Blynk flow examples:
https://github.com/877dev/Node-Red-flow-examples