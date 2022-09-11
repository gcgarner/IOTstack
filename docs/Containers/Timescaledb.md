
### Default port changed

In order to avoid port conflict with PostgreSQL, the public database port is
mapped to **5433** using Docker.

Cross-container access from other containers still works as previously:
`timescaledb:5432`.
