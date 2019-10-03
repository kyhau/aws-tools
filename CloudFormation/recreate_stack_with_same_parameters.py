import boto3
import click


def template_body(template_file):
    with open(template_file, "r") as cf_file:
        return cf_file.read()


def recreate_stack_with_same_parameters(profile_name, stack_name, template_file):
    client = boto3.session.Session(profile_name=profile_name).client("cloudformation")

    resp = client.describe_stacks(StackName=stack_name)
    if "IN_PROGRESS" in resp["Stacks"][0]["StackStatus"]:
        raise Exception(f'Unexpected stack state {resp["Stacks"][0]["StackStatus"]}. Aborted')

    params = resp["Stacks"][0]["Parameters"]

    print(f"Deleting {stack_name}")
    client.delete_stack(StackName=stack_name)
    client.get_waiter("stack_delete_complete").wait(StackName=stack_name)
    print("Confirmed deletion")
    
    print(f"Creating {stack_name}")
    client.create_stack(
        StackName=stack_name,
        TemplateBody=template_body(template_file),
        Parameters=params,
    )
    client.get_waiter("stack_create_complete").wait(StackName=stack_name)
    print("Confirmed creation")


@click.command()
@click.option("--profile", "-p", default="default", help="AWS profile name")
@click.option("--stack", "-s", required=True, help="Stack name")
@click.option("--template", "-t", required=True, help="Template file")
def main(profile, stack, template):
    recreate_stack_with_same_parameters(profile_name=profile, stack_name=stack, template_file=template)


if __name__ == "__main__": main()