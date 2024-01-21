#!/bin/bash
# Update and install Docker
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo usermod -a -G docker ec2-user

aws ecr get-login-password --region eu-west-1 | sudo docker login --username AWS --password-stdin 361614526163.dkr.ecr.eu-west-1.amazonaws.com

docker pull 361614526163.dkr.ecr.eu-west-1.amazonaws.com/payment-service:latest

sudo docker run -d -p 18080:18080 -e DYNAMO_ENDPOINT_URL="https://dynamodb.eu-west-1.amazonaws.com" 361614526163.dkr.ecr.eu-west-1.amazonaws.com/payment-service:latest

