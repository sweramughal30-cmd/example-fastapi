
from fastapi import FastAPI
from . import models
from .database import  engine,get_db
from .routers import post,user,auth,vote
from .config import setting
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine) 

# fast api instance 
app = FastAPI()
# cors policy solution thing
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Root path

@app.get("/")
def root():
    return {"message": "Hello World swera u can do it"}








