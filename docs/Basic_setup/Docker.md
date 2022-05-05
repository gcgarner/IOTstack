
## Logging

When Docker starts a container, it executes its *entrypoint* command. Any
output produced by this command is logged by Docker. By default Docker stores
logs internally together with other data associated to the container image.

This has the effect that when recreating or updating a container, logs shown by
`docker-compose logs` won't show anything associated with the previous
instance. Use `docker system prune` to remove old instances and free up disk
space. Keeping logs only for the latest instance is helpful when testing, but
may not be desirable for production.

By default there is no limit on the log size. Surprisingly, when using a
SD-card this is exactly what you want. If a runaway container floods the log
with output, writing will stop when the disk becomes full. Without a mechanism
to prevent such excessive writing, the SD-card would keep being written to
until the flash hardware [program-erase cycle](
https://www.techtarget.com/searchstorage/definition/P-E-cycle) limit is
reached, after which it is permanently broken.

When using a quality **SSD-drive**, potential flash-wear isn't usually a
concern. Then you can enable log-rotation by either:

1.  Configuring Docker to do it for you automatically. Edit your
    `docker-compose.yml` and add a top-level *x-logging* and a *logging:* to
    each service definition. The Docker compose reference documentation has
    a good [example](https://docs.docker.com/compose/compose-file/compose-file-v3/#extension-fields).

2.  Configuring Docker to [log to the host system's journald](
    https://github.com/SensorsIot/IOTstack/issues/508#issuecomment-1094372250).

    ps. if `/etc/docker/daemon.json` doesn't exist, just create it.

## Aliases

Bash aliases for stopping and starting the stack and other common operations
are in the file `.bash_aliases`. To use them immediately and in future logins,
run in a console:

``` console
$ source ~/IOTstack/.bash_aliases
$ echo "source ~/IOTstack/.bash_aliases" >> ~/.profile
```

These commands no longer need to be executed from the IOTstack directory and can be executed in any directory

``` bash title=".bash_aliases"
--8<-- ".bash_aliases"
```

You can now type `iotstack_up`. The aliases also accept additional parameters,
e.g. `iotstack_stop portainer`.

The `iotstack_update_docker_images` alias will [update docker images](
http://localhost:8000/Updates/#recommended-update-only-docker-images) to newest
released images, build and recreate containers. Do note that using this will
result in a broken containers from time to time, as upstream may release faulty
docker images. Have proper backups, or be prepared to manually pin a previous
release build by editing `docker-compose.yml`.
