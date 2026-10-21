import pytest
from app import models

@pytest.fixture()
def test_vote(test_posts,sessions,test_user):
    new_vote = models.Vote(posts_id = test_posts[3].id,users_id = test_user['id'])
    sessions.add(new_vote)
    sessions.commit()
def test_vote_on_post(authorize_client,test_posts,test_user2):
    res = authorize_client.post("/vote/",json = {"post_id": test_posts[3].id,"dir":1})
    assert res.status_code == 201  
def test_vote_twice_post(authorize_client,test_posts,test_vote):
    res = authorize_client.post("/vote/",json = {"post_id": test_posts[3].id,"dir":1})
    assert res.status_code == 409  
def test_vote_delete(authorize_client,test_posts,test_vote):
    res = authorize_client.post("/vote/",json = {"post_id": test_posts[3].id,"dir":0})
    assert res.status_code == 201
def test_vote_delete_non_exist(authorize_client,test_posts):
    res = authorize_client.post("/vote/",json = {"post_id": test_posts[3].id,"dir":0})
    assert res.status_code == 404
def test_vote_post_non_exist(authorize_client,test_posts):
    res = authorize_client.post("/vote/",json = {"post_id": 80000,"dir":1})
    assert res.status_code == 404
def test_vote_unauthorize(client,test_posts):
    res = client.post("/vote/",json = {"post_id": test_posts[3].id,"dir":1})
    assert res.status_code == 401