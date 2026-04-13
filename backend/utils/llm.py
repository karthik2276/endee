"""
backend/utils/llm.py
---------------------
Singleton FLAN-T5 wrapper + RAG prompt builder.
"""

from __future__ import annotations

import logging
from typing import List

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

logger = logging.getLogger(__name__)


def build_rag_prompt(question: str, context_complaints: List[str]) -> str:
    """Build an instruction prompt for FLAN-T5 from retrieved complaint context."""
    context = "\n".join(f"- {c}" for c in context_complaints[:5])
    return (
        "You are a helpful customer service AI. "
        "Using the similar complaints below, write a concise and empathetic response.\n\n"
        f"Similar complaints:\n{context}\n\n"
        f"Customer question: {question}\n\n"
        "Response:"
    )


class LLMService:
    def __init__(self, model_name: str, max_new_tokens: int = 256) -> None:
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self._tokenizer = None
        self._model = None
        self._device = "cuda" if torch.cuda.is_available() else "cpu"

    def _ensure_loaded(self) -> None:
        if self._model is None:
            logger.info("Loading LLM: %s (device=%s)", self.model_name, self._device)
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self._model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self._model.to(self._device)
            self._model.eval()
            logger.info("LLM ready")

    def generate(self, prompt: str) -> str:
        self._ensure_loaded()
        inputs = self._tokenizer(
            prompt, return_tensors="pt", max_length=1024, truncation=True
        ).to(self._device)
        with torch.no_grad():
            ids = self._model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=3,
            )
        return self._tokenizer.decode(ids[0], skip_special_tokens=True).strip()


_service: LLMService | None = None


def get_llm_service() -> LLMService:
    global _service
    if _service is None:
        from backend.config import settings
        _service = LLMService(settings.llm_model, settings.llm_max_new_tokens)
    return _service
