import pytest

from geoip.exceptions import (
    NotFoundExceptionError,
)


async def test_not_found():
    with pytest.raises(NotFoundExceptionError):
        raise NotFoundExceptionError
