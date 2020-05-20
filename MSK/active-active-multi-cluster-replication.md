# Active/Active Multi-Cluster Replication with MirrorMaker 2

References:
- [1] [KIP-382: MirrorMaker 2.0 (Kafka Improvement Proposals)](
https://cwiki.apache.org/confluence/display/KAFKA/KIP-382%3A+MirrorMaker+2.0)
- [2] [Jira ticket of KIP-382: MirrorMaker 2.0](https://issues.apache.org/jira/browse/KAFKA-7500)
- [3] [Kafka MirrorMaker 2 Readme](https://github.com/apache/kafka/tree/trunk/connect/mirror)
- [4] [A look inside Kafka Mirrormaker 2](https://blog.cloudera.com/a-look-inside-kafka-mirrormaker-2)


1. In MirrorMaker 2, it’s consumer’s job to aggregate across multiple clusters. [1]
   - Downstream consumers can aggregate across multiple clusters by subscribing to the local topic and all
     corresponding remote topics, e.g. topic1, us-west.topic1, us-east.topic1… or by using a regex subscription. 
   - Topics are never merged or repartitioned within the connector. Instead, merging is left to the consumer. 
     This is in contrast to MirrorMaker, which is often used to merge topics from multiple clusters into a single
     aggregate cluster. 
   - Likewise, a consumer can always elect not to aggregate by simply subscribing to the local topic only, e.g. topic1.
     This approach eliminates the need for special purpose aggregation clusters without losing any power or flexibility.

2. How do you go about switching a consumer from one cluster to another, say in the case of a total cluster failure? [2]
   - The key is the RemoteClusterUtils.translateOffsets() method, which works for both failover and fallback scenarios.
   - Failover
     - Two clusters K1 and K2 and configured MM2 replication for TOPIC1. The consumer group is "TOPIC_GROUP".
     - To start with K1 cluster is active and "TOPIC_GROUP" is actively consuming TOPIC1 from K1.
     - Now, the failover to K2 is triggered and the "TOPIC_GROUP" starts consuming from K2. 
       RemoteClusterUtils.translateOffsets is used to seek to the correct offset for K1.TOPIC1.
     - During failover, there were #N messages in TOPIC1 in K1 that were not consumed by "TOPIC_GROUP" but were 
       replicated in K2 and consumed by "TOPIC_GROUP" in K2 as K1.TOPIC1.
   - Fallback
     - When K1 comes back online, you can "failback" from K2 to K1 once a checkpoint for TOPIC_GROUP is emitted
       upstream to K1. The checkpoint will have offsets for TOPIC1 on K1 (translated from K1.TOPIC1 on K2). 
       You can then seek() to skip over the records TOPIC_GROUP already consumed in K2.
     - The tricky part here is that you need to make sure MM2 is configured to emit checkpoints both from K1->K2 and
       K2->K1. Configure the whitelists like:

            K1->K2.topics = TOPIC1, K2.TOPIC1
            K2->K1.topics = TOPIC1, K1.TOPIC1
            K1->K2.groups = TOPIC_GROUP
            K2->K1.groups = TOPIC_GROUP
      - Otherwise, you won't see checkpoints for TOPIC1 going from K2 to K1.

3. More details about RemoteClusterUtils.translateOffsets() [2]
   - The key is the RemoteClusterUtils.translateOffsets() method. This consumes from the checkpoint topic (not the
     offset-sync topic directly), which has both upstream and downstream offsets for each consumer group. 
     The downstream offsets are calculated based on the offset-sync stream, of course, but MirrorCheckpointConnector
     does the translation for you. This makes the translateOffsets() method rather straightforward – it just finds the
     most recent checkpoint for a given group.
   - The translateOffsets() method works both ways: you can translate from a source topic ("topic1") to a remote topic
     ("us-east.topic1") and vice versa, which means your failover and failback logic is identical. In both cases you
     just migrate all your consumer groups from one cluster to another.
   - Also note that migration only requires information that is already stored on the target cluster (the checkpoints),
     so you do not need to connect to a failed cluster in order to failover from it. Obviously that would defeat the
     purpose!
   - Based on translateOffsets(), you can do several nifty things wrt failover/failback, e.g. build scripts that
     bulk-migrate consumer groups from one cluster to another, or add consumer client logic that automatically failover
     to a secondary cluster as needed.
   - In the former case, you can use kafka-consumer-groups.sh to "reset offsets" to those returned by
     translateOffsets(). This will cause consumer state to be transferred to the target cluster, in effect. 
     In the latter, you can use translateOffsets() with KafkaConsumer.seek().
