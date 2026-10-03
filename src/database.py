from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Engine
from sqlmodel import Field, SQLModel, create_engine, func

from src.config import settings


class APIKeys(SQLModel, table=True):
    id: UUID | None = Field(primary_key=True, default_factory=uuid4)
    key_hash: str = Field(unique=True)
    user_id: UUID = Field(index=True)
    created_on: datetime | None = Field(default_factory=func.now)
    last_activity: datetime | None = Field(default=None, nullable=True)


ENGINE: Engine = create_engine(
    settings.DATABASE_URL, echo=settings.DATABASE_CONSOLE_LOGS
)
