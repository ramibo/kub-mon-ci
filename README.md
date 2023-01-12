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

server.py
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
python server.py
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

5.Set up a version control system (e.g. Git) and host the code for the application in a repository
We w
https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github#adding-a-local-repository-to-github-using-git

6.Set up monitoring for the application using Prometheus and Grafana.

6.1. Deploy Prometheus and Grafana into our Minikube cluster using their provided Helm charts.

6.1.1. Install helm :
https://helm.sh/docs/intro/install/

6.1.2. valitate it works with helm version

6.2.1 Install Prometheus

6.2.1.1. Add the Prometheus charts repository to our helm configuration:
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

6.2.1.2. Set Prometheus Operator :
helm install prometheus prometheus-community/kube-prometheus-stack

Output

NAME: prometheus
LAST DEPLOYED: Thu Jan 12 15:26:43 2023
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
kube-prometheus-stack has been installed. Check its status by running:
  kubectl --namespace default get pods -l "release=prometheus"

Visit https://github.com/prometheus-operator/kube-prometheus for instructions on how to create & configure Alertmanager and Prometheus instances using the Operator.

minikube kubectl -- get deployment 
NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
prometheus-grafana                    1/1     1            1           36m
prometheus-kube-prometheus-operator   1/1     1            1           36m
prometheus-kube-state-metrics         1/1     1            1           36m

6.2.1.3. Access graphana
minikube kubectl -- get pod
For prometheus-grafana-* we will run a port forwarding

Find the port to forawrd
minikube kubectl -- logs prometheus-grafana-6485fd848-gp9qz -c grafana |grep 'HTTP Server Listen' 
logger=http.server t=2023-01-12T13:29:44.467505971Z level=info msg="HTTP Server Listen" address=[::]:3000 protocol=http subUrl= socket=

Find the Default user
minikube kubectl -- logs prometheus-grafana-6485fd848-gp9qz -c grafana |grep 'Created default admin'
logger=sqlstore t=2023-01-12T13:29:44.297042721Z level=info msg="Created default admin" user=admin

Password
minikube kubectl -- get secret --namespace default prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
prom-operator

Forward the port
minikube kubectl -- port-forward deployment/prometheus-grafana 3000

6.2.1.3. Access prometheus
minikube kubectl -- get pod
For prometheus-kube-prometheus-prometheus-0 we will run a port forwarding

Find the port to forawrd
minikube kubectl -- logs prometheus-prometheus-kube-prometheus-prometheus-0 |grep 'Listening on' 
ts=2023-01-12T13:31:37.432Z caller=tls_config.go:232 level=info component=web msg="Listening on" address=[::]:9090

Forward the port
minikube kubectl -- port-forward service/prometheus-kube-prometheus-prometheus 9090

<!-- 6.2.1.3 expose the prometheus-server Service using a NodePort.
For service name run minikube kubectl -- get services 

minikube kubectl --  expose service prometheus-server --type=NodePort --target-port=9090 --name=prometheus-server-np

result service/prometheus-server-np exposed

6.2.1.4 Access the Prometheus web interface when the Pod is ready:
minikube service prometheus-server-np

6.3.1 Install Graphana (open a new terminal)

6.3.1.1 Add the Graphana charts repository to our helm configuration:
helm repo add grafana https://grafana.github.io/helm-charts

6.2.1.3. install the provided charts
helm install my-release grafana/grafana

6.2.1.3 expose the grafana Service using a NodePort.
For service name run minikube kubectl -- get services 

minikube kubectl -- expose service my-release-grafana --type=NodePort --target-port=3000 --name=grafana-np

service/grafana-np exposed

6.2.1.4 Get Grafana admin credentials
kubectl get secret --namespace default my-release-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
2I94ADyshlK9XchKUXEqI3U8B72WsTkqkKAjMYAI

6.3.1.5 Access the Grafana web interface using the admin user and the password retrieved:
minikube service grafana-np -->

7. Configure the monitoring tool to collect and display metrics about the application's performance and resource usage. 

7.1 lets edit the following files in the /src folder 

server.py
-----------------------------------------
from flask import Response, Flask, request
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time

app = Flask(__name__)

_INF = float("inf")

graphs = {}
graphs['c'] = Counter('python_request_operations_total', 'The total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10, _INF))

@app.route("/")
def hello():
    start = time.time()
    graphs['c'].inc()
    
    time.sleep(0.600)
    end = time.time()
    graphs['h'].observe(end - start)
    return "Hello World!"

@app.route("/metrics")
def requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
----------------------------------------


requirements.txt
----------------------------------------
Flask == 2.2.2
prometheus_client == 0.15.0

7.2 Build the docker image and Run the docker image container

7.3 push the docker image ( it will overrun the previous image)

7.4 Deploy the application to our k8s cluster

7.4.1 In the root folder , creat a new folders named kubernetes:
mkdir kubernetes
cd kubernetes
mkdir deployments
cd deployments
touch deployment.yaml

7.4.2 ith your editor (vi / VScode ) add the following code to deployment.yaml:
-------------------------------------------------------------------------------

apiVersion: apps/v1
kind: Deployment
metadata:
  name: example-deploy
  labels:
    app: example-app
    test: test
  annotations:
    fluxcd.io/tag.example-app: semver:~1.0
    fluxcd.io/automated: 'true'
spec:
  selector:
    matchLabels:
      app: example-app
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: example-app
    spec:
      containers:
      - name: example-app
        image: rammatz/python_flask_img:1.0.0
        imagePullPolicy: Always
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "256Mi"
            cpu: "500m"   

7.4.2 deploy the yaml file
minikube kubectl -- apply -f deployment.yaml 
output deployment.apps/example-deploy created

7.4.3 create service.yaml to define load balncing of each pod created
minikube kubectl -- get pods
NAME                                                 READY   STATUS    RESTARTS       AGE
example-deploy-6c789dbcd4-hmfb9                      1/1     Running   0              38s
example-deploy-6c789dbcd4-r6vdp                      1/1     Running   0              38s

cd ..
mkdir services
cd services
touch service.yaml

7.4.3.1. ith your editor (vi / VScode ) add the following code to service.yaml:
-------------------------------------------------------------------------------
apiVersion: v1
kind: Service
metadata:
  name: example-service
  labels:
    app: example-app
spec:
  type: LoadBalancer
  selector:
    app: example-app
  ports:
    - protocol: TCP
      name: http
      port: 80
      targetPort: 5000

7.4.4
minikube kubectl -- apply -f service.yaml
service/example-service created

7.4.4
In another window, start the tunnel to create a routable IP for the ‘balanced’ deployment:
minikube tunnel

7.4.5. Check the extrenl IP of the service
minikube kubectl -- get svc 

In our case it's localhost (127.0.0.1)
NAME                                  TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
example-service                       LoadBalancer   10.109.205.76    127.0.0.1     80:31219/TCP   14m

Open a web borwser and login to that IP --> you should see have the hello wold app

minikube kubectl -- get servicemonitor
