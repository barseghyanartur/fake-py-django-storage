from botocore.exceptions import ClientError
from storages.backends.s3 import S3Storage
from storages.utils import clean_name

from .cloud import DjangoCloudStorage

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("DjangoAWSS3Storage",)


class DjangoAWSS3Storage(DjangoCloudStorage):
    """Django AWS S3 storage."""

    storage: S3Storage

    def exists(self: "DjangoAWSS3Storage", filename: str) -> bool:
        """Check if file exists."""
        name = self.storage._normalize_name(clean_name(filename))

        try:
            self.storage.connection.meta.client.head_object(
                Bucket=self.storage.bucket_name, Key=name
            )
            return True
        except ClientError as err:
            if err.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                return False

            # Some other error was encountered. Re-raise it.
            raise
