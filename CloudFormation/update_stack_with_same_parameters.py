import boto3
import click


def template_body(template_file):
    with open(template_file, "r") as cf_file:
        return cf_file.read()


def update_stack_with_same_parameters(profile_name, stack_name, template_file):
    client = boto3.session.Session(profile_name=profile_name).client("cloudformation")
    
    print(f"Updating {stack_name}")
    client.update_stack(
        StackName=stack_name,
        TemplateBody=template_body(template_file),
    )
    client.get_waiter("stack_update_complete").wait(StackName=stack_name)
    print("Updated")


@click.command()
@click.option("--profile", "-p", default="default", help="AWS profile name")
@click.option("--stack", "-s", required=True, help="Stack name")
@click.option("--template", "-t", required=True, help="Template file")
def main(profile, stack, template):
    update_stack_with_same_parameters(profile_name=profile, stack_name=stack, template_file=template)


if __name__ == "__main__": main()