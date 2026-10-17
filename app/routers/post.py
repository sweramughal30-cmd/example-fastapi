
from sqlalchemy import func
from app import oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import models,schemas
from ..database import  get_db
 

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# Fetching  All posts from database
# Endpoint for retrieving posts 
@router.get("/",response_model=List[schemas.Postout])
def get_posts(db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user),limit:int = 10,skip:int = 0,search : Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post , func.count(models.Vote.posts_id).label("votes") ).join(models.Vote,models.Vote.posts_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # for owner related getting posts
    # posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    return  posts




# FETCHING single post from  post gres database
@router.get("/{id}",response_model=schemas.Postout)
def get_post(id:int,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id= %s """, (str(id),))
    # single_post_fetch=cursor.fetchone()
    # single_post_fetch = db.query(models.Post).filter(models.Post.id == id).first()
    single_post_fetch = db.query(models.Post , func.count(models.Vote.posts_id).label("votes") ).join(models.Vote,models.Vote.posts_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not single_post_fetch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} was not found")
    # for owner related getting posts
    # if single_post_fetch.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Your requested action is forbidden or unauthorized")

    return single_post_fetch




# creating posts by getting data send from postman into database of postgres
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def posts_create(post : schemas.PostCreate,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title,content,published) Values(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # my_posts = cursor.fetchone()
    # conn.commit()
    # print(current_user.email)
    my_posts = models.Post(owner_id=current_user.id,**post.dict())
    db.add(my_posts)
    db.commit()
    db.refresh(my_posts)
    return my_posts





# for Deleting post python logic
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
    # delete_postgres=cursor.fetchone()
    # conn.commit()
    delete_postgres_query = db.query(models.Post).filter(models.Post.id==id)
    post_san = delete_postgres_query.first()
    if post_san == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":f"post with id {id} does not exist"})
    if post_san.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Your requested action is forbidden or unauthorized")
    
    delete_postgres_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

# updating the post logic
@router.put("/{id}",response_model=schemas.PostResponse)
def update_posts(id:int,post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET  title=%s,content=%s,published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # update_post= cursor.fetchone()
    # conn.commit()
    update_post_query_obj = db.query(models.Post).filter(models.Post.id==id)
    update_post_query = update_post_query_obj.first()
    if  update_post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"meassage":f"post with id : {id} does not exist"})
    if update_post_query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Your following requested action is forbidden or unauthorized")
    update_post_query_obj.update(post.dict(),synchronize_session=False)
    db.commit()

    return update_post_query_obj.first()
