
### Decoding Encoded authorization failure message

When you see an Encoded authorization failure message like the one below:
([Ref](https://docs.aws.amazon.com/STS/latest/APIReference/API_DecodeAuthorizationMessage.html))

```
A client error (UnauthorizedOperation) occurred when calling the RunInstances operation: 
You are not authorized to perform this operation. Encoded authorization failure message:
FR4gBD7Ph0...
```

You can run the command below to decode the encoded authorization message. 
You will need to have access to `sts:DecodeAuthorizationMessage`.

```
$ aws sts decode-authorization-message --encoded-message FR4gBD7Ph0...
```
