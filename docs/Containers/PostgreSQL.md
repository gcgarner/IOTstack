# PostgreSQL
## References
- [Docker image](https://hub.docker.com/_/postgres)
- [Postgre SQL Homepage](https://www.postgresql.org/)
- [Postgre SQL docs](https://www.postgresql.org/docs/current/index.html)

## About

PostgreSQL is an SQL server, for those that need an SQL database.

The database is available on port `5432`

## Configuration

Optional variables to define in `~/IOTstack/.env`:

* `IOTSTACK_postgres_PASSWORD` database password, defaults to
  *IOtSt4ckpostgresDbPw*.
* `IOTSTACK_postgres_user` database user, defaults to *postuser*.

It is highly recommended to change the password. (For old-menu the database
credentials can be found in the file `./volumes/postgres/postgres.env`.)

## Management

You can interact with the postgress in the container with the command:
``` console
$ docker exec -it postgres psql -d postdb -U postuser
```

Once you have logged in you can reset the password for postuser replacing
`<<password>>` with your new password:
``` sql
ALTER USER postuser WITH PASSWORD '<<password>>';
```

