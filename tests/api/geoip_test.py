import httpx
from fastapi import FastAPI


async def test_geoip(client: httpx.AsyncClient, app: FastAPI) -> None:
    response = await client.get(url=app.url_path_for('geoip'))
    assert response.status_code == httpx.codes.OK
    assert response.json().get('ip') == '8.8.8.8'
    assert response.json().get('country')
    assert response.json().get('city') is None
    assert response.json().get('latitude') == 37.751
    assert response.json().get('longitude') == -97.822
    assert response.json().get('timezone') == 'America/Chicago'


async def test_not_found(client: httpx.AsyncClient, app: FastAPI) -> None:
    client.headers.pop('x-real-ip')
    response = await client.get(url=app.url_path_for('geoip'))
    assert response.status_code == httpx.codes.NOT_FOUND
