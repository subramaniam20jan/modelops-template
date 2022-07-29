#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR

conda env create --force --file=../environment.yaml -n modelops

conda run -n modelops pip install ipykernel

conda run -n modelops python -m ipykernel install --user --name modelops --display-name "Custom env"