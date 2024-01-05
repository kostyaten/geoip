import httpx
from fastapi import FastAPI


async def test_healthcheck(client: httpx.AsyncClient, app: FastAPI) -> None:
    response = await client.get(url=app.url_path_for('healthcheck'))
    assert response.status_code == httpx.codes.OK
