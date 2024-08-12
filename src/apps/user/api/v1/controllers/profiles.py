import logging
from typing import Union

from fastapi import APIRouter
from starlette.responses import JSONResponse, Response

from api.dependencies import UserDep, ProfileUOWDep, ProfileServiceDep
from common.schemas.responses import mixins as response
from modules.schemas.profile import ProfileResponseSchema

profile = APIRouter(prefix="/api/v1/Profile", tags=["Profile"])


@profile.get(
    path="/",
    dependencies=...,
    summary="Получение профиля пользователя",
    responses={
        200: {"model": ProfileResponseSchema},
        401: {"model": response.UnauthorizedResponseSchema},
        403: {"model": response.ForbiddenResponseSchema},
        404: {"model": response.NotFoundResponseSchema},
        500: {"model": response.ServerErrorResponseSchema},
    },
)
async def get_user_info(
        current_user: UserDep, uow: ProfileUOWDep, service: ProfileServiceDep,
) -> Union[ProfileResponseSchema, Response]:
    """Контроллер получения информации профиля пользователя."""
    result = await service.get(uow, current_user.id)
    if result:
        return result
    logging.error(
        {
            "method": "get_user_info",
            "endpoint": "/",
            "status_code": 404,
            "message": "Пользователь не найден",
        }
    )
    return JSONResponse(
        status_code=404, content={"message": "Пользователь не найден"},
    )
