from datetime import datetime
from typing import Optional

from pydantic import BaseModel,EmailStr
from pydantic.types import conint

#----------------------------------------------------------- 
# USERS
#-----------------------------------------------------------

# Class as a schema blueprint for data validation of User REQUEST

class UserBase(BaseModel):
    email: EmailStr
    password : str
class UserCreate(UserBase):
    pass
# Class as a schema blueprint for data validation of User RESPONSE

class User(BaseModel):
    id:int
    email:EmailStr 
    created_at: datetime
    class Config:
        from_attributes = True
# Class as a schema blueprint for Login process
class UserLogin(BaseModel):
    email : EmailStr
    password : str
# ----------------------------------------------------------------
# Token Section (JWT Mechanics
# ----------------------------------------------------------------
class Token(BaseModel):
    access_token :str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None

#----------------------------------------------------------- 
# POSTS
#----------------------------------------------------------- 

# Class as a schema blueprint for data validation of Post REQUEST
class PostBase(BaseModel):
    title : str 
    content : str
    published: bool = True


class  PostCreate(PostBase):
    pass



# Class as a schema blueprint for data validation of Post RESPONSE

class PostResponse(PostBase):
    id:int
    created_at: datetime
    owner_id : int
    owner:User
    class Config:
        from_attributes = True

class Postout(BaseModel):
    Post : PostResponse
    votes : int
    
    class Config:
        from_attributes = True

class vote(BaseModel):
    post_id : int
    dir : conint(le=1)



