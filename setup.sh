#!/bin/bash -eu

minikube delete
minikube start --driver=docker --cpus=2 --memory=4096
eval $(minikube docker-env)

# Build images
docker-compose build

# Create all resources
minikube kubectl -- apply -f k8s/namespace.yaml
minikube kubectl -- apply -f k8s/configmap.yaml
minikube kubectl -- apply -f k8s/db.yaml
minikube kubectl -- apply -f k8s/app.yaml

# Wait for app start
sleep 10

# Check pods
minikube kubectl -- get pods -n my-app

# Check services
minikube kubectl -- get svc -n my-app

# Check deployments
minikube kubectl -- get deployments -n my-app

# Get app address:
# Get cluster IP (for Minikube use 'minikube ip')
# Get NodePort for your app service
echo $(minikube ip):$(minikube kubectl -- get svc app -n my-app -o jsonpath='{.spec.ports[0].nodePort}')
