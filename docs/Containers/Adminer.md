# Adminer
## References
- [Docker](https://hub.docker.com/_/adminer)
- [Website](https://www.adminer.org/)

## About

This is a nice tool for managing databases. Web interface has moved to port 9080. There was an issue where openHAB and Adminer were using the same ports. If you have an port conflict edit the docker-compose.yml and under the adminer service change the line to read:
```
    ports:
      - 9080:8080
```
