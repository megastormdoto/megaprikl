from setuptools import setup, find_packages

setup(
    name="minicompiler",
    version="0.1.0",
    packages=find_packages(where="."),  # Изменили на "."
    package_dir={"": "."},  # Изменили на "."
    entry_points={
        "console_scripts": [
            "compiler=src.cli:main",
        ],
    },
    python_requires=">=3.8",
    author="Your Team",
    description="A mini compiler for a C-like language",
    license="MIT",
)