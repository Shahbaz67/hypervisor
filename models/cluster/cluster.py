
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database.database import Base


class Cluster(Base):
    __tablename__ = "clusters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    total_ram = Column(Integer, nullable=False)  # In MB
    total_cpu = Column(Integer, nullable=False)  # In cores
    total_gpu = Column(Integer, nullable=False)  # Number of GPUs
    allocated_ram = Column(Integer, default=0)   # Allocated resources
    allocated_cpu = Column(Integer, default=0)
    allocated_gpu = Column(Integer, default=0)
    deployments = relationship("Deployment", back_populates="cluster")