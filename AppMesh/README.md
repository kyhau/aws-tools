# App Mesh

See also https://www.nginx.com/blog/what-is-a-service-mesh/
- A service mesh is a configurable, low‑latency infrastructure layer designed to handle a high volume of network‑based interprocess communication among application infrastructure services using APIs.
- A service mesh ensures that communication among containerized and often ephemeral application infrastructure services is fast, reliable, and secure.
- The mesh provides critical capabilities including service discovery, load balancing, encryption, observability, traceability, authentication and authorization, and support for the circuit breaker pattern.

### Useful Links

- AWS [App Mesh](https://aws.amazon.com/app-mesh/)
    - https://github.com/aws/aws-app-mesh-examples
    - https://www.appmeshworkshop.com/
    - To be used to monitor and control communications across microservices applications on AWS.
    - The AWS App Mesh can be used with microservices running on ECS, Amazon EKS, and Kubernetes running on EC2.
    - App Mesh currently uses [Envoy](https://www.envoyproxy.io/), which makes it compatible with other open source and AWS partner tools for monitoring microservices.
    - Observability data can be exported to various AWS and third-party tools, including X-Ray, CloudWatch, and any third-party monitoring and tracing tools that integrate with Envoy.
    - New traffic routing controls can be configured to enable blue/green canary deployments for your services.
    - App Mesh is designed to provide "a consistent, dynamic way to manage the communications between microservices".
        - The logic for monitoring and controlling communications across microservices is put into service as a proxy that runs next to each microservice rather than being built into the code of each microservice.
        - The proxy takes care of all the network traffic that flows in and out of the microservice and offers consistency for "visibility, traffic control, and security capabilities to all of your microservices".

- Buoyant [Linkerd](https://github.com/linkerd/linkerd2)
    - An ultralight, security-first service mesh for Kubernetes.
    - Linkerd adds critical security, observability, and reliability features to your Kubernetes stack with no code change required.

- Google [Istio](https://github.com/istio/istio)
    - An open platform to connect, manage, and secure microservices.
    - One of the best‑known service mesh architectures.
    - Backed by Google, IBM, and Lyft.
