from pydantic import BaseModel

class ClusterCreate(BaseModel):
    name: str
    total_ram: int  # In MB
    total_cpu: int  # Number of cores
    total_gpu: int  # Number of GPUs

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Cluster A",
                "total_ram": 16384,
                "total_cpu": 8,
                "total_gpu": 2
            }
        }

class ClusterResponse(BaseModel):
    id: int
    name: str
    total_ram: int  # In MB
    total_cpu: int  # Number of cores
    total_gpu: int  # Number of GPUs
    allocated_ram: int  # In MB
    allocated_cpu: int  # Number of cores
    allocated_gpu: int  # Number of GPUs

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Cluster A",
                "total_ram": 16384,
                "total_cpu": 8,
                "total_gpu": 2,
                "allocated_ram": 4096,
                "allocated_cpu": 2,
                "allocated_gpu": 1
            }
        }