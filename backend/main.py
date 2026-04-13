"""
backend/main.py
---------------
FastAPI entry point.

Run:
    cd ai-complaint-assistant-v2
    uvicorn backend.main:app --reload --port 8000
"""

from __future__ import annotations

import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add project root to sys.path so `endee` package resolves
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.config import settings
from backend.models.schemas import HealthResponse
from backend.routers import ask, complaints, search
from backend.utils.embeddings import get_embedding_service
from backend.utils.vector_store import get_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=== AI Complaint Assistant starting up ===")

    db = get_db()
    logger.info("Endee DB ready — %d complaints", db.count())

    emb = get_embedding_service()
    emb._ensure_loaded()
    logger.info("Embedding model ready — dim=%d", emb.dimension)

    # LLM is loaded lazily on first /ask call (large download)
    # Uncomment the lines below to pre-warm it on startup:
    # llm = get_llm_service()
    # llm._ensure_loaded()

    logger.info("=== Startup complete ===")
    yield
    logger.info("=== Shutting down ===")


app = FastAPI(
    title="AI Complaint Assistant",
    description="RAG-based complaint system: Endee + SentenceTransformers + FLAN-T5",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(complaints.router)
app.include_router(search.router)
app.include_router(ask.router)


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        total_complaints=get_db().count(),
        embedding_model=settings.embedding_model,
        llm_model=settings.llm_model,
    )


@app.get("/", tags=["System"])
async def root():
    return {"service": "AI Complaint Assistant", "docs": "/docs", "health": "/health"}
