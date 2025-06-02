FROM python:3.11-slim  # this tells us what base docker image to use. the docker community is vast and has done most of the work for us, all we have to do is decide what code to pull in and what requirements to add on top of the image
WORKDIR /code  # this is the working directory for the container. similar to how when you open file explorer, you are taken to your desktop
COPY requirements.txt ./  # this copies the requirements.txt file from your device into the container
RUN pip install -r requirements.txt  # this instructs the container to install the dependencies in the requirements.txt file
COPY app ./app  # this copies the app directory from your device into the container
COPY .env .env  # this copies the .env file from your device into the container
CMD ["streamlit", "run", "app/frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]  # you can pass commands as a list of arguments to the CMD function. this list of commands instructs the container to run streamlit (and passes it the file location, port, and address (in this case, localhost))