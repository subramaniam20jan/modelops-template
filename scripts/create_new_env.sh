#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR

conda env create --force --file=../environment.yaml -p ~/.conda/modelops

conda run -p ~/.conda/modelops pip install ipykernel

conda run -p ~/.conda/modelops python -m ipykernel install --user --name modelops --display-name "Modelops env"