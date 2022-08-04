# Overview

This is a cookiecutter template to get an ML project started on Adalab.

## Pre-requisites

* python 3.10 or later
* cruft 2.11.0 or later (https://cruft.github.io/cruft/)

## Quick start

Clone the template by running the following command.

`cruft clone https://github.com/subramaniam20jan/modelops-template.git`

## Prebuilt example

The template clones with a working example of a housing market scraper and a model to predict per sq m housing price.

## Workflow

1. Clone the template in the adalab environment
2. Add project specific dependencies in your requirements.txt (Optional)
3. Add non python customizations to add, add them to the Dockerfile (Optional)
4. Run `scripts build_custom_image.sh` to generate a docker image based jupyter kernel
5. Hack away with your code!

Additionally if you want to utilize mlflow related features for benchmarking, version control, reproducibility etc. follow the additional steps.

1. Put relevant parts of the code into model.py and etl.py under the steps folder
2. Configure workflow_conf.yaml with relevant input parameters
3. Run notebooks/workflow.py to get mlflow related features

## Notes

1. Project name in the cruft template needs to be a valid MLFlow project name.
2. Project name needs to be a valid conda environment name.
3. Project name needs to be a valid jupyter kernel name.