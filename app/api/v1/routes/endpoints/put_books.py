from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.services.book_service import BookService
from app.api.v1.schemas.book import Book, BookUpdate
from app.core.auth import api_key_dependency
import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

logger = logging.getLogger(__name__)
router = APIRouter()

@router.put("/{book_id}", response_model=Book)
async def update_book(book_id: int, book: BookUpdate, session: AsyncSession = Depends(get_session), _ = Depends(api_key_dependency)):
    try:
        if book_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid book ID. Book ID must be a positive integer."
            )

        # Validate update data if provided
        if book.published_year is not None and (book.published_year < 0 or book.published_year > 2024):
            raise HTTPException(
                status_code=400,
                detail="Invalid published year. Year must be between 0 and 2024."
            )
            
        if book.title is not None and not book.title.strip():
            raise HTTPException(
                status_code=400,
                detail="Book title cannot be empty."
            )
            
        if book.author is not None and not book.author.strip():
            raise HTTPException(
                status_code=400,
                detail="Author name cannot be empty."
            )

        book_service = BookService(session)
        updated_book = await book_service.update_book(book_id, book.model_dump(exclude_unset=True))
        
        if not updated_book:
            raise HTTPException(
                status_code=404,
                detail=f"Book with ID {book_id} not found in the library."
            )
        
        return updated_book
    except IntegrityError as e:
        logger.error(f"Database integrity error in update_book: {str(e)}")
        raise HTTPException(
            status_code=409,
            detail="A book with this title and author already exists."
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error in update_book: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable. Please try again later."
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in update_book: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        ) 