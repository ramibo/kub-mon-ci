# Kubernetes monitoring with Prometheus+Grafana
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white)![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)


## Purpose
Demonstrate a deployment of simple flask web app in kubernetes cluster and monitroing it with Promethues and Grafana.

## Steps

1. Install a local Kubernetes cluster on your computer : 

    1.1. Install docker desktop according to your operation system: 
    [mac](https://docs.docker.com/desktop/install/mac-install/)
    [windows](https://docs.docker.com/desktop/install/windows-install/)
    [linux](https://docs.docker.com/desktop/install/linux-install/)


    1.2. Validate docker runs properly
    `docker info`
 
    1.3. [Install minikube  local Kubernetes](https://minikube.sigs.k8s.io/docs/start/)

    1.4. Start your cluster
    `minikube start`

    1.5. Validate install :
    `minikube kubectl version`

    1.6. Validate node : 
    ```shell
    minikube kubectl -- get nodes 
    NAME       STATUS   ROLES           AGE   VERSION
    minikube   Ready    control-plane   18m   v1.25.3
    ```

2. Create a simple "Hello World" web application with Python and Flask :
  2.1. [Install python and pip](https://www.python.org/downloads/)

  2.2. Create the app folders and files in your root folder:

  ```shell
  mkdir src
  cd src
  touch server.py requirements.txt
  ```

  2.3. With your editor add the following code to : 
  ```python
  #server.py
  #---------
  from flask import Flask
  app = Flask(__name__)

  @app.route("/")
  def hello():
      return "Hello from Python!"

  if __name__ == "__main__":
      app.run(host='0.0.0.0')

  
  #requirements.txt
  #----------------
  Flask == 2.2.2
  ```
  2.4. Validate the web app works locally
  
  ```shell
  #Create Virutal environment
  python3.10 -m venv env

  #activate
  source env/bin/activate

  #Install pakcages from the requirements file
  pip install -r requirements.txt
  
  #Run locally
  python server.py
  This will start a development web server hosting your application at http://localhost:5000.
  Press `CTRL+C`to quit
  
  #Exit Virutal environment
  deactivate
  ``` 
  
  
3. Containerize the application using Docker.
  3.1. Go back to your root folder and create docker files : 
  ```shell
    cd ..
    touch Dockerfile docker-compose.yaml
  ```

  3.2. With your editor add the following code to : 

  ```shell
  #Dockerfile:
  -----------
  FROM python:3.10.9-alpine3.17

  RUN mkdir -p /app
  WORKDIR /app

  COPY ./src/requirements.txt /app/requirements.txt
  RUN pip install -r requirements.txt

  COPY ./src /app/

  EXPOSE 5000
  CMD ["python", "/app/server.py"]

  #docker-compose.yaml:
  -------------------
  version: "3.4"
  services:
    python_flask_serv:
      build:
        context: .
      container_name: python_flask_con
      image: <your_docker_repo_name>/python_flask_img:1.0.0
      ports:
        - 5000:5000
  ```

4. Build and push the Docker image to a registry: 
  4.1. Build the docker image

  `docker-compose build python_flask_serv`  

  4.2. Run the docker image container

  `docker-compose up python_flask_serv`

  4.3. Push the image to dockerhub ( you might need to login to your docker registry account)

  `docker-compose push python_flask_serv`

5. Set up a version control system (e.g. Git) and host the code for the application in a repository
[Instructions](https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github#adding-a-local-repository-to-github-using-git)


6. Set up monitoring for the application using Prometheus and Grafana.
  6.1. Install helm :

  https://helm.sh/docs/intro/install/

  6.2. Valitate it works : 

  `helm version`

  6.3. Install Prometheus - Add the Prometheus charts repository to our helm configuration:

  `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`

  6.4. Set Prometheus Operator :

  `helm install prometheus prometheus-community/kube-prometheus-stack`
  
  ```shell
  minikube kubectl -- get deployment 
  NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
  prometheus-grafana                    1/1     1            1           36m
  prometheus-kube-prometheus-operator   1/1     1            1           36m
  prometheus-kube-state-metrics         1/1     1            1           36m
  ```
  
  6.5. Access Grafana UI.

  `minikube kubectl -- get pod`

  For prometheus-grafana-* we will run a port forwarding

  ```shell
  #Find the port to forawrd:
  minikube kubectl -- logs prometheus-grafana-6485fd848-gp9qz -c grafana |grep 'HTTP Server Listen' 
  #output
  logger=http.server t=2023-01-12T13:29:44.467505971Z level=info msg="HTTP Server Listen" address=[::]:3000 protocol=http subUrl= socket=

  #Find the Default user
  minikube kubectl -- logs prometheus-grafana-6485fd848-gp9qz -c grafana |grep 'Created default admin'
  # output
  logger=sqlstore t=2023-01-12T13:29:44.297042721Z level=info msg="Created default admin" user=admin

  #Password:
  minikube kubectl -- get secret --namespace default prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
  #output
  prom-operator

  #Forward the port:
  minikube kubectl -- port-forward deployment/prometheus-grafana 3000
  ```
  6.6. Access prometheus UI
  ```shell
  minikube kubectl -- get pod
  For prometheus-kube-prometheus-prometheus-0 we will run a port forwarding

  #Find the port to forawrd
  minikube kubectl -- logs prometheus-prometheus-kube-prometheus-prometheus-0 |grep 'Listening on'
  #Output
  ts=2023-01-12T13:31:37.432Z caller=tls_config.go:232 level=info component=web msg="Listening on" address=[::]:9090

  #Forward the port
  minikube kubectl -- port-forward service/prometheus-kube-prometheus-prometheus 9090
  ```
  7. Configure the monitoring tool to collect and display metrics about the application's performance and resource usage. 

  7.1. Edit the following files in the /src folder 

  ```python
  #server.py
  #---------
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


  #requirements.txt
  #----------------
  Flask == 2.2.2
  prometheus_client == 0.15.0
  ``` 
      
  7.2.Build the docker image and Run the docker image container.See step 4.1-2

  7.3 Push the docker image ( it will overrun the previous image).See step 4.3

  7.4 Deploy the application to your Kubernetes cluster
  ```shell
  mkdir kubernetes
  cd kubernetes
  mkdir deployments
  cd deployments
  touch deployment.yaml


  # with your editor add the following code to deployment.yaml:
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: webapp
    labels:
      component: backend
      instance: app
      name: containers-my-app
    namespace: default
  spec:
    selector:
      matchLabels:
        component: backend
        instance: app
        name: containers-my-app
    template:
      metadata:
        labels:
          component: backend
          instance: app
          name: containers-my-app
      spec:
        containers:
        - name: app
          image: <your_docker_repo_name>/python_flask_img:1.0.0
          imagePullPolicy: IfNotPresent
          ports:
          - containerPort: 5000
            name: webapp
          resources:
            requests:
              memory: "64Mi"
              cpu: "50m"
            limits:
              memory: "256Mi"
              cpu: "500m" 

  # deploy the yaml file
  minikube kubectl -- apply -f deployment.yaml 
  
  minikube kubectl -- get pods

  # create service.yaml 

  cd ..
  mkdir services
  cd services
  touch service.yaml

  # with your editor add the following code to service.yaml:
  apiVersion: v1
  kind: Service
  metadata:
    name: webapp
    labels:
      component: backend
      instance: app
      name: containers-my-app
    namespace: default
  spec:
    type: ClusterIP
    ports:
    - name: http
      port: 5000
      protocol: TCP
      targetPort: webapp 
    selector:
      component: backend
      instance: app
      name: containers-my-app
  
  # deploy the yaml file
  minikube kubectl -- apply -f service.yaml 

  # create monitor.yaml
  cd ..
  mkdir servicemonitors
  cd servicemonitors
  touch monitor.yaml

  # with your editor add the following code to monitor.yaml:
  apiVersion: v1
  kind: Service
  metadata:
    name: webapp
    labels:
      component: backend
      instance: app
      name: containers-my-app
      release: prometheus # You need to verify what is your realease name of prometheus
    namespace: default # choose in what name space your prometheus is
  spec:
    type: ClusterIP
    ports:
    - name: http
      port: 5000
      protocol: TCP
      targetPort: webapp 
    selector:
      component: backend
      instance: app
      name: containers-my-app

    # deploy the yaml file
    minikube kubectl -- apply -f monitor.yaml 
  ```
  7.5. Get the web app pod :
    
  `minikube kubectl -- get pod`

  For webapp-* we will run a port forwarding
  
  `kubectl port-forward pods/webapp-6b8dd6d544-687r9 5000:5000 -n default`

  Open a web borwser and login to `localhost:5000` --> you should see have the hello wold app.
