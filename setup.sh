#!/bin/bash -eu

minikube delete
minikube start --driver=docker --cpus=2 --memory=4096
eval $(minikube docker-env)

# Build images
docker-compose build

# Create all resources
kubectl apply -f k8s/ns.yaml
kubectl apply -f k8s/db.yaml
kubectl apply -f k8s/app.yaml

# Check pods
kubectl get pods -n my-app

# Check services
kubectl get svc -n my-app

# Check deployments
kubectl get deployments -n my-app

# Get cluster IP (for Minikube use 'minikube ip')
minikube ip

# Get NodePort for your app service
kubectl get svc app -n my-app -o jsonpath='{.spec.ports[0].nodePort}'
