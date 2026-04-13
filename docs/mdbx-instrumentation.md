# MDBX Instrumentation

Endee uses [libmdbx](https://libmdbx.dqdkfa.ru/) as its embedded storage engine. This document covers how to monitor and tune MDBX performance in production.

## Overview

MDBX (Memory-Mapped Database eXtended) is an LMDB-inspired key-value store used by Endee to persist vectors, payloads, and index metadata. It uses memory-mapped I/O for extremely fast reads.

## Key Metrics

| Metric | Description |
|--------|-------------|
| `mdbx.page_count` | Total pages allocated in the database file |
| `mdbx.overflow_pages` | Pages used for oversized records |
| `mdbx.leaf_pages` | Pages at the B-tree leaf level |
| `mdbx.branch_pages` | Pages at the B-tree branch level |
| `mdbx.depth` | Tree depth (higher = slower lookups) |
| `mdbx.readers` | Number of active read transactions |
| `mdbx.writes` | Cumulative write operations |

## Viewing Stats

With debug builds, MDBX stats are printed at shutdown:

```bash
./install.sh --debug_nd --avx2
NDD_DATA_DIR=./data ./build/ndd
```

```
[MDBX] page_count=48320 leaf=34210 branch=12100 overflow=10
[MDBX] readers=4 txns=1820 writes=922
```

## Tuning

| Parameter | What it does | How to set |
|-----------|-------------|------------|
| `NDD_MDBX_MAPSIZE` | Max memory-mapped file size | Env var (bytes) |
| `NDD_MDBX_MAX_READERS` | Max concurrent readers | Env var |

Example:

```bash
NDD_DATA_DIR=./data NDD_MDBX_MAPSIZE=10737418240 ./build/ndd  # 10 GB map
```

## More

See [docs.endee.io](https://docs.endee.io) for MDBX configuration reference.
