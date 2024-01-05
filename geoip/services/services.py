from .geoip import GeoIP

__all__ = ('Services',)


class Services(object):
    __slots__ = ('geoip',)

    def __init__(self):
        self.geoip = GeoIP(self)
