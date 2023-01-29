import random
import string
import json
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


def get_random_text(len: int = 10) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(len))


def get_signed_url(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }
    s3_client = boto3.client("s3", region_name="us-east-2")
    url = generate_presigned_url(
        s3_client,
        "put_object",
        {"Bucket": "bicscan", "Key": get_random_text(10)},
        300,
    )
    body["presigned_url"] = url
    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def generate_presigned_url(s3_client, client_method, method_parameters, expires_in):
    """
    Generate a presigned Amazon S3 URL that can be used to perform an action.

    :param s3_client: A Boto3 Amazon S3 client.
    :param client_method: The name of the client method that the URL performs.
    :param method_parameters: The parameters of the specified client method.
    :param expires_in: The number of seconds the presigned URL is valid for.
    :return: The presigned URL.
    """
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method, Params=method_parameters, ExpiresIn=expires_in
        )
        logger.info("Got presigned URL: %s", url)
    except ClientError:
        logger.exception(
            "Couldn't get a presigned URL for client method '%s'.", client_method
        )
        raise
    return url
