import logging
import requests
import time
from decimal import Decimal

# C:\Workspace\bitbucket\orca\aws\apigateway\Orca\tests\conftest.py


@pytest.fixture(scope="session")
def null_solver_orca_input_zip():
    dir_name = join(tempfile.gettempdir(), f"{UNIT_TEST_LABEL}_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    makedirs(dir_name)

    # Create input.json
    input_data = {
        "timeout": 1,  # This will make null_solver_orca finish running very quickly
        "expected_return_code": 0
    }
    input_json_file = join(dir_name, "input.json")
    with open(input_json_file, "w") as f:
        json.dump(input_data, f)

    # Create input.zip containing input.json
    input_zip_file = join(dir_name, "input.zip")
    with ZipFile(input_zip_file, "w") as fz:
        fz.write(input_json_file, arcname="input.json")

    yield input_zip_file

    try:
        if exists(dir_name):
            rmtree(dir_name)
    except Exception as e:
        print("Failed to delete {}".format(dir_name))


def test_s3_server_side_encryption_enabled(test_helper, new_job_data_a, null_solver_orca_input_zip):
    """
    Test starting a new job successfully.

    :param test_helper: TestApiHelper instance
    :param new_job_data_a: sample new job's data
    :param null_solver_orca_input_zip:  file name with path of the sample input.zip for null_solver_orca
    """
    tool_name = new_job_data_a["tool_name"]
    tool_version = new_job_data_a["tool_version"]

    # Create new job and retrieve job_id
    response = test_helper.job_post(tool_name=tool_name, req_body_json=new_job_data_a)

    actual_body = test_helper.get_response_body(response)
    job_id = actual_body["job_id"]

    # Upload input.zip
    logging.info("Uploading input.zip")
    input_url = actual_body["input_url"]
    with open(null_solver_orca_input_zip, "rb") as data:
        response = requests.put(input_url, data=data)
        assert test_helper.check_response_code(response, expected_code=200)

    # Confirm AES256 is the Server-side encryption algorithm used when storing this object in S3
    object = test_helper.s3_resource.Object(test_helper.s3_orca_bucket, f"{job_id}/input.zip")
    assert object.server_side_encryption == "AES256"

    # Start running a job
    response = test_helper.job_start(tool_name=tool_name, job_id=job_id)
    assert test_helper.check_response_code(response, expected_code=200)

    # Retrieve the response body
    actual_body = test_helper.get_response_body(response)
    assert actual_body["job_state"] == "RUNNING"

    # Poll for status to change from RUNNING
    cnt = 0
    while actual_body["job_state"] == "RUNNING" and cnt < 20:
        # Wait for a moment for the job to finish running on its own
        logging.info("Sleeping for 5 seconds between status checks...")
        time.sleep(5)
        response = test_helper.job_get(tool_name=tool_name, job_id=job_id)
        actual_body = test_helper.get_response_body(response)
        cnt += 1
    assert actual_body["job_state"] == "COMPLETED"

    # Confirm AES256 is the Server-side encryption algorithm used when storing this object in S3
    object = test_helper.s3_resource.Object(test_helper.s3_orca_bucket, f"{job_id}/output.zip")
    assert object.server_side_encryption == "AES256"

    # Download output.zip
    logging.info("Downloading output.zip")
    output_url = actual_body["output_url"]
    response = requests.get(output_url)
    assert test_helper.check_response_code(response, expected_code=200)

    # Make a direct non-API call to the Jobs DynamoDB table to inspect the final item is as expected before it's removed
    # Note: The items corresponding to these API tests are cleaned out of the DynamoDB tables when the corresponding
    # fixtures are teared down (i.e. they only exist during the lifetime of the test and cannot be inspected manually)
    logging.info("Inspecting the final item in the Jobs DynamoDB table")
    job_item = test_helper.ddb_jobs_table.get_item(Key={"job_id": job_id}).get("Item")

    # Ensure the application can set its own custom application data during the RUNNING state
    # See null_solver_orca/main.py
    assert job_item["application"] == {"organisation": "Biarri Networks", "points": Decimal("0.25")}
    assert job_item["data_source"] is False
    assert job_item["job_id"] == job_id
    assert job_item["job_state"] == "COMPLETED"
    assert job_item["mode"] == "A"
    assert job_item["tool_name"] == tool_name
    assert job_item["tool_version"] == tool_version
    assert job_item["user_id"] == test_helper.username

    # These fields have content unique to the job/instance (e.g. timestamps), so just check it's non-empty
    assert job_item["actual_start_time"]
    assert job_item["actual_stop_time"]
    assert job_item["request_start_time"]
    assert job_item["request_stop_time"]
    assert job_item["task_id"]

    assert len(job_item) == 13