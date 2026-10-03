import contextlib

from starlette.types import ASGIApp

from src.database import ENGINE, SQLModel


@contextlib.asynccontextmanager
async def lifespan(app: ASGIApp):
    # initialize all tables
    SQLModel.metadata.create_all(ENGINE)

    # start application
    yield

    # close database connection
    ENGINE.dispose()
