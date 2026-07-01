PYTHON = python3
SRC = src/main.py

all: run

install:
	uv sync

debug:
	uv run $(PYTHON) -m pdb $(SRC) $(MAP)

run:
	uv run $(PYTHON) $(SRC) $(MAP)

clean:
	rm -rf __pycache__/
	rm -rf src/__pycache__/
	rm -rf .venv/
	rm -rf .mypy_cache/

lint:
	uv run flake8 src/
	uv run mypy src/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 src/
	uv run mypy src/ --strict
.PHONY: all install debug run clean lint lint-strict