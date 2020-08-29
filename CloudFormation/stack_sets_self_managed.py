import boto3
import click


DEFAULT_STACK_SET_PARAMS = {
    "StackSetName": "TODO",
    "Description": "TODO",
    "TemplateBody": "TODO",
    "TemplateURL": "TODO",
    "Parameters": [
    ],
    "Capabilities": [
        "CAPABILITY_IAM", # CAPABILITY_IAM | CAPABILITY_NAMED_IAM | CAPABILITY_AUTO_EXPAND
    ],
    "Tags": [
        {
            "Key": "TODO",
            "Value": "TODO"
        },
    ],
    "AdministrationRoleARN": "TODO",
    "ExecutionRoleName": "TODO",
    "PermissionModel": "SELF_MANAGED", #  SERVICE_MANAGED | SELF_MANAGED
    "AutoDeployment": {
        "Enabled": True,
        "RetainStacksOnAccountRemoval": True,
    },
    "ClientRequestToken": "TODO",
}

DEFAULT_STACK_INSTANCES_PARAMS = {
    "StackSetName": "TODO",
    "Accounts": [],
    "DeploymentTargets": {
        "Accounts": [],
        "OrganizationalUnitIds": []
    },
    "Regions": [],
    "ParameterOverrides": [
        {
            "ParameterKey": "TODO",
            "ParameterValue": "TODO",
            "UsePreviousValue": True,
            "ResolvedValue": "TODO"
        },
    ],
    "OperationPreferences": {
        "RegionOrder": [],
        "FailureToleranceCount": 123,
        "FailureTolerancePercentage": 123,
        "MaxConcurrentCount": 123,
        "MaxConcurrentPercentage": 123
    },
    "OperationId": "TODO",
}


def template_body(template_file):
    with open(template_file, "r") as cf_file:
        return cf_file.read()


def create_stack_set(profile_name, stack_name, template_file):
    client = boto3.session.Session(profile_name=profile_name).client("cloudformation")
    
    params = DEFAULT_STACK_SET_PARAMS
    params["TemplateBody"] = template_body(template_file)
    
    resp = client.create_stack_set(**params)
    stack_set_id = resp["StackSetId"]
    print(stack_set_id)


    params = DEFAULT_STACK_INSTANCES_PARAMS

    resp = client.create_stack_instances(**params)
    operation_id = resp["OperationId"]
    print(operation_id)


@click.command()
@click.option("--template", "-t", required=True, help="Template file")
@click.option("--profile", "-p", default="default", help="AWS profile name")
@click.option("--stack", "-s", required=True, help="Stack name")
def main(template, profile, stack):
    create_stack_set(profile_name=profile, stack_name=stack, template_file=template)


if __name__ == "__main__": 
    main()