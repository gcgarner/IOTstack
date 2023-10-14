# MotionEye

## About

MotionEye is a web frontend for the Motion project.

## References

* MotionEye:
	- [Wiki](https://github.com/motioneye-project/motioneye/wiki)
	- [GitHub](https://github.com/motioneye-project/motioneye)
	- [DockerHub](https://hub.docker.com/r/dontobi/motioneye.rpi)
* Motion project:
	- [Documentation](https://motion-project.github.io/)
	- [GitHub](https://github.com/Motion-Project/motion)

## Service Definition

This is the default service definition:

``` yaml
motioneye:
  image: dontobi/motioneye.rpi:latest
  container_name: "motioneye"
  restart: unless-stopped
  ports:
    - "8765:8765"
    - "8766:8081"
  environment:
    - TZ=${TZ:-Etc/UTC}
  volumes:
    - ./volumes/motioneye/etc_motioneye:/etc/motioneye
    - ./volumes/motioneye/var_lib_motioneye:/var/lib/motioneye
```

## Administrative interface

MotionEye's administrative interface is available on port 8765. For example:

```
http://raspberrypi.local:8765
```

The default username is `admin` (all lower case) with no password.

## Camera streams

The first camera you define in the administrative interface is assigned to internal port 8081. The default service definition maps that to port 8766:

``` yaml
- "8766:8081"
```

You can access the stream with a web browser on port 8766. For example:

```
http://raspberrypi.local:8766
```

Each subsequent camera you define in the administrative interface will be assigned a new internal port number:

* Camera 2 will be internal port 8082, then
* Camera 3 will be internal port 8083,
* and so on.

Each camera you define after the first will need its own port mapping in the service definition in your compose file. For example:

``` yaml
- "8767:8082"
- "8768:8083"
- …
```

Key points:

1. You do not have to make camera streams available outside the container. It is optional.
2. You do not have to accept the default internal port assignments of 8081, 8082 and so on. You can change internal ports in the administrative interface if you wish. If you do this, remember to update the internal (right hand side) ports in the service definition in your compose file.
3. You do not have to adopt the external port sequence 8766, 8767 and so on. Port 8766 is the default for the first camera only because it does not conflict with any other IOTstack template.

## Clip Storage

By default local camera data is stored at the internal path:

```
/var/lib/motioneye/«camera_name»
```

That maps to the external path:

```
~/IOTstack/volumes/motioneye/var_lib_motioneye/«camera_name»
```

Tips:

* The automatic mapping to `«camera_name»` can be unreliable. After defining a camera, it is a good idea to double-check the actual path in the "Root Directory" field of the "File Storage" section in the administrative interface.
* Movie clips are kept forever by default. Depending on other settings, this can quickly run your Pi out of disk space so it's a good idea to tell MotionEye to discard old footage using the "Preserve Movies" field of the "Movies" section in the administrative interface.

### Backup considerations

Although it depends on your exact settings, MotionEye's video storage can represent a significant proportion of your backup files. If you want to constrain your backup files to reasonable sizes, consider excluding the video storage from your routine backups by changing where MotionEye videos are kept. This is one approach:  

1. Be in the appropriate directory:

	``` bash
	$ cd ~/IOTstack
	```

2. Terminate the motioneye container:

	``` bash
	$ docker-compose down motioneye
	```
	
	> see also [if downing a container doesn't work](../Basic_setup/index.md/#downContainer)

3. Move the video storage folder:

	``` bash
	$ sudo mv ./volumes/motioneye/var_lib_motioneye ~/motioneye-videos
	```

4. Open your `docker-compose.yml` in a text editor. Find this line in your `motioneye` service definition:

	``` yaml
	- ./volumes/motioneye/var_lib_motioneye:/var/lib/motioneye
	```

	and change it to be:

	``` yaml
	- /home/pi/motioneye-videos:/var/lib/motioneye
	```

	then save the edited compose file.

5. Start the container again:

	``` bash
	$ docker-compose up -d motioneye
	```

This change places video storage outside of the usual `~/IOTstack/volumes` path, where IOTstack backup scripts will not see it.

An alternative approach is to omit the volume mapping for `/var/lib/motioneye` entirely. Clips will be still be recorded inside the container and you will be able to play and download the footage using the administrative interface. However, any saved clips will disappear each time the container is re-created (not just restarted). Clips stored inside the container also will not form part of any backup.

If you choose this method, make sure you configure MotionEye to discard old footage using the "Preserve Movies" field of the "Movies" section in the administrative interface. This is a per-camera setting so remember to do it for **all** your cameras. If you do not do this, you are still at risk of running your Pi out of disk space, and it's a difficult problem to diagnose.

## Remote motioneye

If you have connected to a remote motion eye note that the directory is on that device and has nothing to do with the container.
