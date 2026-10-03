import hashlib
import secrets
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from src.config import settings
from src.database import APIKeys


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

    def _create_database_entry(self, digest: str):
        # create database entry
        key = APIKeys(key_hash=digest, user_id=self.user_id)

        self.session.add(key)
        self.session.commit()

        return key.id

    def _fetch_all_keys(self):
        # sql query
        query = select(APIKeys).where(APIKeys.user_id == self.user_id)

        # execute
        result = self.session.scalars(query).fetchall()

        return result

    def _delete_api_key(self, key_id: UUID):
        # SQL statement to perform the action
        query = delete(APIKeys).where(APIKeys.id == key_id).returning(APIKeys)

        # execute query
        result = self.session.scalars(query).fetchall()
        self.session.commit()

        return len(result) > 0

    def issue_long_term_key(self):
        # generate key
        key, digest = self._long_term_key()

        # add to database
        key_id = self._create_database_entry(digest)

        return key_id
