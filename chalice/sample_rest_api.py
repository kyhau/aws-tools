"""
$ chalice deploy
...
https://endpoint/dev

$ curl https://endpoint/api
{"hello": "world"}
"""
from chalice import Chalice

app = Chalice(app_name="helloworld")


# You can create Rest APIs:
@app.route("/")
def index():
    return {"hello": "world"}
