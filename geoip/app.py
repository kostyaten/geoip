from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from . import __version__, api
from .logger import logger
from .settings import Environment, settings
from .exceptions import exception_handlers


@asynccontextmanager
async def lifespan(application: FastAPI):
    """
    Lifespan Events
    See - https://fastapi.tiangolo.com/advanced/events/

    :param application: FastAPI
    """
    logger.info(
        f'Startup GeoIP ({__version__}) service',
        extra={
            'environment': settings.environment.lower(),
            'version': __version__,
        },
    )
    yield


app = FastAPI(
    title=settings.app_name,
    description='Microservice for determining country, city, etc. by IP address',
    default_response_class=ORJSONResponse,
    docs_url='/api/' if settings.environment.development == Environment.development else None,
    redoc_url=None,
    openapi_url='/api/v1/openapi.json' if settings.environment.development == Environment.development else None,
    version=__version__,
    debug=True if settings.environment.development == Environment.development else False,
    swagger_ui_parameters={
        'displayRequestDuration': True,
        'persistAuthorization': True,
    },
    lifespan=lifespan,
    exception_handlers=exception_handlers,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# API
app.include_router(api.healthcheck.router, prefix='/api/v1')
app.include_router(api.geoip.router, prefix='/api/v1')
