"""
backend/models/schemas.py
--------------------------
All Pydantic request / response schemas.
"""

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


# ── Add complaint ────────────────────────────────────────────────────────────

class AddComplaintRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=2000)
    category: str = Field(default="general")
    customer_id: Optional[str] = Field(default=None)

class AddComplaintResponse(BaseModel):
    id: str
    message: str
    category: str
    timestamp: str


# ── Search ───────────────────────────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3)
    top_k: Optional[int] = Field(default=None, ge=1, le=20)
    category_filter: Optional[str] = Field(default=None)

class ComplaintResult(BaseModel):
    id: str
    text: str
    category: str
    similarity_score: float
    timestamp: str

class SearchResponse(BaseModel):
    query: str
    results: List[ComplaintResult]
    total_found: int


# ── Ask / RAG ────────────────────────────────────────────────────────────────

class AskRequest(BaseModel):
    question: str = Field(..., min_length=5)
    top_k: Optional[int] = Field(default=None, ge=1, le=10)

class AskResponse(BaseModel):
    question: str
    answer: str
    retrieved_complaints: List[ComplaintResult]
    model_used: str


# ── Health ───────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    total_complaints: int
    embedding_model: str
    llm_model: str
