import click
import logging
import yaml
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)

# See https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings.html#guardduty_findings-severity
severity_defaults = {
    "high": 7,
    "medium": 4,
    "low": 0,
}


class Helper(AwsApiHelper):
    def __init__(self, finding_id):
        super().__init__()
        self._finding_id = finding_id

    @staticmethod
    def list_detectors(client):
        ret = []
        for page in  client.get_paginator("list_detectors").paginate():
            l = page.get("DetectorIds")
            if l is not None:
                ret.extend(l)
        return ret

    @staticmethod
    def create_list_findings_params(finding_type, severity, num):
        params = {
            "FindingCriteria": {
                "Criterion": {
                    "severity": {"Gte": severity_defaults[severity]},
                }
            },
            "SortCriteria": {"AttributeName": "createdAt", "OrderBy": "DESC"},
            "MaxResults": num,
        }
        if finding_type:
            params["Criterion"]["type"] = {"Eq": [finding_type]}
        return params

    def process_request(self, session, account_id, region, kwargs):
        client = session.client("guardduty", region_name=region)
    
        detector_ids = Helper.list_detectors(client)
        if not detector_ids:
            logging.info(f"No detector is found. Skipped {account_id} {region}.")
            return
    
        for detector_id in detector_ids:
            kwargs["DetectorId"] = detector_id
            finding_ids = [self._finding_id] if self._finding_id else \
                client.list_findings(**kwargs).get("FindingIds", [])
            
            findings = client.get_findings(DetectorId=detector_id, FindingIds=finding_ids).get("Findings", [])
            for finding in findings:
                print("--------------------------------------------------------------------------------")
                print(yaml.dump(finding))
        
            if self._finding_id and findings:
                return findings[0]


@click.command()
@click.option("--findingid", "-i", help="Finding ID.")
@click.option("--num", "-n", default=5, show_default=True, help="Number of records returned for each detector/account/region.")
@click.option("--findingtype", "-t", help="Recon Finding Type (e.g. Recon:IAMUser/UserPermissions).")
@click.option("--severity", "-s", default="high", show_default=True, help="Severity: high, medium, low.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(findingid, num, findingtype, severity, profile, region):
    kwargs = Helper.create_list_findings_params(findingtype, severity, num)
    Helper(findingid).start(profile, region, "guardduty", kwargs)


if __name__ == "__main__":
    main()
