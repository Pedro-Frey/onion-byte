from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth, leads, icp, usage, health
from api.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(leads.router, prefix=f"{settings.API_V1_STR}/leads", tags=["leads"])
app.include_router(icp.router, prefix=f"{settings.API_V1_STR}/icp", tags=["icp"])
app.include_router(usage.router, prefix=f"{settings.API_V1_STR}/usage", tags=["usage"])
