=============================
pathurl: object-oriented URLs
=============================

.. image:: https://github.com/spapanik/pathurl/actions/workflows/tests.yml/badge.svg
  :alt: Tests
  :target: https://github.com/spapanik/pathurl/actions/workflows/tests.yml
.. image:: https://img.shields.io/github/license/spapanik/pathurl
  :alt: License
  :target: https://github.com/spapanik/pathurl/blob/main/LICENSE.txt
.. image:: https://img.shields.io/pypi/v/pathurl
  :alt: PyPI
  :target: https://pypi.org/project/pathurl
.. image:: https://pepy.tech/badge/pathurl
  :alt: Downloads
  :target: https://pepy.tech/project/pathurl
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :alt: code style: black
  :target: https://github.com/psf/black
.. image:: https://img.shields.io/badge/build%20automation-yamk-success
  :alt: build automation: yam
  :target: https://github.com/spapanik/yamk
.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json
  :alt: Lint: ruff
  :target: https://github.com/charliermarsh/ruff

``pathurl`` is an objected-oriented way of manipulating URLs.

In a nutshell
-------------

Installation
^^^^^^^^^^^^

The easiest way is to use `poetry`_ to manage your dependencies and add *pathurl* to them.

.. code-block:: toml

    [tool.poetry.dependencies]
    pathurl = "^0.6.0"

Usage
^^^^^

``pathurl`` offers classes to manipulate URLs, paths and query strings. All objects are immutable.

Links
-----

- `Documentation`_
- `Changelog`_


.. _poetry: https://python-poetry.org/
.. _Changelog: https://github.com/spapanik/pathurl/blob/main/CHANGELOG.rst
.. _Documentation: https://pathurl.readthedocs.io/en/latest/
