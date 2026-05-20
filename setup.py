"""Setup configuration for Jira integration framework."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jira-integration-framework",
    version="1.0.0",
    author="rsmedberg-maker",
    description="Python framework for Jira integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rsmedberg-maker/Test",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "jira>=3.13.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.9.1",
            "flake8>=6.1.0",
            "mypy>=1.5.1",
        ],
    },
)
