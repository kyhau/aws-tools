# standards-controls-helper

This script aims to support regularly check any new standards controls available in Security Hub, as well as check if any unexpected changes not under source control.

This script supports
- retrieving current Standard Controls from AWS account and generate a summary for comparison.
- taking a json file containing the expected standard controls to be enabled/disabled.

Example file content:
```
{
    "ACM.1": {
        "Regions": {
            "ap-south-1": {
                "ControlStatus": "ENABLED",
                "DisabledReason": ""
            },
            "ap-southeast-2": {
                "ControlStatus": "DISABLED",
                "DisabledReason": "Not Required ..."
            },
            ...
    }
}
```


## Usage

First, install requirements

```bash
pip install -r requirements.txt
```

### To generate summary and compare AWS FSBP standards controls for a list of regions

```bash
python securityhub_standards_controls_helper.py summary \
    --subscription aws-foundational-security-best-practices-v-1.0.0 \
    --regions "ap-southeast-2,us-east-1,..."
```

### To generate summary and compare CIS standards controls for a list of regions

```bash
python securityhub_standards_controls_helper.py summary \
    --subscription cis-aws-foundations-benchmark-v-1.2.0 \
    --regions "ap-southeast-2,us-east-1,..."
```

### To update AWS Foundational Security Best Practices standards controls of a region

Use `--dry-run` to see the potential changes.

```bash
python securityhub_standards_controls_helper.py update \
    --input-file aws-foundational-security-best-practices-v-1.0.0.json \
    --subscription aws-foundational-security-best-practices-v-1.0.0 \
    --region "ap-southeast-2"
```

### To update CIS AWS Foundations Benchmark standards controls of a regions

Use `--dry-run` to see the potential changes.

```bash
python securityhub_standards_controls_helper.py update \
    --input-file cis-aws-foundations-benchmark-v-1.2.0.json \
    --subscription cis-aws-foundations-benchmark-v-1.2.0 \
    --region "ap-southeast-2"
```
