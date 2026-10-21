from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import setting
from app.database import get_db,Base
import pytest
from alembic import command

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:devserapro@localhost:5432/postgres_test' 
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Testing_SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)



# dependency
def overide_get_db(): 
    db = Testing_SessionLocal()
    try:
        yield db
    finally: 
        db.close


@pytest.fixture(scope="module")
def sessions():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Testing_SessionLocal()
    try:
        yield db
    finally: 
        db.close()

@pytest.fixture(scope="module")
def client(sessions):
    def overide_get_db(): 
        try:
            yield sessions
        finally: 
            sessions.close()
    # command.upgrade("head")
    app.dependency_overrides[get_db] = overide_get_db
    yield TestClient(app)
    # command.upgrade("base")