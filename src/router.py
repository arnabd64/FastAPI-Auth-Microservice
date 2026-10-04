from typing import Annotated, Optional
from uuid import UUID

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.params import Form, Header
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from src.config import settings
from src.dependencies import authenticate, get_session
from src.schemas.responses import AllKeyQueryResponse, KeyCreationResponse
from src.service import APIKeyService

router = APIRouter(prefix=settings.API_ROUTER_PREFIX, tags=["API Key"])


@router.post(
    "/", response_model=KeyCreationResponse, status_code=status.HTTP_201_CREATED
)
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


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_api_key(
    user_id: Annotated[UUID, Header(alias="X-User-Id")],
    key_id: Annotated[UUID, Form()],
    session: Annotated[Session, Depends(get_session)],
):
    service = APIKeyService(user_id=user_id, session=session)
    success: bool = service.delete_api_key(key_id)
    if not success:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.head(
    "/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(authenticate)]
)
def validate_api_key():
    return
