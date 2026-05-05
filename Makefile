.PHONY: help install sync update-lock \
        test quick-test django-test \
        doc8 ruff ruff-fix format mypy pre-commit \
        build-docs rebuild-docs serve-docs \
        compile-requirements compile-requirements-upgrade \
        create-secrets detect-secrets \
        clean-dev clean-test clean \
        update-version package-build check-package-build release test-release \
        django-shell django-runserver django-makemigrations django-apply-migrations \
        shell ipython

SHELL := /bin/bash

PROJECT_NAME ?= fake-py-django-storage
PACKAGE_IMPORT_NAME ?= fakepy/django_storage
PACKAGE_EGG_INFO ?= fake-py-django-storage.egg-info
VERSION ?= 0.1.2

UV ?= uv
PYTHON ?= $(UV) run python
PYTEST ?= $(UV) run pytest
RUFF ?= $(UV) run ruff
MYPY ?= $(UV) run mypy
DOC8 ?= $(UV) run doc8
PRE_COMMIT ?= $(UV) run pre-commit
DETECT_SECRETS ?= $(UV) run detect-secrets
TWINE ?= $(UV) run twine
SPHINX_BUILD ?= $(UV) run sphinx-build
SPHINX_APIDOC ?= $(UV) run sphinx-apidoc

