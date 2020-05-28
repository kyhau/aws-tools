# MSK

Topics
- [Monitoring](#monitoring)
- [Kafka Log Retention and Cleanup Policies](#kafka-log-retention-and-cleanup-policies)
- [Mirror Maker 2](#mirror-maker-2)
- [Other References](#other-references)

### Monitoring
- [Monitoring an Amazon MSK Cluster (AWS Developer Guide)](https://docs.aws.amazon.com/msk/latest/developerguide/monitoring.html)
- [Monirtoring Consumer-Lag with LinkedIn Burrow](https://github.com/linkedin/Burrow)
- Monitoring with Prometheus
   - https://prometheus.io/
   - https://github.com/prometheus/jmx_exporter

### Kafka Log Retention and Cleanup Policies
- Ref-1: https://medium.com/@sunny_81705/kafka-log-retention-and-cleanup-policies-c8d9cb7e09f8, 2019-07-28
- Retention policies
  - Time-based:
     - `log.retention.ms`
     - `log.retention.minutes`
     - `log.retention.hours` (default, 168 = 7 days)
  - Size-based
      - `log.retention.bytes` (default -1)
- `log.cleanup.policy`
  - delete (default) - discard old segments when retention time or size limit has been reached.
  - compact 
     - Selectively remove records for each partition where we have a more recent update with the same primary key.
     - The log is guaranteed to have at least the last state for each key.
  - delete and compact
     - When both methods are enabled, capacity planning is simpler than when you only have compaction set for a
       topic. However, some use cases for log compaction depend on messages not being deleted by log cleanup, so
       consider whether using both is right for your scenario.

### Mirror Maker 2
- https://github.com/apache/kafka/tree/trunk/connect/mirror
- https://cwiki.apache.org/confluence/display/KAFKA/KIP-382%3A+MirrorMaker+2.0

### Other References
- https://sookocheff.com/post/kafka/kafka-in-a-nutshell/
- Kafka Python Client [confluentinc/confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python)
