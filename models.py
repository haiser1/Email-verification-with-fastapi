from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(5000))
    emailVerified = Column(Boolean, default=False)
    otpCode = Column(String(10))
    otpCodeExpired = Column(DateTime)
