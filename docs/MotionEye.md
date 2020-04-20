# MotionQye
## References

* [Website](https://github.com/ccrisan/motioneye/wiki/Install-In-Docker)

## About

MotionEye is a camera/webcam package. The port is set to 8765

## Config

This is the yml entry. Notice that the devices is commented out. This is because if you don't have a camera attached then it will fail to start. Uncomment if you need to. This is for a Pi camera, you will need to add additional lines for usb cameras

```yml
  motioneye:
    image: "ccrisan/motioneye:master-armhf"
    container_name: "motioneye"
    restart: unless-stopped
    ports:
      - 8765:8765 
      - 8081:8081
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - ./volumes/motioneye/etc_motioneye:/etc/motioneye
      - ./volumes/motioneye/var_lib_motioneye:/var/lib/motioneye
    #devices:
    #  - "/dev/video0:/dev/video0"
```

## Login Details

On first login you will be asked for login details. The default user is `admin` (all lowercase) with no password

## Storage

By default local camera data will be stored in `/var/lib/motioneye/camera_name` in the container which equates to the following:

![image](https://user-images.githubusercontent.com/46672225/69735730-df934480-1139-11ea-833b-705c40ee4f8e.png)

![image](https://user-images.githubusercontent.com/46672225/69735408-4fed9600-1139-11ea-8618-f5b6c0064f27.png)

### Remote motioneye

If you have connected to a remote motion eye note that the directory is on that device and has nothing to do with the container.