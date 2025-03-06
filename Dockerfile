# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update
RUN apt-get install -y aircrack-ng libpcap-dev iproute2 net-tools pciutils sudo

# Set the working directory to /app
WORKDIR /app

# Copy the content from the local folder to the image
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip3 install virtualenv && \
    python3 -m virtualenv --python=python3.11 venv && \
    source ./venv/bin/activate && \
    pip3 install -r requirements.txt

# Run main script
CMD [ "sudo", "python3", "-u", "/app/main.py" ]
