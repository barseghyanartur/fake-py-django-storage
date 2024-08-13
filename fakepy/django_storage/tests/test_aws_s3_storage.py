from typing import Any, Dict, Type, Union

import boto3
from django.test import TestCase, override_settings
from fake import FAKER, FILE_REGISTRY
from moto import mock_aws
from parametrize import parametrize

from ..aws_s3 import DjangoAWSS3Storage
from ..base import DjangoBaseStorage

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("TestAWSS3StorageTestCase",)


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": ("storages.backends.s3boto3.S3Boto3Storage"),
            "OPTIONS": {"bucket_name": "test_bucket"},
        },
    }
)
@mock_aws
class TestAWSS3StorageTestCase(TestCase):
    """Test AWS S3 storages."""

    def setUp(self):
        """Set up the mock S3 environment."""
        self.s3 = boto3.client("s3")
        self.s3.create_bucket(Bucket="test_bucket")

    def tearDown(self) -> None:
        super().tearDown()
        FILE_REGISTRY.clean_up()  # Clean up files

    @parametrize(
        "storage_cls, kwargs, prefix, basename, extension",
        [
            # DjangoAWSS3Storage
            (
                DjangoAWSS3Storage,
                {
                    "root_path": "testing",
                    "rel_path": "tmp",
                },
                "zzz",
                None,
                "docx",
            ),
            (
                DjangoAWSS3Storage,
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
        self: "TestAWSS3StorageTestCase",
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
            # DjangoAWSS3Storage
            (
                DjangoAWSS3Storage,
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
        self: "TestAWSS3StorageTestCase",
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
            # DjangoAWSS3Storage
            (
                DjangoAWSS3Storage,
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
        self: "TestAWSS3StorageTestCase",
        storage_cls: Type[DjangoBaseStorage],
        kwargs: Dict[str, Any],
        prefix: str,
        extension: str,
    ) -> None:
        """Test `S3Storage` `abspath`."""
        storage = storage_cls(**kwargs)
        filename = storage.generate_filename(
            prefix=prefix,
            extension=extension,
        )
        self.assertTrue(filename.startswith("root_tmp/rel_tmp/"))

    @parametrize(
        "storage_cls, kwargs, prefix, extension",
        [
            # DjangoAWSS3Storage
            (
                DjangoAWSS3Storage,
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
        self: "TestAWSS3StorageTestCase",
        storage_cls: Type[DjangoBaseStorage],
        kwargs: Dict[str, Any],
        prefix: str,
        extension: str,
    ) -> None:
        """Test `DjangoStorage` `unlink`."""
        storage = storage_cls(**kwargs)
        with self.subTest("Test unlink by S3"):
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
