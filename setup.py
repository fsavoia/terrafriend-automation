from setuptools import find_packages, setup

from src.constants import TerraformSettings as ts

with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

setup(
    name="terrafriend",
    version=ts.VERSION.value,
    description="A tool for managing Terraform workflows.",
    author="Felipe Savoia",
    author_email="felipe@example.com",
    url="https://github.com/felipesavoia/terrafriend",
    packages=find_packages(exclude=["tests", "docs"]),
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "terrafriend=src.terrafriend:cli",
        ],
    },
)
