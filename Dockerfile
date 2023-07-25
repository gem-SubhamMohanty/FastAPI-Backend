# Docker treats each one of these files as layer of the image and caches the result. Keep in mind that docker checks each line in serial order. So if we put COPY . . before RUN pip install --no-cache-dir -r requirements.txt. both are gonna run and RUN pip install --no-cache-dir -r requirements.txt is the longest file to run

# Docker compose can spin up our containers with the desired configuration

# specifying python base image version(documentation)
FROM python:3.9.17

# This is where all of the commands were essentially going to run from (optional)
WORKDIR /usr/src/app

# Copy this .txt to ./ -> /usr/src/app and cache the result
COPY requirements.txt ./

# Responsible for installing all of our dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything in our curren directory (source code)
COPY . .

# Run this command in our container
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]