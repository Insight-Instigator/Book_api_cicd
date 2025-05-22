from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_session
from app.services.book_service import BookService
from app.api.v1.schemas.book import Book
from app.core.auth import api_key_dependency
import logging
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[Book])
async def get_books(session: AsyncSession = Depends(get_session), _ = Depends(api_key_dependency)):
    try:
        book_service = BookService(session)
        books_list = await book_service.get_all_books()
        
        if not books_list:
            raise HTTPException(status_code=404, detail="No books available in the library.")
        
        return books_list
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_books: {str(e)}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable. Please try again later.")
    except Exception as e:
        logger.error(f"Unexpected error in get_books: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int, session: AsyncSession = Depends(get_session), _ = Depends(api_key_dependency)):
    try:
        if book_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid book ID. Book ID must be a positive integer.")
            
        book_service = BookService(session)
        book = await book_service.get_book_by_id(book_id)
        
        if not book:
            raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found in the library.")
        
        return book
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_book: {str(e)}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable. Please try again later.")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_book: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.") 