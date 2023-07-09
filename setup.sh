#!/usr/bin/env bash

set -euo pipefail

pacman --needed -Syu mysql-workbench python3 llvm gnome-keyring gcov
proxychains -q pip3 install -r ./requirements.txt
