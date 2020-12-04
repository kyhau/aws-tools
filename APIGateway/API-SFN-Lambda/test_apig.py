import requests

API_ID = "todo_apig_id"


def test_apig(stage):
    print(f"Testing {stage}...")

    # Start an execution
    resp = requests.post(f"https://{API_ID}.execute-api.ap-southeast-2.amazonaws.com/{stage}/execution")
    body = resp.json()
    sfn_exec_token = body.get("token")
    print(body if sfn_exec_token is None else f"Execution ID: {sfn_exec_token}")
    assert(sfn_exec_token)

    # Retrieve result from the execution
    payload = {"eid": sfn_exec_token}
    resp = requests.get(f"https://{API_ID}.execute-api.ap-southeast-2.amazonaws.com/{stage}/execution", params=payload)
    body = resp.json()
    print(f"Results: {body}")


for i in range(10):
    print("--------------------------------------------------------------------------------")
    print(f"Run {i}")

    test_apig(stage="v0")
