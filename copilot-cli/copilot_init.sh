#!/bin/bash
# https://github.com/aws/copilot-cli
# https://docs.aws.amazon.com/AmazonECS/latest/developerguide/getting-started-aws-copilot-cli.html
set -e

# git clone git@github.com:aws-samples/aws-copilot-sample-service.git demo-app

if [ ! -d "demo-app" ]; then
  echo "Error: demo-app directory does not exist. Please clone the repository first."
  exit 1
fi

pushd demo-app

copilot init --app demo --svc api --svc-type 'Load Balanced Web Service' --dockerfile './Dockerfile' --deploy
#  -a, --app string          Name of the application.
#      --deploy              Deploy your service to a "test" environment.
#  -d, --dockerfile string   Path to the Dockerfile.
#  -h, --help                help for init
#      --port uint16         Optional. The port on which your service listens.
#  -s, --svc string          Name of the service.
#  -t, --svc-type string     Type of service to create. Must be one of:
#                            "Load Balanced Web Service", "Backend Service"
#      --tag string          Optional. The container image tag.

# copilot app delete --env-profiles test=default
popd

: <<'END_COMMENT'
Welcome to the Copilot CLI! We're going to walk you through some questions
to help you get set up with an application on ECS. An application is a collection of
containerized services that operate together.

Ok great, we'll set up a Load Balanced Web Service named api in application demo listening on port 80.

Created the infrastructure to manage services under application demo.

Wrote the manifest for service api at copilot/api/manifest.yml
Your manifest contains configurations like your container size and port (:80).

Created ECR repositories for service api.

Created the infrastructure for the test environment.
- Virtual private cloud on 2 availability zones to hold your services     [Complete]
- Virtual private cloud on 2 availability zones to hold your services     [Complete]
  - Internet gateway to connect the network to the internet               [Complete]
  - Public subnets for internet facing services                           [Complete]
  - Private subnets for services that can't be reached from the internet  [Complete]
  - Routing tables for services to talk with each other                   [Complete]
- ECS Cluster to hold your services                                       [Complete]
- Application load balancer to distribute traffic                         [Complete]

Linked account 123456789012 and region ap-southeast-2 to application demo.

Created environment test in region ap-southeast-2 under application demo.

[+] Building 25.1s (7/7) FINISHED
...

WARNING! Your password will be stored unencrypted in /home/xxx/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
The push refers to repository [123456789012.dkr.ecr.ap-southeast-2.amazonaws.com/demo/api]
...

✔ Deployed api, you can access it at http://demo-Publi-4ZRT0E9ANEG1-1224506604.ap-southeast-2.elb.amazonaws.com.
/c/xxx/github/xxx/copilot-cli

END_COMMENT
