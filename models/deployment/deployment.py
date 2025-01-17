from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from core.database.database import Base
from constants.status import DeploymentStatus

class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cluster_id = Column(Integer, ForeignKey("clusters.id"), nullable=False)
    docker_image = Column(String, nullable=False)
    required_ram = Column(Integer, nullable=False)  # Resource requirements
    required_cpu = Column(Integer, nullable=False)
    required_gpu = Column(Integer, nullable=False)
    priority = Column(Integer, nullable=False)  # Higher number = higher priority
    status = Column(SQLAlchemyEnum(DeploymentStatus), default=DeploymentStatus.PENDING.value)

    cluster = relationship("Cluster", back_populates="deployments")