from fastapi import FastAPI,status,HTTPException,Depends,APIRouter,Response
from .. import schemas,database,models,oauth2
from sqlalchemy.orm import Session
router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)
@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.vote,db: Session = Depends(database.get_db), current_user : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post with id {vote.post_id} does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.posts_id == vote.post_id , models.Vote.users_id == current_user.id )
    found_vote = vote_query.first()
    if (vote.dir == 1 ):
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT,detail = f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(users_id = current_user.id, posts_id = vote.post_id )
        db.add(new_vote)
        db.commit()
        return {"meassage":"Voted successfuly"}
    else:
        if not found_vote:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "Vote does not exist")
        vote_query.delete()
        db.commit()
        return {"messager" : "Vote Deleted successfully"}

        