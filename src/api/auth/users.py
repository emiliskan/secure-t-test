import logging

from fastapi import APIRouter, Depends
from services.users import UsersService, get_user_service
from schemas.user import UserSchema, LoginSchema, TokenSchema

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/users",
    description="Register user.",
)
async def create(
        user: UserSchema,
        service: UsersService = Depends(get_user_service),
) -> TokenSchema:
    return await service.create(user)


@router.get(
    "/users/login",
    description="Login user.",
)
async def login_user(
        login: LoginSchema,
        service: UsersService = Depends(get_user_service),
) -> TokenSchema:
    return await service.login(login)
