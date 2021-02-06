from fastapi import FastAPI
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware

from typing import Optional, List

from .routers import cityio
from .routers import namaphio
from .routers import simio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get('/')
async def root():
    """Root
      Returns constant welcome message. Use this when you check the connection.

    Returns:
      Dict[str, str]: Welcome to namaphIO!!
    """
    return {'msg': "welcome to namaphIO!! documents're located baseurl/docs"}

app.include_router(namaphio.router)
app.include_router(simio.router)
app.include_router(cityio.router)
