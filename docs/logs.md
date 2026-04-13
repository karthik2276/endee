# Logs

Endee's logging system provides structured runtime output for operational visibility and debugging.

## Log Levels

| Level | When used |
|-------|-----------|
| `INFO` | Normal operation — index creation, query counts, startup/shutdown |
| `WARN` | Non-fatal issues — slow queries, near-capacity warnings |
| `ERROR` | Operation failures — write errors, corrupted records |
| `DEBUG` | Verbose internals — available in `--debug_nd` and `--debug_all` builds |

## Log Format

```
[2026-04-13T08:30:01Z] [INFO]  server started on :8080
[2026-04-13T08:30:05Z] [INFO]  index=complaints insert id=c001 dim=384 elapsed=0.8ms
[2026-04-13T08:30:09Z] [INFO]  index=complaints search top_k=5 elapsed=1.2ms results=5
[2026-04-13T08:30:10Z] [WARN]  query latency exceeded 50ms: elapsed=63ms
```

## Enable Debug Logging

Build with `--debug_nd` or set `ND_DEBUG=ON` in CMake for Endee's internal timing and trace logs:

```bash
./install.sh --debug_nd --avx2
```

Or with Docker:

```yaml
environment:
  ND_DEBUG: "1"
```

## Log Output Location

By default, logs go to `stdout`. To redirect to a file:

```bash
NDD_DATA_DIR=./data ./build/ndd >> ./endee.log 2>&1
```

## Docker Compose Log Retention

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "200m"
    max-file: "5"
```

This keeps at most 5 × 200 MB = 1 GB of logs.

## More

See [docs.endee.io](https://docs.endee.io) for log shipping to external systems.
