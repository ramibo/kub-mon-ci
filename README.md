Intro
-------
The following project demonstrates a deployment of simple flask web app in kubernetes cluster and monitroing it with promethues and graphana.



Steps
--------

1.Install a local Kubernetes cluster on your computer
    1.1. Install docker desktop
    mac-https://docs.docker.com/desktop/install/mac-install/
    windows - https://docs.docker.com/desktop/install/windows-install/
    linux -https://docs.docker.com/desktop/install/linux-install/

    1.2
    validate docker runs properly
    docker info

    1.3. Install minikube  local Kubernetes
    https://minikube.sigs.k8s.io/docs/start/


        1.3.1. Start your kluster
        minkube start
        
        1.3.2. Validate install:
        minikube kubectl version
        Flag --short has been deprecated, and will be removed in the future. The --short output will become the default.
        Client Version: v1.25.2
        Kustomize Version: v4.5.7
        Server Version: v1.25.2

        1.3.3 validate node
        minikube kubectl -- get nodes 
        NAME       STATUS   ROLES           AGE   VERSION
        minikube   Ready    control-plane   18m   v1.25.3

2. Create a simple "Hello World" web application with Python and Flask.

2.1 -install python and pip

2.2 - Code the web app:
In your root folder
mkdir src
cd src
touch app.py requirements.txt

With your editor (vi / VScode ) add the following code to : 

app.py
-----------------------------------------
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Python!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
----------------------------------------


requirements.txt
----------------------------------------
Flask


2.3 Validate the webapp works locally

2.3.1 virutal environment

Create
https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
python3.10 -m venv env 

activate 
https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment


source env/bin/activate 

2.3.2
Install pakcages from the requerments file 
https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#using-requirements-files

2.3.3 Run locally
python main.py
This will start a development web server hosting your application at http://localhost:5001.
Flask's default port 5000.

Press CTRL+C to quit
deactivate


3.Containerize the application using Docker.

3.1. Go back to your root folder and create docker files:
cd ..
touch Dockerfile docker-compose.yaml

With your editor (vi / VScode ) add the following code to : 

Dockerfile:
------------------------------------------------------
FROM python:3.10.9-alpine3.17

RUN mkdir -p /app
WORKDIR /app

COPY ./src/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./src /app/

EXPOSE 5000
CMD ["python", "/app/server.py"]

------------------------------------------------------

docker-compose.yaml:

version: "3.4"
services:
  python_flask_serv:
    build:
      context: .
    container_name: python_flask_con
    image: rammatz/python_flask_img:1.0.0
    ports:
      - 5001:5000

------------------------------------------------------

4. Build and push the Docker image to a registry. 

4.1. Build the docker image
docker-compose build <docker-compose.yaml service name >  
docker-compose build python_flask_serv   

4.1.1 Run the docker image container
docker-compose up python_flask_serv 

You should get same result as in 2.3.3

4.2 Push the image to dockerhub ( you might need to login to your docker registry account)
docker-compose push python_flask_serv