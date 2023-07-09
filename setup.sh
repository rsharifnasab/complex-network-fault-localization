#!/usr/bin/env bash

set -euo pipefail

(
    cd mysql
    ./setup.sh
)
pacman --needed -Syu mysql-workbench python3 llvm
