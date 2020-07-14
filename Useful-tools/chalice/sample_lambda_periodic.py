from chalice import Chalice, Rate

app = Chalice(app_name="helloworld")


# Automatically runs every 5 minutes
@app.schedule(Rate(5, unit=Rate.MINUTES))
def periodic_task(event):
    return {"hello": "world"}