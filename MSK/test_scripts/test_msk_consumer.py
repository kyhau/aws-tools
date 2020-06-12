# See https://docs.confluent.io/current/clients/confluent-kafka-python/index.html#pythonclient-consumer
# See https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-python3-boto3/
from confluent_kafka import Consumer, KafkaError

app_settings = {
    "bootstrap.servers": "TODO",
    "group.id": "TODO",
    "topic": "TODO",
}

c = Consumer({
    "bootstrap.servers": app_settings["bootstrap.servers"],
    "group.id": app_settings["group.id"],
    "auto.offset.reset": "latest",    # smallest, earliest, beginning, largest, latest, end, error
})

c.subscribe([app_settings["topic"]])

while True:
    msg = c.poll(0.1)

    if msg is None:
        print("No Data")
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue

    print(f"Received message: {msg.value().decode('utf-8')}")

c.close()