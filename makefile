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
LINT = $(PYTHON) -m pylint --load-plugins=pylint.extensions.mccabe --max-complexity=10
LINT3 = $(LINT) --init-hook="sys.path.insert(0, './')"

all: tests

test:
	$(PYTEST) -s --cov-append $(TESTS)/test/$(T)
	$(COVERAGE) html --skip-covered

tests: flake8 pep257 lint
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

tests3: flake8 pep257 lint3
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

# https://pypi.org/project/radon/
radon:
	$(PYTHON) -m radon cc $(TESTS)/test -s -a -nc --no-assert
	$(PYTHON) -m radon cc $(SOURCE) -s -a -nc

flake8:
	$(PYTHON) -m flake8 --max-line-length=120 $(TESTS)
	$(PYTHON) -m flake8 --max-line-length=120 $(SOURCE)

lint:
	$(LINT) $(TESTS)/test
	$(LINT) $(SOURCE)

lint3:
	$(LINT3) $(TESTS)/test
	$(LINT3) $(SOURCE)

pep257:
	$(PYTHON) -m pep257 $(SOURCE)
	$(PYTHON) -m pep257 --match='.*\.py' $(TESTS)/test

dist:
	$(PYTHON) setup.py sdist bdist_wheel

upload_piptest: tests dist
	$(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload_pip: tests dist
	$(PYTHON) -m twine upload dist/*

setup: setup_python setup_pip

setup3: setup_python3 setup_pip

setup_pip:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install --upgrade --force-reinstall -r tests/requirements.txt
	$(PYTHON) -m pip install -r deploy.txt

setup_python:
	$(PYTHON_BIN) -m pip install virtualenv
	$(PYTHON_BIN) -m virtualenv ./venv

setup_python3:
	$(PYTHON_BIN) -m venv ./venv
