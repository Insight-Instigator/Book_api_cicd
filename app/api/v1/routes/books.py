from fastapi import APIRouter
from app.api.v1.routes.endpoints import get_books, post_books, put_books, delete_books, options_books, login_user

router = APIRouter()

# Include all endpoint routers
router.include_router(get_books.router)
router.include_router(post_books.router)
router.include_router(put_books.router)
router.include_router(delete_books.router)
router.include_router(options_books.router) 
router.include_router(login_user.router)