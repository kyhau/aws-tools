# CodeArtifact notes


1. You can make packages in one repository available to another repository in the SAME domain.
    - To do this, configure one repository as an upstream of the other.
    - All package versions available to the upstream repository are also available to the downstream repository.
    - In addition, all packages that are available to the upstream repository through an external connection to a public repository are available to the downstream repository.
    - ([Source](https://docs.aws.amazon.com/codeartifact/latest/ug/welcome.html))

2. Creating a domain based on organizational ownership ([Source](https://aws.amazon.com/blogs/devops/integrating-aws-codeartifact-package-mgmt-flow/))
    - Whenever a package is fetched from a repository, the asset is cached in your CodeArtifact domain to minimize the cost of subsequent downstream requests.
    - A given asset only needs to be stored once in a domain, even if it’s available in two—or two thousand—repositories. That means you only pay for storage once.
    - Copying a package version with the `CopyPackageVersions` API is only possible between repositories within the same CodeArtifact domain.

        ```
        REPO              DOMAIN         DOMAIN_OWNER
        my-shared-repo    domain-my-org  111122223333
        my-team-repo      domain-my-org  444455556666
        ```

3. Organization domain
    - CodeArtifact domains make it easier to manage multiple repositories across an organization. You can use a domain to apply permissions across many repositories owned by different AWS accounts. An asset is stored only once in a domain, even if it's available from multiple repositories. ([Source](https://docs.aws.amazon.com/codeartifact/latest/ug/domains.html))

    - Although an organization can have multiple domains, the recommendation is to have a single production domain that contains all published artifacts so that development teams can find and share packages across their organization. A second pre-production domain can be useful for testing changes to the production domain configuration. ([Source](https://docs.aws.amazon.com/codeartifact/latest/ug/domain-overview.html))

3. Cross-account domains
    - Domain names only need to be unique within an account, which means there could be multiple domains within a region that have the same name. Because of this, if you want to access a domain that is owned by an account you are not authenticated to, you must provide the domain owner ID along with the domain name
