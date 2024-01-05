from fastapi import APIRouter

router = APIRouter(
    tags=['Health check'],
)


@router.get(path='/healthcheck/', include_in_schema=True, name='healthcheck')
async def healthcheck() -> dict:
    return {'result': 'success'}
