import os
from abc import abstractmethod
from pathlib import Path
from typing import Optional, Union

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from fake import BaseStorage

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("DjangoBaseStorage",)

DEFAULT_ROOT_PATH = "tmp"
DEFAULT_REL_PATH = "tmp"


class DjangoBaseStorage(BaseStorage):
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

    def __init__(
        self: "DjangoBaseStorage",
        root_path: Optional[Union[str, Path]] = DEFAULT_ROOT_PATH,
        rel_path: Optional[str] = DEFAULT_REL_PATH,
        *args,
        **kwargs,
    ) -> None:
        """
        :param root_path: Root path of the storage directory.
        :param rel_path: Relative path of the storage directory.
        :param *args:
        :param **kwargs:
        """
        self.root_path = root_path or ""
        self.rel_path = rel_path or ""
        super().__init__(*args, **kwargs)
        self.storage = default_storage

    def generate_filename(
        self: "DjangoBaseStorage",
        extension: str,
        prefix: Optional[str] = None,
        basename: Optional[str] = None,
    ) -> str:
        """Generate filename."""
        dir_path = os.path.join(self.root_path, self.rel_path)

        if not extension:
            raise Exception("Extension shall be given!")

        if not basename:
            basename = self.generate_basename(prefix)

        filename = f"{basename}.{extension}"

        return os.path.join(dir_path, filename)

    def write_text(
        self: "DjangoBaseStorage",
        filename: str,
        data: str,
        encoding: Optional[str] = None,
    ) -> int:
        """Write text."""
        if filename.startswith("/"):
            filename = filename[1:]
        content = ContentFile(data.encode(encoding or "utf-8"))
        # saved_path = self.storage.save(filename, content)
        self.storage.save(filename, content)
        return len(data)

    def write_bytes(
        self: "DjangoBaseStorage",
        filename: str,
        data: bytes,
    ) -> int:
        """Write bytes."""
        content = ContentFile(data)
        if filename.startswith("/"):
            filename = filename[1:]
        # saved_path = self.storage.save(filename, content)
        self.storage.save(filename, content)
        return len(data)

    def exists(self: "DjangoBaseStorage", filename: str) -> bool:
        """Check if file exists."""
        return self.storage.exists(filename)

    @abstractmethod
    def relpath(self: "DjangoBaseStorage", filename: str) -> str:
        """Return relative path."""

    @abstractmethod
    def abspath(self: "DjangoBaseStorage", filename: str) -> str:
        """Return absolute path."""

    def unlink(self: "DjangoBaseStorage", filename: str) -> None:
        """Delete the file."""
        self.storage.delete(filename)
