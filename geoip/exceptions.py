from typing import TypeAlias, Callable, Any, Coroutine, TypeVar

from fastapi import HTTPException, status
from .logger import logger

__all__ = (
    'exception_handlers',
    'NotFoundExceptionError',
)

from fastapi.responses import ORJSONResponse

from starlette.requests import Request
from starlette.responses import Response


class MainExceptionError(HTTPException):
    def __init__(self, message: str, code: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.code = code
        self.status_code = status_code


class NotFoundExceptionError(MainExceptionError):
    """Object not found"""

    def __init__(
        self,
        message: str = 'Object not found',
        code: str = 'object_not_found',
        status_code: int = status.HTTP_404_NOT_FOUND,
    ):
        super().__init__(message=message, code=code, status_code=status_code)


ExceptionType = TypeVar('ExceptionType')


def exception(exc_type: ExceptionType):
    async def wrapper(
        request: Request,
        err: NotFoundExceptionError,
    ):
        logger.error(f'{err.message}', extra={'message': err.message, 'code': err.code})
        return ORJSONResponse(
            status_code=err.status_code,
            content={
                'error': {
                    'message': err.message,
                    'code': err.code,
                },
            },
        )

    return wrapper


ExceptionHandlers: TypeAlias = (
    dict[int | type[Exception], Callable[[Request, Any], Coroutine[Any, Any, Response]]] | None
)

exception_handlers: ExceptionHandlers = {
    NotFoundExceptionError: exception(NotFoundExceptionError),
}
