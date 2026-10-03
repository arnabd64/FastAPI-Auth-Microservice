from typing import Annotated, Optional
from uuid import UUID

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.params import Form, Header
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from src.config import settings
from src.dependencies import get_session
from src.schemas.responses import (
    AllKeyQueryResponse,
    DeleteKeyResponse,
    KeyCreationResponse,
)
from src.service import APIKeyService

router = APIRouter(prefix=settings.API_ROUTER_PREFIX, tags=["API Key"])


@router.post("/", response_model=KeyCreationResponse)
def issue_api_key(
    user_id: Annotated[UUID, Header(alias="X-User-Id")],
    display_name: Annotated[str, Form()],
    session: Annotated[Session, Depends(get_session)],
):
    # create service
    service = APIKeyService(session=session, user_id=user_id)

    return service.issue_long_term_key(display_name=display_name)


@router.get("/", response_model=AllKeyQueryResponse)
def list_api_keys(
    user_id: Annotated[UUID, Header(alias="X-User-Id")],
    session: Annotated[Session, Depends(get_session)],
):
    # start service
    service = APIKeyService(user_id=user_id, session=session)

    # get all keys
    return service.fetch_all_keys()


@router.delete("/", response_model=DeleteKeyResponse)
def delete_api_key(
    user_id: Annotated[UUID, Header(alias="X-User-Id")],
    key_id: Annotated[UUID, Form()],
    session: Annotated[Session, Depends(get_session)],
):
    service = APIKeyService(user_id=user_id, session=session)
    success: bool = service.delete_api_key(key_id)
    if not success:
        return DeleteKeyResponse(error=True, message="invalid key_id value")
    return DeleteKeyResponse(error=True, message="Deleted Key")
