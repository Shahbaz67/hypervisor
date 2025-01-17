from pydantic import BaseModel
from typing import Optional
from constants.role import Role


# Pydantic Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    role: str

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = Role.VIEWER.value  # Default role

class UserResponse(BaseModel):
    username: str
    role: str
    # organization: Optional[str]

    class Config:
        from_attributes = True

class OrganizationCreate(BaseModel):
    name: str

class OrganizationResponse(BaseModel):
    name: str
    invite_code: str
    # Define other fields here

    class Config:
        from_attributes = True

class OrganizationJoin(BaseModel):
    invite_code: str

class OrganizationJoinResponse(BaseModel):
    username: str
    organization_name: str
    invite_code: str