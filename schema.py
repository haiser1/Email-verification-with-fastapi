from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class EmailVerified(BaseModel):
    email: EmailStr
    otpCode: str

class RefreshOtp(BaseModel):
    email: EmailStr