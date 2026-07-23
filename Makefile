.PHONY: install test lint format clean

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=src

lint:
	ruff check src/

format:
	ruff format src/

clean:
	rm -rf .venv build dist *.egg-info
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache
	find . -name "*.pyc" -delete
