import json
import os
import urllib.parse

import boto3

KENDRA_DATA_SOURCE_ID = os.environ["KENDRA_DATA_SOURCE_ID"]
KENDRA_INDEX_ID = os.environ["KENDRA_INDEX_ID"]


def lambda_handler(event, context):
    # Get the S3 bucket and key from the event
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )

    print(f"Received s3://{bucket}/{key} PUT notification")

    # Create a Kendra client
    kendra_client = boto3.client("kendra")

    sync_response = kendra_client.start_data_source_sync_job(
        Id=KENDRA_DATA_SOURCE_ID, IndexId=KENDRA_INDEX_ID
    )
    print(sync_response)