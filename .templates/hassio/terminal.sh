#!/bin/bash

echo "you are about to enter the shell for hassio"
echo "to update, type: hassio ha update --version=X.XX.X"
echo "to exit: exit"

docker exec -it hassio sh
