#!/bin/bash

echo 'to generate a new password hash copy the following line and change PASSWORD'
echo $'node -e "console.log(require(\'bcryptjs\').hashSync(process.argv[1], 8));" PASSWORD'
echo 'then "exit"'

docker exec -it nodered bash
