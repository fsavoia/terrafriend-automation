from setuptools import setup, find_packages

setup(
    name="terrafriend",
    version="1.0.0",
    description="A tool for managing Terraform workflows.",
    author="Felipe Savoia",
    author_email="felipe@example.com",
    url="https://github.com/felipesavoia/terrafriend",
    packages=find_packages(),
    install_requires=[
        "click",
        "gitpython",
        "termcolor",
    ],
    entry_points={
        "console_scripts": [
            "terrafriend=src.terrafriend:cli",
        ],
    },
)