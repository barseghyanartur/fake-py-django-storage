from google.cloud.exceptions import NotFound
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import clean_name

from .cloud import DjangoCloudStorage

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("DjangoGoogleCloudStorage",)


class DjangoGoogleCloudStorage(DjangoCloudStorage):
    """Django GoogleCloudStorage storage."""

    storage: GoogleCloudStorage

    def exists(self: "DjangoGoogleCloudStorage", filename: str) -> bool:
        """Check if file exists."""

        if not filename:  # root element aka the bucket
            try:
                self.storage.client.get_bucket(self.storage.bucket)
                return True
            except NotFound:
                return False

        name = self.storage._normalize_name(clean_name(filename))
        return bool(self.storage.bucket.get_blob(name))
