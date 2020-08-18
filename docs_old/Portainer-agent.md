# Portainer agent
## References 
- [Docker](https://hub.docker.com/r/portainer/agent)
- [Docs](https://portainer.readthedocs.io/en/stable/agent.html)

## About

The protainer agent is a great way to add a second docker instance to a existing portainer instance. this allows you to mananage multiple docker enviroments form one prortainer instance

## Adding to an existing instance

When you want to add the the agent to an existing portianer instance. 

* You go to the endpoints tab.
* Click on `Add endpoint`
* Select Agent
* Enter the name of the agent
* Enter the url of the endpoint `ip-of-agent-instance:9001`
* Click on add endpoint