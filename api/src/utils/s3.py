import boto3
from botocore.config import Config
from fastapi import Depends

from api.src.config import settings


def create_s3_session():
    session = boto3.Session(aws_access_key_id=settings.S3_ACCESS_KEY,
                            aws_secret_access_key=settings.S3_SECRET_KEY)
    s3 = session.client('s3', endpoint_url=settings.S3_URL, config=Config(signature_version="s3v4"))
    return s3


def create_s3_folder(folder_name, s3=create_s3_session()):
    folder = folder_name + '/'
    s3.put_object(Bucket=settings.S3_BUCKET, Key=folder)
    return folder


def create_presigned_s3_url(s3_uri, s3=create_s3_session()):
    presigned_s3_url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': settings.S3_BUCKET, 'Key': s3_uri},
    ExpiresIn=3600,)
    return presigned_s3_url


def upload_file_to_s3(path, s3_uri, s3=create_s3_session()):
    s3.upload_file(path,
                   settings.S3_BUCKET,
                   s3_uri)