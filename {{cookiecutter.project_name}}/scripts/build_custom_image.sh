#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if docker login harbor.staging-adalab.adamatics.io --get-login; then
    echo "Already logged into harbor"
else
    echo "Not logged into harbor yet, please login."
    docker login harbor.staging-adalab.adamatics.io
fi

# Build the docker image
docker build . -t {{cookiecutter.custom_image}}

# Install a new kernel with this image as the backend
python -m ipykernel install --user --name {{cookiecutter.project_name}}_docker_backed --display-name "{{cookiecutter.project_name}} docker-backed"

cp $SCRIPT_DIR/docker_kernel.json ~/.local/share/jupyter/kernels/{{cookiecutter.project_name}}_docker_backed/kernel.json

# Create a simple environment as well
# conda env create --file=environment.yaml
