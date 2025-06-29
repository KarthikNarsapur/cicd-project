# cicd for python-docker

Simple containerized Python web app

## Getting started

Use the command `docker-compose up --build` to build the Dockerfile and run locally.

### Azure

You can use the link below to deploy the ARM template to Azure to create the infrastructure

[![Deploy To Azure](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazure.svg?sanitize=true)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Frivoric%2Fwebsitemon%2Fmaster%2Fazuredeploy.json)
[![Visualize](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/visualizebutton.svg?sanitize=true)](http://armviz.io/#/?load=https%3A%2F%2Fraw.githubusercontent.com%2Frivoric%2Fwebsitemon%2Fmaster%2Fazuredeploy.json)

You can use the template to deploy images from Docker Hub or from your own Azure Container Registry (ACR).
If you do not have an ACR the template can be ran with deployContainerRegistry set to true and containerRegistryName / Username / Password left blank.
This will deploy an ACR and generic blank app service. Normally this step would be done with a separate shared resources ARM template but I've included it to keep it simple.
You can manually deploy using the AZ CLI to this set up (see link below).

Next step is to build the docker container(s) and push the docker image(s) up to this registry in the normal way (see link below if you are unsure).

Finally you can run the template in normal mode to deploy the docker container.
If you are using Docker Hub you do not need to pass in a username and password. If you are using your own ACR you do.

## Links

### Azure

If you are looking for manual way to build and deploy the container look at the following tutorial -
https://docs.microsoft.com/en-us/azure/app-service/containers/tutorial-custom-docker-image

Documentation for environment variables used in multi-container app services -
https://docs.microsoft.com/en-us/azure/app-service/containers/app-service-linux-faq#custom-containers

### Docker

