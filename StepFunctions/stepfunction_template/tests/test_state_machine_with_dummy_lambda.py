import json
import time
import uuid

# Maximum number of loops allowed before failing the test
MAX_LOOP_COUNT_TO_BREAK = 15


def run_test_case(sfn_client, sfn_arn, test_data_dict, start_tier_id="1"):
    resp = sfn_client.start_execution(
        stateMachineArn=sfn_arn,
        name=str(uuid.uuid4()),
        input=json.dumps({
            "tier_id": start_tier_id,
            "test_case_data": test_data_dict
        })
    )
    assert resp["ResponseMetadata"]["HTTPStatusCode"] == 200

    execution_arn = resp["executionArn"]
    print("Started state machine execution: {}".format(execution_arn))

    resp = None
    status = "RUNNING"
    cnt = 0

    while status not in ["SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"]:

        # Raise exception if looping many times
        if cnt == MAX_LOOP_COUNT_TO_BREAK:
            raise Exception("{} loops already, something got stuck?".format(MAX_LOOP_COUNT_TO_BREAK))
        cnt += 1

        resp = sfn_client.describe_execution(executionArn=execution_arn)
        status = resp["status"]
        time.sleep(1)

    return resp


def test_all_good(sfn_client, sfn_arn):
    """Test case: all good
    """
    test_case_data = {
        # Tier 1 is fine and ends with `completed`
        "1": {
            "start_job": {"end_state": "running_job"},
            "check_progress": {"iterations": 1, "end_state": "completed"}
        },
        # Tier 2 has 2 iterations and and ends with `completed`
        "2": {
            "start_job": {"end_state": "running_job"},
            "check_progress": {"iterations": 2, "end_state": "completed"}
        }
    }
    resp = run_test_case(sfn_client, sfn_arn, test_case_data)
    assert resp["status"] == "SUCCEEDED"


def test_cancel_at_job_start_at_tier_1(sfn_client, sfn_arn):
    """The job is cancelled even before the first tier is started.
    """
    test_case_data = {
        # The job is cancelled even before the first tier is started
        "1": {
            "start_job": {"end_state": "cancelled"},
            "check_progress": {"iterations": 1, "end_state": "cancelled"}
        }
    }
    resp = run_test_case(sfn_client, sfn_arn, test_case_data)

    # Job has been cancelled, the state machine ends in PASS state.
    assert resp["status"] == "SUCCEEDED"

    # 'output' returns status == "cancelled.
    ret = json.loads(resp["output"])
    assert ret["message"] == "Cancelled"
    assert ret["status"] == "cancelled"


def test_cancel_at_check_progress_at_tier_1(sfn_client, sfn_arn):
    """The job is cancelled after it is started.
    """
    test_case_data = {
        "1": {
            "start_job": {"end_state": "running_job"},
            "check_progress": {"iterations": 2, "end_state": "cancelled"}
        }
    }
    resp = run_test_case(sfn_client, sfn_arn, test_case_data)

    # Job has been cancelled, the state machine ends in PASS state.
    assert resp["status"] == "SUCCEEDED"

    # 'output' returns status == "cancelled.
    ret = json.loads(resp["output"])
    assert ret["message"] == "Cancelled"
    assert ret["status"] == "cancelled"


def test_terminate_at_job_start_at_tier_2(sfn_client, sfn_arn):
    """The job is terminated when starting job at tier 2
    """
    test_case_data = {
        # Tier 1 is fine and ends with `completed`
        "1": {
            "start_job": {"end_state": "running_job"},
            "check_progress": {"iterations": 1, "end_state": "completed"}
        },
        # Tier 2 has 1 iteration and and ends with `terminated`
        "2": {
            "start_job": {"end_state": "terminated"},
            "check_progress": {"iterations": 1, "end_state": "terminated"}
        }
    }
    resp = run_test_case(sfn_client, sfn_arn, test_case_data)
    assert resp["status"] == "FAILED"


def test_terminate_at_check_progress_at_tier_2(sfn_client, sfn_arn):
    """The job is terminated after job started at tier 2
    """
    test_case_data = {
        # Tier 1 is fine and ends with `completed`
        "1": {
            "start_job": {"end_state": "running_job"},
            "check_progress": {"iterations": 1, "end_state": "completed"}
        },
        # Tier 2 has 1 iteration and and ends with `terminated`
        "2": {
            "start_job": {"end_state": "running_job"},
            "check_progress": {"iterations": 1, "end_state": "terminated"}
        }
    }
    resp = run_test_case(sfn_client, sfn_arn, test_case_data)
    assert resp["status"] == "FAILED"
