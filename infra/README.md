# Endee Infrastructure

This directory (`infra/`) contains Docker and deployment configuration for Endee.

It is part of the upstream [endee-io/endee](https://github.com/endee-io/endee) repository.

## Contents

- `Dockerfile` — Multi-stage Docker build for the Endee server binary
- Additional deployment manifests (Kubernetes, systemd, etc.)

## Build Docker Image

```bash
# Intel/AMD (recommended for most machines)
docker build \
  --ulimit nofile=100000:100000 \
  --build-arg BUILD_ARCH=avx2 \
  -t endee-oss:latest \
  -f ./infra/Dockerfile \
  .

# Apple Silicon Mac
docker build \
  --ulimit nofile=100000:100000 \
  --build-arg BUILD_ARCH=neon \
  -t endee-oss:latest \
  -f ./infra/Dockerfile \
  .
```

## Run with Docker Compose

```bash
docker compose up -d
```

See the [getting started guide](../docs/getting-started.md) for full details.
