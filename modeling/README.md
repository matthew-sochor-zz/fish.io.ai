# Modeling the fish

This code runs much much faster on GPU, which we are currently getting using AWS p2.xlarge instances.

Note: much of this configuration will only work with the what-is-my-fish AWS account where we have an AMI, security groups and users established. 

# Infrastructure

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

# Modeling

## Get the Data

Download the current fish data sets with:

`make pullData`

Clean up your file system (by deleting all of your data, so beware!)

`make cleanData`

## Configure your environment

You can set modeling parameters in the environment file (.env) 

Go ahead and edit that to set all kinds of things (including starting weights from checkpoints!)

## Modeling

Split the data into test and train:

`make split`

Pre-generate features to speed up computation:

`make features`

Train the model

`make train`

Predict your test set from weights.  Update weights of interest in .env and:

`make predict`