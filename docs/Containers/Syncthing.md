# Syncthing

Syncthing is a continuous file synchronization program. It synchronizes files between two or more computers in real time, safely protected from prying eyes. Your data is your data alone and you deserve to choose where it is stored, whether it is shared with some third party, and how it's transmitted over the internet.

Forget about using propietary solutions and take control of your data. Syncthing is an open source solution for synchronizing your data in a p2p way. 

## References

- [Syncthing home page](https://syncthing.net/)
- [GitHub repository](https://github.com/syncthing/syncthing)
- [linuxserver.io docker image](https://docs.linuxserver.io/images/docker-syncthing) - The one used here
- [Official Syncthing docker image](https://hub.docker.com/r/syncthing/syncthing) - Not the one used here

    - For more information about official syncthing image have a look at [here](https://github.com/syncthing/syncthing/blob/main/README-Docker.md) 
  
## Web interface

The web UI can be found on  `yourip:8384`

## Data & volumes

Configuration data is available under `/config` containers directroy and mapped to `./volumes/syncthing/config` . 

The data you want to sync must be under `/app` directory.

## Ports

Have a look at `~/IOTStack/.templates/syncthing/service.yml` or linuxserve docker documentation, by the way, used ports are; 

```      
    ports:
      - 8384:8384 # Web UI
      - 22000:22000/tcp # TCP file transfers
      - 22000:22000/udp # QUIC file transfers
      - 21027:21027/udp # Receive local discovery broadcasts
```   
   
      
