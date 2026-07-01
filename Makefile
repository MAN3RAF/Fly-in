PYTHON = python3
SRC = src/main.py

all: run

install:
	uv sync

debug:
	$(PYTHON) -m pdb $(SRC) $(MAP)

run:
	$(PYTHON) $(SRC) $(MAP)

clean:
	rm -rf __pycache__/
	rm -rf src/__pycache__/
	rm -rf .venv/
	rm -rf .mypy_cache/

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: all install debug run clean lint lint-strict