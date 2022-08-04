#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR

conda env create --force --file=../environment.yaml -p ~/.conda/{{cookiecutter.project_name}}

conda run -p ~/.conda/{{cookiecutter.project_name}} pip install ipykernel

conda run -p ~/.conda/{{cookiecutter.project_name}} python -m ipykernel install --user --name {{cookiecutter.project_name}} --display-name "{{cookiecutter.project_name}} env"