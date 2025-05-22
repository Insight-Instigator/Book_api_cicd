from fastapi import FastAPI
from app.api.v1.routes import books
import logging
import os
from app.middleware.api_middleware import  ApiKeyPropagationMiddleware
from jose import JWTError, jwt

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

# Create FastAPI application
app = FastAPI(
    title="Book API",
    description="A RESTful API for managing books",
    version="1.0.0"
)

app.add_middleware(ApiKeyPropagationMiddleware)


@app.middleware("http")
async def custom_cookie_middleware(request, call_next):
    response: Response = await call_next(request)
    if "oauth_session" in response.headers.get("set-cookie", ""):
        response.headers["set-cookie"] = response.headers["set-cookie"].replace("SameSite=Lax", "SameSite=None")
    return response
# Include routers
app.include_router(books.router, prefix="/books", tags=["books"])

