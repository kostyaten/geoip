from typing import AsyncGenerator

import httpx
import pytest
from fastapi import FastAPI
from geoip.app import app as application
from asgi_lifespan import LifespanManager


@pytest.fixture()
async def app() -> AsyncGenerator[FastAPI, None]:
    async with LifespanManager(application):
        yield application


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[httpx.AsyncClient, None]:
    headers = {'x-real-ip': '2a02:d200::1'}

    async with httpx.AsyncClient(app=app, base_url='http://localhost.local', headers=headers) as client:
        try:
            yield client
        finally:
            await client.aclose()
