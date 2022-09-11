# Migration: network change

Networking under both *new menu* (master branch) and *old menu* (old-menu branch) has undergone a significant change. This will not affect new users of IOTstack (who will adopt it automatically). Neither will it affect existing users who do not use the menu to maintain their stacks (see [adopting networking changes by hand](#networkHandEdit) below).
 
Users who *do* use the menu to maintain their stacks will also be unaffected *until the next menu run*, at which point it will be prudent to down your stack entirely and re-select all your containers. Downing the stack causes Docker to remove all associated networks as well as the containers.

These changes mean that networking is **identical** under both *old* and *new* menus. To summarise the changes:

1. Only two internal networks are defined – as follows:

	* "default" which adopts the name `iotstack_default` at runtime.
	* "nextcloud" which adopts the name `iotstack_nextcloud` at runtime.
	
	If you are using docker-compose v2.0.0 or later then the `iotstack_nextcloud` network will only be instantiated if you select NextCloud as one of your services. Earlier versions of docker-compose instantiate all networks even if no service uses them (which is why you get those warnings at "up" time).

2. The only service definitions which now have `networks:` directives are:

	* NextCloud: joins the "default" and "nextcloud" networks; and
	* NextCloud_DB: joins the "nextcloud" network.
	
	All other containers will join the "default" network, automatically, without needing any `networks:` directives.

#### <a name="networkHandEdit"> adopting networking changes by hand </a>

If you maintain your `docker-compose.yml` by hand, you can adopt the networking changes by doing the following:

1. Take your stack down. This causes Docker to remove any existing networks. 
2. Remove **all** `networks:` directives wherever they appear in your `docker-compose.yml`. That includes: 

	* the `networks:` directives in all service definitions; and
	* the `networks:` specifications at the end of the file.

3. Append the contents of the following file to your `docker-compose.yml`:

	```
	~/IOTstack/.templates/docker-compose-base.yml
	```

	For example:
	
	```
	$ cat ~/IOTstack/.templates/docker-compose-base.yml >>~/IOTstack/docker-compose.yml
	```
	
	The `docker-compose-base.yml` file is named `env.yml` in the *old-menu* branch.

4. If you run the NextCloud service then:

	* Add these lines to the NextCloud service definition:

		```
		networks:
		  - default
		  - nextcloud
		```

	* Add these lines to the NextCloud_DB service definition:

		```
		networks:
		  - nextcloud
		```

5. Bring up your stack.	
