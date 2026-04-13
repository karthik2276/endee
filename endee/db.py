"""
endee/db.py
-----------
Core Endee vector database.

Public API
----------
    db = EndeeDB(path)
    db.insert(id, vector, metadata)        -> Record
    db.search(vector, top_k, filter)       -> List[SearchResult]
    db.get(id)                             -> Optional[Record]
    db.delete(id)                          -> bool
    db.count()                             -> int
    db.all()                               -> List[Record]

Storage: JSONL file, one JSON object per line.
Search:  Cosine similarity (brute-force, works well up to ~100 k records).
"""

from __future__ import annotations

import json
import math
import os
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class Record:
    """A stored embedding record."""
    id: str
    vector: List[float]
    metadata: Dict[str, Any]
    created_at: float = field(default_factory=time.time)


@dataclass
class SearchResult:
    """One result returned by EndeeDB.search()."""
    id: str
    score: float                  # cosine similarity 0-1 (higher = more similar)
    metadata: Dict[str, Any]
    created_at: float


# ---------------------------------------------------------------------------
# Math helpers
# ---------------------------------------------------------------------------

def _dot(a: List[float], b: List[float]) -> float:
    return sum(x * y for x, y in zip(a, b))

def _norm(v: List[float]) -> float:
    return math.sqrt(sum(x * x for x in v))

def _cosine(a: List[float], b: List[float]) -> float:
    na, nb = _norm(a), _norm(b)
    if na == 0.0 or nb == 0.0:
        return 0.0
    return _dot(a, b) / (na * nb)

def _unit(v: List[float]) -> List[float]:
    n = _norm(v)
    if n == 0.0:
        return v
    return [x / n for x in v]


# ---------------------------------------------------------------------------
# EndeeDB
# ---------------------------------------------------------------------------

class EndeeDB:
    """
    Persistent vector database backed by a JSONL file.

    Example
    -------
    >>> db = EndeeDB("data/complaints.jsonl")
    >>> db.insert("c1", embedding, {"text": "...", "category": "billing"})
    >>> results = db.search(query_embedding, top_k=5)
    >>> for r in results:
    ...     print(r.score, r.metadata["text"])
    """

    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._index: Dict[str, Record] = {}
        self._load()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load(self) -> None:
        """Read all records from the JSONL file into memory."""
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    rec = Record(**obj)
                    self._index[rec.id] = rec
                except Exception:
                    continue   # skip corrupt lines

    def _save(self) -> None:
        """Flush the full in-memory index back to disk (rewrite)."""
        with self.path.open("w", encoding="utf-8") as fh:
            for rec in self._index.values():
                fh.write(json.dumps(asdict(rec)) + "\n")

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def insert(
        self,
        id: Optional[str],
        vector: List[float],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Record:
        """
        Store a new embedding.

        Parameters
        ----------
        id       : unique record ID; a UUID4 is generated if None
        vector   : list of floats (embedding)
        metadata : arbitrary key-value pairs stored alongside the vector
        """
        if id is None:
            id = str(uuid.uuid4())
        if metadata is None:
            metadata = {}
        rec = Record(id=id, vector=vector, metadata=metadata)
        self._index[id] = rec
        self._save()
        return rec

    def get(self, id: str) -> Optional[Record]:
        """Return the record with the given ID, or None."""
        return self._index.get(id)

    def delete(self, id: str) -> bool:
        """Delete a record. Returns True if it existed."""
        if id in self._index:
            del self._index[id]
            self._save()
            return True
        return False

    def count(self) -> int:
        """Number of stored vectors."""
        return len(self._index)

    def all(self) -> List[Record]:
        """Return all records (unordered)."""
        return list(self._index.values())

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
        self,
        vector: List[float],
        top_k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """
        Find the top-K most similar vectors using cosine similarity.

        Parameters
        ----------
        vector  : query embedding
        top_k   : number of results to return
        filter  : optional metadata equality filter
                  e.g. {"category": "billing"} restricts to that category

        Returns
        -------
        List[SearchResult] sorted by descending similarity score.
        """
        if not self._index:
            return []

        q = _unit(vector)
        scored: List[tuple[float, Record]] = []

        for rec in self._index.values():
            # Apply optional metadata filter
            if filter:
                if not all(rec.metadata.get(k) == v for k, v in filter.items()):
                    continue
            score = _cosine(q, _unit(rec.vector))
            scored.append((score, rec))

        scored.sort(key=lambda t: t[0], reverse=True)

        return [
            SearchResult(
                id=rec.id,
                score=round(score, 6),
                metadata=rec.metadata,
                created_at=rec.created_at,
            )
            for score, rec in scored[:top_k]
        ]
