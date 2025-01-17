from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, organization
from core.database.database import engine
from sqlalchemy.orm import Session
from tasks import schedule_deployments, preempt_deployments
import asyncio


app = FastAPI(openapi_url="/hypervisor/openai.json", docs_url="/hypervisor/docs", redoc_url="/hypervisor/redoc")


#Routers
app.include_router(users.user_router)
app.include_router(organization.organization_router)

