
## Resources

*   Search github [issues](https://github.com/SensorsIot/IOTstack/issues?q=).
    Note: Also closed issues or pull-requests may have valuable hints.

*   Ask questions on [IOTStack Discord](https://discord.gg/ZpKHnks). Or report
    how you were able to fix a problem.

*   There are over 40 gists about IOTstack. These address a diverse range of
    topics from small convenience scripts to complete guides. These are
    individual contributions that aren't reviewed.

    You can add your own keywords into the search:
    [https://gist.github.com/search?q=iotstack](https://gist.github.com/search?q=iotstack)

## FAQ

!!! danger "Breaking update"
    A change done 2022-01-18 will require [manual steps](
    ../Updates/migration-network-change.md)
    or you may get an error like:  
    `ERROR: Service "influxdb" uses an undefined network "iotstack_nw"`


## Getting a clean slate

If you create a mess and can't see how to recover, try proceeding like this:

``` console
$ cd ~/IOTstack
$ docker-compose down
$ cd
$ mv IOTstack IOTstack.old
$ git clone https://github.com/SensorsIot/IOTstack.git IOTstack
```

In words:

1. Be in the right directory.
2. Take the stack down.
3. The `cd` command without any arguments changes your working directory to
   your home directory (variously known as `~` or `$HOME` or `/home/pi`).
4. Move your existing IOTstack directory out of the way. If you get a
   permissions problem:

    * Re-try the command with `sudo`; and
    * Read [a word about the `sudo` command](What-is-sudo.md). Needing `sudo`
      in this situation is an example of over-using `sudo`.

5. Check out a clean copy of IOTstack.

Now, you have a clean slate and can start afresh by running the menu:

``` console
$ cd ~/IOTstack
$ ./menu.sh
```

The `IOTstack.old` directory remains available as a reference for as long as
you need it. Once you have no further use for it, you can clean it up via:

``` console
$ cd
$ sudo rm -rf ./IOTstack.old # (1)
```

1. The `sudo` command is needed in this situation because some files and
   folders (eg the "volumes" directory and most of its contents) are owned by
   root.
