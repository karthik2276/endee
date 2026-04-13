"""
backend/routers/search.py
--------------------------
POST /search
  1. Encode query text -> vector
  2. Call Endee db.search(vector, top_k, filter)
  3. Return ranked ComplaintResult list
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from backend.config import settings
from backend.models.schemas import ComplaintResult, SearchRequest, SearchResponse
from backend.utils.embeddings import get_embedding_service
from backend.utils.vector_store import get_db

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Search"])


@router.post("/search", response_model=SearchResponse)
async def search_complaints(payload: SearchRequest) -> SearchResponse:
    try:
        top_k  = payload.top_k or settings.search_top_k
        vector = get_embedding_service().encode(payload.query)

        meta_filter = None
        if payload.category_filter and payload.category_filter.strip():
            meta_filter = {"category": payload.category_filter.strip().lower()}

        raw = get_db().search(vector=vector, top_k=top_k, filter=meta_filter)
        logger.info("search query='%s' -> %d results", payload.query, len(raw))

        results = [
            ComplaintResult(
                id=r.id,
                text=r.metadata.get("text", ""),
                category=r.metadata.get("category", "general"),
                similarity_score=r.score,
                timestamp=r.metadata.get("timestamp", ""),
            )
            for r in raw
        ]
        return SearchResponse(query=payload.query, results=results, total_found=len(results))
    except Exception as exc:
        logger.exception("search failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
