..  Copyright (c) 2024, Janus Heide.
..  All rights reserved.
..
.. Distributed under the "BSD 3-Clause License", see LICENSE.rst.

Dlister
=======

.. image:: https://github.com/janusheide/dlister/actions/workflows/unittests.yml/badge.svg
    :target: https://github.com/janusheide/dlister/actions/workflows/unittests.yml
    :alt: Unit tests

.. image:: https://img.shields.io/pypi/pyversions/dlister
   :alt: PyPI - Python Version

.. image:: https://img.shields.io/librariesio/github/janusheide/dlister
   :alt: Libraries.io dependency status for GitHub repo


Print or save to a file, dependencies in a pyproject.toml file based on defined
match operators. This is similar to a dependency 'freeze' but with added
configurability.

This can be useful for finding and testing with the oldest versions of the
dependencies for which support is declared in pyproject.toml.


Getting Started
---------------

Install and run::

    pip install dlister
    dlister --help


    usage: dlister [-h]
                   [-i INFILE]
                   [-o OUTPUT]
                   [-m [{<,<=,==,>=,>,~=} ...]]
                   [--skip [SKIP ...]]
                   [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [--log-file LOG_FILE]
                   [-v]
                   [dependencies ...]

    Print Python Project Dependencies.

    positional arguments:
    dependencies          path(s) to input file(s) (default: [])

    options:
    -h, --help            show this help message and exit
    -i INFILE, --infile INFILE
                          path(s) to input file(s) (default: pyproject.toml)
    -o OUTPUT, --output OUTPUT
                          output file. (default: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>)
    -m [{<,<=,==,>=,>,~=} ...], --match-operators [{<,<=,==,>=,>,~=} ...]
                          operators to upgrade. (default: ['==', '>='])
    --skip [SKIP ...]     dependencies to skip. (default: [])
    --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                          logging level. (default: WARNING)
    --log-file LOG_FILE   pipe loggining to file instead of stdout. (default: None)
    -v, --version         show program's version number and exit


Usage
-----

Run::

    dlister
    packaging==22.0
    tomli==2.0.0; python_version < "3.11"

    dlister -m "<=" "=="
    packaging==24.1
    tomli==2.0.2; python_version < "3.11"

    dlister test
    packaging==22.0
    tomli==2.0.0; python_version < "3.11"
    brundle==1.1.0
    isort==5.13.2
    mypy==1.13.0
    ruff==0.7.1
    pytest==8.3.3
    pytest-cov==5.0.0

    dlister "*"
    packaging==22.0
    tomli==2.0.0; python_version < "3.11"
    brundle==1.1.0
    isort==5.13.2
    mypy==1.13.0
    ruff==0.7.1
    pytest==8.3.3
    pytest-cov==5.0.0
    bouillon==2.6.0
    build==1.2.2.post1
    licensecheck==2024.3
    uppd==1.3.0
    twine==5.1.1

    dlister test -o requirements.old


Development
-----------

Setup, run tests and release::

    pip install .[dev]
    brundle
    pytest
    bouillon release 1.2.3
