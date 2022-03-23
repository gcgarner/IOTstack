# PostgreSQL
## References
- [Docker](https://hub.docker.com/_/postgres)
- [Website](https://www.postgresql.org/)
## About
PostgreSQL is an SQL server, for those that need an SQL database. The database credentials can be found in the file `./volumes/postgres/postgres.env`. It is highly recommended to change the user, password and default database

If you left the docker-compose.yml file with the default values, you can interact with the postgress in the container with the follwoing command, replacing `<<raspberypi ip>>` with the ip address to your RasperyPi.  
`docker exec -it postgres psql -h <<raspberypi ip>> -d postdb -U postuser`

Once you have logged in you should change the default password to postuser replacing `<<password>>` with your new password.
`ALTER USER postuser WITH PASSWORD '<<password>>';`

You can find more information about working with postgres at https://www.postgresql.org/docs/8.0/.  
