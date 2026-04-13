# Payload Filtering

Endee supports metadata-aware filtering during vector search, allowing you to restrict results to records matching specific payload conditions.

## Overview

When you insert a vector, you can attach arbitrary metadata (`payload`) to it. At search time, you can filter by those fields — only vectors whose payload matches your conditions will be scored and returned.

## Inserting with Payload

```bash
curl -X POST http://localhost:8080/api/v1/index/complaints/insert \
  -H "Content-Type: application/json" \
  -d '{
    "id": "c001",
    "vector": [0.11, 0.25, ...],
    "payload": {
      "category": "billing",
      "status": "open",
      "priority": 2,
      "customer_id": "cust_789"
    }
  }'
```

## Filtering at Search Time

```bash
curl -X POST http://localhost:8080/api/v1/index/complaints/search \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [0.12, 0.24, ...],
    "top_k": 5,
    "filter": {
      "must": [
        {"key": "category", "match": {"value": "billing"}},
        {"key": "status",   "match": {"value": "open"}}
      ]
    }
  }'
```

## Filter Conditions

| Condition | Description | Example |
|-----------|-------------|---------|
| `match.value` | Exact equality | `{"key": "category", "match": {"value": "billing"}}` |
| `range` | Numeric range | `{"key": "priority", "range": {"gte": 1, "lte": 3}}` |
| `should` | OR logic | At least one condition must match |
| `must_not` | Exclusion | None of the conditions must match |

## Python Example (via our Python wrapper)

```python
from endee import EndeeDB

db = EndeeDB("./data/complaints.jsonl")

results = db.search(
    vector=query_embedding,
    top_k=5,
    filter={"category": "billing"}   # equality filter
)
```

## More

See [docs.endee.io](https://docs.endee.io) for full filter syntax reference.
