======================
fake-py-django-storage
======================
.. External references

.. _fake.py: https://fakepy.readthedocs.io
.. _faker-file: https://faker-file.readthedocs.io
.. _Django: https://www.djangoproject.com
.. _django-storages: https://django-storages.readthedocs.io

.. Internal references

.. _fake-py-django-storage: https://github.com/barseghyanartur/fake-py-django-storage
.. _Read the Docs: http://fake-py-django-storage.readthedocs.io
.. _Contributor guidelines: https://fake-py-django-storage.readthedocs.io/en/latest/contributor_guidelines.html

`Django`_ storage for `fake.py`_.

.. image:: https://img.shields.io/pypi/v/fake-py-django-storage.svg
   :target: https://pypi.python.org/pypi/fake-py-django-storage
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/fake-py-django-storage.svg
    :target: https://pypi.python.org/pypi/fake-py-django-storage/
    :alt: Supported Python versions

.. image:: https://github.com/barseghyanartur/fake-py-django-storage/actions/workflows/test.yml/badge.svg?branch=main
   :target: https://github.com/barseghyanartur/fake-py-django-storage/actions
   :alt: Build Status

.. image:: https://readthedocs.org/projects/fake-py-django-storage/badge/?version=latest
    :target: http://fake-py-django-storage.readthedocs.io
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/barseghyanartur/fake-py-django-storage/#License
   :alt: MIT

.. image:: https://coveralls.io/repos/github/barseghyanartur/fake-py-django-storage/badge.svg?branch=main&service=github
    :target: https://coveralls.io/github/barseghyanartur/fake-py-django-storage?branch=main
    :alt: Coverage

`fake-py-django-storage`_ is a `Django`_ storage integration for `fake.py`_ - a
standalone, portable library designed for generating various
random data types for testing.

Features
========
- Almost seamless integration with `Django`_ (and `django-storages`_).

Prerequisites
=============
Python 3.9+

Installation
============

.. code-block:: sh

    pip install fake-py-django-storage

Documentation
=============
- Documentation is available on `Read the Docs`_.
- For guidelines on contributing check the `Contributor guidelines`_.

Usage
=====
`FileSystemStorage` of `Django`
-------------------------------
.. code-block:: python

    from fake import FAKER
    from fakepy.django_storage.filesystem import DjangoFileSystemStorage

    STORAGE = DjangoFileSystemStorage(
        root_path="tmp",  # Optional
        rel_path="sub-tmp",  # Optional
    )

    pdf_file = FAKER.pdf_file(storage=STORAGE)

    STORAGE.exists(pdf_file)

AWS S3 (using `django-storages`)
--------------------------------
.. code-block:: python

    from fake import FAKER
    from fakepy.django_storage.aws_s3 import DjangoAWSS3Storage

    STORAGE = DjangoAWSS3Storage(
        root_path="tmp",  # Optional
        rel_path="sub-tmp",  # Optional
    )

    pdf_file = FAKER.pdf_file(storage=STORAGE)

    STORAGE.exists(pdf_file)

Google Cloud Storage (using `django-storages`)
----------------------------------------------
.. code-block:: python

    from fake import FAKER
    from fakepy.django_storage.google_cloud_storage import (
        DjangoGoogleCloudStorage,
    )

    STORAGE = DjangoGoogleCloudStorage(
        root_path="tmp",  # Optional
        rel_path="sub-tmp",  # Optional
    )

    pdf_file = FAKER.pdf_file(storage=STORAGE)

    STORAGE.exists(pdf_file)

Azure Cloud Storage (using `django-storages`)
---------------------------------------------
.. code-block:: python

    from fake import FAKER
    from fakepy.django_storage.azure_cloud_storage import (
        DjangoAzureCloudStorage,
    )

    STORAGE = DjangoAzureCloudStorage(
        root_path="tmp",  # Optional
        rel_path="sub-tmp",  # Optional
    )

    pdf_file = FAKER.pdf_file(storage=STORAGE)

    STORAGE.exists(pdf_file)

Tests
=====

.. code-block:: sh

    pytest

Writing documentation
=====================

Keep the following hierarchy.

.. code-block:: text

    =====
    title
    =====

    header
    ======

    sub-header
    ----------

    sub-sub-header
    ~~~~~~~~~~~~~~

    sub-sub-sub-header
    ^^^^^^^^^^^^^^^^^^

    sub-sub-sub-sub-header
    ++++++++++++++++++++++

    sub-sub-sub-sub-sub-header
    **************************

License
=======

MIT

Support
=======
For security issues contact me at the e-mail given in the `Author`_ section.

For overall issues, go to `GitHub <https://github.com/barseghyanartur/fake-py-django-storage/issues>`_.

Author
======

Artur Barseghyan <artur.barseghyan@gmail.com>
