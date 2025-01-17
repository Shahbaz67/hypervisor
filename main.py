from fastapi import FastAPI
from routers import users, organization, cluster, deployment
from core.database.database import engine
from sqlalchemy.orm import Session
from tasks import schedule_deployments, preempt_deployments
import asyncio


app = FastAPI(openapi_url="/hypervisor/openai.json", docs_url="/hypervisor/docs", redoc_url="/hypervisor/redoc")

# lifespan context manager
async def lifespan(app: FastAPI):
    with Session(engine) as db:  #runs at the start of the app
        print("App has started!")
        asyncio.create_task(periodic_scheduler(db))  # Start background periodic task

    yield  # control back to FastAPI app

    with Session(engine) as db:  # shutdown logic
        print("App is shutting down!")

# function runs every 30 seconds
async def periodic_scheduler(db: Session):
    while True:
        schedule_deployments(db)
        preempt_deployments(db)
        await asyncio.sleep(30)  # Sleep for 30 seconds


#Routers
app.include_router(users.user_router)
app.include_router(organization.organization_router)
app.include_router(cluster.cluster_router)
app.include_router(deployment.deployment_router)

