from pydantic import BaseModel


class RedeployContainerData(BaseModel):
    containerId: str
    newTag: str

    healthCheck: bool = False
    healthcheckTimeout: float = 30