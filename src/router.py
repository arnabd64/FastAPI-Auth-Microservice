from typing import Annotated
from uuid import UUID

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.params import Form, Header
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from src.config import settings
from src.dependencies import get_session
from src.service import APIKeyService

router = APIRouter(prefix=settings.API_ROUTER_PREFIX, tags=["API Key"])


@router.post("/")
def issue_api_key(
    user_id: Annotated[UUID, Header(alias="X-User-Id")],
    session: Annotated[Session, Depends(get_session)],
):
    # create service
    service = APIKeyService(session=session, user_id=user_id)

    key_id = service.issue_long_term_key()

    return {"key_id": key_id}


@router.get("/")
def list_api_keys(
    user_id: Annotated[UUID, Header(alias="X-User-Id")],
    session: Annotated[Session, Depends(get_session)],
):
    # start service
    service = APIKeyService(user_id=user_id, session=session)

    # get all keys
    keys = service._fetch_all_keys()

    return {"data": keys}


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_api_key(
    user_id: Annotated[UUID, Header(alias="X-User-Id")],
    key_id: Annotated[UUID, Form()],
    session: Annotated[Session, Depends(get_session)],
):
    service = APIKeyService(user_id=user_id, session=session)
    success: bool = service._delete_api_key(key_id)
    if not success:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
