from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, organization, cluster, deployment
from core.database.database import engine
from sqlalchemy.orm import Session
from tasks import schedule_deployments, preempt_deployments
import asyncio


app = FastAPI(openapi_url="/hypervisor/openai.json", docs_url="/hypervisor/docs", redoc_url="/hypervisor/redoc")

# Define the lifespan context manager
async def lifespan(app: FastAPI):
    # This block will run at the start of the app
    with Session(engine) as db:
        print("App has started!")
        # Optional: Start the periodic task manually on startup
        # This will kick off the periodic task in the background
        asyncio.create_task(periodic_scheduler(db))  # Start background task

    # Yield control back to FastAPI (this will run the app)
    yield

    # Shutdown logic can go here if needed
    with Session(engine) as db:
        print("App is shutting down!")

# The function that runs every 30 seconds
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

