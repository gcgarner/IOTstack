#!/bin/bash

echo 'Use the command "psql DATABASE USER" to enter your database, replace DATABASE and USER with your values'
echo "Remember to end queries with a semicolon ;"
echo ""
echo "IOTstack postgres Documentation: https://sensorsiot.github.io/IOTstack/Containers/PostgreSQL/"
echo ""
echo "docker exec -it postgres bash"

docker exec -it postgres bash
