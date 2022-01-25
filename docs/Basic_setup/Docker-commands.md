# Docker commands
## Aliases

I've added bash aliases for stopping and starting the stack. They can be installed in the docker commands menu. These commands no longer need to be executed from the IOTstack directory and can be executed in any directory

```bash
alias iotstack_up="docker-compose -f ~/IOTstack/docker-compose.yml up -d"
alias iotstack_down="docker-compose -f ~/IOTstack/docker-compose.yml down"
alias iotstack_start="docker-compose -f ~/IOTstack/docker-compose.yml start"
alias iotstack_stop="docker-compose -f ~/IOTstack/docker-compose.yml stop"
alias iotstack_update="docker-compose -f ~/IOTstack/docker-compose.yml pull"
alias iotstack_build="docker-compose -f ~/IOTstack/docker-compose.yml build"
```

You can now type `iotstack_up`, they even accept additional parameters `iotstack_stop portainer`
