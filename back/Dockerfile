# pull official base image
FROM python:3.10

WORKDIR /usr/src

# set working directory
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean
    
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# Additional configurations for Dood
#VOLUME /var/run/docker.sock:/var/run/docker.sock