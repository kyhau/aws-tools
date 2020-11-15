import json
import logging
import os

import boto3

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)
logging.info(f"boto3.__version__: {boto3.__version__}")


DEFAULT_COLLECTION_ID = os.environ.get("DEFAULT_COLLECTION_ID", "k-test-1")
DEFAULT_BUCKET = os.environ.get("DEFAULT_BUCKET", "todo")

reko_client = boto3.client("rekognition") # , region_name="ap-southeast-2"
s3_client = boto3.resource("s3")


green_status = lambda resp: resp["ResponseMetadata"]["HTTPStatusCode"]

dump_data = lambda ret: ",".join([ret["FaceId"], ret["ImageId"], ret["ExternalImageId"], str(ret["Confidence"])])


def list_faces(collection_id):
    resp = reko_client.list_faces(CollectionId=collection_id)
    for ret in resp["Faces"]:
        logging.info(dump_data(ret))
    return resp["Faces"]


def index_faces(collection_id, image_source, external_image_id):
    resp = reko_client.index_faces(CollectionId=collection_id, Image=image_source, ExternalImageId=external_image_id)
    ret = green_status(resp)
    for rec in resp["FaceRecords"]:
        face = rec["Face"]
        logging.info(dump_data(face))
    return ret


def search_faces_by_image(collection_id, image_source):
    ret, similarity = None, 0.0

    resp = reko_client.search_faces_by_image(CollectionId=collection_id, Image=image_source)
    for rec in resp["FaceMatches"]:
        if rec["Similarity"] > similarity:
            ret = rec["Face"]
            logging.info(f'{dump_data(ret)}, {rec["Similarity"]}')

    return ret


def search_local_image(collection_id, image_file):
    with open(image_file, "rb") as image:
        param = {"Bytes": image.read()}

    return search_faces_by_image(collection_id, param)


def search_s3_image(collection_id, bucket, object_key, version=None):
    ret = {"Bucket": bucket, "Name": object_key}
    if version:
        ret["Version"] = version

    return search_faces_by_image(collection_id, {"S3Object": ret})


def index_faces_in_s3(collection_id, bucket):
    my_bucket = s3_client.Bucket(bucket)
    for f in my_bucket.objects.all():
        param = {"S3Object": {"Bucket": bucket, "Name": f.key}}
        index_faces(collection_id, param, f.key)


def lambda_response(message, status_code=200):
    logging.info(message)
    return {
        "body": json.dumps(message),
        "headers": {"Content-Type": "application/json"},
        "statusCode": status_code,
    }


def lambda_handler(event, context):
    """
    Trigger from S3 event notification
    E.g. https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html
    """
    message = {}
    for record in event.get("Records", []):
        if "s3" in record:
            bucket, object_key = record["s3"]["bucket"]["name"], record["s3"]["object"]["key"]
            message[f"{bucket}/{object_key}"] = search_s3_image(DEFAULT_COLLECTION_ID, bucket, object_key)

    return lambda_response(message)


def main():
    """Run locally"""

    local_image = "data/hocc_2.jpg"

    # Create collection if not exists
    try:
        reko_client.create_collection(CollectionId=DEFAULT_COLLECTION_ID)
    except Exception as e:
        if "ResourceAlreadyExistsException" not in str(e):
            raise

    # Index images located in the default S3 bucket
    logging.info("Index faces in S3")
    index_faces_in_s3(DEFAULT_COLLECTION_ID, DEFAULT_BUCKET)

    logging.info("List all faces")
    list_faces(DEFAULT_COLLECTION_ID)

    # Test looking up a face
    logging.info("Search face")
    search_local_image(DEFAULT_COLLECTION_ID, local_image)

    #for collection_id in reko_client.list_collections()["CollectionIds"]:
    reko_client.delete_collection(CollectionId=DEFAULT_COLLECTION_ID)


if __name__ == "__main__":
     main()
