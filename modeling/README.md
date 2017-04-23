# Modeling the fish

This code runs much much faster on GPU, which we are currently getting using AWS p2.xlarge instances.

Note: much of this configuration will only work with the what-is-my-fish AWS account where we have an AMI, security groups and users established. 

## Prereqs

Install aws-cli and terraform.  Get a role, public and secret key for your AWS account.  

Configure your local aws environment wiht `aws configure`

Add your pem key to your keychain with `ssh-add ~/.ssh/<yourkey>.pem`

## Create and use GPU on AWS

`make start`

This will create a spot request, give it a few minutes to get an instance, then...

`make connect`

This will find the ip and ssh into the instance.

When you are done, destroy your infrastructure with:

`make stop`