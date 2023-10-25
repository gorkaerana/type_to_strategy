format:
	venv/bin/ruff format .

type_check:
	venv/bin/mypy .

lint:
	venv/bin/ruff .

test:
	venv/bin/pytest -vv tests/

tooling: format type_check lint
