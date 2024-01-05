from __future__ import annotations

import sys
from contextvars import ContextVar

import loguru
import orjson
from loguru import logger

from .settings import settings, Environment

cxt_request_id: ContextVar[str | None] = ContextVar('request_id', default=None)

__all__ = ('logger', 'cxt_request_id')


def logger_filter_err(record: loguru.Record):
    if record['level'].name in ['WARNING', 'ERROR', 'CRITICAL']:
        return record


def logger_filter_info(record: loguru.Record):
    if record['level'].name in ['TRACE', 'DEBUG', 'INFO', 'SUCCESS']:
        return record


def sink(message):  # pragma: no cover
    name = message.record['name']
    module = message.record['module']
    line = message.record['line']
    level = message.record['level'].name
    subset = {
        'date': message.record['time'].isoformat(),
        'message': message.record['message'],
        'level': level,
        'name': f'{name}:{module}:{line}',
        **message.record.get('extra'),
    }
    line = orjson.dumps(subset).decode('utf-8')
    if level in ['WARNING', 'ERROR', 'CRITICAL']:
        sys.stderr.write(f'{line}\n')
    else:
        sys.stdout.write(f'{line}\n')


logger.remove(0)
if settings.environment in [Environment.production, Environment.stage]:  # pragma: no cover
    logger.add(sink, level=settings.log_level.upper(), serialize=True)
else:
    logger.add(sys.stdout, level=settings.log_level.upper(), filter=logger_filter_info)  # type: ignore
    logger.add(sys.stderr, level=settings.log_level.upper(), filter=logger_filter_err)  # type: ignore
