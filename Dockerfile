# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set the working directory to /image_thumbnail
WORKDIR /image_thumbnail

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /image_thumbnail
COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#FROM python:3.9
#
## Set environment variables
#ENV PYTHONUNBUFFERED 1
#ENV PYTHONDONTWRITEBYTECODE 1
#
## Set the working directory to /app
#WORKDIR /image_thumbnail
#
## Copy the current directory contents into the container at /app
#COPY . /image_thumbnail
#
## Install the required packages
#RUN pip install -r requirements.txt
#
## Expose port 8000
#EXPOSE 8000
#
## Run the command to start the server
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]