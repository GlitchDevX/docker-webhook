from fastapi import FastAPI

from src.docker_webhook.app.middleware.cors import Cors
from src.docker_webhook.app.middleware.secret_check import SecretCheck
from .routers import containers, redeploy

app = FastAPI()

app.include_router(containers.router)
app.include_router(redeploy.router)

app.add_middleware(SecretCheck)
app.add_middleware(Cors)