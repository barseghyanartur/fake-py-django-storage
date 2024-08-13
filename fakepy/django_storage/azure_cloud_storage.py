from storages.backends.azure_storage import AzureStorage

from .cloud import DjangoCloudStorage

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("DjangoAzureCloudStorage",)


class DjangoAzureCloudStorage(DjangoCloudStorage):
    """Django AzureCloudStorage storage."""

    storage: AzureStorage

    def exists(self: "DjangoAzureCloudStorage", filename: str) -> bool:
        """Check if file exists."""
        if not filename:
            return True

        blob_client = self.storage.client.get_blob_client(
            self.storage._get_valid_path(filename)
        )
        return blob_client.exists()
