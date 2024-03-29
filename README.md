# Payment Service and BISA Service

This repository contains two services, Payment Service and BISA Service, that perform the following tasks:

## Payment Service

The Payment Service is responsible for processing payment transactions for end consumers by communicating with a payment provider BISA. It accepts payment requests and interacts with BISA to authenticate, authorise and settle transactions. A record of all transactions is kept, with sensisitive data obsfucated.

## BISA Service

BISA service replicates a Payment Processor or Bank in that here we store plain card data and account information and perform transactions against a consumers account. 

## Configuration

Terraform and AWS CLI are required.

To deploy the services, you need to set up AWS credentials. Create a `.aws/credentials` file in your user's root directory with the following format:

```plaintext
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

Now from within each of the services infra/ directories you can perform the following commands to deploy a service. 

`terraform init`

`terraform apply --auto-approve`

You must deploy BISA Service first and update the BISA_HOST_IP variable from within Payment Service's AppConfig class, the public IPs will be outputted as part of the terraform apply job. 

Then when finished, clean down with:

`terraform destroy --auto-approve`

## Local Development

When not passing the application a DYNAMODB_ENDPOINT_URL the application knows to configure local infrastructure.

Each service has a requirements.txt for dependencies and a compose.yml that can be used to spin up local dynamodb tables by using the following command at a service root.

`docker compose up`

The services run on the same port as they are intended to be seperate, due to this you would be required to migrate one when running both services locally.
