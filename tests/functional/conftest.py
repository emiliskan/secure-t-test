import asyncio
import time
from dataclasses import dataclass

import pytest
import aiohttp
import jwt
from multidict import CIMultiDictProxy

import settings


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
async def auth_header(auth) -> dict:
    return {"Authorization": f"Bearer {auth}"}


@pytest.fixture
async def auth() -> str:
    playload = {
        "sub": settings.USER_ID,
        "exp": time.time() + 100500
    }
    return jwt.encode(playload, settings.JWT_SECRET, settings.JWT_ALGORITHM)


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(autouse=True, scope="session")
async def init_data():
    # TODO: init data
    pass


@pytest.fixture
def make_get_request(session):

    async def inner(method: str, params: dict = None, data: dict = None, headers: dict = None) -> HTTPResponse:
        url = f"http://{settings.API_SERVICE_URL}/{settings.API}/{method}"
        async with session.get(url, params=params, headers=headers, json=data) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_post_request(session):

    async def inner(method: str, data: dict = None, headers: dict = None) -> HTTPResponse:
        url = f"http://{settings.API_SERVICE_URL}/{settings.API}/{method}"
        async with session.post(url, json=data, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_patch_request(session):

    async def inner(method: str, data: dict = None, headers: dict = None) -> HTTPResponse:
        url = f"http://{settings.API_SERVICE_URL}/{settings.API}/{method}"
        async with session.patch(url, json=data, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_delete_request(session):

    async def inner(method: str, headers: dict = None) -> HTTPResponse:
        url = f"http://{settings.API_SERVICE_URL}/{settings.API}/{method}"
        async with session.delete(url, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner