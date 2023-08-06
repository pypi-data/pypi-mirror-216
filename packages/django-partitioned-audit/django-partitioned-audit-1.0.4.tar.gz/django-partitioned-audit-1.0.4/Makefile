SHELL := /bin/bash
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
VENVDIR := $(ROOT_DIR)/.venv
PYTHON := python3.11

clean:
	rm -rf dist/ django_partitioned_audit.egg-info/ build/

build-package:
	$(VENVDIR)/bin/python -m build --sdist .
	$(VENVDIR)/bin/python -m build --wheel .

build-test-recreate: clean build-package
	test -e tests/app_install_test/venv && rm -rf tests/app_install_test/venv
	python3.11 -m venv tests/app_install_test/venv
	$(ROOT_DIR)/tests/app_install_test/venv/bin/pip install \
		dist/django_partitioned_audit-$(shell $(VENVDIR)/bin/python setup.py --version)-py3-none-any.whl
	$(ROOT_DIR)/tests/app_install_test/venv/bin/pip install django psycopg2-binary

build-test-run:
	echo "drop database if exists sdist_test_install" | $(MAKE) psql
	echo "create database sdist_test_install" | $(MAKE) psql
	cd $(ROOT_DIR)/tests/app_install_test && \
		$(ROOT_DIR)/tests/app_install_test/venv/bin/python \
			$(ROOT_DIR)/tests/app_install_test/manage.py migrate
	cd $(ROOT_DIR)/tests/app_install_test && \
		$(ROOT_DIR)/tests/app_install_test/venv/bin/python \
			$(ROOT_DIR)/tests/app_install_test/manage.py manage_partition_tables create
	cd $(ROOT_DIR)/tests/app_install_test && \
		$(ROOT_DIR)/tests/app_install_test/venv/bin/python \
			$(ROOT_DIR)/tests/app_install_test/manage.py manage_partition_tables list
	cd $(ROOT_DIR)/tests/app_install_test && \
		$(ROOT_DIR)/tests/app_install_test/venv/bin/python \
			$(ROOT_DIR)/tests/app_install_test/manage.py manage_partition_tables simulate --extra-days 30

build-upload:
	$(VENVDIR)/bin/twine upload \
		dist/django_partitioned_audit-$(shell $(VENVDIR)/bin/python setup.py --version)-py3-none-any.whl \
		dist/django-partitioned-audit-$(shell $(VENVDIR)/bin/python setup.py --version).tar.gz

build-upload-testpypi:
	$(VENVDIR)/bin/twine upload --repository testpypi \
		dist/django_partitioned_audit-$(shell $(VENVDIR)/bin/python setup.py --version)-py3-none-any.whl \
		dist/django-partitioned-audit-$(shell $(VENVDIR)/bin/python setup.py --version).tar.gz

tox:
	$(VENVDIR)/bin/tox $(ARGS)

tox-latest:
	# run tests with latest versions
	$(VENVDIR)/bin/tox -e py311-django42-postgres15 $(ARGS)

tox-oldest-latest:
	# run tests with oldest and latest versions
	$(VENVDIR)/bin/tox -e py38-django32-postgres12,py311-django42-postgres15 $(ARGS)

tox-some:
	$(VENVDIR)/bin/tox -e py38-django32-postgres12,py39-django32-postgres12,py310-django41-postgres13,py310-django42-postgres14,py311-django42-postgres15 $(ARGS)

#
# targets for common tasks on local development environment
#

setup-environment:
	if [ -e $(VENVDIR)/bin/activate ] ; then \
  		echo "Virtualenv already exists"; \
  	else \
		echo "Using $(PYTHON) to create virtualenv..."; \
		$(PYTHON) -m venv $(VENVDIR) ; \
  	fi
	$(VENVDIR)/bin/pip install --upgrade setuptools pip pip-tools
	$(MAKE) pip-sync
	# https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html#development-mode
	$(VENVDIR)/bin/pip install --editable .

pip-compile:
	$(VENVDIR)/bin/pip-compile -o tests/requirements-test.txt tests/requirements-test.in
	$(VENVDIR)/bin/pip-compile -o tests/requirements-ci.txt tests/requirements-ci.in
	$(VENVDIR)/bin/pip-compile -o tests/requirements-dev.txt tests/requirements-dev.in

