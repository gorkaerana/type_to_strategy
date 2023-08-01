black:
	venv/bin/black .

mypy:
	venv/bin/mypy .

ruff:
	venv/bin/ruff .

test:
	venv/bin/pytest -vv .

tooling: black mypy ruff
