.PHONY: requirements install

requirements:
	pip freeze | grep -v "^-e" > requirements.txt

install:
	pip install -e .