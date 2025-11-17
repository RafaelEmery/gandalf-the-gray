lint:
	@poetry run ruff check .

lint-fix:
	@poetry run ruff check . --fix

format:
	@poetry run ruff format .

hello:
	@poetry run python -m gandalf.hello

index:
	@poetry run python -m gandalf.indexer

ollama:
	@ollama serve

chat:
	@poetry run python -m gandalf.chat