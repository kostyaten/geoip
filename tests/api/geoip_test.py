from pathlib import Path

import httpx
from fastapi import FastAPI
from pytest_mock import MockerFixture

from geoip.settings import settings


async def test_geoip(client: httpx.AsyncClient, app: FastAPI, mocker: MockerFixture) -> None:
    mocker.patch.object(settings, 'geo_lite2_city', Path(f'{settings.base_dir}/tests/GeoLite2-City-Test.mmdb'))

    response = await client.get(url=app.url_path_for('geoip'))
    assert response.status_code == httpx.codes.OK

    assert response.json().get('ip') == '2a02:d200::1'
    assert response.json().get('country') == 'FI'
    assert response.json().get('city') is None
    assert response.json().get('latitude') == 64.0
    assert response.json().get('longitude') == 26.0
    assert response.json().get('timezone') == 'Europe/Helsinki'


async def test_not_found(client: httpx.AsyncClient, app: FastAPI, mocker: MockerFixture) -> None:
    mocker.patch.object(settings, 'geo_lite2_city', Path(f'{settings.base_dir}/tests/GeoLite2-City-Test.mmdb'))

    client.headers.pop('x-real-ip')
    response = await client.get(url=app.url_path_for('geoip'))
    assert response.status_code == httpx.codes.NOT_FOUND
