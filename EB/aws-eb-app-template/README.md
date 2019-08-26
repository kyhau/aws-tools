# Sample repo template for creating ElasticBeanstalk app

This repo contains templates for building/deploying an EB application.
- [app/.ebextensions/](app/.ebextensions)
- [app/.elasticbeanstalk/](app/.elasticbeanstalk)
- [app/sample_service/](app/sample_service)
- [app/.dockerignore](app/.dockerignore)
- [app/.ebignore](app/.ebignore)
- [app/.gitignore](app/.gitignore)
- [app/Dockerfile](app/Dockerfile)
- [aws/cloudformation/EB-CloudWatchPolicy.template ](aws/cloudformation/EB-CloudWatchPolicy.template)
- [aws/cloudformation/EB-IAM-Deploy.template](aws/cloudformation/EB-IAM-Deploy.template)
- [aws/cloudformation/S3-Configs.template](aws/cloudformation/S3-Configs.template)
- [aws/cloudformation/S3-RootLogs.template](aws/cloudformation/S3-RootLogs.template)
- [deploy/eb_deployment_helper.sh](deploy/eb_deployment_helper.sh)
- [deploy/requirements-deploy.txt](deploy/requirements-deploy.txt)
- [deploy/setup_aws_profile.py](deploy/setup_aws_profile.py)

## Initialise EB Application and generate .elasticbeanstalk and .gitignore
Only need to do it once

```
$ pip install awsebcli six

# Change to the source directory
$ cd app

$ eb init --profile ${AWS_PROFILE}
# - Region: sydney
# - Application name: SampleService
# - Platform version: Docker 17.03.1-ce (or latest)
# - ssh key: my-sampleservice-key

$ eb create SampleService-dev --cname sampleservice-dev --vpc
# See also http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-getting-started.html
# - Environment Name: SampleService-dev
# - DNS CNAME prefix: sampleservice-dev
# - Load balancer type: application
```


## Deploy application and update Elastic Beanstalk Environment

See also [EB CLI Reference: `eb config`](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-config.html).

1. To build and test the Docker image for the application. 
   You need to install `docker` if you want to run it locally:

       $ cd deploy
       $ ./eb_deployment_helper.sh --build-image 

2. To also deploy the application and update settings/configurations within EC2 instances:
  
       $ cd deploy
       $ ./eb_deployment_helper.sh --build-image \
             [--push-image] \
             --eb-deploy --eb-env [EB_ENV_NAME]

3. To update Elastic Beanstalk Environment for instant change in After Creation state:

    1. Make sure you have the latest EB environment first. 
       Because `aws:elasticbeanstalk:managedactions:platformupdate` is enabled, the Docker/platform version in
       `Platform:PlatformArn` can be different from the last saved `*.cfg.yml` file.
    
           $ cd app/
           $ eb use [EB_ENV_NAME]              # Ensure all operations take effect to a specific EB environment
           $ eb config delete [EB_ENV_NAME]    # Delete the named saved configuration (in EB S3)
           $ eb config save [EB_ENV_NAME]      # Save the environment configuration settings for the current running
                                               # environment to .elasticbeanstalk/saved_configs/ with the filename
                                               # [EB_ENV_NAME].cfg.yml.
    
    2. Edit `app/.elasticbeanstalk/saved_configs/[EB_ENV_NAME].cfg.yml`.

    3. Create Pull Request for review.

    4. Apply the change 

           $ cd deploy
           $ ./eb_deployment_helper.sh --eb-config-update --eb-env [EB_ENV_NAME]


## To ssh to the EC2 using EB CLI

```
eb ssh [EB_ENV_NAME] --profile [profile-name]
```

## See all logs

```
eb logs --all
```


## Locations of file on EB EC2 Instances

### `/opt/elasticbeanstalk/hooks/appdeploy/`

1. `opt/elasticbeanstalk/hooks/appdeploy/pre/`
     1. `00clean_dir.sh` - Clean directory where source will be downloaded, removes docker containers and images.
     2. `01unzip.sh` - Download source from S3 and unzip it.
     3. `02loopback-check.sh` - Verify you don't have docker loopback setting set.
     4. `03build.sh` - Build your docker image from your `Dockerfile` or `Dockerrun.aws.json`. 

2. `/opt/elasticbeanstalk/hooks/appdeploy/enact/`
     1. `00run.sh` - Execute `docker run` against the image that was generated in the pre stage based on environment
        variables and settings in your `Dockerrun.aws.json`.
     2. `01flip.sh` - Convert from aws-staging to current-app etc.

3. `/opt/elasticbeanstalk/hooks/appdeploy/post/`

See also
- [elastic-beanstalk docker app not updating upon deploy](
  https://stackoverflow.com/questions/27051683/elastic-beanstalk-docker-app-not-updating-upon-deploy/27083854)
- [Elastic Beanstalk: Under the Hood](https://dev.bleacherreport.com/eb-under-the-hood-e7988736919f)
- [Elastic Beanstalk: Under the Hood 2  - Nginx](
  https://dev.bleacherreport.com/elastic-beanstalk-under-the-hood-2-nginx-89599e2179fb)


### Log Location on Amazon EC2 Instances

- /var/log/eb-activity.log
- /var/log/eb-commandprocessor.log
- /var/log/eb-docker/containers/eb-current-app/stdouterr.log
- /var/log/docker
- /var/log/docker-events.log
- /var/log/nginx/access.log
- /var/log/nginx/error.log
- /opt/elasticbeanstalk/tasks/taillogs.d/
- /opt/elasticbeanstalk/tasks/bundlelogs.d/
- /opt/elasticbeanstalk/tasks/publishlogs.d/
- /opt/python/log/

See also
- https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.cloudwatchlogs.html
- https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.logging.html


## HTTPS / SSL Certificate

You can use a certificate stored in IAM with Elastic Load Balancing load balancers and CloudFront distributions.

Otherwise create yours:

1. Your profile should have the following permissions
    1. `iam:UploadServerCertificate`
    1. `iam:ListServerCertificates`

```
CALL aws iam upload-server-certificate ^
  --server-certificate-name elastic-beanstalk-x509 ^
  --certificate-body file://example.com.crt ^
  --private-key file://example.com.key ^
  --certificate-chain file://intermediate.crt ^
  --profile k-eb-deploy

:: Show all certificates
CALL aws iam list-server-certificates --profile k-eb-deploy
```

For details see [Update a certificate to IAM](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/configuring-https-ssl-upload.html).


## Ignore files

If no .ebignore is present, but a .gitignore is, the EB CLI will ignore files
specified in the .gitignore. If an .ebignore file is present, the EB CLI will
not read the .gitignore.

For details see [EB .ebignore](
http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-configuration.html#eb-cli3-ebignore).