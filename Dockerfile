# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update
RUN apt-get install -y libpcap-dev iproute2 net-tools pciutils sudo

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the image
COPY ./requirements.txt ./requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy the content from the local folder to the image
COPY . .

# Run main script
CMD [ "sudo", "python3", "-u", "/app/main.py" ]
