from pydantic import BaseModel


class GeoIP(BaseModel):
    ip: str
    country: str = 'US'
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None
