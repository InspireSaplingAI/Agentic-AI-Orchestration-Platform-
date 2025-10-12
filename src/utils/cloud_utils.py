# src/utils/cloud_utils.py
import os
import boto3
from google.cloud import storage
import logging

log = logging.getLogger(__name__)

# ----------------------
# AWS Helpers
# ----------------------
def get_s3_client():
    """Return a boto3 S3 client."""
    return boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

def upload_to_s3(bucket: str, key: str, local_path: str):
    client = get_s3_client()
    client.upload_file(local_path, bucket, key)
    log.info("Uploaded %s to s3://%s/%s", local_path, bucket, key)


# ----------------------
# GCP Helpers
# ----------------------
def get_gcs_client():
    """Return a GCP storage client."""
    return storage.Client()

def upload_to_gcs(bucket_name: str, blob_name: str, local_path: str):
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_path)
    log.info("Uploaded %s to gs://%s/%s", local_path, bucket_name, blob_name)
