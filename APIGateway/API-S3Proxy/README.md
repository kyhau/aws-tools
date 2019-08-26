# AWS-API-S3Proxy #

An API created with Amazon API gateway as an Amazon S3 Proxy.

## API

Documentation: [API](API.md) (generated with swagger2markdown)

## How to use

1. The DataService API uses [AWS_IAM](http://docs.aws.amazon.com/apigateway/latest/developerguide/permissions.html)
   for authorisation.

1. You can also [use Postman to call an API](http://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-use-postman-to-call-api.html)

1. See `deploy\tests\test_api.py` for examples of calling the DataService API.

## Architecture

```
 _____________     ____     
| API Gateway |-->| S3 |
|_____________|   |____|
```

1. A S3 bucket acts as the backend storage.
1. A API Gateway as S3 proxy.
1. Auth: AWS_IAM  


## Infrastructure

1. Use `DataService-IAM.template` to create IAM roles and policies.
1. Use `DataService-S3.template` to create S3 buckets (stage and prod) accessible by ApiGateway.
1. Use `deploy\deploy_and_test_api_methods.bat|sh` to reimport the API Swagger file to AWS and run method-level tests.
1. Use `deploy\deploy_and_test_api_stage.bat|sh` to deploy a stage of the DataService API and run stage-level tests.


#### Running method-level tests

Set environment variables:

- aws_access_key_id= (TODO)
- aws_secret_access_key= (TODO)
- api_stage=[stage|prod]

```bash
cd aws/deploy
./deploy_and_test_api_methods.sh
```

#### Running stage-level tests

Set environment variables (see above).

```bash
cd deploy
./deploy_and_test_api_stage.sh {stage_name}
```


#### To generate API.md

```cmd
pip install swagger2markdown
swagger2markdown -i DataServiceAPI_swagger.json -o API.md
```

#### References

1. [S3 Bucket Restriction](http://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html)
1. [S3 Transfer Acceleration](http://docs.aws.amazon.com/AmazonS3/latest/dev/transfer-acceleration.html)

