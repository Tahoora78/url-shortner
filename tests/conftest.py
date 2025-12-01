import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import main, database, models, crud


@pytest.fixture(scope="session")
def engine(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("data") / "test_shortener.db"
    db_url = f"sqlite:///{db_path}"

    engine = create_engine(db_url, connect_args={"check_same_thread": False})

    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    database.engine = engine
    database.SessionLocal = TestSessionLocal
    crud.SessionLocal = TestSessionLocal

    class DummyLock:
        def __init__(self, *a, **kw):
            self._acquired = True

        def acquire(self, blocking=True):
            return True

        def release(self):
            return None

    class DummyRedis:
        def lock(self, *a, **kw):
            return DummyLock()

    crud.redis_client = DummyRedis()

    models.Base.metadata.create_all(bind=engine)

    crud.KEY_BUFFER = [f"CODE{i:04d}" for i in range(1, 1000)]

    yield engine

    try:
        engine.dispose()
    except Exception:
        pass

    try:
        os.remove(str(db_path))
    except Exception:
        pass


@pytest.fixture()
def client(engine):
    client = TestClient(main.app)
    yield client
