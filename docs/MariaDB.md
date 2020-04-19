## Source
* [Docker hub](https://hub.docker.com/r/linuxserver/mariadb/)
* [Webpage](https://mariadb.org/)

## About

MariaDB is a fork of MySQL. This is an unofficial image provided by linuxserver.io because there is no official image for arm

## Conneting to the DB

The port is 3306. It exists inside the docker network so you can connect via `mariadb:3306` for internal connections. For external connections use `<your Pis IP>:3306`

![image](https://user-images.githubusercontent.com/46672225/69734358-7f030800-1137-11ea-9874-7d2c86b3d239.png)

## Setup

Before starting the stack edit the `./services/mariadb/mariadb.env` file and set your access details. This is optional however you will only have one shot at the preconfig. If you start the container without setting the passwords then you will have to either delete its volume directory or enter the terminal and change manually

The env file has three commented fields for credentials, either **all three** must be commented or un-commented. You can't have only one or two, its all or nothing.

## Terminal

A terminal is provided to access mariadb by the cli. execute `./services/maraidb/terminal.sh`. You will need to run `mysql -uroot -p` to enter mariadbs interface