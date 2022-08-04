FROM harbor.staging-adalab.adamatics.io/base_images/{{ cookiecutter.base_image }}_base:latest

# Add environment related files
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy aws credential
COPY credentials /root/.aws/credentials
