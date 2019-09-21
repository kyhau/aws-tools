import logging

# Set debugging configs
logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s %(message)s")
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

# Default assumptions
DEFAULT_WAIT_TIME_SECS = 1


# Variables referenced in StateMachineDefinition.json (+ addition vars for unit tests)
class SFN_VAR:
    JOB_ID = "job_id"
    MESSAGE = "message"
    PROJECT_ID = "project_id"
    STATUS = "status"
    TIER_ID = "tier_id"
    WAIT_TIME = "wait_time"
    # For unit tests only
    ITERATIONS = "iterations"
    TEST_CASE_DATA = "test_case_data"


###############################################################################
# State machine's tasks

def start_job(state_data):
    """
    Start a new job for the current tier
    """
    logging.debug("start_job: tier({})".format(state_data[SFN_VAR.TIER_ID]))
    dummy_job_id = "dummy_job_id_{}".format(state_data[SFN_VAR.TIER_ID])

    test_case_data = state_data[SFN_VAR.TEST_CASE_DATA]
    status = test_case_data[state_data[SFN_VAR.TIER_ID]]["start_job"]["end_state"]

    state_data[SFN_VAR.STATUS] = status
    state_data[SFN_VAR.ITERATIONS] = 1

    if status == "cancelled":
        state_data[SFN_VAR.MESSAGE] = "Cancelled"

    elif status == "terminated":
        state_data[SFN_VAR.JOB_ID] = dummy_job_id
        state_data[SFN_VAR.MESSAGE] = "Caught error at start_job"

    else:
        state_data[SFN_VAR.JOB_ID] = dummy_job_id
        state_data[SFN_VAR.STATUS] = "running_job"

    state_data[SFN_VAR.WAIT_TIME] = DEFAULT_WAIT_TIME_SECS
    return state_data


def update_state_from_progress(state_data):
    """
    Check the progress of the current tier and process the job data and status accordingly.
    """
    test_case_data = state_data[SFN_VAR.TEST_CASE_DATA]
    tier_id = state_data[SFN_VAR.TIER_ID]

    # Compare iteration
    curr_iter = state_data[SFN_VAR.ITERATIONS]
    expected_iter = test_case_data[tier_id]["check_progress"]["iterations"]

    logging.debug("check_progress: tier({}/{}), iter({}/{})".format(
        state_data[SFN_VAR.TIER_ID], len(test_case_data), curr_iter, expected_iter
    ))

    if expected_iter == curr_iter:
        # Reached last expected iteration
        state_data[SFN_VAR.STATUS] = test_case_data[tier_id]["check_progress"]["end_state"]

        if state_data[SFN_VAR.STATUS] == "cancelled":
            state_data[SFN_VAR.MESSAGE] = "Cancelled"

        # Check if more tier
        if len(test_case_data) == int(tier_id):
            state_data[SFN_VAR.TIER_ID] = "None"
            state_data[SFN_VAR.JOB_ID] = None
        else:
            state_data[SFN_VAR.TIER_ID] = str(int(tier_id) + 1)
    else:
        curr_iter += 1

    state_data[SFN_VAR.ITERATIONS] = curr_iter
    state_data[SFN_VAR.WAIT_TIME] = DEFAULT_WAIT_TIME_SECS
    return state_data


def lambda_handler(event, context):
    logging.debug("##################################################################")

    state_data = {v: event.get(v) for k, v in SFN_VAR.__dict__.items() if not k.startswith("__")}
    state_data[SFN_VAR.WAIT_TIME] = DEFAULT_WAIT_TIME_SECS

    if state_data[SFN_VAR.JOB_ID] is None:
        return start_job(state_data)

    return update_state_from_progress(state_data)
