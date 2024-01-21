# Payment Service and BISA Service

This repository contains two services, Payment Service and BISA Service, that perform the following tasks:

## Payment Service

The Payment Service is responsible for processing payment transactions for end consumers by communicating with a payment provider BISA. It accepts payment requests and interacts with BISA to authenticate, authorise and settle transactions. A record of all transactions is kept, with sensisitive data obsfucated.

## BISA Service

BISA service replicates a Payment Processor or Bank in that here we store plain card data and account information and perform transactions against a consumers account. 

## Configuration

To configure the services and deploy locally, you need to set up AWS credentials. Create a `.aws/credentials` file in your user's root directory with the following format:

```plaintext
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

Now from within each of the services infra/ directories you can perform the following commands to deploy a service. 

`terraform init`

`terraform apply --auto-approve`

You must deploy BISA Service first and update the BISA_HOST_IP variable from within Payment Service's AppConfig class, the public IPs will be outputted as part of the terraform apply job. 
