import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from core.auth import auth
from db.models.comments import Comment
from schemas.comment import CommentSchema
from services.comments import get_comments_service
from services.comments import CommentsService
from services.exceptions import NotAllowed, NotFound
from schemas.base import ListQuery

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/posts/{post_id}/comments",
    description="Post comments list.",
    response_model=list[CommentSchema]
)
async def get_comments(
        query: ListQuery,
        post_id: int = Query(None, description="Post ID"),
        service: CommentsService = Depends(get_comments_service),
) -> list[Comment]:
    return await service.read(post_id, query)


@router.post(
    "/posts/comments",
    description="Create comment.",
)
async def create(
        comment: CommentSchema,
        service: CommentsService = Depends(get_comments_service),
        user_id: int = Depends(auth),
) -> Comment:
    return await service.create(user_id, comment)


@router.delete(
    "/posts/comments/{comment_id}",
    description="Delete comment."
)
async def delete(
        comment_id: int = Query(None, description="Comment ID"),
        service: CommentsService = Depends(get_comments_service),
        user_id: int = Depends(auth),
) -> None:
    try:
        await service.delete(user_id, comment_id)
    except NotAllowed:
        raise HTTPException(status_code=HTTPStatus.METHOD_NOT_ALLOWED)
    except NotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)


@router.patch(
    "/posts/comments/{comment_id}",
    description="Update comment.",
)
async def update_comment(
        comment: CommentSchema,
        comment_id: int = Query(None, description="Comment ID"),
        service: CommentsService = Depends(get_comments_service),
        user_id: int = Depends(auth),
) -> Comment:

    try:
        await service.update(user_id, comment_id, comment)
    except NotAllowed:
        raise HTTPException(status_code=HTTPStatus.METHOD_NOT_ALLOWED)
    except NotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)