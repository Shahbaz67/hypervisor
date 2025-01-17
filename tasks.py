from sqlalchemy.orm import Session
from models.cluster.cluster import Cluster
from models.deployment.deployment import Deployment


def schedule_deployments(db: Session):
    queued_deployments = db.query(Deployment).filter(Deployment.status == "queued").order_by(Deployment.priority.desc()).all()

    for deployment in queued_deployments:
        cluster = db.query(Cluster).filter(Cluster.id == deployment.cluster_id).first()
        if (deployment.required_ram <= cluster.total_ram - cluster.allocated_ram and
            deployment.required_cpu <= cluster.total_cpu - cluster.allocated_cpu and
            deployment.required_gpu <= cluster.total_gpu - cluster.allocated_gpu):
            
            # Allocate resources
            cluster.allocated_ram += deployment.required_ram
            cluster.allocated_cpu += deployment.required_cpu
            cluster.allocated_gpu += deployment.required_gpu

            # Update deployment status
            deployment.status = "running"
            db.commit()
            
def preempt_deployments(db: Session):
    queued_deployments = db.query(Deployment).filter(Deployment.status == "queued").order_by(Deployment.priority.desc()).all()

    for deployment in queued_deployments:
        cluster = db.query(Cluster).filter(Cluster.id == deployment.cluster_id).first()
        if cluster:
            running_deployments = db.query(Deployment).filter(
                Deployment.cluster_id == cluster.id, Deployment.status == "running"
            ).order_by(Deployment.priority).all()

            for running_deployment in running_deployments:
                if (deployment.required_ram <= cluster.total_ram - cluster.allocated_ram + running_deployment.required_ram and
                    deployment.required_cpu <= cluster.total_cpu - cluster.allocated_cpu + running_deployment.required_cpu and
                    deployment.required_gpu <= cluster.total_gpu - cluster.allocated_gpu + running_deployment.required_gpu):
                    
                    # Deallocate resources from the lower-priority deployment
                    cluster.allocated_ram -= running_deployment.required_ram
                    cluster.allocated_cpu -= running_deployment.required_cpu
                    cluster.allocated_gpu -= running_deployment.required_gpu

                    running_deployment.status = "queued"
                    break

            # Allocate resources for the high-priority deployment
            cluster.allocated_ram += deployment.required_ram
            cluster.allocated_cpu += deployment.required_cpu
            cluster.allocated_gpu += deployment.required_gpu
            deployment.status = "running"
            db.commit()