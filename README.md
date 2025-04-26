# Simple Flask App with Docker and K8s

A step-by-step guide to creating a very simple Flask web application, using
MySQL/MariaDB database, containerizing with Docker, and deploying with
K8s/minikube. The presented application is quite lightweight due to the use of
[alpine](https://www.alpinelinux.org/) and
[minikube](https://minikube.sigs.k8s.io/docs) Inspired by
[chesahkalu](https://github.com/chesahkalu/Simple-Flask-App-Docker) and
[wangxian](https://github.com/wangxian/alpine-mysql).

## Requirements

 * [Docker](https://docs.docker.com/get-started/get-docker)
 * [Docker Compose](https://docs.docker.com/compose/install)
 * [Minikube](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)

## Setup Containers

The presented application uses an external database server for both reading and
writing some data. All environment variables are in `.env` file and can be
modified if needed.

Flask application and database server may be setup just using `docker compose`
and `docker-compose.yaml`:

    $ docker compose up --build

Or you can try to do it manually.

### Create Network

For container intercommunication we need to create a network:

    $ docker network create -d bridge my-network

### Setup Database Server

A docker image based on [alpine](https://www.alpinelinux.org/) and
[MariaDB](https://mariadb.org/).

the image can be built manually:

    $ docker build db -t db

or with docker-compose using:

    $ docker compose build db

The container can be run manually:

    $ # only root user
    $ docker run -it --name db --network=my-network -p 3306:3306 -v ~/appdata/mysql:/app/mysql -e MYSQL_DATABASE=appdb -e MYSQL_ROOT_PASSWORD=root db
    $ # use normal user of app
    $ docker run -it --name db --network=my-network -p 3306:3306 -v ~/appdata/mysql:/app/mysql -e MYSQL_DATABASE=appdb -e MYSQL_USER=app -e MYSQL_PASSWORD=pass -e MYSQL_ROOT_PASSWORD=root db

Or with using docker-compose:

    $ docker compose up -d db

To check if the server is running, you can try to connect to the server with
`MYSQL_PASSWORD` value as pass:

    $ mysql -P 3306 --protocol=TCP -u app -p

### Setup Flask App

To access the database, in addition to the
[Flask](https://flask.palletsprojects.com/en/stable/) module itself, we will
also need [Flask-MySQL](https://flask-mysql.readthedocs.io/en/stable/) module.
All required modules must be included in the `app/requirements.txt` file.

the image can be built manually:

    $ docker build app -t app

or with docker-compose using:

    $ docker compose build app

The container can be run manually:

    $ docker run -it --name app --network=my-network -p 5000:5000 -e MYSQL_DATABASE=appdb -e MYSQL_USER=app -e MYSQL_PASSWORD=pass -e MYSQL_HOST=db -e MYSQL_PORT=3306 app

Or with using docker-compose:

    $ docker compose up app

Now we can use address like `http://127.0.0.1:5000` from stdout and check our
web app!

## Setup Pods

### Create configs

First of all we need to create yaml configs for database and app deployment and
service and optionally for
[namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/),
[configmaps](https://kubernetes.io/docs/concepts/configuration/configmap/) and
[secrets](https://kubernetes.io/docs/concepts/configuration/secret/).

Let's make `my-app` namespace and copy database access vars into
`cofingmap.yaml`. This does not violate the DRY principle, since these variables
were added into `docker-compose.yaml` only for demonstration and can be removed
from there, since we will not run the containers ourselves.

Now all we have to do is just run the script:

    $ ./setup.sh

The script can easily be adapted to use k8s instead minikube. Just replace
`minikube kubectl --` with `kubectl`.
