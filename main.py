from fastapi import FastAPI, Depends, HTTPException, status
from database import session_local, engine
from schema import UserSchema, LoginUser
from typing import Annotated
from models import Users
from sqlalchemy.orm import Session
import models
import bcrypt
from send_email import send_email_virification


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_session_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_session_db)]

@app.get('/', tags=['Root'])
async def root():
    return {"message": "Hello World!"}

@app.post('/register/users', status_code=status.HTTP_201_CREATED, tags=['register'])
async def register_user(user_req: UserSchema, db : db_dependency):
    user = db.query(Users).filter(Users.email == user_req.email).first()
    if user:
        raise HTTPException(status_code=400, detail='User already registered') 
    hash_password = bcrypt.hashpw(user_req.password.encode('utf-8'), bcrypt.gensalt(10))

    add_user = Users(username=user_req.username, email=user_req.email, password=hash_password)
    
    # code = '12345'
    # send_email_virification(user_req.email, code)
    db.add(add_user)
    db.commit()
    db.refresh(add_user)
    return {"message": "Register user success"}

@app.post('/login/users', status_code=status.HTTP_200_OK, tags=['login'])
async def login_user(user_req: LoginUser, db: db_dependency):
    user = db.query(Users).filter(Users.email == user_req.email).first()
    if not user:
        raise HTTPException(status_code=400, detail='Email or password wrong')
    
    match_password = bcrypt.checkpw(user_req.password.encode('utf-8'), user.password.encode('utf-8',))

    if not match_password:
        raise HTTPException(status_code=400, detail='Email or password wrong')

    return {'message': "login success"}







