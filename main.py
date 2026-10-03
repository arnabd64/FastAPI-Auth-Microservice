from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from src.lifespan import lifespan
from src.router import router

app = FastAPI(lifespan=lifespan)

app.include_router(router)


@app.get("/", response_class=PlainTextResponse)
def root():
    return "service is ok"
