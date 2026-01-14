from pydantic import BaseModel
from typing import Optional


class OrganizationCreate(BaseModel):
    name: str
    industry: str
    size: int


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[int] = None


class OrganizationResponse(BaseModel):
    id: str
    name: str
    industry: str
    size: int
