# Mosquitto
## References
- [Docker](https://hub.docker.com/_/eclipse-mosquitto)
- [Website](https://mosquitto.org/)

[Setting up passwords](https://www.youtube.com/watch?v=1msiFQT_flo)

## Security
By default, the Mosquitto container has no password. You can leave it that way if you like but its always a good idea to secure your services.

Step 1
To add the password run `./services/mosquitto/terminal.sh`, I put some helper text in the script. Basically, you use the `mosquitto_passwd -c /mosquitto/config/pwfile MYUSER` command, replacing MYUSER with your username. it will then ask you to type your password and confirm it. exiting with `exit`. 

Step 2
Edit the file called services/mosquitto/mosquitto.conf and remove the comment in front of password_file. Restart the container with `docker-compose restart mosquitto`. Type those credentials into Node-red etc.
