#!/bin/bash
# https://docs.aws.amazon.com/AmazonECS/latest/developerguide/launch_container_instance.html

your_cluster_name="TODO"

echo ECS_CLUSTER=${your_cluster_name} >> /etc/ecs/ecs.config
