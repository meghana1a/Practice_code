from pydantic import BaseModel, Field
from typing import Optional


class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=2)
    industry: str = Field(..., min_length=2)
    size: int = Field(..., ge=1)


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[int] = Field(None, ge=1)


class OrganizationResponse(BaseModel):
    id: str
    name: str
    industry: str
    size: int
