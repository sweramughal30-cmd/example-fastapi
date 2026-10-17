
from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils
from ..database import  engine,get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# USERS TABLE DATA FOR DATABASE
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.User)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    # hash the password
    hashed_password = utils.hash_pass(user.password)
    user.password = hashed_password
    user_created = models.User(**user.dict())
    db.add(user_created)
    db.commit()
    db.refresh(user_created)
    return user_created  
@router.get("/{id}",response_model=schemas.User)
def get_user(id:int,db:Session=Depends(get_db)):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":f"the user with id:{id} was not found"})
    return user