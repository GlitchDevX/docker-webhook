from fastapi import FastAPI
from .routers import containers, redeploy

app = FastAPI()

app.include_router(containers.router)
app.include_router(redeploy.router)
