from .base import DjangoBaseStorage

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("DjangoFileSystemStorage",)


class DjangoFileSystemStorage(DjangoBaseStorage):
    """Django-based storage class using Django's default storage backend.

    Usage example:

    .. code-block:: python

        from fakepy.django_storage.filesystem import DjangoFileSystemStorage

        storage = DjangoFileSystemStorage()
        docx_file = storage.generate_filename(
            prefix="zzz_", extension="docx"
        )
        storage.write_bytes(docx_file, b"Sample bytes data")

    Initialization with params:

    .. code-block:: python

        from fakepy.django_storage.filesystem import DjangoFileSystemStorage

        storage = DjangoFileSystemStorage()
        docx_file = storage.generate_filename(
            prefix="example", extension="docx"
        )
    """

    def relpath(self: "DjangoFileSystemStorage", filename: str) -> str:
        """Return relative path."""
        return filename

    def abspath(self: "DjangoFileSystemStorage", filename: str) -> str:
        """Return absolute path."""
        return self.storage.joinpath(filename)
