from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="alx-utils",
    version="0.8",
    description="A collection of utility tools for ALX",
    author="BIO",
    url="https://github.com/amasin76/alx-utils",
    packages=find_packages(include=["src", "src.*", "tools", "tools.*"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={
        "tools.checker": ["test.bash"],
    },
    install_requires=[
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "alx-utils=src.alx_utils:main",
        ],
    },
)
