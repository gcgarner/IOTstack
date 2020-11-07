#!/bin/bash

echo "run 'mysql -uroot -p' for terminal access"
echo ""
echo "IOTstack mariadb Documentation: https://sensorsiot.github.io/IOTstack/Containers/MariaDB/"
echo ""
echo "docker exec -it mariadb bash"

docker exec -it mariadb bash
