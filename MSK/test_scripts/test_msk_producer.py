# See https://docs.confluent.io/current/clients/confluent-kafka-python/index.html#pythonclient-producer
# See https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-python3-boto3/
from confluent_kafka import Producer
from faker import Faker
from faker.providers import internet
import json
import uuid

app_settings = {
    "bootstrap.servers": "TODO",
    "group.id": "TODO",
    "topic": "TODO",
}

p = Producer({"bootstrap.servers": app_settings["bootstrap.servers"]})
fake = Faker("en_AU")
fake.add_provider(internet)


def generate_random_data():
    return {
        "id": str(uuid.uuid4()),
        "hostname": fake.hostname(),
        "dst": fake.ipv4(),
    }


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is None:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
    else:
        print(f"Message delivery failed: {err}")


for i in range(0, 1000):
    x = json.dumps(generate_random_data())
    print(x)

    # Trigger any available delivery report callbacks from previous produce() calls
    p.poll(0)

    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    p.produce(app_settings["topic"], x.encode("utf-8"), callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()
