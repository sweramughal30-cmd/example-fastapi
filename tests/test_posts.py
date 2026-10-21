from typing import List
from app import schemas 
import pytest
def test_get_all_posts(authorize_client,test_posts):
    res = authorize_client.get("/posts/")
    def validate(post):
        return schemas.Postout(**post)
    posts_map = map(validate,res.json())
    posts_list = list(posts_map)
     
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauth_user_all_posts(client,test_posts):
    res= client.get("/posts/")
    assert res.status_code == 401

def test_unauth_user_one_posts(client,test_posts):
    res= client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
def test_get_one_not_exist(authorize_client,test_posts):
    res = authorize_client.get(f"/posts/8888")
    assert res.status_code == 404
def test_get_one_post(authorize_client, test_posts):
    res= authorize_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = schemas.Postout(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title
@pytest.mark.parametrize("title,content,published",[
    ("awesomw title" , "awesomw con", True),
    ("pizza title" , "awesomw paappp", False),
    ("awesomw buildings  title" , "wahoo", True),
])
def test_create_post(authorize_client,test_user,test_posts,title,content,published):
    res = authorize_client.post("/posts/",json={"title":title,"content":content,"published":published})
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published== published
    assert created_post.owner_id == test_user['id']
def test_create_post_def_pub(authorize_client,test_user,test_posts):
    res = authorize_client.post("/posts",json={"title":"awessososoo","content":"content"})
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "awessososoo"
    assert created_post.content == "content"
    assert created_post.published== True
    assert created_post.owner_id == test_user['id']

def test_unauth_user_create_posts(client,test_user,test_posts):
    res = client.post("/posts/",json={"title":"awessososoo","content":"content"})
    assert res.status_code == 401

def test_unauthorize_user_delete_post(client,test_user,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
def test_delete_success(authorize_client,test_user,test_posts):
    res = authorize_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204
def test_delete_post_non_exist(authorize_client,test_user,test_posts):
    res = authorize_client.delete(f"/posts/8000")
    assert res.status_code == 404

def test_delete_post_other_post(authorize_client,test_user,test_posts):
    res = authorize_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
def test_update_post(authorize_client,test_user,test_posts):
    data ={
        "title":"updated title",
        "content":"updated content",
        "id": test_posts[0].id
    }
    res = authorize_client.put(f"/posts/{test_posts[0].id}",json = data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorize_client,test_user,test_posts,test_user2):
    data ={
        "title":"updated title",
        "content":"updated content",
        "id": test_posts[3].id
    }
    res = authorize_client.put(f"/posts/{test_posts[3].id}",json = data)
    assert res.status_code == 403
def test_unauthorize_user_update_post(client,test_user,test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
def test_update_post_non_exist(authorize_client,test_user,test_posts):
    data ={
        "title":"updated title",
        "content":"updated content",
        "id": test_posts[0].id
    }
    res = authorize_client.put(f"/posts/8000",json =data)
    assert res.status_code == 404
