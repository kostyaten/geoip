from fastapi import APIRouter
from fastapi.requests import Request
from pydantic import IPvAnyAddress

from .. import services
from ..logger import logger
from ..exceptions import NotFoundExceptionError
from . import models

router = APIRouter(
    tags=['Health check'],
)


@router.get(path='/geoip/', name='geoip')
async def geoip(request: Request) -> models.GeoIP:
    service = services.Services()

    ip = request.headers.get('x-real-ip', request.headers.get('x-forwarded-for'))

    if ip is None:
        raise NotFoundExceptionError(message='Invalid IP address', code='invalid_ip_address')

    result = await service.geoip.detect(ip=IPvAnyAddress(ip))

    logger.info(
        f'IP Address: {ip}, country={result.country}, city={result.city or "n/a"}',
        extra={'country': result.country, 'city': result.city or 'n/a'},
    )

    return models.GeoIP.model_validate(result.model_dump())
