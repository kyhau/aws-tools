# EventBridge

Jump to
- [Useful Tools](#useful-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [EventBridge Pipes](#eventbridge-pipes)

---

## Useful Tools
- [aws/event-ruler](https://github.com/aws/event-ruler) - a Java library that allows matching Rules to Events. An event is a list of fields, which may be given as name/value pairs or as a JSON object


## Useful Articles and Blogs
- [Filtering events in Amazon EventBridge with wildcard pattern matching](https://aws.amazon.com/blogs/compute/filtering-events-in-amazon-eventbridge-with-wildcard-pattern-matching/), AWS, 2023-10-12


## EventBridge Pipes

```
Source -> Filtering (optional) --> Enrichment (optional) --> Target
```

- [Decoupling event publishing with Amazon EventBridge Pipes](https://aws.amazon.com/blogs/compute/decoupling-event-publishing-with-amazon-eventbridge-pipes/), AWS, 2023-07-11
- [Implementing architectural patterns with Amazon EventBridge Pipes](https://aws.amazon.com/blogs/compute/implementing-architectural-patterns-with-amazon-eventbridge-pipes/), AWS, 2023-02-09
- [Create Point-to-Point Integrations Between Event Producers and Consumers with Amazon EventBridge Pipes](https://aws.amazon.com/blogs/aws/new-create-point-to-point-integrations-between-event-producers-and-consumers-with-amazon-eventbridge-pipes/), AWS, 2022-12-01
- Patterns / Examples
    - [aws-samples/amazon-eventbridge-pipes-architectural-patterns](https://github.com/aws-samples/amazon-eventbridge-pipes-architectural-patterns)
    - [demo-trigger-stepfunctions-from-sqs](https://github.com/aws-samples/aws-stepfunctions-examples/blob/main/sam/demo-trigger-stepfunctions-from-sqs/template.yaml)