TEST_TARGET ?= quick-test
RUFF_PATHS ?= .
MYPY_PATHS ?= fakepy/django_storage/*.py

DOCS_DIR ?= docs
BUILD_DOCS_DIR ?= builddocs
DOCS_REQUIREMENTS ?= $(DOCS_DIR)/requirements.txt
DOCS_PORT ?= 5001

help:
	@echo "Common targets:"
	@echo "  make install          Sync uv environment with all groups and extras"
	@echo "  make test             Run tests (pytest)"
	@echo "  make quick-test      Run pytest through uv"
	@echo "  make ruff           Run ruff check"
	@echo "  make mypy          Run mypy"
	@echo "  make build-docs    Build documentation with Sphinx"


# -----------------------------------------------------------------------
# Docker-based testing
# -----------------------------------------------------------------------

docker-build:
	docker compose build

# List all available environments in the Docker container
docker-list-envs: docker-build
	docker compose run --rm tox -l

docker-test: docker-build
	docker compose run --rm tox

# Usage: make docker-test-env ENV=py312
docker-test-env: docker-build
	@if [ -z "$(ENV)" ]; then \
		echo "Usage: make test-env ENV=py312"; \
		exit 1; \
	fi
	docker compose run --rm tox -e $(ENV)

docker-shell: docker-build
	docker compose run --rm --entrypoint bash tox

# Usage: make docker-shell-env ENV=py312
docker-shell-env: docker-build
	@if [ -z "$(ENV)" ]; then \
		echo "Usage: make shell-env ENV=py312"; \
		exit 1; \
	fi
	docker compose run --rm --entrypoint bash tox -e $(ENV)

# ----------------------------------------------------------------------------
# Installation
# ----------------------------------------------------------------------------

sync install:
	$(UV) sync --all-groups --all-extras

update-lock:
	$(UV) lock --upgrade

# -----------------------------------------------------------------------
# uv-based testing
# -----------------------------------------------------------------------

test: $(TEST_TARGET)

quick-test:
	$(PYTEST)

django-test:
	cd examples/django/ && $(PYTEST) -vrx -s

# -----------------------------------------------------------------------
# Code quality (run locally)
# -----------------------------------------------------------------------

doc8:
	$(DOC8)

ruff:
	$(RUFF) check $(RUFF_PATHS)

ruff-fix:
	$(RUFF) check $(RUFF_PATHS) --fix

format:
	$(UV) run black .
	$(UV) run isort .

mypy:
	$(MYPY) $(MYPY_PATHS)

pre-commit-install:
	$(PRE_COMMIT) install

pre-commit: pre-commit-install
	$(PRE_COMMIT) run --all-files

# ----------------------------------------------------------------------------
# Security
# ----------------------------------------------------------------------------

create-secrets:
	$(DETECT_SECRETS) scan > .secrets.baseline

detect-secrets:
	$(DETECT_SECRETS) scan --baseline .secrets.baseline

# ----------------------------------------------------------------------------
# Documentation
# ----------------------------------------------------------------------------

build-docs:
	$(SPHINX_APIDOC) fakepy/django_storage --full -o $(DOCS_DIR) -H 'fake-py-django-storage' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -f -d 20
	$(SPHINX_BUILD) -n -a -b html $(DOCS_DIR) $(BUILD_DOCS_DIR)
	cd $(BUILD_DOCS_DIR) && zip -r ../$(BUILD_DOCS_DIR).zip . -x ".*"

rebuild-docs:
	$(SPHINX_APIDOC) fakepy/django_storage --full -o $(DOCS_DIR) -H 'fake-py-django-storage' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -f -d 20
	@if [ -f "$(DOCS_DIR)/conf.py.distrib" ]; then cp "$(DOCS_DIR)/conf.py.distrib" "$(DOCS_DIR)/conf.py"; fi
	@if [ -f "$(DOCS_DIR)/index.rst.distrib" ]; then cp "$(DOCS_DIR)/index.rst.distrib" "$(DOCS_DIR)/index.rst"; fi

serve-docs:
	cd $(BUILD_DOCS_DIR) && $(PYTHON) -m http.server $(DOCS_PORT)

compile-requirements:
	$(UV) pip compile pyproject.toml --all-extras --group docs -o $(DOCS_REQUIREMENTS)

compile-requirements-upgrade:
	$(UV) pip compile pyproject.toml --all-extras --group docs -o $(DOCS_REQUIREMENTS) --upgrade

# -----------------------------------------------------------------------
# Dev-handy
# -----------------------------------------------------------------------

ipython:
	$(UV) run ipython

shell:
	$(UV) run ipython

django-shell:
	$(PYTHON) examples/django/manage.py shell

django-runserver:
	$(PYTHON) examples/django/manage.py runserver 0.0.0.0:8000 --traceback -v 3

django-makemigrations:
	$(PYTHON) examples/django/manage.py makemigrations

django-apply-migrations:
	$(PYTHON) examples/django/manage.py migrate

# -----------------------------------------------------------------------
# Housekeeping
# -----------------------------------------------------------------------

clean-dev:
	find . -name "*.orig" -exec rm -rf {} +
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf dist/ build/ $(PACKAGE_EGG_INFO) src/*.egg-info *.egg-info
	rm -rf .cache/ .mypy_cache/ .ruff_cache/

clean-test:
	find . -name "*.pyc" -exec rm -rf {} +
	find . -name "*.py,cover" -exec rm -rf {} +
	rm -rf .coverage .coverage.* .pytest_cache/ htmlcov/
	rm -rf builddocs/ testdocs/ .coverage

clean:
	rm -rf build/ dist/ .cache/ htmlcov/
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	rm -rf $(BUILD_DOCS_DIR)/

# ----------------------------------------------------------------------------
# Release
# ----------------------------------------------------------------------------

update-version:
	$(PYTHON) -c "from pathlib import Path; import re; p=Path('pyproject.toml'); s=p.read_text(); s=re.sub(r'^version = \"[^\"]+\"', 'version = \"$(VERSION)\"', s, count=1, flags=re.M); p.write_text(s)"
	$(PYTHON) -c "from pathlib import Path; import re; p=Path('$(PACKAGE_IMPORT_NAME)/__init__.py'); s=p.read_text(); s=re.sub(r'^__version__ = \"[^\"]+\"', '__version__ = \"$(VERSION)\"', s, count=1, flags=re.M); p.write_text(s)"

package-build:
	$(PYTHON) -m build .

check-package-build:
	$(TWINE) check dist/*

release:
	$(TWINE) upload dist/* --verbose

test-release:
	$(TWINE) upload --repository testpypi dist/* --verbose
