.PHONY: lint lint-fix

lint:
    poetry run ruff check .

lint-fix:
    poetry run ruff check . --fix

format:
    poetry run ruff format .