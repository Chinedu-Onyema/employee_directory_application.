# Install python dependencies using
# python slim 3.12 version as the base image
# builder is an alias for python slim 3.12 version
# which will be referenced in the final image build
FROM python:3.12-slim
#------------------------------------------------------


# we are trying to keep the flask app image as lightweight
# as possible. The python 3.12 slim base image we have chosen
# makes our image lightweight but there are some packages (pillow)
# needed for our application to function that is not installed in our chosen base image.
# the base image by default. we need to exclusively install these packages.
# apt-get update — refreshes the list of available packages from Debian's repositories
# apt-get install -y --no-install-recommends libjpeg62-turbo zlib1g libpng16-16
# installs three system libraries that Pillow's compiled _imaging extension needs at runtime
# to handle JPEG, zlib-compressed, and PNG image data. -y auto-confirms the install
# --no-install-recommends skips optional extra packages to keep the image smaller.
# rm -rf /var/lib/apt/lists/* deletes the package list cache apt-get update downloaded 
# because we don't need it anymore once packages are installed. This shrinks the final image
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    libpng16-16 \
    && rm -rf /var/lib/apt/lists/*
#-------------------------------------------------------------



# Set the working directory in the docker image
WORKDIR /app
#-------------------------------------------------------


# Copy the requirements.txt file to the
# docker image file system dependencies file
COPY requirements.txt /app
#--------------------------------------------------------


# install all the dependencies stated inside this file
# for your flask application to function.
# --user installs the dependencies to /root/.local folder
# instead of /usr/local/lib/ general system python folder.
# this keeps all dependencies in one single directory
# --no-cache-dir means don't save a cache of the downloaded packages.
# Normally pip saves a cache in case you need to reinstall later
# but inside a Docker image you'll never reinstall,
# so the cache is just wasted space. This keeps the image smaller.
RUN pip install --user --no-cache-dir -r requirements.txt
#----------------------------------------------------------


# this copies all the files from your GitHub repo to
# to the working directory inside your docker image 
COPY . /app
#-----------------------------------------------------------


# starts the flask application by executing the
# the application.py python file to start the flask application container
CMD ["python", "application.py"]
