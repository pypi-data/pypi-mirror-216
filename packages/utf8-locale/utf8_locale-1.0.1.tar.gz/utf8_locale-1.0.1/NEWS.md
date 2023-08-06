<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# Changelog

All notable changes to the utf8-locale project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2023-06-29

### Fixes

- Python:
    - do not pass the `python_version` option to mypy
    - correctly annotate a test function that returns a `mock.patch()` object
    - many minor changes suggested by Ruff
- Rust:
    - a couple of minor changes suggested by Clippy

### Additions

- Add a Nix expression to only run the Python unit tests using `pytest`
- Add two shell helpers for running the Nix expressions with several
  versions of Python
- Python:
    - add a Ruff Tox test environment
    - add Tox environment tags for the `tox-stages` tool
    - add a manually-invoked `pyupgrade` Tox test environment

### Other changes

- Convert this changelog to the "Keep a Changelog" format.
- Drop the years from my copyright notices.
- Switch to SPDX copyright and license tags and add a "reuse" Tox environment for
  validating the SPDX tags
- Python:
    - drop Python 3.7 support
    - add the `ruff` and `ruff-all` Tox testing environments, test with Ruff 0.0.275
    - drop the `pep8` and `pylint` Tox testing environments, Ruff does most of that
    - order the Tox environment list a bit more logically
    - adapt the `tox.ini` file format for Tox 4.x
    - use black 23.x and mypy 1.x with no changes
    - use Pytest's own data-driven testing functions instead of the `ddt` library
    - switch to `hatchling` for the PEP 517 build
    - use Ruff's isort implementation
    - move the mypy configuration to the `pyproject.toml` file
    - use `functools.lru_cache()` in the test suite
- Rust:
    - use variables inline in `format!()` strings, declare MSRV 1.58
    - silence clippy's complaints about using blanket restrictions and
      using the question mark operator

## [1.0.0] - 2022-10-30

### Incompatible changes

- Rust:
    - the `get_preferred_languages()` function now accepts a reference to
      the environment variables, since it does not need to modify them
    - mark the public enums and structs as non-exhaustive
    - all functions now return errors instead of exiting the program
    - use our own error type instead of returning `Box<dyn error>`

### New features

- Add a Nix expression for running the Python tests in a clean environment
- Rust:
    - allow hashmaps to be constructed with different hashers
    - keep the `Cargo.lock` file under version control

### Fixes

- C:
    - use `regerror()` more robustly; thanks, John Scott
    - when freeing a list, free the correct pointer
    - add a missed `free()` in an error handling case
    - allow C++ programs to use the `utf8_locale.h` header file
    - do not use reserved identifiers as an include guard
- Python:
    - specify both lower and upper version constraints for the libraries used in
      the test environments
- Rust:
    - actually run the preferred language test with real data, not with
      an empty array

### Other changes

- Python:
    - use pylint 2.14, drop some message overrides
    - type annotations: use the standard `dict`, `list`, etc, types instead of
      the `typing` generics
    - list Python 3.10 and 3.11 as supported versions
    - drop the `flake8` + `hacking` Tox test environment
- Rust:
    - mark some functions as `const`, `inline`, and `must-use`
    - document the errors returned by the library functions
    - use the `thiserror` and `anyhow` libraries for error handling instead of
      the `quick-error` one
    - use the `once_cell` library for initializing static values instead of
      the `lazy_static` one
    - fix many minor issues reported by the `clippy` tool and add
      the `run-clippy` tool to run some stringent checks
    - refactor the internal `build_weights()` function to avoid integer
      arithmetic; when we mean to use the number of items in a hashmap,
      use the number of items in the hashmap
    - explicitly override some of the `clippy` diagnostics

## [0.3.0] - 2022-02-20

### Incompatible changes

- Rust:
    - the individual functions are no longer visible by default in
      the top-level namespace; the new builder interface is preferred

### New features

- Add a new object-oriented interface for the Python and Rust
  implementations: configure a `Utf8Detect` or `LanguagesDetect` object,
  and invoke their `.detect()` method instead of invoking the individual
  functions.
- Add a C implementation: a `libutf8_locale` library and a `u8loc`
  executable built using CMake.
- Add the `tests/full.sh` development helper tool that rebuilds all
  the implementations and runs their respective tests.
- Python:
    - move the languages test data to the `tests/data.json` definitions, too
    - add an object-oriented builder interface
- Rust:
    - add an object-oriented builder interface
    - add the beginnings of a unit test suite using the JSON test definitions

### Fixes

- Fix the functional test's behavior if the u8loc executable does not
  advertise the query-preferred feature.

### Other changes

- Add `*.c`, `*.h`, and `*.1` file definitions to the EditorConfig file.
- Python:
    - drop the `b0` suffix from the `black` tool versioned dependencies;
      the `black` tool is no longer in beta since version 22
- Rust:
    - use the `lazy_static` crate to only compile regular expressions once
    - import struct names directly as a more idiomatic style

## [0.2.0] - 2022-02-01

### New features

- The "C" language is now appended to the end of the list returned by
  the `get_preferred_languages()` function if it is not already there!
- Add the `get_utf8_vars()` function returning an environment-like
  dictionary that only contains the variables that need to be set,
  i.e. `LC_ALL` and `LANGUAGE`.
- Add the `u8loc` command-line tool to the Python implementation.
- Add the `u8loc.1` manual page.
- Add the `tests/functional.py` functional testing tool.
- Add an EditorConfig definitions file.
- Add a Rust implementation.

### Other changes

- Bring the Python build infrastructure somewhat more up to date.
- Require Python 3.7 for dataclasses support.
- Push the Python implementation into a `python/` source subdirectory.

## [0.1.1] - 2021-04-05

### New features

- Add a manifest file for the source distribution.

### Fixes

- Ignore locales with weird names instead of erroring out.
- Ignore the type of a `subprocess.check_output()` mock in the test suite.

## [0.1.0] - 2021-01-04

### Started

- First public release.

[Unreleased]: https://gitlab.com/ppentchev/utf8-locale/-/compare/release%2F1.0.1...main
[1.0.1]: https://gitlab.com/ppentchev/utf8-locale/-/compare/release%2F1.0.0...release%2F1.0.1
[1.0.0]: https://gitlab.com/ppentchev/utf8-locale/-/compare/release%2F0.3.0...release%2F1.0.0
[0.3.0]: https://gitlab.com/ppentchev/utf8-locale/-/compare/release%2F0.2.0...release%2F0.3.0
[0.2.0]: https://gitlab.com/ppentchev/utf8-locale/-/compare/release%2F0.1.1...release%2F0.2.0
[0.1.1]: https://gitlab.com/ppentchev/utf8-locale/-/compare/release%2F0.1.0...release%2F0.1.1
[0.1.0]: https://gitlab.com/ppentchev/utf8-locale/-/tags/release%2F0.1.0
