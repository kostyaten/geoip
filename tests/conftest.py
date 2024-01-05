from typing import AsyncGenerator, Generator
from loguru import logger

from _pytest.logging import LogCaptureFixture
from pytest import fixture
from geoip.services import Services


@fixture(name='services')
async def services_fixture() -> AsyncGenerator[Services, None]:
    services = Services()
    yield services


@fixture
def caplog(caplog: LogCaptureFixture) -> Generator[LogCaptureFixture, None, None]:
    handler_id = logger.add(
        caplog.handler,
        format='{message}',
        level=0,
        filter=lambda record: record['level'].no >= caplog.handler.level,
        enqueue=False,
    )
    yield caplog
    logger.remove(handler_id)
