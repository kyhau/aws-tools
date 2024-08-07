# AWS SageMaker

Jump to
- [Useful Libs and Tools](#useful-libs-and-tools)
- [SageMaker Studio](#sagemaker-studio)
- [Neuron](#neuron)

---

## Useful Libs and Tools

- [sagemaker-python-sdk](https://github.com/aws/sagemaker-python-sdk) - AWS SageMaker SDK (Python)
- [sagemaker-studio-image-build-cli](https://github.com/aws-samples/sagemaker-studio-image-build-cli)
- [amazon-sagemaker-examples](https://github.com/aws/amazon-sagemaker-examples)


## SageMaker Studio

- Setup
- Data processing
    - SageMaker Data Wrangler
    - SageMaker Feature Store (Offline or Online)
        - Train models with Offiine
        - Performs low-latency inferecing with Online
        - There are three main ways to store features in Amazon SageMaker:
            1. Using Amazon SageMaker Feature Store as an Amazon SageMaker Data Wrangler destination after preprocessing steps have been completed and features have been added.
            2. Exporting a notebook from SageMaker Data Wrangler that runs through feature definition, feature group creation, and ingestion of data into SageMaker Feature Store.
            3. Using the SageMaker Python SDK in a custom notebook that runs through feature definition, feature group creation, and ingestion of data into SageMaker Feature Store.
- Model development
    - SageMaker Experiments (similar to MLflow)
        - Use Amazon SageMaker built-in algorithms or pretrained models ([link](https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html))
    - SageMaker fully-managed MLflow
    - SageMaker Debugger
    - SageMaker Operators for Kubernetes ([link](https://docs.aws.amazon.com/sagemaker/latest/dg/kubernetes-sagemaker-operators.html))
    - SageMaker Estimator - to run a training job
    - Hyperparameter tuning ([link](https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-how-it-works.html))
    - SageMaker Autopilot
        - [Training modes and algorithm support](https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-model-support-validation.html)
    - SageMaker Clarify - to detect bias in pre-training data and post-training models and access explainability reports.
        - [Learn how Amazon SageMaker Clarify helps detect bias](https://aws.amazon.com/blogs/machine-learning/learn-how-amazon-sagemaker-clarify-helps-detect-bias/), AWS, 2022-09-01
    - SageMaker JumpStart
        - Supported foundation models 220+
- Deployment and Inference
    - Model registry
    - SageMaker Pipelines - [SageMaker Model Building Pipelines steps](https://docs.aws.amazon.com/sagemaker/latest/dg/build-and-manage-steps.html)
    - SageMaker hosting services
    - Production endpoint testing strategies
    - Model Cards -  when they want to publish their model in public
- Monitoring


## Neuron
- AWS Neuron samples https://awsdocs-neuron.readthedocs-hosted.com/en/latest/general/quick-start/github-samples.html
