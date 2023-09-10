# Import necessary modules from FastAPI and project-specific modules.
from fastapi import APIRouter, Depends
from app.core.api.v1 import swagger, user, auth, post, comment

from app.core import config
# Create an API router with the prefix "/api"
router = APIRouter(prefix="/v1")

@router.get("/", tags=["Root"])
async def root():
    return {"version": config.settings.APP_VERSION}

router.include_router(
    swagger.router, 
    tags=["Swagger"],
)

router.include_router(
    user.router, 
    prefix="/user", 
    tags=["Users"],
)

router.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["Auth"],
)


router.include_router(
    post.router, 
    prefix="/post", 
    tags=["Posts"],
)

router.include_router(
    comment.router, 
    prefix="/comment", 
    tags=["Comments"],
)