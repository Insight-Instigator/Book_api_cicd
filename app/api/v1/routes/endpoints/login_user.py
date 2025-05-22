from jose import jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.services.book_service import BookService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
SECRET_KEY = "rida_kee_secret_key"
ALGORITHM = "HS256"

@router.post("/token")
async def login(role: str):
    token_data = {
        "role": role  # or "user"
    }
    jwt_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": jwt_token, "token_type": "bearer"}
