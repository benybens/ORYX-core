.PHONY: install install-cad test lint format sweep cad clean

install:
	pip install -e ".[dev]"

install-cad:
	conda env create -f environment.yml

test:
	pytest --cov --cov-report=term-missing

lint:
	ruff check .
	black --check .
	mypy cad simulation propulsion flight_control optimization --ignore-missing-imports

format:
	ruff check --fix .
	black .

sweep:
	python scripts/run_sweep.py

cad:
	python scripts/generate_cad.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
