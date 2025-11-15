lint:
	@poetry run ruff check .

lint-fix:
	@poetry run ruff check . --fix

format:
	@poetry run ruff format .

hello:
	@poetry run python -m gandalf.hello