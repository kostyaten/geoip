import geoip2.database
from ..settings import settings
from pydantic import IPvAnyAddress
from . import models


class GeoIP:
    __slots__ = ('services',)

    def __init__(self, services):
        self.services = services

    @staticmethod
    async def detect(*, ip: IPvAnyAddress) -> models.GeoIP:
        with geoip2.database.Reader(settings.geo_lite2_city) as reader:
            response = reader.city(str(ip))

            return models.GeoIP(
                ip=str(ip),
                country=str(response.country.iso_code),
                city=response.city.name,
                latitude=response.location.latitude,
                longitude=response.location.longitude,
                timezone=response.location.time_zone,
            )
