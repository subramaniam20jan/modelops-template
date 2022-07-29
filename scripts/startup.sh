#!/usr/bin/env bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if docker login harbor.staging-adalab.adamatics.io --get-user; then
    echo "Already logged into harbor"
else
    echo "Not logged into harbor yet, please login."
    docker login harbor.staging-adalab.adamatics.io
fi

docker build . -t modelops_template

python -m ipykernel install --user --name python_in_docker --display-name "Python in Docker"

cp $SCRIPT_DIR/docker_kernel.json ~/.local/share/jupyter/kernels/python_in_docker/kernel.json

# Create a simple environment as well
conda env create --file=environment.yaml

## Create a conda environment based on a container
## Container should be based on the docker image defined

# Should have this folder mounted into the container