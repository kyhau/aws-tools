"""
List items of
```
{
  "AccountId": string,
  "ClusterArn": string,
  "HighSeverityCount": sum-of-critical-and-high-severity,
  "Image": string,
  "LastStatus": string,
  "LaunchType": string,
  "Region": string,
  "TaskArn": string
}
```
"""
from boto3.session import Session
from botocore.exceptions import ClientError
import boto3
import click
from collections import defaultdict
import logging
import re

from helper.aws import AwsApiHelper
from helper.ser import dump_json

logging.getLogger().setLevel(logging.INFO)


def get_session_for_account(account_id, role_name):
    try:
        role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
        ret = boto3.client("sts").assume_role(RoleArn=role_arn, RoleSessionName="image_scan_checker")
        cred = {
            "aws_access_key_id": ret["Credentials"]["AccessKeyId"],
            "aws_secret_access_key": ret["Credentials"]["SecretAccessKey"],
            "aws_session_token": ret["Credentials"]["SessionToken"]
        }
        return Session(**cred)
    except Exception as e:
        logging.debug(f"Failed to assume role {role_name} in {account_id}: {e}")
        return


class EcrHelper():
    def __init__(self, cross_account_role_name):
        self._cross_account_role_name = cross_account_role_name
        self._global_ecr_checked_images = {}
    
    def check_image_scan_findings(self, images, region, src_account_id, src_session):
        for ecr_account_id, image_info_list in self.group_images_by_account(images).items():

            if ecr_account_id == src_account_id:
                session_2 = src_session
            else:
                session_2 = get_session_for_account(ecr_account_id, region)

            if session_2 is None:
                logging.info(f"Do not have access to {ecr_account_id}. Skipped")

                for image_info in image_info_list:
                    self._global_ecr_checked_images[image_info["image"]] = -3
                continue

            ecr_client = session_2.client("ecr", region_name=region)

            for image_info in image_info_list:
                self.describe_image_scan_findings(ecr_client, ecr_account_id, image_info)
    
    def describe_image_scan_findings(self, ecr_client, ecr_account_id, image_info):
        high_cnt = 0
        params = {
            "registryId": ecr_account_id,
            "repositoryName": image_info["repository"],
            "imageId": image_info["image_id"],
            "maxResults": 1000,
        }

        try:
            for item in ecr_client.get_paginator("describe_image_scan_findings").paginate(**params):
                if item["imageScanStatus"]["status"] == "COMPLETE":
                    severity_counts = item["imageScanFindings"]["findingSeverityCounts"]
                    high_cnt = high_cnt + severity_counts.get("CRITICAL", 0) + severity_counts.get("HIGH", 0)
            
            self._global_ecr_checked_images[image_info["image"]] = high_cnt
    
        except ClientError as e:
            if e.response["Error"]["Code"] in ["RepositoryNotFoundException"]:
                self._global_ecr_checked_images[image_info["image"]] = -2
                logging.error(f"Unable to process {params}: {e}")

    def group_images_by_account(self, images):
        acc_images_dict = defaultdict(list)
        for image in set(images):
            if image in self._global_ecr_checked_images:
                # skip if we have already checked it
                continue
            
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
            acc_images_dict[ecr_account_id].append({"image": image, "repository": repository, "image_id": image_id})
        return acc_images_dict


class EcsHelper(AwsApiHelper):
    def __init__(self, ecr_helper):
        super().__init__()
        self._ecr_helper = ecr_helper

    def lookup_image_details(self, results, region, account_id, session):
        self._ecr_helper.check_image_scan_findings(
            [item["Image"] for item in results if item["Image"] is not None], region, account_id, session)

        for item in results:
            high_severity_cnt = self._ecr_helper._global_ecr_checked_images.get(item["Image"], -1)
            if high_severity_cnt == -1:
                item["ImageScanError"] = "NullImage"
            elif high_severity_cnt == -2:
                item["ImageScanError"] = "RepositoryNotFound"  # e.g Tag is removed
            elif high_severity_cnt == -3:
                item["ImageScanError"] = "AccessDenied"
            item["HighSeverityCount"] = max(high_severity_cnt, 0)

        return results if results is not None else []

    def process_request(self, session, account_id, region, kwargs):
        client = session.client("ecs", region_name=region)
        results = []
        
        cluster_arns = [item for item in self.paginate(client, "list_clusters")]
        for cluster_arn in cluster_arns:
            task_arns = [item for item in self.paginate(client, "list_tasks", {"cluster": cluster_arn})]

            while len(task_arns) > 0:
                # Note that `tasks` supports a list of up to 100 task IDs or full ARN entries.
                check_tasks = task_arns[0:min(100, len(task_arns))]
                
                for task in client.describe_tasks(cluster=cluster_arn, tasks=check_tasks)["tasks"]:
                    # Retrieve Image in running containers, or container definitions (if it's
                    # Fargate or the running containers (task["containers"]) has "Image"==None)
                    
                    containers = task["containers"]
                    none_image_found = any(c.get("image") is None for c in containers)
                    if task["launchType"] == "FARGATE" or none_image_found:
                        resp = client.describe_task_definition(
                            taskDefinition=task["taskDefinitionArn"])
                        containers = resp["taskDefinition"]["containerDefinitions"]

                    for container in containers:
                        data = {
                            "Image": container.get("image"),  # can have None image
                            "ClusterArn": task["clusterArn"],
                            "LaunchType": task["launchType"],
                            "TaskArn": task["taskArn"],
                            "LastStatus": task["lastStatus"],
                            "AccountId": account_id,
                            "Region": region,
                        }
                        results.append(data)
                task_arns = task_arns[100:]

        for result in self.lookup_image_details(results, region, account_id, session):
            print(dump_json(result))


@click.command()
@click.option("--x-role-name", "-x", help="Name of a cross account role for accessing cross account images")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(x_role_name, profile, region):
    ecr_helper = EcrHelper(x_role_name)
    EcsHelper(ecr_helper).start(profile, region, "ecs")


if __name__ == "__main__":
    main()
