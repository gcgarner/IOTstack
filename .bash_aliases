IOTSTACK_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
alias iotstack_up="cd "$IOTSTACK_HOME" && docker-compose up -d --remove-orphans"
alias iotstack_down="cd "$IOTSTACK_HOME" && docker-compose down --remove-orphans"
alias iotstack_start="cd "$IOTSTACK_HOME" && docker-compose start"
alias iotstack_stop="cd "$IOTSTACK_HOME" && docker-compose stop"
alias iotstack_pull="cd "$IOTSTACK_HOME" && docker-compose pull"
alias iotstack_build="cd "$IOTSTACK_HOME" && docker-compose build --pull --no-cache"
alias iotstack_update_docker_images='f(){ iotstack_pull "$@" && iotstack_build "$@" && iotstack_up --build "$@"; }; f'
