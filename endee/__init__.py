"""
endee/__init__.py
-----------------
Python wrapper for the Endee vector database.

This package provides the Python-facing API used by the AI Complaint Assistant
backend. It implements a lightweight JSONL-backed vector store with cosine
similarity search, mirroring the Endee HTTP API's core concepts (insert,
search, filter, count).

Part of the fork: https://github.com/endee-io/endee

Public API
----------
    from endee import EndeeDB, Record, SearchResult

    db = EndeeDB("./data/complaints.jsonl")
    db.insert(id, vector, metadata)        -> Record
    db.search(vector, top_k, filter)       -> List[SearchResult]
    db.get(id)                             -> Optional[Record]
    db.delete(id)                          -> bool
    db.count()                             -> int
    db.all()                               -> List[Record]
"""

from .db import EndeeDB, Record, SearchResult

__all__ = ["EndeeDB", "Record", "SearchResult"]
__version__ = "1.3.0"
