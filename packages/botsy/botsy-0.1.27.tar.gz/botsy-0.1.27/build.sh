#!/usr/bin/env bash

# To build
poetry build

# Install localy
poetry install

# upload to testpypi
poetry publish --repository testpypi

# Install from testpy
pip install --index-url https://test.pypi.org/simple/ --upgrade botsy

# upload to pypi
# poetry publish