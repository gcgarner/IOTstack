# Portainer agent
## References 
- [Docker](https://hub.docker.com/r/portainer/agent)
- [Docs](https://portainer.readthedocs.io/en/stable/agent.html)

## About

The portainer agent is a great way to add a second docker instance to an existing portainer instance. This allows you to manage multiple docker environments from one portainer instance.

## Adding to an existing instance

When you want to add the agent to an existing portainer instance. 

* You go to the endpoints tab.
* Click on `Add endpoint`
* Select Agent
* Enter the name of the agent
* Enter the url of the endpoint `ip-of-agent-instance:9001`
* Click on add endpoint
