# Sparse Search

Endee supports sparse vector retrieval as part of hybrid search workflows.

## Overview

Sparse vectors represent text using term-frequency-based representations (e.g. BM25, SPLADE). Combined with dense vector search, sparse retrieval improves precision for queries where exact term matches matter alongside semantic similarity.

## Creating an Index with Sparse Support

When creating an index via the HTTP API, enable sparse support:

```bash
curl -X POST http://localhost:8080/api/v1/index/create \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_hybrid_index",
    "dimension": 384,
    "sparse": true,
    "metric": "cosine"
  }'
```

## Inserting Vectors with Sparse Components

```bash
curl -X POST http://localhost:8080/api/v1/index/my_hybrid_index/insert \
  -H "Content-Type: application/json" \
  -d '{
    "id": "doc1",
    "vector": [0.1, 0.2, ...],
    "sparse_vector": {"42": 0.85, "178": 0.31, "991": 0.67},
    "payload": {"text": "Example document", "category": "billing"}
  }'
```

## Hybrid Search Query

```bash
curl -X POST http://localhost:8080/api/v1/index/my_hybrid_index/search \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [0.1, 0.2, ...],
    "sparse_vector": {"42": 0.9, "178": 0.4},
    "top_k": 10,
    "fusion": "rrf"
  }'
```

`fusion: "rrf"` uses Reciprocal Rank Fusion to combine dense and sparse scores.

## Supported Fusion Methods

| Method | Description |
|--------|-------------|
| `rrf` | Reciprocal Rank Fusion — default, balanced fusion |
| `weighted` | Weighted sum with explicit `alpha` parameter (0.0–1.0) |

## More

See [docs.endee.io](https://docs.endee.io) for full API reference.
