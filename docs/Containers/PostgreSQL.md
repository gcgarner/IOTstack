# PostgreSQL

## References

- [Docker image](https://hub.docker.com/_/postgres)
- [Postgre SQL Homepage](https://www.postgresql.org/)
- [Postgre SQL docs](https://www.postgresql.org/docs/current/index.html)

## About

PostgreSQL is an SQL server, for those that need an SQL database.

The database is available on port `5432`

## Configuration

The service definition includes the following environment variables:

* `TZ` your timezone. Defaults to `Etc/UTC`
* `POSTGRES_USER`. Initial username. Defaults to `postuser`.
* <a name="postgrespw"></a>`POSTGRES_PASSWORD`. Initial password associated with initial username. Defaults to `IOtSt4ckpostgresDbPw` (`postpassword` for old menu).
* `POSTGRES_DB`. Initial database. Defaults to `postdb`.

You can either edit the environment variables directly or provide your own substitutes by editing `~/IOTstack/.env`. Example:

``` console
$ cat ~/IOTstack/.env
TZ=Australia/Sydney
POSTGRES_PASSWORD=oneTwoThree
```

When the container is brought up:

* `TZ` will have the value `Australia/Sydney` (from `.env`)
* `POSTGRES_PASSWORD` will have the value `oneTwoThree` (from `.env`)
* `POSTGRES_USER` will have the value `postuser` (the default); and
* `POSTGRES_DB` will have the value `postdb` (the default).

The `TZ` variable takes effect every time the container is brought up. The other environment variables only work the first time the container is brought up.

It is highly recommended to select your own password before you launch the container for the first time. See also [Getting a clean slate](#cleanSlate).

## Management

You can interact with the PostgreSQL Relational Database Management System running in the container via its `psql` command. You can invoke `psql` like this:

``` console
$ docker exec -it postgres bash -c 'PGPASSWORD=$POSTGRES_PASSWORD psql $POSTGRES_DB $POSTGRES_USER'
```

> Because of the single quotes (<kbd>'</kbd>) surrounding everything after the `-c`, expansion of the environment variables is deferred until the command is executed *inside* the container.

You can use any of the following methods to exit `psql`:

* Type "\q" and press <kbd>return</kbd>
* Type "exit" and press <kbd>return</kbd>
* Press <kbd>control</kbd>+<kbd>D</kbd>

### password change

Once you have logged into `psql` you can reset the password like this:

``` sql
# ALTER USER «user» WITH PASSWORD '«password»';
```

Replace:

* `«user»` with the username (eg the default username is `postuser`)
* `«password»` with your new password.

Notes:

* Changing the password via the `ALTER` command does **not** update the value of the [`POSTGRES_PASSWORD`](#postgrespw) environment variable. You need to do that by hand.
* Whenever you make a change to a running container's environment variables, the changes will not take effect until you re-create the container by running:

	``` console
	$ cd ~/IOTstack
	$ docker-compose up -d postgresql
	```

## Getting a clean slate { #cleanSlate }

If you need to start over, proceed like this:

``` console
$ cd ~/IOTstack
$ docker-compose down postgres
$ sudo rm -rf ./volumes/postgres
$ docker-compose up -d postgres
```

> see also [if downing a container doesn't work](../Basic_setup/index.md/#downContainer)
