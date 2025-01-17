from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from models.cluster.cluster import Cluster
from models.deployment.deployment import Deployment
from schemas.deployment.deployment import DeploymentCreate, DeploymentResponse
from core.database.database import get_db
from core.database.database import Base, engine
from constants.status import DeploymentStatus


Base.metadata.create_all(engine)

deployment_router = APIRouter(prefix="/hypervisor/deployment", tags=["Deployments"])

@deployment_router.post("/create", response_model=DeploymentResponse)
def create_deployment(deployment: DeploymentCreate, db: Session = Depends(get_db)):
    cluster = db.query(Cluster).filter(Cluster.id == deployment.cluster_id).first()
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")

    if (deployment.required_ram > cluster.total_ram - cluster.allocated_ram or
        deployment.required_cpu > cluster.total_cpu - cluster.allocated_cpu or
        deployment.required_gpu > cluster.total_gpu - cluster.allocated_gpu):
        deployment_status = DeploymentStatus.QUEUED.value
    else:
        deployment_status = DeploymentStatus.RUNNING.value
        cluster.allocated_ram += deployment.required_ram
        cluster.allocated_cpu += deployment.required_cpu
        cluster.allocated_gpu += deployment.required_gpu

    deployment_dict = deployment.model_dump()
    deployment_dict["status"] = deployment_status 

    new_deployment = Deployment(**deployment_dict)
    
    db.add(new_deployment)
    db.commit()
    db.refresh(new_deployment)
    return new_deployment