"""
backend/routers/complaints.py
------------------------------
POST /add-complaint
  1. Encode complaint text -> embedding vector
  2. Store vector + metadata in Endee
  3. Return the assigned record ID
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from backend.models.schemas import AddComplaintRequest, AddComplaintResponse
from backend.utils.embeddings import get_embedding_service
from backend.utils.vector_store import get_db

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Complaints"])


@router.post("/add-complaint", response_model=AddComplaintResponse)
async def add_complaint(payload: AddComplaintRequest) -> AddComplaintResponse:
    try:
        vector = get_embedding_service().encode(payload.text)
        record_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()

        get_db().insert(
            id=record_id,
            vector=vector,
            metadata={
                "text":        payload.text,
                "category":    payload.category,
                "customer_id": payload.customer_id or "anonymous",
                "timestamp":   timestamp,
            },
        )
        logger.info("Stored complaint id=%s category=%s", record_id, payload.category)
        return AddComplaintResponse(
            id=record_id,
            message="Complaint stored successfully in Endee.",
            category=payload.category,
            timestamp=timestamp,
        )
    except Exception as exc:
        logger.exception("add_complaint failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
