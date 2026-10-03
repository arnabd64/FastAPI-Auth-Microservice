import contextlib

from starlette.types import ASGIApp

from src.database import ENGINE, SQLModel
from sqlalchemy.exc import OperationalError


@contextlib.asynccontextmanager
async def lifespan(app: ASGIApp):
    # initialize all tables\
    # try-except applied when multiple uvicorn workers are
    # executing the same lifespan method
    try:
        SQLModel.metadata.create_all(ENGINE)

    except OperationalError as e:
        if "already exists" not in str(e):
            raise e

    # start application
    yield

    # close database connection
    ENGINE.dispose()
