import hashlib
import secrets
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from src.config import settings
from src.database import APIKeys
from src.schemas.responses import (
    AllKeyQueryResponse,
    DeleteKeyResponse,
    KeyCreationResponse,
    _SingleKeyQueryResponse,
)


class APIKeyService:
    def __init__(self, session: Session, user_id: UUID):
        self.user_id: UUID = user_id
        self.session = session

    def _long_term_key(self):
        # 1. generate secret key
        secret: str = secrets.token_urlsafe(settings.KEY_LENGTH)

        # 2. generate the SHA-256 Hash of the secret
        digest: str = hashlib.sha256(secret.encode("utf-8")).hexdigest()

        # 3. format the key
        key = f"{settings.KEY_PREFIX}-{secret}"

        return key, digest

    def fetch_all_keys(self):
        # sql query
        query = select(APIKeys).where(APIKeys.user_id == self.user_id)

        # execute
        results = self.session.scalars(query).fetchall()

        # format output
        keys = [
            _SingleKeyQueryResponse(
                id=key.id,
                display_name=key.display_name,
                created_on=key.created_on,
                last_activity=key.last_activity,
            )
            for key in results
        ]
        return AllKeyQueryResponse(error=False, keys_found=len(keys), keys=keys)

    def delete_api_key(self, key_id: UUID):
        # SQL statement to perform the action
        query = delete(APIKeys).where(APIKeys.id == key_id).returning(APIKeys)

        # execute query
        result = self.session.scalars(query).fetchall()
        self.session.commit()

        return len(result) > 0

    def issue_long_term_key(self, display_name: str | None = None):
        """Creates a new persistent API key"""
        # generate key
        key, digest = self._long_term_key()

        # create database record
        api_key = APIKeys(
            key_hash=digest, display_name=display_name, user_id=self.user_id
        )

        # add to database
        self.session.add(api_key)
        self.session.commit()

        return KeyCreationResponse(
            error=False, id=api_key.id, key=key, display_name=display_name
        )
