import uuid
from datetime import date, datetime
from typing import List

from pydantic import BaseModel


class Project(BaseModel):
    uid: uuid.UUID
    name: str
    description: str | None
    adress: str | None
    telephone: str | None
    created_at: datetime
    update_at: datetime


class ProjectCreateModel(BaseModel):
    name: str
    description: str | None
    adress: str | None
    telephone: str | None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "sample name",
                "description": "sample description",
                "adress": "sample adress",
                "telephone": "sample telephone",
            }
        }
    }


class ProjectUpdateModel(BaseModel):
    name: str | None
    description: str | None
    adress: str | None
    telephone: str | None

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "sample name",
                "description": "sample description",
                "adress": "sample adress",
                "telephone": "sample telephone",
            }
        }
    }


class ProjectRead(Project):
    pass