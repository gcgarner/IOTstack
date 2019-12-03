#!/bin/bash

echo 'Use the command "psql DATABASE USER" to enter your database, replace DATABASE and USER with your values'
echo "Remember to end queries with a semicolon ;"

docker exec -it postgres bash