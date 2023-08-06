import pathlib
from typing import Any, Protocol
import urllib.parse

import boto3

from .delegate import FileDelegate, FileTag
from .record import FileRecord


class S3Credentials(Protocol):
    access_key_id: str
    secret_access_key: str
    session_token: str


class FileS3Delegate(FileDelegate):
    """
    A file delegate intented for client-side use. Protected methods are not implemented.
    Capable of uploading and deleting files from S3 given an authenticated boto3 Bucket resource.
    """

    __boto_session: boto3.Session
    __s3_bucket: Any  # boto3.resource("s3").Bucket(...)

    def __init__(self, bucket_name: Any, credentials: S3Credentials) -> None:
        self.__boto_session = boto3.Session(
            aws_access_key_id=credentials.access_key_id,
            aws_secret_access_key=credentials.secret_access_key,
            aws_session_token=credentials.session_token,
        )
        self.__s3_bucket = self.__boto_session.resource("s3").Bucket(bucket_name)

    def delete_file(self, key: str) -> None:
        self.__s3_bucket.delete_objects(
            Delete={
                "Objects": [{"Key": key}],
            }
        )

    def download_file(self, key: str, local_path: pathlib.Path) -> None:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        self.__s3_bucket.download_file(key, str(local_path))

    def upload_file(
        self, local_path: pathlib.Path, key: str, tags: dict[FileTag, str] | None = None
    ) -> None:
        upload_file_args: dict[str, Any] = {
            "Filename": str(local_path),
            "Key": key,
        }

        if tags is not None:
            serializable_tags = {tag.value: value for tag, value in tags.items()}
            encoded_tags = urllib.parse.urlencode(serializable_tags)
            upload_file_args["ExtraArgs"] = {"Tagging": encoded_tags}

        self.__s3_bucket.upload_file(**upload_file_args)

    def protected_upsert_file_record(
        self,
        bucket: str,
        key: str,
    ) -> FileRecord:
        """Admin only"""
        raise NotImplementedError("protected_upsert_file_record")

    def protected_delete_file_record(
        self,
        bucket: str,
        key: str,
    ) -> None:
        """Admin only"""
        raise NotImplementedError("protected_delete_file_record")
