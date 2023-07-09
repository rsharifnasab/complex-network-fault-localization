#!/usr/bin/env bash

set -euo pipefail


git clone https://github.com/mchalupa/dg
cd dg
mkdir build
cd build
cmake ..
make -j4
