import boto3
import os
from base64 import b64decode


def decrypt_for_lambda(encrypted_data):
    # Decrypt code should run once and variables stored outside of the function
    # handler so that these are decrypted once per container
    expected_token = boto3.client("kms").decrypt(
        CiphertextBlob=b64decode(encrypted_data),
        EncryptionContext={"LambdaFunctionName": os.environ["AWS_LAMBDA_FUNCTION_NAME"]},
    )["Plaintext"].decode("utf-8")
    return expected_token
