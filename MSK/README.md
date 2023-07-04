# MSK

Topics
- [MSK Serverless](#msk-serverless)
- [Monitoring](#monitoring)
- [Kafka Log Retention and Cleanup Policies](#kafka-log-retention-and-cleanup-policies)
- [Mirror Maker 2](#mirror-maker-2)
- [Other References](#other-references)

---
### MSK Serverless
- Limitations and things to consider - [The Pro’s and Con’s of using AWS MSK Serverless](https://digio.com.au/learn/blog/the-pros-and-cons-of-using-aws-msk-serverless/), Sinnappu J., 2022-07-18

### Monitoring
- [Monitoring an Amazon MSK Cluster (AWS Developer Guide)](https://docs.aws.amazon.com/msk/latest/developerguide/monitoring.html)
- [Monirtoring Consumer-Lag with LinkedIn Burrow](https://github.com/linkedin/Burrow)
- Monitoring with Prometheus
   - https://prometheus.io/
   - https://github.com/prometheus/jmx_exporter

### Kafka Log Retention and Cleanup Policies
- Ref-1: https://docs.aws.amazon.com/msk/latest/developerguide/msk-configuration-properties.html
- Ref-2: https://medium.com/@sunny_81705/kafka-log-retention-and-cleanup-policies-c8d9cb7e09f8, 2019-07-28
- Ref-3: https://www.allprogrammingtutorials.com/tutorials/configuring-messages-retention-time-in-kafka.php
- See example [mskconfig.properties](mskconfig.properties)

### Mirror Maker 2
- https://github.com/apache/kafka/tree/trunk/connect/mirror
- https://cwiki.apache.org/confluence/display/KAFKA/KIP-382%3A+MirrorMaker+2.0

### Other References
- https://sookocheff.com/post/kafka/kafka-in-a-nutshell/
- Kafka Python Client [confluentinc/confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python)
