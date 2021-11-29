FROM python:3-slim

# Create app directory
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip list > /python_installed_packages.txt

# Bring over the main scripts
COPY src/servicex_did_finder_girder.py .

# build stamp
RUN echo "Timestamp:" `date --utc` | tee /image-build-info.txt

# Make sure python isn't buffered
ENV PYTHONUNBUFFERED=1

ENTRYPOINT [ "python3", "/usr/src/app/servicex_did_finder_girder.py" ]
