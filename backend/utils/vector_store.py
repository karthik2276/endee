"""
backend/utils/vector_store.py
------------------------------
Singleton wrapper around EndeeDB.

Endee is imported from the /endee directory at the project root
(the locally cloned endee-io/endee repository).
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

# Project root = two levels up from this file (backend/utils/vector_store.py)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Ensure project root is on sys.path so `import endee` resolves
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from endee import EndeeDB  # noqa: E402

_db: EndeeDB | None = None


def get_db() -> EndeeDB:
    """Return (or lazily create) the module-level EndeeDB singleton."""
    global _db
    if _db is None:
        # Import here to avoid circular imports at module load time
        from backend.config import settings

        db_path = Path(settings.endee_db_path)
        if not db_path.is_absolute():
            db_path = PROJECT_ROOT / db_path

        logger.info("Opening Endee DB at: %s", db_path)
        _db = EndeeDB(str(db_path))
        logger.info("Endee DB ready — %d records", _db.count())
    return _db
