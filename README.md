# Kubernetes monitoring with Prometheus+Grafana
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white)![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)![GHACTIONS](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)


## Purpose
Demonstrate a deployment of a simple flask web app in kubernetes cluster and monitroing it with Promethues and Grafana and continues deployment with Github Actions.

## Steps

1. **Install a local Kubernetes cluster on your computer :** 

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

2. **Create a simple "Hello World" web application with Python and Flask :**

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
        return "Hello from Python!!"

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

3. **Containerize the application using Docker.**

    3.1. Go back to your root folder and create docker files : 
    ```shell
      cd ..
      touch Dockerfile docker-compose.yaml
    ```

    3.2. With your editor add the following code to : 

      ```shell
      #Dockerfile:
      -----------
      FROM python:3.10.9-slim-buster

      RUN mkdir -p /app
      RUN apt-get update -y && apt-get install -y gcc
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
          image: <your_docker_repo_name>/python_flask_img:latest
          ports:
            - 5000:5000
    ```

4. **Build and push the Docker image to a registry:** 

    4.1. Build the docker image

    `docker-compose build python_flask_serv`  

    4.2. Run the docker image container

    `docker-compose up python_flask_serv`

    4.3. Push the image to dockerhub ( you might need to login to your docker registry account)

    `docker-compose push python_flask_serv`

