import hashlib
from datetime import datetime, timezone

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.config import settings
from src.database import ENGINE, APIKeys
from src.logging import get_logger

logger = get_logger(__name__)

def get_session():
    session = Session(ENGINE)
    try:
        yield session

    except Exception as e:
        session.rollback()
        raise

    finally:
        session.close()


def authenticate(
    bearer: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    session: Session = Depends(get_session),
):
    # retrieve the api_key
    api_key: str = bearer.credentials

    # validations
    parts: list[str] = api_key.split("-")

    if len(parts) != 2:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid api key format")

    if parts[0] != settings.KEY_PREFIX:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "prefix mismatch")

    # extract the secret
    secret: str = parts[-1]

    # hash the key
    digest: str = hashlib.sha256(secret.encode("utf-8")).hexdigest()

    # match with database
    query = select(APIKeys).where(APIKeys.key_hash == digest)

    # run query
    record = session.scalars(query).first()

    if record is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # update the last_activity field on the database
    record.last_activity = datetime.now(timezone.utc)
    session.commit()

    # record found
    logger.info("User Authenticated", extra={"user_id": record.user_id, "key_id": record.id})
    return {"id": record.id, "user_id": record.user_id}
