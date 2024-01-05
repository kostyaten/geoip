from _pytest.logging import LogCaptureFixture
from pytest_mock import MockerFixture

from geoip.logger import logger


def test_logger(caplog: LogCaptureFixture):
    logger.info('test')

    for message in caplog.messages:
        assert message == 'test'

    for record in caplog.records:
        assert record.module == 'logger_test'


def test_environment(mocker: MockerFixture, caplog: LogCaptureFixture):
    logger.info('test info')
    logger.error('test error')
    for record in caplog.records:
        if record.levelname == 'INFO':
            assert record.message == 'test info'
        elif record.levelname == 'ERROR':
            assert record.message == 'test error'
