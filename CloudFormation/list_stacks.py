import click
from boto3.session import Session


@click.command()
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--name-contains", "-n", help="Find stacks with the given string in the name")
def main(profile, name_contains):
    session = Session(profile_name=profile)
    result = []

    paginator = session.client("cloudformation").get_paginator("describe_stacks")
    for page in paginator.paginate():
        for stack in page["Stacks"]:
            if name_contains is None or name_contains.lower() in stack["StackName"].lower():
                result.append((stack["StackName"], stack["CreationTime"]))

    # Sort by creation time in reverse order
    result.sort(key=lambda tup: tup[1], reverse=True)
    for r in result:
        print(r[0])


if __name__ == "__main__": main()
