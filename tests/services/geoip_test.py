from pathlib import Path

from pydantic import IPvAnyAddress
from pytest_mock import MockerFixture

from geoip.services import Services
from geoip.settings import settings


# Test data, for the GeoLite2-City-Test.mmdb database
# https://github.com/maxmind/MaxMind-DB/blob/main/source-data/GeoIP2-City-Test.json


async def test_detect_jp(services: Services, mocker: MockerFixture) -> None:
    mocker.patch.object(settings, 'geo_lite2_city', Path(f'{settings.base_dir}/tests/GeoLite2-City-Test.mmdb'))

    response = await services.geoip.detect(ip=IPvAnyAddress('2001:218::'))
    assert response.ip == '2001:218::'
    assert response.country == 'JP'
    assert response.latitude == 35.68536
    assert response.longitude == 139.75309
    assert response.timezone == 'Asia/Tokyo'


async def test_detect_de(services: Services, mocker: MockerFixture):
    mocker.patch.object(settings, 'geo_lite2_city', Path(f'{settings.base_dir}/tests/GeoLite2-City-Test.mmdb'))

    response = await services.geoip.detect(ip=IPvAnyAddress('2a02:e800::'))
    assert response.ip == '2a02:e800::'
    assert response.country == 'DE'
    assert response.latitude == 51.5
    assert response.longitude == 10.5
    assert response.timezone == 'Europe/Berlin'
