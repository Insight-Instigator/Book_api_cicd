import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert
from models import books
from db_config import DATABASE_URL

# Sample book data
sample_books = [
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "published_year": 2008,
        "genre": "Programming",
        "available": True
    },
    {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt",
        "published_year": 1999,
        "genre": "Software Engineering",
        "available": True
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "published_year": 1949,
        "genre": "Dystopian",
        "available": True
    },
    {
        "id": 4,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "published_year": 1960,
        "genre": "Fiction",
        "available": True
    },
    {
        "id": 5,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "published_year": 1925,
        "genre": "Fiction",
        "available": True
    }
]

async def seed_database():
    try:
        # Create engine
        engine = create_async_engine(DATABASE_URL, echo=True)
        
        print("Connecting to database...")
        async with engine.begin() as conn:
            # Insert sample books
            for book in sample_books:
                await conn.execute(insert(books).values(**book))
                print(f"Inserted book: {book['title']}")
            
        print("\nDatabase seeding completed successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        print("\nPlease check:")
        print("1. Database connection is working")
        print("2. Tables are created")
        print("3. Database credentials are correct")

if __name__ == "__main__":
    asyncio.run(seed_database()) 