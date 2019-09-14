import boto3


def print_all(page):
    from arki_common.utils import print_json
    print_json(page)
    """
    Response Syntax:
    {
        'Accounts': [
            {
                'Id': 'string',
                'Arn': 'string',
                'Email': 'string',
                'Name': 'string',
                'Status': 'ACTIVE'|'SUSPENDED',
                'JoinedMethod': 'INVITED'|'CREATED',
                'JoinedTimestamp': datetime(2015, 1, 1)
            },
        ],
        'NextToken': 'string'
    }
    """


def list_all_accounts():
    client = boto3.client("organizations")
    paginator = client.get_paginator("list_accounts")

    for page in paginator.paginate():
        print_all(page)

        # Print account id, status
        for acc in page["Accounts"]:
            print(f"{acc['Id']}, {acc['Status']}")


def list_account_aliases():
    iam = boto3.client('iam')

    # List account aliases through the pagination interface
    paginator = iam.get_paginator('list_account_aliases')
    for response in paginator.paginate():
        print(response['AccountAliases'])


list_all_accounts()

