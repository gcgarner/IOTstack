#!/bin/bash

# Create config files for Blynk custom server

#current user
u=$(whoami)

#Check if the config directory already exists:
if [ ! -d ./volumes/blynk_server/data/config ]; then
	#Create the config directory
    sudo mkdir -p ./volumes/blynk_server/data/config

    #Create the properties files:
	#cd ~/IOTstack/volumes/blynk_server/data/config
    sudo touch ./volumes/blynk_server/data/config/server.properties
    sudo touch ./volumes/blynk_server/data/config/mail.properties
    
    #Give permissions:
    sudo chown -R $u:$u ./volumes/blynk_server/data/config
    
    #Populate the server.properties file:
    sudo echo "hardware.mqtt.port=8440
    http.port=8080
    force.port.80.for.csv=false
    force.port.80.for.redirect=true
    https.port=9443
    data.folder=./data
    logs.folder=./logs
    log.level=info
    user.devices.limit=10
    user.tags.limit=100
    user.dashboard.max.limit=100
    user.widget.max.size.limit=20
    user.message.quota.limit=100
    notifications.queue.limit=2000
    blocking.processor.thread.pool.limit=6
    notifications.frequency.user.quota.limit=5
    webhooks.frequency.user.quota.limit=1000
    webhooks.response.size.limit=96
    user.profile.max.size=128
    terminal.strings.pool.size=25
    map.strings.pool.size=25
    lcd.strings.pool.size=6
    table.rows.pool.size=100
    profile.save.worker.period=60000
    stats.print.worker.period=60000
    web.request.max.size=524288
    csv.export.data.points.max=43200
    hard.socket.idle.timeout=10
    enable.db=false
    enable.raw.db.data.store=false
    async.logger.ring.buffer.size=2048
    allow.reading.widget.without.active.app=false
    allow.store.ip=true
    initial.energy=1000000
    admin.rootPath=/admin
    restore.host=blynk-cloud.com
    product.name=Blynk
    admin.email=admin@blynk.cc
    admin.pass=admin
    " > ./volumes/blynk_server/data/config/server.properties

    #Populate the mail.properties file:
    sudo echo "mail.smtp.auth=true
    mail.smtp.starttls.enable=true
    mail.smtp.host=smtp.gmail.com
    mail.smtp.port=587
    mail.smtp.username=YOUR_GMAIL@gmail.com
    mail.smtp.password=YOUR_GMAIL_APP_PASSWORD
    mail.smtp.connectiontimeout=30000
    mail.smtp.timeout=120000
    " > ./volumes/blynk_server/data/config/mail.properties

    #Information messages:
    echo "Sample properties files created in ~/IOTstack/volumes/blynk_server/data/config"
    echo "Make sure you edit the files with your details, and restart the container to take effect."

	

fi










