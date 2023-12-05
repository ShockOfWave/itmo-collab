import os
import boto3
from botocore.config import Config
from api.src.utils.paths import get_project_path
from api.src.config import settings


def create_s3_session():
    session = boto3.Session(
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
    )
    s3 = session.client(
        "s3", endpoint_url=settings.S3_URL, config=Config(signature_version="s3v4")
    )
    return s3


def create_s3_folder(folder_name, s3=create_s3_session()):
    folder = folder_name + "/"
    s3.put_object(Bucket=settings.S3_BUCKET, Key=folder)
    return folder


def create_presigned_s3_url(s3_uri, s3=create_s3_session()):
    presigned_s3_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET, "Key": s3_uri},
        ExpiresIn=3600,
    )
    return presigned_s3_url


def upload_file_to_s3(path, s3_uri, s3=create_s3_session()):
    s3.upload_file(path, settings.S3_BUCKET, s3_uri)


def download_file_from_s3(
    s3_uri,
    s3=create_s3_session(),
    path_to_local_storage: str = os.path.join(get_project_path(), "api", "weight"),
):
    """Download file from s3 bucket

    Args:
        s3_uri (_type_): Path to file in s3 bucket
        s3 (_type_, optional): Init s3 session. Defaults to create_s3_session().
        path_to_local_storage (str, optional): Path to file in local storate.
        Defaults to os.path.join(get_project_path(), 'api', 'weight').
    """
    s3.download_file(settings.S3_BUCKET, s3_uri, path_to_local_storage)
