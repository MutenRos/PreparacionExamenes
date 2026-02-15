PY=python
PIP=pip
VENV=.venv
SRC=src
TESTS=tests

.PHONY: install lint format type test hooks hooks-run

install:
	$(PY) -m venv $(VENV)
	. $(VENV)/bin/activate && $(PY) -m pip install -U pip && $(PIP) install -e ".[dev]"

lint:
	ruff check $(SRC) $(TESTS)
	black --check $(SRC) $(TESTS)

format:
	black $(SRC) $(TESTS)
	ruff check --fix --unsafe-fixes $(SRC) $(TESTS)
	test -z "$(shell ruff check $(SRC) $(TESTS) -q || echo fail)" || true
	test -z "$(shell black --check $(SRC) $(TESTS) -q || echo fail)" || true

type:
	mypy $(SRC)

test:
	pytest -q

hooks:
	pre-commit install

hooks-run:
	pre-commit run --all-files
