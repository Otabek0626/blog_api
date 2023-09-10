from fastapi import Depends, APIRouter, status, HTTPException, UploadFile
from app.core import schemas, crud, database, oauth2, utils
import typing as t
from sqlalchemy.orm import Session

router = APIRouter()

# Define a maximum allowed number of files
MAX_FILES_ALLOWED = 5


@router.post("/", response_model=schemas.PostReturn, status_code=status.HTTP_201_CREATED)
async def cerate_post(exercise_type: str, post_text: str, photos: t.List[UploadFile], db: Session = Depends(database.get_db), current_user: str = Depends(oauth2.require_user)):
    if len(photos) > MAX_FILES_ALLOWED:
        raise HTTPException(
            status_code=400, detail=f"Maximum {MAX_FILES_ALLOWED} files allowed.")

    post = await crud.post_create(db, schemas.PostCreate(user_id=current_user.id, exercise_type=exercise_type, post_text=post_text))

    for photo in photos:
        path = await utils.save_photo(photo)
        await crud.photo_create(db, schemas.PhotoCreate(post_id=post.id, photo_url=path))
    db.refresh(post)
    return post


@router.get("/", response_model=t.List[schemas.PostReturn])
async def get_all_posts_endpoint(db: Session = Depends(database.get_db), current_user: str = Depends(oauth2.require_user)):
    posts = await crud.get_posts(db)
    return posts


@router.get("/user", response_model=t.List[schemas.PostReturn])
async def get_only_user_posts_endpoint(db: Session = Depends(database.get_db), current_user: str = Depends(oauth2.require_user)):
    posts = await crud.get_only_user_posts(db, user_id=current_user.id)
    return posts


@router.put("/{post_id}", response_model=schemas.PostReturn, status_code=status.HTTP_201_CREATED)
async def update_post_endpoint(post_id: int, post: schemas.PostUpdate, db: Session = Depends(database.get_db), current_user: str = Depends(oauth2.require_user)):
    post = await crud.post_update(db, post_id, current_user.id, post)
    return post


@router.delete("/{post_id}", response_model=schemas.PostReturn, status_code=status.HTTP_202_ACCEPTED)
async def delete_post_endpoint(post_id: int, db: Session = Depends(database.get_db), current_user: str = Depends(oauth2.require_admin)):
    post = await crud.post_delete(db, post_id)
    return post
