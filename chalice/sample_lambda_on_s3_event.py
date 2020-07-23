from chalice import Chalice

app = Chalice(app_name="helloworld")


# Whenever an object is uploaded to 'mybucket'
# this lambda function will be invoked.
@app.on_s3_event(bucket='mybucket')
def handler(event):
    print("Object uploaded for bucket: %s, key: %s"
          % (event.bucket, event.key))
