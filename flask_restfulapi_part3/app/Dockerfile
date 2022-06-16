# base image - python
FROM python:3.8
ENV PYTHONUNBUFFERED True

# define any environ variables here if you want
# by default, we use /content because it is consistent with google colab's setup
ENV APP_HOME /content

# some basic shell commands
RUN apt-get update && apt-get install zip unzip nano wget -y

# define the working directory inside the docker image
WORKDIR $APP_HOME

# copy in all the stuff in the app folder into the docker image 
# this will copy stuff into the working directory inside the docker image
COPY . ./

# pip install stuff
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# always ensure that the flask, gunicorn, and eventlet setups are all the right versions that actually work
# thats why we do them manually here, so it will overwrite any version that may have been downloaded
# in requirements.txt
RUN pip install Flask==2.0.1
RUN pip install gunicorn==20.1.0 
RUN pip install eventlet==0.30.2

# anything else
RUN mkdir -p temp

# run gunicorn
# note: PORT is an environ variable defined by GCP itself, so we do not need to define here 
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 src:app