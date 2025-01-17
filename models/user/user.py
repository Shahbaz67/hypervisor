from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database.database import Base
import uuid


# Models
class Organization(Base):
    __tablename__ = "organizations"
    name: str = Column(String, primary_key=True, unique=True, nullable=False)
    invite_code: str = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    users = relationship("User", back_populates="organization")


class User(Base):
    __tablename__ = "users"
    username: str = Column(String, primary_key=True, unique=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    role: str = Column(String, nullable=False)
    organization_name: str = Column(String, ForeignKey("organizations.name"), nullable=True)
    organization = relationship("Organization", back_populates="users")



