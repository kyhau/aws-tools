from chalice import Chalice

app = Chalice(app_name="helloworld")


# Invoke this lambda function whenever a message
# is sent to the ``my-queue-name`` SQS queue.
@app.on_sqs_message(queue='my-queue-name')
def handler(event):
    for record in event:
        print("Message body: %s" % record.body)