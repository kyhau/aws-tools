from abc import ABC, abstractmethod
import click
from datetime import datetime, time, timedelta
import logging
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class MainHelper(AwsApiHelper):
    def __init__(self, inspector_helper_clz):
        super().__init__()
        self._inspector_helper_clz = inspector_helper_clz
        
    def process_request(self, session, account_id, region, kwargs):
        self._inspector_helper_clz(session, region, account_id).process_request()


class InspectorHelper(ABC):
    def __init__(self, session, region, account_id):
        self._client = session.client("inspector", region_name=region)
        self._region = region
        self._account_id = account_id
    
    @abstractmethod
    def process_response(self, item):
        pass

    @abstractmethod
    def get_assessment_run_details(self, item):
        pass
    
    def find_latest_assessment_run_arn(self, days):
        """Find recent assessment runs in the last N days"""
        begin_date = datetime.combine(datetime.today(), time.min) - timedelta(days)
        filter = {"startTimeRange": {"beginDate": begin_date}, "states": ["COMPLETED"]}
        assessment_run_arns = []
        for page in self._client.get_paginator("list_assessment_runs").paginate(filter=filter).result_key_iters():
            assessment_run_arns.extend(page)
    
        # Find latest assessment run's ARN
        arn, latest_date = None, None
        while len(assessment_run_arns) > 0:
            # Note that assessmentRunArns supports max 10 items
            check_arns = assessment_run_arns[0:min(10, len(assessment_run_arns))]
            for item in self._client.describe_assessment_runs(assessmentRunArns=check_arns)["assessmentRuns"]:
                if latest_date is None or latest_date < item["createdAt"]:
                    arn, latest_date = item["arn"], item["createdAt"]
            assessment_run_arns = assessment_run_arns[10:]
        return arn, latest_date

    def process_request(self):
        # Find recent assessment runs in the last 60 days
        arn, latest_date = self.find_latest_assessment_run_arn(days=60)
        ret = []
        if arn is not None:
            for item in self.get_assessment_run_details(arn):
                data = self.process_response(item)
                if data:
                    data.update({"AccountId": self._account_id, "Region": self._region, "RunDate": str(latest_date)})
                    print(data)
                    ret.append(data)
        return ret


class InspectorFindingsHelper(InspectorHelper):
    def __init__(self, session, region, account_id):
        super().__init__(session, region, account_id)

    def process_response(self, item):
        return {
            "Id": item["assetAttributes"]["agentId"],
            "FindingArn": item["arn"],
            "FindingId": item["id"],
            "NumericSeverity": item["numericSeverity"],
            "Severity": item["severity"],
        }

    def get_assessment_run_details(self, run_arn):
        params = {"assessmentRunArns": [run_arn], "filter": {"severities": ["High"]}}
        findings = []
        for page in self._client.get_paginator("list_findings").paginate(**params).result_key_iters():
            findings.extend(page)
    
        while len(findings) > 0:
            # Note that findingArns supports max 100 items
            check_findings = findings[0:min(100, len(findings))]
            for item in self._client.describe_findings(findingArns=check_findings)["findings"]:
                yield item
            findings = findings[100:]


class InspectorAgentsHelper(InspectorHelper):
    def process_response(self, item):
        return {
            "Id": item["agentId"],
        }

    def get_assessment_run_details(self, run_arn):
        params = {
            "assessmentRunArn": run_arn,
            "filter": {"agentHealths": ["HEALTHY"], "agentHealthCodes": ["HEALTHY", "IDLE", "RUNNING"]},
        }
        for page in self._client.get_paginator("list_assessment_run_agents").paginate(**params).result_key_iters():
            for item in page:
                yield item


@click.group(help="A Inspector helper for retrieving results of the last assessment run")
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region; use 'all' for all regions")
@click.pass_context
def main_cli(ctx, profile, region):
    ctx.obj = {"profile": profile, "region": region}


@main_cli.command(help="Retrieve the agents (instance IDs) of the last assessment run")
@click.pass_context
def list_agents(ctx):
    MainHelper(InspectorAgentsHelper).start(ctx.obj["profile"], ctx.obj["region"], "inspector")


@main_cli.command(help="Retrieve the findings of the last assessment run")
@click.pass_context
def list_findings(ctx):
    MainHelper(InspectorFindingsHelper).start(ctx.obj["profile"], ctx.obj["region"], "inspector")


if __name__ == "__main__":
    main_cli(obj={})
