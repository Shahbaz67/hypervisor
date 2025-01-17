from pydantic import BaseModel


class DeploymentCreate(BaseModel):
    name: str
    cluster_id: int
    docker_image: str
    required_ram: int  # In MB
    required_cpu: int  # Number of cores
    required_gpu: int  # Number of GPUs
    priority: int  # Higher value = higher priority

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Deployment A",
                "cluster_id": 1,
                "docker_image": "my_image:latest",
                "required_ram": 1024,
                "required_cpu": 2,
                "required_gpu": 1,
                "priority": 5
            }
        }

class DeploymentResponse(BaseModel):
    id: int
    name: str
    cluster_id: int
    docker_image: str
    required_ram: int  # In MB
    required_cpu: int  # Number of cores
    required_gpu: int  # Number of GPUs
    priority: int  # Higher value = higher priority
    status: str  # e.g., "queued", "running", "completed", "failed"

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Deployment A",
                "cluster_id": 1,
                "docker_image": "my_image:latest",
                "required_ram": 1024,
                "required_cpu": 2,
                "required_gpu": 1,
                "priority": 5,
                "status": "queued"
            }
        }