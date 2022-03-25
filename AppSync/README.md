# AppSync

AppSync is a data aggregator serving GraphQL query results. With AppSync, you can define the query schemas and "resolvers" for the data feeds. It also has the power feature of allowing real time subscriptions via the Apollo JS library (SDK), so apps can have live changes when upstream data changes as well as offline mode.

AppSync is a fully managed service that makes it easy to develop GraphQL APIs by handling the heavy lifting of securely connecting to data sources like AWS DynamoDB, Lambda, and more. Adding caches to improve performance, subscriptions to support real-time updates, and client-side data stores that keep off-line clients in sync are just as easy. Once deployed, AWS AppSync automatically scales your GraphQL API execution engine up and down to meet API request volumes. ([Source](https://aws.amazon.com/appsync/))

- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
- [Useful Diagrams](#useful-diagrams)

---
## Useful Libs and Tools

- [aws-mobile-appsync-sdk-android](https://github.com/awslabs/aws-mobile-appsync-sdk-android) -  Android SDK for AWS AppSync. 
- [aws-mobile-appsync-sdk-js](https://github.com/awslabs/aws-mobile-appsync-sdk-js) -  JavaScript library files for Offline, Sync, Sigv4. includes support for React Native
- [aws-mobile-appsync-sdk-ios](https://github.com/awslabs/aws-mobile-appsync-sdk-ios) -  iOS SDK for AWS AppSync


---
## Useful Articles and Blogs

- How do Amplify and AppSync work together?
    - They have both been designed with each other in mind. A GraphQL API can be created in the AppSync Console, or created with Amplify for use by AppSync. The [AppSync documentation](https://docs.aws.amazon.com/appsync/latest/devguide/building-a-client-app.html#aws-appsync-building-a-client-app) recommends using Amplify if building a complete application.
- [Apollo GraphQL Federation with AWS AppSync](https://aws.amazon.com/blogs/mobile/federation-appsync-subgraph/), AWS, 2022.02
- [Direct Lambda Resolvers: AWS AppSync GraphQL APIs without VTL](https://aws.amazon.com/blogs/mobile/appsync-direct-lambda/), AWS, 2020.08

---
## Useful Diagrams

Amplify and AppSync ([Source](https://techroads.org/what-are-aws-amplify-and-appsync-and-should-i-use-them/))

![appsync-amplify](https://techroads.org/content/images/2020/08/appsync-amplify-o.jpg)