5. **Set up a version control system (e.g. Git) and host the code for the application in a repository**

    [Instructions](https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github#adding-a-local-repository-to-github-using-git)

6. **Set up monitoring for the application using Prometheus and Grafana.**

    6.1. Install helm :

    https://helm.sh/docs/intro/install/

    6.2. Valitate it works : 

    `helm version`

    6.3. Install Prometheus - Add the Prometheus charts repository to our helm configuration:

    `minikube kubectl -- create namespace prometheus-monitoring`

    `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`

    6.4. Set Prometheus Operator :

    `helm install prometheus prometheus-community/kube-prometheus-stack -n prometheus-monitoring`
    
    ```shell
    minikube kubectl -- get deployment 
    NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
    prometheus-grafana                    1/1     1            1           36m
    prometheus-kube-prometheus-operator   1/1     1            1           36m
    prometheus-kube-state-metrics         1/1     1            1           36m
    ```
    
    6.5. Access prometheus UI
    ```shell
    minikube kubectl -- get pod -n prometheus-monitoring
    For prometheus-kube-prometheus-prometheus-0 we will run a port forwarding

    #Find the port to forawrd
    minikube kubectl -- logs prometheus-prometheus-kube-prometheus-prometheus-0 -n prometheus-monitoring |grep 'Listening on'
    #Output
    ts=2023-01-12T13:31:37.432Z caller=tls_config.go:232 level=info component=web msg="Listening on" address=[::]:9090

    #Forward the port
    minikube kubectl -- port-forward service/prometheus-kube-prometheus-prometheus 9090 -n prometheus-monitoring
    ```

    6.6. Access Grafana UI.

    `minikube kubectl -- get pod -n prometheus-monitoring`

    For prometheus-grafana-* we will run a port forwarding

    ```shell
    #Find the port to forawrd:
    minikube kubectl -- logs prometheus-grafana-6485fd848-gp9qz -c grafana -n prometheus-monitoring |grep 'HTTP Server Listen' 
    #output
    logger=http.server t=2023-01-12T13:29:44.467505971Z level=info msg="HTTP Server Listen" address=[::]:3000 protocol=http subUrl= socket=

    #Find the Default user
    minikube kubectl -- logs prometheus-grafana-6485fd848-gp9qz -c grafana -n prometheus-monitoring |grep 'Created default admin'
    # output
    logger=sqlstore t=2023-01-12T13:29:44.297042721Z level=info msg="Created default admin" user=admin

    #Password:
    minikube kubectl -- get secret --namespace default prometheus-grafana -o jsonpath="{.data.admin-password}" -n prometheus-monitoring | base64 --decode ; echo
    #output
    prom-operator

    #Forward the port:
    minikube kubectl -- port-forward deployment/prometheus-grafana 3000 -n prometheus-monitoring
    ```

7. **Configure the monitoring tool to collect and display metrics about the application's performance and resource usage.** 

    7.1. Edit the following files in the /src folder 

    ```python
    #server.py
    #---------
    from flask import Response, Flask, request
    import prometheus_client
    from prometheus_client.core import CollectorRegistry
    from prometheus_client import Summary, Counter, Histogram, Gauge
    import time
    import psutil

    app = Flask(__name__)
    CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

    _INF = float("inf")

    graphs = {}
    graphs['c'] = Counter('python_request_operations_total', 'The total number of processed requests')
    graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10, _INF))
    graphs['m'] = Gauge('system_usage','Hold current system resource usage',['resource_type'])

    @app.route("/")
    def hello():
        start = time.time()
        graphs['c'].inc()
        
        time.sleep(0.600)
        end = time.time()
        graphs['h'].observe(end - start)
        graphs['m'].labels('CPU').set(psutil.cpu_percent())
        graphs['m'].labels('Memory').set(psutil.virtual_memory()[2])

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
    psutil==5.9.4
    ``` 
        
    7.2.Build the docker image and Run the docker image container.See step 4.1-2

    7.3 Push the docker image ( it will overrun the previous image).See step 4.3

    7.4 Deploy the application to your Kubernetes cluster
    ```shell

    #create a namespace for the application
    minikube kubectl -- create namespace my-app 
  
    #create directories
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
      namespace: my-app
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
            image: <your_docker_repo_name>/python_flask_img:latest
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
      namespace: my-app
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
    apiVersion: monitoring.coreos.com/v1
    kind: ServiceMonitor
    metadata:
      name: webapp-super
      labels:
        component: backend
        instance: app
        name: containers-my-app
        release: prometheus # You need to verify what is your realease name pf prometheus
      namespace: prometheus-monitoring # choose in what name space your prometheus is 
    spec:
      namespaceSelector:
        matchNames:
        - default
        - my-app
      selector:
        matchLabels:
          component: backend
          instance: app
          name: containers-my-app
      endpoints:
      - port: http # http - is a port name which was put in service.yaml
      - path: /metrics

      # deploy the yaml file
      minikube kubectl -- apply -f monitor.yaml 
    ```
    In you promethus UI you should see the following under Targets:
    ![prom-targets](/images/prom-targets.jpg)
    7.5. Get the web app service :
    
    `minikube kubectl -- get service --all-namespaces`

    For webapp we will run a port forwarding
    
    `minikube kubectl -- port-forward service/webapp 5000 -n my-app`

    Open a web borwser and login to `localhost:5000` --> you should see have the hello world app.

    7.6. To create Dashboard in Grafana take the following steps:
      - Access Grafna UI on port 3000 ( see step 6.6) 
      - Open the sidebar menu and selct Dashboards --> New Dashboard --> Add a new panel.
      - In the Edit Panel page set the follwong :
        Data source : Promethues
        Metric: we will use "python_request_operations_total" ( you can find more at localhost:5000/metrics ).
      - Click on "Run queries" and Save. Here is an example :
        ![panels](/images/panels.jpg)

Bonus section:

  1.  **Set up a build pipeline using a CI/CD tool.**

      1.a. Configure the pipeline to automatically build and test the application whenever code is pushed to the repository. 
      
      - In your github repo , setup the following [secrets](https://docs.github.com/en/codespaces/managing-codespaces-for-your-organization/managing-encrypted-secrets-for-your-repository-and-organization-for-github-codespaces#adding-secrets-for-a-repository) :

        DOCKERHUB_USERNAME --> your dockerhub user name
        DOCKERHUB_TOKEN --> your dockerhub personal [Access Token](https://docs.github.com/en/codespaces/managing-codespaces-for-your-organization/managing-encrypted-secrets-for-your-repository-and-organization-for-github-codespaces#adding-secrets-for-a-repository)

      - Create the following folders and files in your root folder:

        ```shell
        mkdir .github
        cd .github
        mkdir workflows
        touch ci.yml
        ```

      - With your editor add the following code to :
    
        ```shell
        name: CI
        on:
          push:
            branches:
              - '**'
        jobs:
          build-and-test:
            runs-on: ubuntu-latest
            strategy:
              matrix:
                python-version: ['3.10']
            steps:
              - uses: actions/checkout@v3
              - name: Set up Python ${{ matrix.python-version }}
                uses: actions/setup-python@v4
                with:
                  python-version: ${{ matrix.python-version }}
              - name: Install dependencies
                run: |
                  python -m pip install --upgrade pip
                  pip install -r src/requirements.txt --no-cache-dir
              - name: Unittest
                run: python -m unittest src/tests/test_server.py

          push-to-dockerhub:
            needs: [build-and-test]
            runs-on: ubuntu-latest
            env:
              DOCKER_USER: ${{secrets.DOCKERHUB_USERNAME}}
              DOCKER_PASSWORD: ${{secrets.DOCKERHUB_TOKEN}}
              REPO_NAME: python_flask_img
            steps:
            - uses: actions/checkout@v2 # first action : checkout source code
            - name: docker login
              run: | # log into docker hub account
                docker login -u $DOCKER_USER -p $DOCKER_PASSWORD  
            - name: Build the Docker image # push The image to the docker hub
              run: docker build . --file Dockerfile --tag $DOCKER_USER/$REPO_NAME:latest
            - name: Docker Push
              run: docker push $DOCKER_USER/$REPO_NAME:latest
        ```

      1.b. Configure the pipeline to automatically deploy the application to the Kubernetes cluster whenever a new version is built and tested successfully. 

        - Expoe the Kubernetes API to the internet :

          - Download [ngrok](https://ngrok.com/download)
          - Use kube-proxy to proxy requests to the API from localhost:
            ```shell
            kubectl proxy --port=8001 --accept-hosts='.*\.ngrok.io'
            ```
          - In a new terminal, open an ngrok tunnel (port 8001 is the default Kubernetes API port):
            ```shell
            ngrok http 8001
            ```
            
          - The ngrok UI will output an HTTPS address that points directly to your minikube‘s API port. You can now use that URL to run kubectl commands against.
          ![ngrok](/images/ngrok.jpg)
          <br>
          - Add the following to the end of ci.yml (In the repo it's commneted as requires addtional step for KUBE_CONFIG. Uncommnet to enable )
            ```shell
              deploy-to-k8s-cluster:
                needs: [build-and-test,push-to-dockerhub]
                runs-on: ubuntu-latest
                steps:
                - uses: actions/checkout@v3
                - name: Start minikube
                  uses: medyagh/setup-minikube@master
                - name: Create kube config
                  run: |
                    mkdir -p $HOME/.kube/
                    echo "${{ secrets.KUBE_CONFIG }}" > $HOME/.kube/config
                    chmod 600 $HOME/.kube/config
                - name: Try the cluster
                  run: minikube kubectl -- get pods -A
                - name: Apply the deployment YAML
                  run: minikube kubectl -- apply -f kubernetes/deployments/deployment.yaml
            ```

          - Create a modified copy of your local kube config.
            ```shell
            $ kubectl config view --flatten > ~/Desktop/kube_config
              Remove `certificate-authority-data` line
              Add `insecure-skip-tls-verify: true` line
              Replace `server` value to `https://117b-2a02-c7f-e84f-c900-85c1-38ee-a128-9cec.ngrok.io`
              ```
              Finally it should look like something like below : 

              ```shell
              apiVersion: v1
              clusters:
              - cluster:
                  insecure-skip-tls-verify: true
                  server: https://117b-2a02-c7f-e84f-c900-85c1-38ee-a128-9cec.ngrok.io
                name: nonprod
              - cluster:
                  insecure-skip-tls-verify: true
                  server: https://117b-2a02-c7f-e84f-c900-85c1-38ee-a128-9cec.ngrok.io
                name: prod
              contexts:
              - context:
                  cluster: nonprod
                  user: nonprod
                name: nonprod
              - context:
                  cluster: prod
                  user: prod
                name: prod
              current-context: nonprod
              kind: Config
              preferences: {}
              users:
              - name: nonprod
                user:
                  client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0F...==
                  client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVp...=
              - name: prod
                user:
                  client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0F...==
                  client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVk...=
              ```
              
              
          
          - Copy this content into `KUBE_CONFIG` GitHub secret.
          - Commit your code.

  2. **What additional steps or considerations would be necessary to make this setup production-grade**

      1. Deploy each componnet (app / prometheus / grafana) on a sperate node in the cluster. 
      Or , on a seprate node in a seprate cluster.
      In addtiion , devide to dev / stage / prod environments.

      2. Deploymnet should be on a cloud environemnt ( e.g ec2 / Azure ) instead on a local host with ngrok.

      3. For CI in Github - add security application( SCA / SAST) which can integrate with the repositry and open issues / alert on sequrity.
