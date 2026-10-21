from app import schemas
# from .database import client,sessions
import pytest
from jose import jwt
from app.config import setting


# def test_root(client):
#     res = client.get('/')
#     print(res.json().get("message")) 
#     assert res.json().get('message') == 'bind mount works!ddddd!!!!!'
    # assert res.status_code == 200
def test_create_user(client):
    res = client.post("/users/",json={"email":"sera@gmail.com","password":"1234"})

    new_user = schemas.User(**res.json())
    assert new_user.email == "sera@gmail.com"
    assert res.status_code == 201
def test_user_login(client, test_user):
    res = client.post("/login",data={"username": test_user['email'],"password":test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,setting.secret_key,algorithms=[setting.algorithm])
    id = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type =="bearer"
    assert res.status_code == 200 
@pytest.mark.parametrize("email,password,status_code",[
    ("serawrong@gmail.com","1234",403),
    ("sera@gmail.com","wrong1234",403),
    ("wrong@gmail.com","wrong1234",403),
    (None,"1234",422),
    ("sera@gmail.com",None,422),
])
def test_incorrect_login(test_user,client,email,password,status_code):
    res = client.post("/login",data={"username": email,"password":password})

    assert res.status_code == status_code

    # assert res.json().get('detail') == 'Invalid Credentials '