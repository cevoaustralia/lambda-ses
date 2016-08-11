# lambda-ses

A simple email forwarder for static websites.

# Overview

The application is partially an experiment on writing the smallest application
that can serve the function of delivering SES emails from a HTTP POST.

Current approach is to leaverage the  [zappa](https://github.com/Miserlou/Zappa) toolkit to automate
the creation of the AWS services, API Gateway and Lambda.

To manage the HTTP POST workflow [flask](http://flask.pocoo.org/) was chosen as a simple web microframework.

# Development

Local development is simple, check out the code and run
the flask container.

## Install requirements
```
pip install -r requirements.txt
```

## Run Flask
```
python ses_forwarder.py
```

This should launch the flask container listening on port 5000 that you can access to simulate the connection to

## Test Curl the endpoint
```
curl -H "Content-Type: application/json" -X POST -d '{"subject":"this is the subject","body":"and this is the body"}' http://localhost:5000/contact
```

# Configuration

Configuration for the lambda is externalised into a JSON file `config.json`. This file contains the configurable
options that need to be set for the lambda function to
work for you.

## Example content

Create a `config.json` file in the root folder of this project and customise the following example:
```
{
  "from_address": "aws-lambda@example.com",
  "to_address": "support@example.com"
}
```

# Deployment

Deployment is managed by Zappa.

Zappa will be installed as part of the `pip install -r requirements.txt` command but still requires minimal configuration for your environment.

## Example Content

Create a `zappa_settings.json` file that contains the s3 bucket you want to deploy your application to before it is deployed into AWS Lambda.

```
{
    "dev": {
        "app_function": "ses_forwarder.send_email",
        "s3_bucket": "lambda.ses_forwarder"
    }
}
```

See the [Zappa documentation](https://github.com/Miserlou/Zappa#advanced-settings) for further details for advanced configuration of the `zappa_settings.json` file.
