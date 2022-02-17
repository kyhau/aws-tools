"""
Find Windows images size >= 1 GB referenced in current clusters in all specified aws accounts
"""
import json
import logging
import os
import re
from collections import defaultdict

from boto3.session import Session

logging.getLogger().setLevel(logging.INFO)

profiles = {
    "111111111111": "profile-1",
    "222222222222": "profile-2",
    "333333333333": "profile-3",
}

GB = 1024 * 1024 * 1024
g_account_tasks = {}
g_images = []
os.makedirs(f"outputs", exist_ok=True)


def write_json_file(filename, data, indent=0, sort_keys=True):
    with open(filename, "w") as f:
        return json.dump(data, f, indent=indent, sort_keys=sort_keys)


def paginate(client, func_name, kwargs=None):
    for page in client.get_paginator(func_name).paginate(**kwargs if kwargs else {}).result_key_iters():
        for item in page:
            yield item


def check_container_instance_platform(ecs_client, session, region, cluster_arn):
    container_instance_arns = ecs_client.list_container_instances(cluster=cluster_arn).get("containerInstanceArns", [])
    if container_instance_arns:
        container_instances = ecs_client.describe_container_instances(cluster=cluster_arn, containerInstances=[container_instance_arns[0]]).get("containerInstances", [])
        if container_instances:
            ec2_instance_id = container_instances[0]["ec2InstanceId"]
            if ec2_instance_id:
                 ec2_instances = session.client("ec2", region_name=region).describe_instances(InstanceIds=[ec2_instance_id])["Reservations"][0]["Instances"]
                 if ec2_instances:
                     # Platform (string) -- The value is Windows for Windows instances; otherwise blank.
                     return ec2_instances[0].get("Platform")


def check_ecs_tasks(account_id, region, profile):
    session = Session(profile_name=profile)
    client = session.client("ecs", region_name=region)
    results = []

    cluster_arns = [item for item in paginate(client, "list_clusters")]
    for cluster_arn in cluster_arns:
        task_arns = [item for item in paginate(client, "list_tasks", {"cluster": cluster_arn})]

        while len(task_arns) > 0:
            # Note that `tasks` supports a list of up to 100 task IDs or full ARN entries.
            check_tasks = task_arns[0:min(100, len(task_arns))]

            for task in client.describe_tasks(cluster=cluster_arn, tasks=check_tasks)["tasks"]:
                # Retrieve Image in running containers, or container definitions (if it's
                # Fargate or the running containers (task["containers"]) has "Image"==None)

                containers = task["containers"]
                none_image_found = any(c.get("image") is None for c in containers)

                # Get platform (attempt 1)
                os_family = task.get("platformFamily")  # seems alway null


                if task["launchType"] == "FARGATE" or none_image_found:
                    resp = client.describe_task_definition(taskDefinition=task["taskDefinitionArn"])
                    containers = resp["taskDefinition"]["containerDefinitions"]

                    # Get platform (attempt 2)
                    os_family = resp["taskDefinition"].get("runtimePlatform", {}).get("operatingSystemFamily")  # seems alway null

                if os_family is None:
                    # Get platform (attempt 3)
                    os_family = check_container_instance_platform(client, session, region, task["clusterArn"])

                for container in containers:
                    data = {
                        "image": container.get("image"),  # can have None image
                        "imageDigest": container.get("imageDigest"),
                        "clusterArn": task["clusterArn"],
                        "launchType": task["launchType"],
                        "osFamily": os_family,
                        "taskArn": task["taskArn"],
                        "lastStatus": task["lastStatus"],
                        "accountId": account_id,
                        "region": region,
                    }
                    results.append(data)

                    if container.get("image"):
                        g_images.append(container.get("image"))

            task_arns = task_arns[100:]

    g_account_tasks[account_id] = results

    write_json_file(f"outputs/{account_id}_tasks.json", results, indent=2, sort_keys=True)


def group_images_by_account(images):
    acc_images_dict = defaultdict(dict)
    for image in set(images):
        # Possible formats: repository-url/image, repository-url/image:tag, repository-url/image@digest
        matched = re.search("(\d+)\.dkr\.ecr\..+?\.amazonaws\.com\/([^:@]+)([:|@]*)(.*)$", image)
        if matched is None:
            continue

        ecr_account_id, repository, separator = matched.groups()[0], matched.groups()[1], matched.groups()[2]
        if ecr_account_id is None:
            continue

        image_tag = image_digest = None
        if separator == ":":  # tag
            image_tag = matched.groups()[3]
        elif separator == "@":  # digest
            image_digest = matched.groups()[3]
        else:
            image_tag = "latest"

        image_id = {}
        if image_tag not in (None, ""):
            image_id["imageTag"] = image_tag
        elif image_digest not in (None, ""):
            image_id["imageDigest"] = image_digest
        acc_images_dict[ecr_account_id][image] = {"repository": repository, "image_id": image_id}
    return acc_images_dict


def check_ecr_images(g_images, region):
    # {account_id: {image: {"image": image, "repository": repository, "image_id": image_id}
    acc_images_dict = group_images_by_account(g_images)

    for account_id, image_data in acc_images_dict.items():
        ecr_client = Session(profile_name=profiles[account_id]).client("ecr", region_name=region)
        for image, data in image_data.items():
            try:
                ret_images = ecr_client.describe_images(repositoryName=data["repository"], imageIds=[data["image_id"]])["imageDetails"]
                acc_images_dict[account_id][image].update({"imageSizeInBytes": ret_images[0]["imageSizeInBytes"]})
                assert(len(ret_images)==1)
            except Exception as e:
                logging.error(e)

    write_json_file(f"outputs/ecr_images.json", acc_images_dict, indent=2, sort_keys=True)
    return acc_images_dict


def main():
    region = "ap-southeast-2"

    # Check ecs tasks, task definitions, container instances;
    # and store the data to g_account_tasks and g_images
    for account_id, profile in profiles.items():
        check_ecs_tasks(account_id, region, profile)

    # Retrieve ECR images' info
    acc_images_dict = check_ecr_images(g_images, region)

    # Create summary for images size >= 1 GB or osFamily is not None
    ret = []
    for account_id, tasks in g_account_tasks.items():
        for task in tasks:
            try:
                image_size = acc_images_dict[account_id][task["image"]]["imageSizeInBytes"]
            except:
                image_size = 0
            task.update({"imageSizeInBytes": image_size})

            if task["osFamily"]:
                ret.append(task)

            if float(image_size)/GB >= 1:
                ret.append(task)

        # Rewrite file with size
        write_json_file(f"outputs/{account_id}_tasks.json", tasks, indent=2, sort_keys=True)

    write_json_file(f"outputs/ecr_images_windowsge_1GB.json", ret, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
