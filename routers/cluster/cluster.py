from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from models.cluster.cluster import Cluster
from models.user.user import User
from schemas.cluster.cluster import ClusterCreate, ClusterResponse
from core.database.database import get_db
from auth.user import get_current_user
from core.database.database import Base, engine


Base.metadata.create_all(engine)

cluster_router = APIRouter(prefix="/hypervisor/cluster", tags=["Clusters"])

@cluster_router.post("/create", response_model=ClusterResponse)
def create_cluster(cluster: ClusterCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_cluster = Cluster(
        name=cluster.name,
        total_ram=cluster.total_ram,
        total_cpu=cluster.total_cpu,
        total_gpu=cluster.total_gpu,
    )
    db.add(new_cluster)
    db.commit()
    db.refresh(new_cluster)
    return new_cluster