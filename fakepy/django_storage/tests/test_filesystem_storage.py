from typing import Any, Dict, Type, Union

from django.test import TestCase, override_settings
from fake import FAKER, FILE_REGISTRY
from parametrize import parametrize

from ..base import DjangoBaseStorage
from ..filesystem import DjangoFileSystemStorage

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("TestStoragesTestCase",)


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": (
                "django.core.files.storage.filesystem.FileSystemStorage"
            ),
            "OPTIONS": {},
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
class TestStoragesTestCase(TestCase):
    """Test storages."""

    def tearDown(self) -> None:
        super().tearDown()
        FILE_REGISTRY.clean_up()  # Clean up files

    @parametrize(
        "storage_cls, kwargs, prefix, basename, extension",
        [
            # DjangoFileSystemStorage
            (
                DjangoFileSystemStorage,
                {
                    "root_path": "testing",
                    "rel_path": "tmp",
                },
                "zzz",
                None,
                "docx",
            ),
            (
                DjangoFileSystemStorage,
                {
                    "root_path": "testing",
                    "rel_path": "tmp",
                },
                None,
                "my_zzz_filename",
                "docx",
            ),
        ],
    )
    def test_storage(
        self: "TestStoragesTestCase",
        storage_cls: Type[DjangoBaseStorage],
        kwargs: Dict[str, Any],
        prefix: Union[str, None],
        basename: Union[str, None],
        extension: str,
    ) -> None:
        """Test storage."""
        storage = storage_cls(**kwargs)
        # Text file
        filename_text = storage.generate_filename(
            basename=basename, prefix=prefix, extension=extension
        )
        # Write to the text file
        text_result = storage.write_text(filename_text, "Lorem ipsum")
        # Check if file exists
        self.assertTrue(storage.exists(filename_text))
        # Assert correct return value
        self.assertIsInstance(text_result, int)
        # Clean up
        storage.unlink(filename_text)

        # Bytes
        filename_bytes = storage.generate_filename(
            basename=basename, prefix=prefix, extension=extension
        )
        # Write to bytes file
        bytes_result = storage.write_bytes(filename_bytes, b"Lorem ipsum")
        # Check if file exists
        self.assertTrue(storage.exists(filename_bytes))
        # Assert correct return value
        self.assertIsInstance(bytes_result, int)

        # Clean up
        storage.unlink(filename_bytes)

    @parametrize(
        "storage_cls, kwargs, prefix, extension",
        [
            # DjangoFileSystemStorage
            (
                DjangoFileSystemStorage,
                {
                    "root_path": "testing",
                    "rel_path": "tmp",
                },
                "zzz",
                "",
            ),
        ],
    )
    def test_storage_generate_filename_exceptions(
        self: "TestStoragesTestCase",
        storage_cls: Type[DjangoBaseStorage],
        kwargs: Dict[str, Any],
        prefix: str,
        extension: str,
    ) -> None:
        """Test storage `generate_filename` exceptions."""
        storage = storage_cls(**kwargs)

        with self.assertRaises(Exception):
            # Generate filename
            storage.generate_filename(prefix=prefix, extension=extension)

        with self.assertRaises(Exception):
            # Generate filename
            storage.generate_filename(basename=prefix, extension=extension)

    @parametrize(
        "storage_cls, kwargs, prefix, extension",
        [
            # DjangoFileSystemStorage
            (
                DjangoFileSystemStorage,
                {
                    "root_path": "root_tmp",
                    "rel_path": "rel_tmp",
                },
                "",
                "tmp",
            ),
        ],
    )
    def test_storage_abspath(
        self: "TestStoragesTestCase",
        storage_cls: Type[DjangoBaseStorage],
        kwargs: Dict[str, Any],
        prefix: str,
        extension: str,
    ) -> None:
        """Test `FileSystemStorage` `abspath`."""
        storage = storage_cls(**kwargs)
        filename = storage.generate_filename(
            prefix=prefix,
            extension=extension,
        )
        self.assertTrue(filename.startswith("root_tmp/rel_tmp/"))

    @parametrize(
        "storage_cls, kwargs, prefix, extension",
        [
            # DjangoFileSystemStorage
            (
                DjangoFileSystemStorage,
                {
                    "root_path": "root_tmp",
                    "rel_path": "rel_tmp",
                },
                "",
                "tmp",
            ),
        ],
    )
    def test_storage_unlink(
        self: "TestStoragesTestCase",
        storage_cls: Type[DjangoBaseStorage],
        kwargs: Dict[str, Any],
        prefix: str,
        extension: str,
    ) -> None:
        """Test `DjangoStorage` `unlink`."""
        storage = storage_cls(**kwargs)
        with self.subTest("Test unlink by Django"):
            filename_1 = storage.generate_filename(
                prefix=prefix,
                extension=extension,
            )
            storage.write_text(filename=filename_1, data=FAKER.text())
            self.assertTrue(storage.exists(filename_1))
            storage.unlink(filename_1)
            self.assertFalse(storage.exists(filename_1))

        with self.subTest("Test unlink by str"):
            filename_2 = storage.generate_filename(
                prefix=prefix,
                extension=extension,
            )
            storage.write_text(filename=filename_2, data=FAKER.text())
            self.assertTrue(storage.exists(filename_2))
            storage.unlink(str(filename_2))
            self.assertFalse(storage.exists(filename_2))
