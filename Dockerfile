FROM python:3.10-slim

# RUN apt-get update -y && apt-get install libblas-dev  liblapack-dev -y

# Add dependencies for environment management
RUN pip install --upgrade pip ipython ipykernel poetry

WORKDIR /app

# Add environment related files
# COPY pyproject.toml /app/
# COPY poetry.lock /app/
# RUN poetry config virtualenvs.create false
# RUN poetry install
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy aws credential
COPY credentials /root/.aws/credentials

# Add source code
COPY . /app/
