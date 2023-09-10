from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core import models, schemas
from app.core.utils import hash_password

# CRUD operations for Users

async def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()

async def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()

async def get_users(db: Session) -> List[models.User]:
    return db.query(models.User).all()

async def user_create(db: Session, user: schemas.UserCreate) -> models.User:
    _user = await get_user_by_username(db, user.username)
    if _user:
        raise HTTPException(detail=f"Username {user.username} is already exist", status_code=status.HTTP_409_CONFLICT)
    
    user.password = await hash_password(user.password)
    db_user = models.User(
        **user.dict()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def user_update(db: Session, user_id: int, user: schemas.UserUpdate) -> models.User:
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = await hash_password(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def user_delete(db: Session, user_id: int) -> models.User:
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

async def get_post_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

async def get_posts(db: Session) -> List[models.Post]:
    return db.query(models.Post).all()

async def get_only_user_posts(db: Session, user_id) -> List[models.Post]:
    return db.query(models.Post).filter(user_id == user_id).all()

async def post_create(db: Session, post: schemas.PostCreate):
    post = models.Post(
        **post.dict()
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


async def post_update(db: Session, post_id: int, user_id: int, post: schemas.PostUpdate) -> schemas.PostReturn:
    db_post = await get_post_by_id(db, post_id)
    if not db_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if db_post.user_id != user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You are not post owner")
    
    update_data = post.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

async def post_delete(db: Session, post_id: int) -> models.Post:
    post = await get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="post not found")
    db.delete(post)
    db.commit()
    return post

async def photo_create(db: Session, photo: schemas.PhotoCreate):
    photo = models.Photo(
        **photo.dict()
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

async def comment_create(db: Session, comment: schemas.CommentCreate, user_id):
    comment = models.Comment(
        **comment.dict(), user_id = user_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

async def get_comments(db: Session) -> List[models.Comment]:
    return db.query(models.Comment).all()

async def get_comment_by_id(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

async def comment_update(db: Session, comment_id: int, user_id: int, comment: schemas.CommentUpdate) -> schemas.CommentReturn:
    db_comment = await get_comment_by_id(db, comment_id)
    if not db_comment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    
    if db_comment.user_id != user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You are not comment owner")
    
    update_data = comment.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_comment, key, value)

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

async def comment_delete(db: Session, comment_id: int) -> models.Comment:
    comment = await get_post_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="comment not found")
    db.delete(comment)
    db.commit()
    return comment