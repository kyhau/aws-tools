from boto3.session import Session
import logging

logging.getLogger().setLevel(logging.INFO)

ParameterKey = "/apps/sample-app/xxx/token"


def get_secure_string(parameter_key):
    session = Session(profile_name="default")
    try:
        return session.client("ssm").get_parameter(Name=parameter_key, WithDecryption=True)["Parameter"]["Value"]
    except Exception as e:
        logging.error(f"Unable to retrieve data from parameter store: {e}")


get_secure_string(ParameterKey)
