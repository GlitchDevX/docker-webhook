from pydantic import BaseModel


class RedeployImageData(BaseModel):
    imageName: str
    newTag: str = "latest"
    allowNew: bool = True # allows creation of new container if non is existing
    environment: list[str] = []

    healthCheck: bool = False
    healthcheckTimeout: float = 30