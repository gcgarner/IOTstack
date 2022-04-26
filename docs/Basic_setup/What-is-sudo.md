# What is sudo?

Many first-time users of IOTstack get into difficulty by misusing the `sudo` command. The problem is best understood by example. In the following, you would expect `~` (tilde) to expand to `/home/pi`. It does:

``` console
$ echo ~/IOTstack
/home/pi/IOTstack
```

The command below sends the same `echo` command to `bash` for execution. This is what happens when you type the name of a shell script. You get a new instance of `bash` to run the script:

``` console
$ bash -c 'echo ~/IOTstack'
/home/pi/IOTstack
```

Same answer. Again, this is what you expect. But now try it with `sudo` on the front:

``` console
$ sudo bash -c 'echo ~/IOTstack'
/root/IOTstack
```

Different answer. It is different because `sudo` means "become root, and then run the command". The process of becoming root changes the home directory, and that changes the definition of `~`.

Any script designed for working with IOTstack assumes `~` (or the equivalent `$HOME` variable) expands to `/home/pi`. That assumption is invalidated if the script is run by `sudo`.

Of necessity, any script designed for working with IOTstack will have to invoke `sudo` **inside** the script **when it is required**. You do not need to second-guess the script's designer.

Please try to minimise your use of `sudo` when you are working with IOTstack. Here are some rules of thumb:

1. Is what you are about to run a script? If yes, check whether the script already contains `sudo` commands. Using `menu.sh` as the example:

	``` console
	$ grep -c 'sudo' ~/IOTstack/menu.sh
	28
	```

	There are numerous uses of `sudo` within `menu.sh`. That means the designer thought about when `sudo` was needed.

2. Did the command you **just executed** work without `sudo`? Note the emphasis on the past tense. If yes, then your work is done. If no, and the error suggests elevated privileges are necessary, then re-execute the last command like this:

	``` console
	$ sudo !!
	```

It takes time, patience and practice to learn when `sudo` is **actually** needed. Over-using `sudo` out of habit, or because you were following a bad example you found on the web, is a very good way to find that you have created so many problems for yourself that will need to reinstall your IOTstack. *Please* err on the side of caution!

## Configuration

To edit sudo functionality and permissions use: `sudo visudo`

For instance, to allow sudo usage without prompting for a password:
```bash
# Allow members of group sudo to execute any command without password prompt
%sudo   ALL=(ALL:ALL) NOPASSWD:ALL
```

For more information: `man sudoers`