pip-compile-upgrade:
	$(VENVDIR)/bin/pip-compile --upgrade -o tests/requirements-test.txt tests/requirements-test.in
	$(VENVDIR)/bin/pip-compile --upgrade -o tests/requirements-ci.txt tests/requirements-ci.in
	$(VENVDIR)/bin/pip-compile --upgrade -o tests/requirements-dev.txt tests/requirements-dev.in

pip-sync:
	$(VENVDIR)/bin/pip-sync tests/requirements-dev.txt

pip-compile-sync: pip-compile pip-sync

pre-commit-all-files:
	$(VENVDIR)/bin/pre-commit run --all-files

pylint:
	$(VENVDIR)/bin/pre-commit run pylint --all-files

docker-compose-up-d:
	$(VENVDIR)/bin/docker-compose -f ./tests/docker-compose.yml up -d

docker-compose-stop:
	$(VENVDIR)/bin/docker-compose -f ./tests/docker-compose.yml stop

docker-compose-kill:
	$(VENVDIR)/bin/docker-compose -f ./tests/docker-compose.yml kill

docker-compose-rm:
	$(VENVDIR)/bin/docker-compose -f ./tests/docker-compose.yml rm -svf

psql: psql15

psql12:
	env PGPASSWORD=test12 psql -h localhost -p 55012 -U test12 template1

psql13:
	env PGPASSWORD=test13 psql -h localhost -p 55013 -U test13 template1

psql14:
	env PGPASSWORD=test14 psql -h localhost -p 55014 -U test14 template1

psql15:
	env PGPASSWORD=test15 psql -h localhost -p 55015 -U test15 template1

test:
	$(VENVDIR)/bin/pytest -s $(ARGS)

django-manage:
	env \
		DJANGO_SETTINGS_MODULE=config.settings \
		PYTHONPATH=$(ROOT_DIR):$(ROOT_DIR)/tests/app_django \
		$(VENVDIR)/bin/$(PYTHON) $(ROOT_DIR)/tests/app_django/manage.py $(ARGS)

django-runserver:
	env \
		DJANGO_SETTINGS_MODULE=config.settings \
		PYTHONPATH=$(ROOT_DIR):$(ROOT_DIR)/tests/app_django \
		$(VENVDIR)/bin/$(PYTHON) $(ROOT_DIR)/tests/app_django/manage.py runserver

django-kill-db:
	echo "drop database if exists django_partitioned_audit_app" | $(MAKE) psql
	echo "create database django_partitioned_audit_app" | $(MAKE) psql
	$(MAKE) django-manage ARGS=migrate
	$(MAKE) django-manage ARGS="manage_partition_tables create"
	$(MAKE) django-manage ARGS="manage_partition_tables list"

test-stresstest-gunicorn:
	# LAUNCH GUNICORN FROM PYTHON --> https://docs.gunicorn.org/en/stable/custom.html#custom-application
	env \
		DJANGO_SETTINGS_MODULE=config.settings \
		PYTHONPATH=$(ROOT_DIR):$(ROOT_DIR)/tests/app_django \
		$(VENVDIR)/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8011 --workers 20 --threads 1 --reuse-port

test-stresstest-run:
	# LAUNCH GUNICORN FROM PYTHON --> https://docs.gunicorn.org/en/stable/custom.html#custom-application
	env \
		DJANGO_SETTINGS_MODULE=config.settings \
		PYTHONPATH=$(ROOT_DIR):$(ROOT_DIR)/tests/app_django \
		$(VENVDIR)/bin/$(PYTHON) $(ROOT_DIR)/tests/app_django/manage.py stresstest $(ARGS)

test-readme:
	env TEST_README=1 $(VENVDIR)/bin/pytest -qs tests/test_examples_on_readme.py

bumpversion-patch: build-test-recreate build-test-run tox-some
	$(VENVDIR)/bin/bumpversion --commit --tag release
	$(MAKE) build-package
	$(MAKE) build-upload
	$(VENVDIR)/bin/bumpversion --commit --no-tag patch
	# git push origin && git push origin --tags

bumpversion-patch-quick: build-test-recreate build-test-run tox-latest
	$(VENVDIR)/bin/bumpversion --commit --tag release
	$(MAKE) build-package
	$(MAKE) build-upload
	$(VENVDIR)/bin/bumpversion --commit --no-tag patch
	# git push origin && git push origin --tags
