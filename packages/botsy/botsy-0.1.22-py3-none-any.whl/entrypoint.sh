#!/bin/bash
set -e

if [[ -n "$TEST_PYPI_BUILD" ]]; then
    poetry build
    poetry config repositories.testpypi https://test.pypi.org/legacy/
    poetry config http-basic.testpypi $PYPI_USERNAME $PYPI_PASSWORD
    poetry publish -r testpypi
elif [[ -n "$PYPI_BUILD" ]]; then
    poetry build
    poetry config http-basic.pypi $PYPI_USERNAME $PYPI_PASSWORD
    poetry publish
fi