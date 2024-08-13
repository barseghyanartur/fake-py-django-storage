from .base import DjangoBaseStorage

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("DjangoCloudStorage",)


class DjangoCloudStorage(DjangoBaseStorage):

    def relpath(self: "DjangoCloudStorage", filename: str) -> str:
        """Return relative path."""
        return filename

    def abspath(self: "DjangoCloudStorage", filename: str) -> str:
        """Return absolute path."""
        return self.storage.url(filename)
