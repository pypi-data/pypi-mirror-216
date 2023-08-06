#!/bin/sh
#
# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

set -e

# Run the Python test suite, prepare .tox/functional/bin/python3
[ -n "$NO_CLEAN$NO_PYTHON_CLEAN" ] || rm -rf .tox
tox-delay -p all -e unit_tests,functional

# Build the Rust project and run the test suite against it
: "${CARGO:=cargo}"
[ -n "$NO_CLEAN$NO_RUST_CLEAN" ] || $CARGO clean
$CARGO fmt -- --check
$CARGO doc --no-deps
$CARGO build
$CARGO clippy
.tox/functional/bin/python3 -B -u tests/functional.py -p target/debug/u8loc

# Build the Rust project in release mode and run the test suite against it
: "${CARGO:=cargo}"
$CARGO fmt -- --check
$CARGO doc --no-deps --release
$CARGO build --release
$CARGO clippy --release
.tox/functional/bin/python3 -B -u tests/functional.py -p target/release/u8loc

# Build the C project, run the test suite against it, install it locally
[ -n "$NO_CLEAN$NO_C_CLEAN" ] || rm -rf obj
cmake -S . -B obj -DUSE_BDE_CFLAGS=ON -DUSE_WERROR=ON
make -C obj
.tox/functional/bin/python3 -B -u tests/functional.py -p obj/c/u8loc/u8loc

rm -rf temproot
mkdir temproot
make -C obj install DESTDIR="$(pwd)/temproot"
find temproot/ -ls

# All fine?
echo 'Everything seems to be fine!'
