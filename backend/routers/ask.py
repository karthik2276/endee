"""
backend/routers/ask.py
-----------------------
POST /ask  — full RAG pipeline
  1. Embed question
  2. Retrieve similar complaints from Endee
  3. Build prompt with retrieved context
  4. Generate answer with FLAN-T5
  5. Return answer + retrieved complaints
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from backend.config import settings
from backend.models.schemas import AskRequest, AskResponse, ComplaintResult
from backend.utils.embeddings import get_embedding_service
from backend.utils.llm import build_rag_prompt, get_llm_service
from backend.utils.vector_store import get_db

logger = logging.getLogger(__name__)
router = APIRouter(tags=["RAG"])


@router.post("/ask", response_model=AskResponse)
async def ask(payload: AskRequest) -> AskResponse:
    try:
        top_k  = payload.top_k or settings.search_top_k
        vector = get_embedding_service().encode(payload.question)
        raw    = get_db().search(vector=vector, top_k=top_k)

        logger.info("RAG retrieved %d docs for '%s'", len(raw), payload.question)

        retrieved = [
            ComplaintResult(
                id=r.id,
                text=r.metadata.get("text", ""),
                category=r.metadata.get("category", "general"),
                similarity_score=r.score,
                timestamp=r.metadata.get("timestamp", ""),
            )
            for r in raw
        ]

        if retrieved:
            prompt = build_rag_prompt(payload.question, [r.text for r in retrieved])
            answer = get_llm_service().generate(prompt)
        else:
            answer = (
                "No relevant complaints found in the database. "
                "Please add some complaints first using the 'Add Complaint' tab."
            )

        return AskResponse(
            question=payload.question,
            answer=answer,
            retrieved_complaints=retrieved,
            model_used=settings.llm_model,
        )
    except Exception as exc:
        logger.exception("ask failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
