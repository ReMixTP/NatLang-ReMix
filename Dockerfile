FROM ubuntu:16.04

# Update OS
# RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y upgrade

# Install Python
RUN apt-get install -y python3-dev python3-pip
RUN pip3 install --upgrade pip

# Add requirements.txt
COPY requirements.txt /webapp/

# Install uwsgi Python web server
RUN pip3 install uwsgi

# Set the default directory for our environment
ENV HOME /webapp
WORKDIR /webapp

# Install app requirements
RUN pip3 install -r requirements.txt

# Create app directory
COPY ./ /webapp/

# Expose port 8000 for uwsgi
EXPOSE 8000

ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8000", "--module", "app:app", "--processes", "1", "--threads", "8"]
