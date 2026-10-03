from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class KeyCreationResponse(BaseModel):
    error: bool
    id: UUID
    key: str
    display_name: str | None


class _SingleKeyQueryResponse(BaseModel):
    id: UUID
    display_name: str
    created_on: datetime
    last_activity: datetime | None = None


class AllKeyQueryResponse(BaseModel):
    error: bool
    keys_found: int
    keys: list[_SingleKeyQueryResponse]


class DeleteKeyResponse(BaseModel):
    error: bool
    message: str
