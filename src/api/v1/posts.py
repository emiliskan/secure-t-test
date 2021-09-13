import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from core.auth import auth
from db.models.post import Post
from services.posts import PostsService, get_post_service
from services.exceptions import NotAllowed, NotFound
from schemas.post import PostSchema
from schemas.base import ListQuery

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/posts",
    description="Posts list.",
    response_model=list[PostSchema]
)
async def get_posts(
        query: ListQuery,
        service: PostsService = Depends(get_post_service),
) -> list[Post]:
    return await service.read(query)


@router.post(
    "/posts",
    description="Create post.",
)
async def create(
        post: PostSchema,
        service: PostsService = Depends(get_post_service),
        user_id: int = Depends(auth),
) -> Post:
    return await service.create(user_id, post)


@router.get(
    "/posts/{post_id}",
    description="Get post.",
    response_model=PostSchema
)
async def get(
        post_id: int = Query(None, description="Post ID"),
        service: PostsService = Depends(get_post_service),
) -> Post:

    try:
        post = await service.get(post_id)
    except NotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return post


@router.delete(
    "/posts/{post_id}",
    description="Remove post."
)
async def delete(
        post_id: int = Query(None, description="Post ID"),
        service: PostsService = Depends(get_post_service),
        user_id: int = Depends(auth),
) -> None:
    try:
        await service.delete(user_id, post_id)
    except NotAllowed:
        raise HTTPException(status_code=HTTPStatus.METHOD_NOT_ALLOWED)
    except NotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)


@router.patch(
    "/posts/{post_id}",
    description="Update post.",
)
async def update_post(
        post: PostSchema,
        post_id: int = Query(None, description="Post ID"),
        service: PostsService = Depends(get_post_service),
        user_id: int = Depends(auth),
) -> Post:

    try:
        return await service.update(user_id, post_id, post)
    except NotAllowed:
        raise HTTPException(status_code=HTTPStatus.METHOD_NOT_ALLOWED)
    except NotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)