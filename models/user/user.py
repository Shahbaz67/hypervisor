from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from core.database.database import Base
from core.config import settings
from passlib.context import CryptContext
import uuid
from constants.role import Role
from sqlalchemy.ext.declarative import declarative_base


# Models
class Organization(Base):
    __tablename__ = "organizations"
    name: str = Column(String, primary_key=True, unique=True, nullable=False)
    invite_code: str = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    users = relationship("User", back_populates="organization")


class User(Base):
    __tablename__ = "users"  # The table name in the database
    username: str = Column(String, primary_key=True, unique=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    role: str = Column(String, nullable=False)
    organization_name: str = Column(String, ForeignKey("organizations.name"), nullable=True)
    organization = relationship("Organization", back_populates="users")



