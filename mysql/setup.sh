#!/usr/bin/env bash

set -euo pipefail

wget -c https://zenodo.org/record/2582968/files/code4bench.rar
unrar x ./code4bench.rar
