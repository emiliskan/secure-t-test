import logging

from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/")
async def new_post():
    pass
