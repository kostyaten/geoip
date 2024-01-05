import os
from enum import Enum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ('settings', 'LogLevel', 'Environment')


class LogLevel(str, Enum):
    """A class for determining logging levels"""

    trace: str = 'TRACE'
    debug: str = 'DEBUG'
    info: str = 'INFO'
    success: str = 'SUCCESS'
    warning: str = 'WARNING'
    error: str = 'ERROR'
    critical: str = 'CRITICAL'


class Environment(str, Enum):
    """A class for determining environments"""

    development: str = 'DEVELOPMENT'
    stage: str = 'STAGE'
    production: str = 'PRODUCTION'


class Settings(BaseSettings):
    app_name: str = 'GeoIP'

    base_dir: Path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    """ Path to working directory """

    log_name: str = app_name
    """Logger name"""

    log_level: LogLevel = LogLevel.info
    """ Logging level """

    environment: Environment = Environment.production
    """ Environment """

    geo_lite2_city: Path = Path('/usr/local/share/geoip/GeoLite2-City.mmdb')

    model_config = SettingsConfigDict(
        env_file=f"{base_dir}/.env",
        env_file_encoding='utf-8',
        extra='allow',
    )


settings = Settings()
