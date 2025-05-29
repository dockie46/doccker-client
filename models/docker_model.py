from typing import List
from pydantic import BaseModel


class DockerContainer(BaseModel):
    id: str
    name: str

    def __str__(self):
        return f"DockerContainer(id={self.id}, name={self.name})"


class DockerImage(BaseModel):
    id: str
    name: str

    def __str__(self):
        return f"DockerImage(id={self.id}, name={self.name})"


class ContainerStats(BaseModel):
    name: str
    memory_usage: float


class PredictionResult(BaseModel):
    data: List[ContainerStats]
    predicted_next: float
    summary: str
