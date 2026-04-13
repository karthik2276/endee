# Backup System

Endee provides backup and restore APIs to protect your vector index data.

## Overview

Backups capture a consistent snapshot of your index — including all vectors, payloads, and the HNSW graph — and write them to a specified location. Restores load a snapshot back into a running or newly started server.

## Trigger a Backup

```bash
curl -X POST http://localhost:8080/api/v1/index/complaints/backup \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "/data/backups/complaints_2026-04-13"
  }'
```

Response:

```json
{
  "status": "ok",
  "backup_id": "bkp_20260413_153200",
  "destination": "/data/backups/complaints_2026-04-13",
  "record_count": 25000,
  "elapsed_ms": 312
}
```

## List Backups

```bash
curl http://localhost:8080/api/v1/index/complaints/backup/list
```

## Restore from Backup

```bash
curl -X POST http://localhost:8080/api/v1/index/complaints/restore \
  -H "Content-Type: application/json" \
  -d '{
    "source": "/data/backups/complaints_2026-04-13"
  }'
```

## Scheduled Backups (Docker Compose)

You can schedule backups using a cron container alongside Endee:

```yaml
services:
  endee:
    image: endee-oss:latest
    ports: ["8080:8080"]
    volumes:
      - endee-data:/data
      - ./backups:/backups

  backup:
    image: curlimages/curl:latest
    entrypoint: >
      sh -c "while true; do
        sleep 86400;
        curl -X POST http://endee:8080/api/v1/index/complaints/backup
          -d '{\"destination\": \"/backups/daily\"}';
      done"
    depends_on: [endee]
```

## More

See [docs.endee.io](https://docs.endee.io) for backup scheduling and S3 export options.
