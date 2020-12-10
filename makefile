.PHONY: all setup tests dist
# make tests >debug.log 2>&1

ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
PTEST = venv/Scripts/pytest.exe
COVERAGE = venv/Scripts/coverage.exe
else
PYTHON = ./venv/bin/python
PTEST = ./venv/bin/pytest
COVERAGE = ./venv/bin/coverage
endif

SOURCE = oeg_iv
TESTS = tests
PYTEST = $(PTEST) --cov=$(SOURCE) --cov-report term:skip-covered

all: tests

test:
	$(PYTEST) -s --cov-append $(TESTS)/test/$(T)
	$(COVERAGE) html --skip-covered

tests: pep257 flake8 lint
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

flake8:
	$(PYTHON) -m flake8 --max-line-length=120 $(TESTS)
	$(PYTHON) -m flake8 --max-line-length=120 $(SOURCE)

lint:
	$(PYTHON) -m pylint $(TESTS)/test
	$(PYTHON) -m pylint $(SOURCE)

# https://www.python.org/dev/peps/pep-0257/
pep257:
	$(PYTHON) -m pep257 $(TESTS)
	$(PYTHON) -m pep257 $(SOURCE)

dist:
	$(PYTHON) setup.py sdist bdist_wheel

upload_piptest: tests dist
	$(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload_pip: tests dist
	$(PYTHON) -m twine upload dist/*

setup: setup_python setup_pip

setup_pip:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r tests/requirements.txt

setup_python:
	$(PYTHON_BIN) -m pip install virtualenv
	$(PYTHON_BIN) -m virtualenv ./venv
