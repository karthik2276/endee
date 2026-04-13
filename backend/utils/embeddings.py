"""
backend/utils/embeddings.py
----------------------------
Singleton SentenceTransformer wrapper.
Loaded once on first use; reused for every request.
"""

from __future__ import annotations

import logging
from typing import List, Union

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model: SentenceTransformer | None = None

    def _ensure_loaded(self) -> None:
        if self._model is None:
            logger.info("Loading embedding model: %s", self.model_name)
            self._model = SentenceTransformer(self.model_name)
            logger.info("Embedding model ready")

    def encode(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """Encode one string or a list of strings into unit-normalised embeddings."""
        self._ensure_loaded()
        single = isinstance(text, str)
        texts = [text] if single else text
        vecs = self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        result = [v.tolist() for v in vecs]
        return result[0] if single else result

    @property
    def dimension(self) -> int:
        self._ensure_loaded()
        return self._model.get_sentence_embedding_dimension()


_service: EmbeddingService | None = None


def get_embedding_service() -> EmbeddingService:
    global _service
    if _service is None:
        from backend.config import settings
        _service = EmbeddingService(settings.embedding_model)
    return _service
