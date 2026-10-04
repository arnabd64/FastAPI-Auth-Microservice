from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.dependencies import authenticate, get_session
from src.lifespan import lifespan
from src.router import router

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, allow_headers=["X-User-Id"], allow_methods=["GET", "POST", "DELETE"]
)

app.include_router(router)


@app.get("/", response_class=PlainTextResponse)
def root():
    return "service is ok"


@app.get("/health", response_class=PlainTextResponse)
def healthcheck(session: Session = Depends(get_session)):
    try:
        _ = session.execute(text("SELECT 1;"))

    except Exception as e:
        return PlainTextResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=f"Encountered: {str(e)}",
        )

    return "ok"


@app.get("/protected")
def protected_route(credentials: dict = Depends(authenticate)):
    return credentials
