import boto3

task_id = "TODO"
cluster_name = "TODO"


def is_task_stopped(cluster_name, task_id):
    ret = boto3.client("ecs").describe_tasks(
        cluster=cluster_name,
        tasks=[task_id]
    )
    print(ret["tasks"][0]["lastStatus"])

    assert task_id == ret["tasks"][0]["taskArn"]
    return ret["tasks"][0]["lastStatus"] ==  "STOPPED"


assert is_task_stopped(cluster_name, task_id)
