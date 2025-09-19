# ELB Notes

- [Useful Libs and Tools](#useful-libs-and-tools)
- [Useful Articles and Blogs](#useful-articles-and-blogs)
    - [ALB](#alb)
    - [NLB](#nlb)
    - [GWLB](#gwlb)

---

## Useful Libs and Tools


## Useful Articles and Blogs

- [Using Load Balancer Capacity Unit Reservation to prepare for sharp increases in traffic](https://aws.amazon.com/blogs/networking-and-content-delivery/using-load-balancer-capacity-unit-reservation-to-prepare-for-sharp-increases-in-traffic/), AWS, 2025-01-28
- [Elastic Load Balancer: Maximizing Benefits and Keeping Costs Low](https://aws.amazon.com/blogs/networking-and-content-delivery/elb-maximizing-benefits-and-keeping-costs-low/), AWS, 2023-10-25
    - Optimize your client connections
        - Connection Pooling
        - Connection retry strategies such as Exponential backoff and injecting jitter
        - Connection idle timeout feature
        - TLS 1.3 for ELB
        - TLS session re-use for certain use cases
    - Optimize inbound and outbound traffic
        - compress the payload
        - combining requests
        - Serializing the data you are transferring with an efficient protocol is critical
        - obtain data that could be accessed directly from the authoritative data provider, instead of via ELB
        - Block/Filter/Cache requests at the edge to avoid charges associated with illegitimate or incorrectly formatted requests
    - Cross-Zone Load Balancing
    - Good housekeeping
        - Consolidate ELBs
        - set up metrics that track your underlying service behavior, e.g. identifying malfunctioning clients
        - remove unused ELBs

### ALB

- [Security best practices when using ALB authentication](https://aws.amazon.com/blogs/networking-and-content-delivery/security-best-practices-when-using-alb-authentication/), AWS, 2024-08-15
- [Automating HTTP/S Redirects and certificate management at scale](https://aws.amazon.com/blogs/networking-and-content-delivery/automating-http-s-redirects-and-certificate-management-at-scale/), AWS, 2023-03-21
    - How to build a scalable and cost-effective solution to handle HTTP/S redirects at scale for **multiple domains** by using
        - ALB to perform rule-based redirects,
        - AWS Global Accelerator to get static IP addresses, and
        - AWS Lambda to host redirect logic on serverless infrastructure.
    - This method simplifies deployments while benefiting from the scale, availability, and reliability of AWS infrastructure and services.
- [Using static IP addresses for Application Load Balancers (NLB->ALB)](https://aws.amazon.com/blogs/networking-and-content-delivery/using-static-ip-addresses-for-application-load-balancers/), 2018-04-20


### NLB

- [Automate OIDC client secret rotation with Application Load Balancer](https://aws.amazon.com/blogs/security/automate-oidc-client-secret-rotation-with-application-load-balancer/), AWS, 2025-09-16
- [Preserving client IP address with Proxy protocol v2 and Network Load Balancer](https://aws.amazon.com/blogs/networking-and-content-delivery/preserving-client-ip-address-with-proxy-protocol-v2-and-network-load-balancer/), AWS, 2024-07-16
- [Enhance observability for Network Load Balancers using Amazon CloudWatch Internet Monitor](https://aws.amazon.com/blogs/mt/enhance-observability-for-network-load-balancers-using-amazon-cloudwatch-internet-monitor/), AWS, 2023-07-27
- [Scaling NLB target groups by connections](https://aws.amazon.com/blogs/networking-and-content-delivery/scaling-nlb-target-groups-by-connections/), AWS, 2023-06-05


### GWLB

- [Virtual Private Gateway Ingress Routing support for Gateway Load Balancer](https://aws.amazon.com/blogs/networking-and-content-delivery/announcing-amazon-virtual-private-gateway-ingress-routing-support-for-gateway-load-balancer/), AWS, 2023-08-30
