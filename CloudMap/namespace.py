import boto3

client = boto3.client('servicediscovery')


def create_namespace_for_api_calls(namespace_name):
    response = client.create_http_namespace(Name=namespace_name)
    print(response)


def list_namespaces():
    response = client.list_namespaces()
    print(response)


create_namespace_for_api_calls("k-ns-apicalls")
