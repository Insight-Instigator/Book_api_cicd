from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.services.book_service import BookService
from app.api.v1.schemas.book import Book, BookCreate
from app.core.auth import api_key_dependency
import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi.exceptions import RequestValidationError

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=Book, status_code=201)
async def create_book(book: BookCreate, session: AsyncSession = Depends(get_session), _ = Depends(api_key_dependency)):
    try:
        # Validate book data
        if book.published_year < 0 or book.published_year > 2024:
            raise HTTPException(
                status_code=400,
                detail="Invalid published year. Year must be between 0 and 2024."
            )
            
        if not book.title.strip():
            raise HTTPException(
                status_code=400,
                detail="Book title cannot be empty."
            )
            
        if not book.author.strip():
            raise HTTPException(
                status_code=400,
                detail="Author name cannot be empty."
            )

        book_service = BookService(session)
        return await book_service.create_book(book.model_dump())
    except IntegrityError as e:
        logger.error(f"Database integrity error in create_book: {str(e)}")
        raise HTTPException(
            status_code=409,
            detail="A book with this title and author already exists."
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error in create_book: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable. Please try again later."
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_book: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        ) 