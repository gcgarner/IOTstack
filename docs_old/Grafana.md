# Grafana

## References

- [Docker](https://hub.docker.com/r/grafana/grafana)
- [Website](https://grafana.com/)

## Setting your time-zone

The default *~/IOTstack/services/grafana/grafana.env* contains this line:

```
#TZ=Africa/Johannesburg
```

Uncomment that line and change the right hand side to [your own timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).


## Security
 
If Grafana has just been installed but has **never** been launched then the following will be true:

* The folder *~/IOTstack/volumes/grafana* will not exist; and
* The file *~/IOTstack/services/grafana/grafana.env* will contain these lines:

	```
	#GF_SECURITY_ADMIN_USER=admin
	#GF_SECURITY_ADMIN_PASSWORD=admin
	```

You should see those lines as **documentation** rather than something you are being invited to edit. It is telling you that the default administative user for Grafana is "admin" and that the default password for that user is "admin".

If you do not change anything then, when you bring up the stack and use a browser to connect to your Raspberry Pi on port 3000, Grafana will:

* Expect you to login as user "admin" with password "admin"; and then
* Force you to change the default password to something else.

Thereafter, you will login as "admin" with whatever password you chose. You can change the administrator's password as often as you like via the web UI (*profile* button, *change password* tab).

This method (of **not** touching these two keys in *grafana.env*) is the recommended approach. *Please* try to resist the temptation to fiddle!

### I want a different admin username (not recommended)

If, before you bring up the stack for the first time, you do this:

```
GF_SECURITY_ADMIN_USER=jack
#GF_SECURITY_ADMIN_PASSWORD=admin
```

then, when you bring up the stack and connect on port 3000, Grafana will:

* Expect you to login as user "jack" with password "admin"; and then
* Force you to change the default password to something else.

Thereafter, "jack" will be the Grafana administrator and you will login with the password you chose, until you decide to change the password to something else via the web UI.

Don't think you can come back later and tweak the Grafana administrator name in the environment variables. It doesn't work that way. It's a one-shot.

### I want a different default admin password (not recommended)

Well, first off, the two methods above both make you set a different password on first login so there probably isn't much point to this.

But, if you *really* insist…

If, before you bring up the stack for the first time, you do this:

```
#GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=jack
```
 
then, when you bring up the stack and use a browser to connect to your Raspberry Pi on port 3000, Grafana will expect you to login as user "admin" with password "jack".

Grafana will not force you to change the password on first login but you will still be able to change it via the web UI.

But don't think you can come back later and change the password in the environment variables. It doesn't work that way. It's a one-shot.

### I want to change everything (not recommended)

If, before you bring up the stack for the first time, you do this:

```
GF_SECURITY_ADMIN_USER=bill
GF_SECURITY_ADMIN_PASSWORD=jack
```

then, when you bring up the stack and use a browser to connect to your Raspberry Pi on port 3000, Grafana will expect you to login as user "bill" with password "jack".

Grafana will not force you to change the password on first login but you will still be able to change it via the web UI.

But don't think you can come back later and tweak either the username or password in the environment variables. It doesn't work that way. It's a one-shot.

### Distilling it down

**Before** Grafana is launched for the first time:

* *GF\_SECURITY\_ADMIN\_USER* has a default value of "admin". You *can* explicitly set it to "admin" or some other value. Whatever option you choose then that's the account name of Grafana's administrative user. But choosing any value other than "admin" is probably a bad idea.
* *GF\_SECURITY\_ADMIN\_PASSWORD* has a default value of "admin". You can explicitly set it to "admin" or some other value. If its value is "admin" then you will be forced to change it the first time you login to Grafana. If its value is something other than "admin" then that will be the password until you change it via the web UI.

These two environment keys **only** work for the **first** launch of Grafana. Once Grafana has been launched, you can **never** change either the username or the password by editing *grafana.env*.

For this reason, it is better to leave *grafana.env* in its shrink-wrapped state. Your first login is as "admin/admin" and then you set the password you actually want when Grafana prompts you to change it.

### HELP – I forgot my Grafana admin password!

Assuming your IOTstack is up, the magic incantation is:

```
$ docker exec grafana grafana-cli --homepath "/usr/share/grafana" admin reset-admin-password "admin"
```

Then, use a browser to connect to your Raspberry Pi on port 3000. Grafana will:

* Expect you login as user "admin" with password "admin"; and then
* Force you to change the default password to something else.

This magic incantation assumes that your administrative username is "admin". If you ignored the advice above and changed the administator username to something else then all bets are off. It might work anyway but we haven't tested it. Sorry. But that's why we said changing the username was not recommended.

## Overriding Grafana settings

Grafana documentation contains [a list of settings](https://grafana.com/docs/installation/configuration/). Settings are described in terms of how they appear in ".ini" files.

An example of the sort of thing you might want to do is to enable anonymous access to your Grafana dashboards. The [Grafana documentation](https://grafana.com/docs/grafana/latest/auth/overview/#anonymous-authentication) describes this in ".ini" format as:

```
[auth.anonymous]
enabled = true

# Organization name that should be used for unauthenticated users
org_name = Main Org.

# Role for unauthenticated users, other valid values are `Editor` and `Admin`
org_role = Viewer
```

".ini" format is not really appropriate in a Docker context. Instead, you use environment variables to override Docker's settings. Environment variables are placed in *~/IOTstack/services/grafana/grafana.env*.

You need to convert ".ini" format to environment variable syntax. The rules are:

* Start with "GF_", then
* Append the \[section name\], replacing any periods with underscores, then
* Append the section key "as is", then
* Append an "=", then
* Append the right hand side in quotes.

Applying those rules gets you:

```
GF_AUTH_ANONYMOUS_ENABLED="true"
GF_AUTH_ANONYMOUS_ORG_NAME="Main Org."
GF_AUTH_ANONYMOUS_ORG_ROLE="Viewer"
```

> It is not strictly necessary to encapsulate every right hand side value in quotes. In the above, both "true" and "Viewer" would work without quotes, whereas "Main Org." needs quotes because of the embedded space.

After you have changed *~/IOTstack/services/grafana/grafana.env*, you need to propagate the changes into the Grafana container:

```
$ cd ~/IOTstack
$ docker-compose stop grafana
$ docker-compose up -d
```

> In theory, the second command could be omitted, or both the second and third commands could be replaced with "docker-compose restart grafana" but experience suggests stopping the container is more reliable.

A slightly more real-world example would involve choosing a different default organisation name for anonymous access. This example uses "ChezMoi".

First, the environment key needs to be set to that value:

```
GF_AUTH_ANONYMOUS_ORG_NAME=ChezMoi
```

Then that change needs to be propagated into the Grafana container as explained above.

Next, Grafana needs to be told that "ChezMoi" is the default organisation:

1. Use your browser to login to Grafana as an administrator.
2. From the "Server Admin" slide-out menu on the left hand side, choose "Orgs".
3. In the list that appears, click on "Main Org". This opens an editing panel.
4. Change the "Name" field to "ChezMoi" and click "Update".
5. Sign-out of Grafana. You will be taken back to the login screen. Your URL bar will look something like this:

	```
	http://myhost.mydomain.com:3000/login
	```
6. Edit the URL to remove the "login" suffix and press return. If all your changes were applied successfully, you will have anonymous access and the URL will look something like this:
	
	```
	http://myhost.mydomain.com:3000/?orgId=1
	```

## HELP – I made a mess!

"I made a bit of a mess with Grafana. First time user. Steep learning curve. False starts, many. Mistakes, unavoidable. Been there, done that. But now I **really** need to start from a clean slate. And, yes, I understand there is no *undo* for this."

Begin by stopping Grafana:

```
$ cd ~/IOTstack
$ docker-compose stop grafana
```

You have two options:

1. Destroy your settings and dashboards but retain any plugins you may have installed:

	```
	$ sudo rm ~/IOTstack/volumes/grafana/data/grafana.db
	```

2. Nuke everything (triple-check this command **before** you hit return):

	```
	$ sudo rm -rf ~/IOTstack/volumes/grafana/data
	```

This is where you should edit *~/IOTstack/services/grafana/grafana.env* to correct any problems (such as choosing an administrative username other than "admin").

When you are ready, bring Grafana back up again:

```
$ cd ~/IOTstack
$ docker-compose up -d
```

Grafana will automatically recreate everything it needs. You will be able to login as "admin/admin".
