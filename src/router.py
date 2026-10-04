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
    """
    ## Description
    Generates a new API Key against an User ID

    ## Inputs
    1. `user_id`: User's unique identifier
    2. `display_name`: Name of the API Key that will be used for better identification of the key.

    ## Responses
    - `201`: Successfully created the key
    """
    # create service
    service = APIKeyService(session=session, user_id=user_id)

    return service.issue_long_term_key(display_name=display_name)


@router.get("/", response_model=AllKeyQueryResponse)
def list_api_keys(
    user_id: Annotated[UUID, Header(alias="X-User-Id")],
    session: Annotated[Session, Depends(get_session)],
):
    """
    ## Description
    Retrieves all the API keys against an user's id

    ## Inputs
    1. `user_id`: User's unique identifier

    ## Responses
    - `200`: Returns the details of all keys. If no key is found then an empty array is sent.
    """
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
    """
    ## Description
    Deletes an API Key

    ## Inputs
    1. `user_id`: User's unique identifier
    2. `key_id`: The key's unique identifier

    ## Responses
    - `204`: Successfully deleted api key
    - `401`: Key not found
    """
    service = APIKeyService(user_id=user_id, session=session)
    success: bool = service.delete_api_key(key_id)
    if not success:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.head(
    "/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(authenticate)]
)
def validate_api_key():
    """
    ## Description
    Validates an API Key

    ## Inputs
    1. Authorization Bearer Token: the API key to validate

    ## Response
    - `204`: Valid API Key
    - `401`: Invalid or Unauthorized
    """
    return
