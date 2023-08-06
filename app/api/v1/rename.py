# from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.controllers import rename as rename_controller

from app.schemas.rename import (
    RenameInDB,
    # RenameCreate,
    # RenameUpdate,
)

from app.utils.dep import get_token_content

router = APIRouter()


@router.get('/closed', response_model=RenameInDB)
async def get_pg_user_by_name(
    name: str,
    token=Depends(get_token_content),
):
    """ return user object from pg_users postgres table """
    if result := await rename_controller.get_by_name(name):
        return result
    else:
        # make sure to raise excepions in router if possible
        raise HTTPException(404)


@router.get('/', response_model=RenameInDB)
async def get_pg_user_by_name(
    name: str,
):
    """ return user object from pg_users postgres table """
    if result := await rename_controller.get_by_name(name):
        return result
    else:
        # make sure to raise excepions in router if possible
        raise HTTPException(404)
