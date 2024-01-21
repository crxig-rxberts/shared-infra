#!/bin/bash

cd ..

aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 361614526163.dkr.ecr.eu-west-1.amazonaws.com

docker build -t bisa-service .

docker tag bisa-service:latest 361614526163.dkr.ecr.eu-west-1.amazonaws.com/bisa-service:latest

docker push 361614526163.dkr.ecr.eu-west-1.amazonaws.com/bisa-service:latest
