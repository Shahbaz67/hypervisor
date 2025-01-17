from typing import List
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from schemas.user.user import OrganizationCreate, OrganizationResponse, OrganizationJoin, OrganizationJoinResponse
from auth.user import require_role, get_current_user
from models.user.user import User, Organization
from core.database.database import Base, engine, get_db
from sqlalchemy.orm import Session
import uuid


Base.metadata.create_all(engine)

organization_router = APIRouter(prefix="/hypervisor/organization", tags=["Organization"])

@organization_router.post("/create", response_model=OrganizationResponse)
def create_organization(org: OrganizationCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role("Admin"))):
    # Check if organization name already exists
    if db.query(Organization).filter(Organization.name == org.name).first():
        raise HTTPException(status_code=400, detail="Organization name already exists")

    invite_code = str(uuid.uuid4())
    new_org = Organization(name=org.name, invite_code=invite_code)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    return OrganizationResponse(
        name=new_org.name,
        invite_code=invite_code
    )


@organization_router.get("/all", response_model=List[OrganizationResponse])
def get_all_organizations(db: Session = Depends(get_db)):
    organizations = db.query(Organization).all()  # Query all organizations
    if not organizations:
        raise HTTPException(status_code=404, detail="No organizations found")
    return organizations


@organization_router.post("/join", response_model=OrganizationJoinResponse)
def join_organization(org: OrganizationJoin, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user is None:
        raise HTTPException(status_code=400, detail="Not authenticated")
    
    orgDb = db.query(Organization).filter(Organization.invite_code == org.invite_code).first()
    current_user.organization_name = orgDb.name

    return OrganizationJoinResponse(
        username=current_user.username,
        organization_name=orgDb.name,
        invite_code=orgDb.invite_code
    )

