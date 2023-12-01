.PHONY: requirements install clean build

requirements:
	@pip freeze | grep -v "^-e" > requirements.txt

install:
	@pip install -e .

clean:
	@rm -rf build dist *.egg-info
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
	@find . -name ".pytest_cache" -delete
	@find . -name ".coverage" -delete
	@find . -name ".cache" -delete
	@find . -name ".mypy_cache" -delete
	@find . -name ".DS_Store" -delete
	@find . -name ".ipynb_checkpoints" -delete
	@find . -name ".tox" -delete
	@find . -name ".eggs" -delete
	@find . -name "htmlcov" -delete
	@find . -name "dist" -delete
	@find . -name "build" -delete
	@find . -name "docs/_build" -delete

build:
	python setup.py sdist bdist_wheel
