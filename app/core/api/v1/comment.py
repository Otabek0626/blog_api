from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core import schemas, crud, database, oauth2
from app.core.models import Comment, User

router = APIRouter()


@router.post("/", response_model=schemas.CommentReturn, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(oauth2.require_user)
):
    created_comment = await crud.comment_create(db, comment, current_user.id)
    return created_comment


@router.get("/", response_model=List[schemas.CommentReturn])
async def get_all_comments(
    db: Session = Depends(database.get_db),
    current_user: User = Depends(oauth2.require_user)
):
    comments = await crud.get_comments(db)
    return comments


@router.get("/{comment_id}", response_model=schemas.CommentReturn)
async def get_comment_by_id(
    comment_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(oauth2.require_user)
):
    comment = await crud.get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.put("/{comment_id}", response_model=schemas.CommentReturn)
async def update_comment(
    comment_id: int,
    comment: schemas.CommentUpdate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(oauth2.require_user)
):
    updated_comment = await crud.update_comment(db, comment_id, current_user.id, comment)
    return updated_comment


@router.delete("/{comment_id}", response_model=schemas.CommentReturn, status_code=status.HTTP_202_ACCEPTED)
async def delete_comment(
    comment_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(oauth2.require_admin)
):
    deleted_comment = await crud.delete_comment(db, comment_id)
    return deleted_comment
