# Endee Tests

This directory (`tests/`) contains the test suite for the Endee vector database engine.

It is part of the upstream [endee-io/endee](https://github.com/endee-io/endee) repository.

## Running Tests

Build the project first (see [docs/getting-started.md](../docs/getting-started.md)), then:

```bash
cd build
ctest --output-on-failure -j$(nproc)
```

## Test Categories

- **Unit tests** — individual component tests (index, storage, filtering, math)
- **Integration tests** — full request/response cycle tests against the HTTP API
- **Performance benchmarks** — throughput and latency measurements for HNSW search
