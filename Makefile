# THIS FILE WILL KEEP ALL THE COMPLEX COMMANDS I WILL FOR TESTING THIS PROJECT.
# IT IS LIKE A COOK BOOK GUIDE.
# install the all the libraries used for this project from the requirements.txt.
# Upgrade the python pip command to its latest version which is Python's package installer. It will download and installs Python libraries (packages) like
# Flask, Flask-WTF, etc from the internet which are all found in the requirements.txt so we can use them in our code
# Without pip install, trying to import flask or import boto3 in your code would fail with ModuleNotFoundError.
install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt


# Test all the .py files to make sure that they are reusable and work before production
test:
	python -m pytest -vv --cov=application --cov=config --cov=database \
	--cov=database_dynamo --cov=util
	python -m pytest -vv test_application.py
	python -m pytest -vv test_config.py
	python -m pytest -vv test_database_dynamo.py
	python -m pytest -vv test_database.py
	python -m pytest -vv test_util.py


# Give potential warnings about the logic/code structure in other to prevent future issues in production
lint:
	pylint --disable=R,C *.py || true

# pylint --disable=R,C *.py || true --- Use the '|| true' function to avoid warning errors from make --
# Remove white spaces and other indentation or bad logic/code structure by formatting all the .py files
format:
	black *.py


# Automatically run all the functions at once together.
all: install lint test format
