from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import setting
from app.database import get_db,Base
import pytest
from app.oauth2 import create_access_token
from alembic import command
from app import models

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
        db.close()


@pytest.fixture(scope="function")
def sessions():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Testing_SessionLocal()
    try:
        yield db
    finally: 
        db.close()

@pytest.fixture(scope="function")
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
@pytest.fixture
def test_user(client):
    user_data = {"email":"serasshhhs@gmail.com",
    "password":"1234455"}
    res = client.post("/users/",json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email":"serasshhh1111s@gmail.com",
    "password":"1234455"}
    res = client.post("/users/",json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture

def token(test_user):
    return create_access_token({"user_id": test_user['id']})
@pytest.fixture


def authorize_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
@pytest.fixture
def test_posts(test_user,sessions,test_user2):
    posts_data = [{
        "title":"one T",
        "content":"one C",
        "owner_id":test_user['id']
    },
    {
        "title":"Two T",
        "content":"two C",
        "owner_id":test_user['id']
    },
    {
        "title":"3 T",
        "content":"3 C",
        "owner_id":test_user['id']
    },    {
        "title":"4 T",
        "content":"4 C",
        "owner_id":test_user2['id']
    }
    ]
    def create_post_model(post):
        return models.Post(**post)
    
    posts_map = map(create_post_model,posts_data)
    posts = list(posts_map) 
    sessions.add_all(posts)
    # sessions.add_all([
    #     models.Post(title = "one T",content="one C",owner_id=test_user['id']),
    #     models.Post(title = "Two T",content="two C",owner_id=test_user['id']),
    #     models.Post(title = "3 T",content="3 C",owner_id=test_user['id']),
    # ])
    sessions.commit()

    posts = sessions.query(models.Post).all()
    return posts