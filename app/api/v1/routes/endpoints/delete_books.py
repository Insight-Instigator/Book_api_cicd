from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.services.book_service import BookService
import logging
from app.core.auth import api_key_dependency
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)
router = APIRouter()

@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int, session: AsyncSession = Depends(get_session), _ = Depends(api_key_dependency)):
    try:
        if book_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid book ID. Book ID must be a positive integer."
            )

        book_service = BookService(session)
        if not await book_service.delete_book(book_id):
            raise HTTPException(
                status_code=404,
                detail=f"Book with ID {book_id} not found in the library."
            )
    except SQLAlchemyError as e:
        logger.error(f"Database error in delete_book: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable. Please try again later."
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in delete_book: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        ) 