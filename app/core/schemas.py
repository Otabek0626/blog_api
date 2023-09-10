from pydantic import BaseModel
from fastapi import UploadFile, File
from datetime import datetime
import typing as t

class UserBase(BaseModel):
    username: str
    is_admin: t.Optional[bool] = False

class UserCreate(BaseModel):
    username: str
    password: str
    
class UserAdminCreate(BaseModel):
    username: str
    password: str
    is_admin: t.Optional[bool] = False

class UserReturn(BaseModel):
    id: int
    username: str
    is_admin: t.Optional[bool] = False

    class ConfigDict:
        from_attributes = True
    
class UserUpdate(UserBase):
    username: str
    password: t.Optional[str] = None

class UserAdminUpdate(UserBase):
    username: str
    is_admin: t.Optional[bool] = False
    password: t.Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class PostCreate(BaseModel):
    user_id: int
    exercise_type: str
    post_text: str

class PostUpdate(BaseModel):
    exercise_type: t.Optional[str] = None
    post_text: t.Optional[str] = None

class PhotoCreate(BaseModel):
    post_id: int
    photo_url: str



class PhotoReturn(BaseModel):
    id: int
    post_id: int
    photo_url: str
    created_at: datetime
    updated_at: datetime
    
    class ConfigDict:
        from_attributes = True

class CommentCreate(BaseModel):
    post_id: int
    comment_text: str

class CommentUpdate(BaseModel):
    comment_text: str

class CommentReturn(BaseModel):
    id: int
    post_id: int
    user_id: int
    comment_text: str
    created_at: datetime
    updated_at: datetime
    
    class ConfigDict:
        from_attributes = True

class PostReturn(BaseModel):
    id: int
    user_id: int
    exercise_type: str
    post_text: str
    created_at: datetime
    updated_at: datetime
    photos: t.List[PhotoReturn]
    comments: t.List[CommentReturn]
    
    class ConfigDict:
        from_attributes = True