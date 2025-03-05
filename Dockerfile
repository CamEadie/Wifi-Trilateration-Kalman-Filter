# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update
RUN apt-get install -y aircrack-ng libpcap-dev iproute2 net-tools
RUN apt-get install -y pciutils
RUN apt-get install -y sudo

# Copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install scapy

# Copy every content from the local folder to the image
COPY . .

# Run main script
#CMD ["/bin/bash"]
CMD [ "sudo", "python3", "-u", "/app/main.py" ]
