from fastapi import FastAPI, Depends, HTTPException, status
from database import session_local, engine
from schema import UserSchema, LoginUser, EmailVerified, RefreshOtp
from typing import Annotated
from models import Users
from sqlalchemy.orm import Session
import models
import bcrypt
from send_email import send_email_virification, generate_code
import datetime


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

@app.post('/users/register', status_code=status.HTTP_201_CREATED, tags=['Register'])
async def register_user(user_req: UserSchema, db : db_dependency):
    user = db.query(Users).filter(Users.email == user_req.email).first()
    if user:
        raise HTTPException(status_code=400, detail='User already registered') 
    
    otpCodeExpired = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    otp_code = generate_code()
    hash_password = bcrypt.hashpw(user_req.password.encode('utf-8'), bcrypt.gensalt(10))

    add_user = Users(username=user_req.username, email=user_req.email, password=hash_password, otpCode=otp_code, otpCodeExpired=otpCodeExpired)
    db.add(add_user)
    db.commit()
    db.refresh(add_user)
    send_email_virification(user_req.email, otp_code)
    return {"message": "Register user success, check your email for the verification code"}


@app.post('/users/verified', status_code=status.HTTP_200_OK, tags=['Email Verified'])
async def email_verified(user_req: EmailVerified, db: db_dependency):
    user = db.query(Users).filter(Users.email == user_req.email).first()
    if not user:
        raise HTTPException(status_code=400, detail='Your email is not registered')
    
    time_now = datetime.datetime.utcnow()
    if user_req.otpCode != user.otpCode:
        raise HTTPException(status_code=400, detail='Your otp code is invalid')
    
    if time_now > user.otpCodeExpired:
        raise HTTPException(status_code=400, detail='Your otp code is expired')
    db.query(Users).filter(Users.email == user_req.email).update({'emailVerified': True})
    db.commit()
    
    return {'message': 'Your email has been successfully verified'}


@app.post('/users/login', status_code=status.HTTP_200_OK, tags=['Login'])
async def login_user(user_req: LoginUser, db: db_dependency):
    user = db.query(Users).filter(Users.email == user_req.email).first()
    if not user:
        raise HTTPException(status_code=400, detail='Email or password wrong')
    if user.emailVerified == False:
        raise HTTPException(status_code=400, detail='Your email has not been verified')
    
    match_password = bcrypt.checkpw(user_req.password.encode('utf-8'), user.password.encode('utf-8',))

    if not match_password:
        raise HTTPException(status_code=400, detail='Email or password wrong')

    return {'message': "login success"}


@app.post('/users/refresh_otp', status_code=status.HTTP_200_OK, tags=['Refresh OTP'])
async def refresh_otp(user_req: RefreshOtp, db: db_dependency):
    user = db.query(Users).filter(Users.email == user_req.email).first()
    if not user:
        raise HTTPException(status_code=400, detail='Your email is not registered')
    
    if user.emailVerified == True:
        raise HTTPException(status_code=400, detail='Your email is already verified')

    otpCodeExpired = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    otp_code = generate_code()
    db.query(Users).filter(Users.email == user_req.email).update({'otpCode': otp_code, "otpCodeExpired": otpCodeExpired})
    db.commit()
    send_email_virification(user_req.email, otp_code)
    return {"message": "Check your email for the verification code"}








