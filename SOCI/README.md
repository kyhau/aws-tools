# Seekable OCI (SOCI) for lazy loading container images

Source: [What's New](https://aws.amazon.com/about-aws/whats-new/2022/09/introducing-seekable-oci-lazy-loading-container-images/)

> [Lazy loading](https://en.wikipedia.org/wiki/Lazy_loading) is an approach where data is downloaded from the registry in parallel with the application startup. Container images are stored as an ordered list of layers, and layers are most often stored as gzipped tar files.

> A SOCI (Seekable OCI) index is generated separately from the container image, and is stored in the registry as an [OCI Artifact](https://github.com/opencontainers/artifacts) and linked back to the container image by [OCI Reference Types](https://github.com/opencontainers/tob/blob/main/proposals/wg-reference-types.md). This means that the container images do not need to be converted, image digests do not change, and image signatures remain valid.

Repo: https://github.com/awslabs/soci-snapshotter/blob/main/docs/GETTING_STARTED.md

