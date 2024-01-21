#!/bin/bash

cd ..
ls
pwd


aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 361614526163.dkr.ecr.eu-west-1.amazonaws.com

docker build -t payment-service .

docker tag payment-service:latest 361614526163.dkr.ecr.eu-west-1.amazonaws.com/payment-service:latest

docker push 361614526163.dkr.ecr.eu-west-1.amazonaws.com/payment-service:latest
