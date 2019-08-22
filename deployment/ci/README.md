# How To Build

```bash
# Log in to Docker Hub
> docker login
# Build Image
> docker build --tag passthesecret/ci-build-environment .
# Push to Docker Hub
> docker push passthesecret/ci-build-environment:latest
```
