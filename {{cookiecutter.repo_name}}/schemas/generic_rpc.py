import math
from typing import Any, Dict, List

from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict)


class DeleteRequest(BaseModel):
    {{cookiecutter.business_key}}: str = Field(default_factory=str)


class GetRequest(BaseModel):
    {{cookiecutter.business_key}}: str = Field(default_factory=str)


class ItemResponse(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict)


class ListRequest(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict)
    limit: int = Field(default=math.inf, ge=0)
    offset: int = Field(default=0, ge=0)
    ordering: List[str] = Field(default=["id"])


class ListResponse(BaseModel):
    data: List[Dict[str, Any]] = Field(default_factory=list)
    count: int = Field(default_factory=int)


class ResultResponse(BaseModel):
    result: bool = Field(default_factory=bool)


class UpdateRequest(BaseModel):
    {{cookiecutter.business_key}}: str = Field(default_factory=str)
    data: Dict[str, Any] = Field(default_factory=dict)


class BulkCreateRequest(BaseModel):
    data: List[Dict[str, Any]] = Field(default_factory=list)
