# Book API

A modern, asynchronous RESTful API for managing books, built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features
- CRUD operations for books (Create, Read, Update, Delete)
- Asynchronous database access for high performance
- Pydantic models for data validation
- Modular, scalable, and production-ready project structure
- Automatic interactive API docs (Swagger UI and ReDoc)
- Logging to file and console

## Tech Stack
- Python 3.8+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- asyncpg
- Pydantic
- Uvicorn
- python-dotenv

## Project Structure
```
app/
├── api/v1/routes/           # API endpoint routers
│   ├── books.py
│   └── endpoints/
│       ├── get_books.py
│       ├── post_books.py
│       ├── put_books.py
│       ├── delete_books.py
│       └── options_books.py
├── api/v1/schemas/          # Pydantic schemas
│   └── book.py
├── core/                    # DB connection
│   └── database.py
├── models/                  # SQLAlchemy models
│   └── models.py
├── services/                # Business logic
│   └── book_service.py
├── main.py                  # App entrypoint
logs/
└── app.log                  # Log file
```

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Insight-Instigator/Personal-learning.git
cd book-api
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the project root:
```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
```

### 4. Run the application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the API docs
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Example API Usage

### Create a new book
```bash
curl -X POST "http://localhost:8000/books/" -H "Content-Type: application/json" -d '{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "published_year": 1925,
  "genre": "Fiction",
  "available": true
}'
```

### Get all books
```bash
curl http://localhost:8000/books/
```

### Get a book by ID
```bash
curl http://localhost:8000/books/1
```

### Update a book
```bash
curl -X PUT "http://localhost:8000/books/1" -H "Content-Type: application/json" -d '{
  "title": "Updated Title"
}'
```

### Delete a book
```bash
curl -X DELETE http://localhost:8000/books/1
```


