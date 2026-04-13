import pytest
from unittest.mock import MagicMock
import sys
from pathlib import Path

# Add project root to sys.path
root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_path))

# -----------------------------------------------------------------------------
# Early Mocking: Prevent heavy ML libraries from loading during tests
# -----------------------------------------------------------------------------
mock_stub = MagicMock()
sys.modules["sentence_transformers"] = mock_stub
sys.modules["transformers"] = mock_stub
sys.modules["torch"] = mock_stub
sys.modules["endee"] = mock_stub

pytest_plugins = ("pytest_asyncio",)

@pytest.fixture(autouse=True)
def mock_app_dependencies(monkeypatch):
    """
    Mock internal service getters to return clean mocks.
    """
    # 1. Mock Database
    mock_db = MagicMock()
    mock_db.count.return_value = 42
    mock_db.search.return_value = []
    monkeypatch.setattr("backend.utils.vector_store.get_db", lambda: mock_db)
    
    # 2. Mock Embedding Service
    mock_emb = MagicMock()
    mock_emb.dimension = 384
    mock_emb.encode.return_value = [0.1] * 384
    monkeypatch.setattr("backend.utils.embeddings.get_embedding_service", lambda: mock_emb)
    
    # 3. Mock LLM Service
    mock_llm = MagicMock()
    mock_llm.generate.return_value = "This is a mock AI response."
    monkeypatch.setattr("backend.utils.llm.get_llm_service", lambda: mock_llm)

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from backend.main import app
    with TestClient(app) as c:
        yield c
