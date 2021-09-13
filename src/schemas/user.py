from schemas.base import AbstractModel


class BaseUserSchema(AbstractModel):

    username: str
    password: str


class UserSchema(BaseUserSchema):

    class Config:
        orm_mode = True


class LoginSchema(BaseUserSchema):
    ...


class TokenSchema(AbstractModel):
    access_token: str
