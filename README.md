# ⬡ AI Complaint Assistant — Built on Endee Vector Database

> **Forked from [endee-io/endee](https://github.com/endee-io/endee)**  
> Internship Project Submission — SDE / AI / ML Intern Evaluation  
> Practical AI/ML use case built on top of the Endee vector database.

[Quick Start](#setup-instructions) • [Architecture](#system-architecture) • [How Endee is Used](#how-endee-is-used) • [API Endpoints](#api-endpoints) • [Features](#features) • [Tech Stack](#tech-stack)

---

## About This Fork

This repository is a **fork of [endee-io/endee](https://github.com/endee-io/endee)** — a high-performance open-source vector database built for AI search and retrieval workloads.

On top of the original Endee C++ engine and infrastructure, this fork adds a **full-stack AI Complaint Assistant** application that demonstrates a complete **Retrieval-Augmented Generation (RAG)** pipeline using Endee as the sole vector database.

**Original Endee repo contents (preserved in this fork):**
- `src/` — Endee C++ source code
- `infra/` — Docker build configuration (`infra/Dockerfile`)
- `docs/` — Getting started, filtering, sparse search, backup, logs documentation
- `tests/` — C++ test suite
- `third_party/` — Bundled third-party libraries (MDBX, hnswlib, etc.)
- `CMakeLists.txt`, `install.sh`, `run.sh`, `docker-compose.yml`
- `.github/workflows/` — CI pipeline

**Added by this fork (AI Complaint Assistant):**
- `backend/` — FastAPI backend (RAG pipeline, embedding service, LLM)
- `frontend/` — React + Vite + TypeScript frontend
- `data/` — Seed data and ingestion scripts
- `endee/` — Python wrapper (`EndeeDB`) used by the Python backend

---

## Project Overview

The **AI Complaint Assistant** allows users to store, semantically search, and intelligently query customer complaints using natural language.

It demonstrates a complete **RAG (Retrieval-Augmented Generation)** pipeline:

```
User Query
    │
    ▼
SentenceTransformer (all-MiniLM-L6-v2)
    │  generates 384-dim embedding
    ▼
Endee Vector Database  ◄──── core of this project
    │  cosine similarity search → top-K complaints
    ▼
FLAN-T5 (google/flan-t5-base)
    │  context-aware answer generation
    ▼
AI Response + Retrieved Complaints
```

**Use case:** A customer support team loads past complaints into Endee, then asks natural language questions like *"What are the most common billing issues?"* and gets an AI-generated answer grounded in real complaint data.

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                   React Frontend (Vite + TS)                  │
│  ┌─────────────┐  ┌──────────────────┐  ┌────────────────┐  │
│  │  AI Chat    │  │ Semantic Search  │  │ Add Complaint  │  │
│  │ (AskPanel)  │  │ (SearchPanel)    │  │ (AddComplaint) │  │
│  └──────┬──────┘  └────────┬─────────┘  └───────┬────────┘  │
└─────────┼──────────────────┼────────────────────┼───────────┘
          │ POST /ask        │ POST /search        │ POST /add-complaint
          ▼                  ▼                     ▼
┌──────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                           │
│                                                              │
│  ┌─────────────────┐    ┌───────────────────────────────┐   │
│  │  Embedding Svc  │    │      Endee Vector DB           │   │
│  │ (MiniLM-L6-v2)  │───►│  insert() / search() / count() │   │
│  └─────────────────┘    │  Persistent JSONL storage      │   │
│  ┌─────────────────┐    └───────────────────────────────┘   │
│  │   LLM Service   │                                         │
│  │  (FLAN-T5-base) │                                         │
│  └─────────────────┘                                         │
└──────────────────────────────────────────────────────────────┘
```

---

## How Endee is Used

This project uses **Endee** (this forked repository) as the sole vector database. The Python wrapper in `endee/__init__.py` and `endee/db.py` provides `EndeeDB` — a JSONL-backed, cosine-similarity vector store.

The backend imports it directly:

```python
from endee import EndeeDB

db = EndeeDB("./data/complaints.jsonl")
```

### Storing a complaint embedding

```python
# POST /add-complaint
vector = embedding_service.encode(complaint_text)   # 384-dim float list

db.insert(
    id=record_id,
    vector=vector,
    metadata={
        "text": complaint_text,
        "category": "billing",
        "timestamp": "2026-04-13T08:30:00Z"
    }
)
```

### Semantic similarity search

```python
# POST /search
query_vector = embedding_service.encode(user_query)

results = db.search(
    vector=query_vector,
    top_k=5,
    filter={"category": "billing"}   # optional metadata filter (see docs/filter.md)
)
# returns List[SearchResult] sorted by cosine similarity score (0–1)
```

### Full RAG pipeline

```python
# POST /ask
query_vector  = embedding_service.encode(question)
raw_results   = db.search(vector=query_vector, top_k=5)   # Endee retrieval
context_texts = [r.metadata["text"] for r in raw_results]
prompt        = build_rag_prompt(question, context_texts)
answer        = llm_service.generate(prompt)              # FLAN-T5 generation
```

### Endee API methods used

| Method | Where used |
|--------|-----------|
| `EndeeDB(path)` | `backend/utils/vector_store.py` — open/create the DB file |
| `db.insert(id, vector, metadata)` | `backend/routers/complaints.py`, `data/seed_complaints.py` |
| `db.search(vector, top_k, filter)` | `backend/routers/search.py`, `backend/routers/ask.py` |
| `db.count()` | `backend/main.py`, `/health` endpoint |

---

## Features

- **Complaint Ingestion** — text → embedding → Endee storage
- **Semantic Search** — natural language query → cosine similarity → ranked results
- **RAG Pipeline** — Endee retrieval + FLAN-T5 generation in a single `/ask` call
- **AI Chat Interface** — conversational UI with expandable retrieved context
- **Category Filtering** — filter semantic search by complaint type (uses Endee payload filter)
- **Live Status Bar** — real-time backend health, model info, complaint count
- **25 Sample Complaints** — pre-seeded across 6 categories

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Vector Database** | Endee (this repo) — JSONL-backed, cosine similarity |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` (384-dim) |
| **LLM** | `google/flan-t5-base` (offline, HuggingFace) |
| **Backend** | Python 3.10 · FastAPI · Pydantic v2 · Uvicorn |
| **Frontend** | React 18 · Vite · TypeScript · CSS Modules |

---

## Project Structure

```
endee/                                  ← forked repo root (endee-io/endee)
│
├── .github/
│   └── workflows/
│       └── ci.yml                      ← CI pipeline (from original Endee)
│
├── src/                                ← Endee C++ source (original, preserved)
├── infra/
│   ├── Dockerfile                      ← Docker build for Endee C++ server
│   └── README.md
├── docs/
│   ├── getting-started.md              ← Endee setup guide (Docker, CMake, install.sh)
│   ├── filter.md                       ← Payload filtering docs
│   ├── sparse.md                       ← Sparse/hybrid search docs
│   ├── backup-system.md                ← Backup and restore docs
│   ├── logs.md                         ← Logging docs
│   └── mdbx-instrumentation.md        ← MDBX storage tuning docs
├── tests/                              ← Endee C++ test suite (original)
├── third_party/                        ← Bundled libs: MDBX, hnswlib, etc.
│
├── CMakeLists.txt                      ← Endee CMake build (AVX2/AVX512/NEON/SVE2)
├── docker-compose.yml                  ← Docker Compose for Endee server
├── install.sh                          ← Automated build script (Linux/macOS)
├── run.sh                              ← Start the built Endee server
├── .clang-format                       ← C++ code style
├── .gitignore
├── LICENSE                             ← Apache 2.0
├── CONTRIBUTING.md
│
├── endee/                              ← Python wrapper around EndeeDB (added by this fork)
│   ├── __init__.py                     ← exports EndeeDB, Record, SearchResult
│   └── db.py                           ← JSONL-backed vector store (cosine similarity)
│
├── backend/                            ← FastAPI AI backend (added by this fork)
│   ├── main.py                         ← FastAPI app, CORS, startup lifecycle
│   ├── config.py                       ← Settings from .env (pydantic-settings)
│   ├── requirements.txt
│   ├── .env
│   ├── routers/
│   │   ├── complaints.py               ← POST /add-complaint
│   │   ├── search.py                   ← POST /search
│   │   └── ask.py                      ← POST /ask (full RAG pipeline)
│   ├── models/
│   │   └── schemas.py                  ← Pydantic v2 request/response schemas
│   └── utils/
│       ├── embeddings.py               ← SentenceTransformer singleton
│       ├── llm.py                      ← FLAN-T5 + RAG prompt builder
│       └── vector_store.py             ← EndeeDB singleton wrapper
│
├── frontend/                           ← React + Vite frontend (added by this fork)
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       ├── main.tsx                    ← entry point with ErrorBoundary
│       ├── App.tsx
│       ├── ErrorBoundary.tsx
│       └── components/
│           ├── StatusBar.tsx           ← live backend health bar
│           ├── AskPanel.tsx            ← AI chat (RAG) panel
│           ├── SearchPanel.tsx         ← semantic search panel
│           ├── AddComplaint.tsx        ← complaint ingestion form
│           └── ComplaintCard.tsx       ← result card component
│
└── data/
    └── seed_complaints.py              ← seeds 25 complaints into Endee
```

---

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- ~3 GB disk space (HuggingFace model downloads on first run)

### Step 1 — Fork & Clone (MANDATORY for submission)

> Do **not** download as a ZIP. You **must** fork first.

1. Visit [https://github.com/endee-io/endee](https://github.com/endee-io/endee)
2. Click ⭐ **Star** the repository
3. Click **Fork** → fork to your account
4. Clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/endee.git
cd endee
```

### Step 2 — Install Python backend

```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux / macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 3 — Seed sample data

```bash
cd ..                          # back to repo root
python data/seed_complaints.py
```

This inserts 25 pre-written complaints into Endee across 6 categories.

### Step 4 — Start the backend

```bash
uvicorn backend.main:app --reload --port 8000
```

Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Step 5 — Start the frontend

```bash
cd frontend
npm install
npm run dev
```

App: [http://localhost:5173](http://localhost:5173)

### Step 6 — Verify

```bash
curl http://localhost:8000/health
# {"status":"ok","total_complaints":25,"embedding_model":"all-MiniLM-L6-v2",...}
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/add-complaint` | Encode complaint text and store vector + metadata in Endee |
| `POST` | `/search` | Semantic similarity search via `db.search()` |
| `POST` | `/ask` | Full RAG pipeline — Endee retrieval + FLAN-T5 generation |
| `GET`  | `/health` | Backend status, complaint count, model names |
| `GET`  | `/` | Service info + docs link |

---

## Example Queries

**Search:** `"charged twice on my card"`
```json
{
  "query": "charged twice on my card",
  "results": [
    {
      "text": "I was charged twice for the same order...",
      "category": "billing",
      "similarity_score": 0.913452
    }
  ],
  "total_found": 5
}
```

**Ask:** `"What delivery issues are most common?"`
```
"Based on the complaints, the most common delivery issues include late arrivals,
packages delivered to wrong addresses, and damaged packaging during transit."
```

---

## Push to GitHub

```bash
git add .
git commit -m "feat: AI Complaint Assistant — RAG pipeline built on Endee vector database"
git push origin main
```

Submission URL: `https://github.com/YOUR_USERNAME/endee`

---

## Endee Original Documentation

- [Getting Started](docs/getting-started.md) — Docker, install.sh, CMake build
- [Payload Filtering](docs/filter.md)
- [Sparse / Hybrid Search](docs/sparse.md)
- [Backup System](docs/backup-system.md)
- [Logs](docs/logs.md)
- [MDBX Instrumentation](docs/mdbx-instrumentation.md)
- [Hosted Docs](https://docs.endee.io/quick-start)

---

## Community (Endee)

- Discord: [discord.gg/5HFGqDZQE3](https://discord.gg/5HFGqDZQE3)
- Website: [endee.io](https://endee.io)
- Enterprise / branding: [enterprise@endee.io](mailto:enterprise@endee.io)

---

## License

This project inherits the **Apache License 2.0** from the upstream Endee repository.  
See [LICENSE](LICENSE) for full terms.

> "Endee" and the Endee logo are trademarks of Endee Labs. This fork is an independent project and does not imply official endorsement or affiliation.
