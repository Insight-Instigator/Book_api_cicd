from fastapi import APIRouter, Depends
from app.core.auth import api_key_dependency

router = APIRouter()
 
@router.options("/")
async def options_books(_ = Depends(api_key_dependency)):
    return {
        "allowed_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    } 