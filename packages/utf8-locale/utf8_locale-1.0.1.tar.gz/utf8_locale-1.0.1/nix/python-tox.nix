# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

{ pkgs ? import <nixpkgs> { }
, py-ver ? 311
}:
let
  python-name = "python${toString py-ver}";
  python = builtins.getAttr python-name pkgs;
  # tomli is needed until https://github.com/NixOS/nixpkgs/pull/194020 goes in
  python-with-tox = python.withPackages (p: with p; [ tomli tox ]);
in
pkgs.mkShell {
  buildInputs = [
    pkgs.git
    python-with-tox
  ];
  shellHook = ''
    set -e
    tox run-parallel
    exit
  '';
}
