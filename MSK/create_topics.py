# See https://github.com/confluentinc/confluent-kafka-python
from confluent_kafka.admin import AdminClient, NewTopic

app_settings = {
    "bootstrap.servers": "TODO",
    "topics": [
         "topic1",
         "topic2",
     ],
}


a = AdminClient({"bootstrap.servers": app_settings["bootstrap.servers"]})

# Note: In a multi-cluster production scenario, it is more typical to use a replication_factor of 3 for durability.
new_topics = [NewTopic(topic, num_partitions=3, replication_factor=1) for topic in app_settings["topics"]]

# Call create_topics to asynchronously create topics. A dict of <topic,future> is returned.
fs = a.create_topics(new_topics)

# Wait for each operation to finish.
for topic, f in fs.items():
    try:
        f.result()  # The result itself is None
        print(f"Topic {topic} created")
    except Exception as e:
        print(f"Failed to create topic {topic}: {e}")
