# Endee C++ Source

This directory (`src/`) contains the C++ source code for the Endee vector database engine.

It is part of the upstream [endee-io/endee](https://github.com/endee-io/endee) repository.

> **Note for fork contributors:** Do not delete or modify this directory.
> It contains the core C++ implementation of the Endee server.

## Key Components

- **HNSW Index** — Hierarchical Navigable Small World graph for approximate nearest-neighbor search
- **MDBX Storage** — Embedded key-value store for persistent vector and metadata storage
- **HTTP Server** — Lightweight REST API server (listens on port 8080)
- **Query Executor** — Handles dense vector search, sparse retrieval, payload filtering, and hybrid queries
- **SIMD Math** — CPU-optimised dot product and normalisation via AVX2 / AVX512 / NEON / SVE2

## Build

See [docs/getting-started.md](../docs/getting-started.md) or run:

```bash
./install.sh --release --avx2
```
