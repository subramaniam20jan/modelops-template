#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Remove conda env
conda remove -y -p ~/.conda/{{cookiecutter.project_name}} --all

# Remove the kernels
jupyter kernelspec remove -y {{cookiecutter.project_name}}_docker_backed
jupyter kernelspec remove -y {{cookiecutter.project_name}}