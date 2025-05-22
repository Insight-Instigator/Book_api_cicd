# from lib import *
# from models.shopify_models import ApiKey
# from db.database import get_db


# @contextmanager
# def get_db_session():
#     db = next(get_db())
#     try:
#         yield db
#     finally:
#         db.close()

from fastapi import Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi.responses import Response
from urllib.parse import urlparse, parse_qs


class ApiKeyPropagationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Middleware to propagate API key across the request lifecycle.
        Supports API key extraction from both the Authorization header and query parameters.
        """
        # Check the Authorization header for the API key
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            # Extract the API key (remove the "Bearer " prefix)
            api_key = auth_header.split("Bearer ")[1]
            request.state.api_key = api_key
        else:
            # Fallback to query parameters if the Authorization header is not present
            api_key = request.query_params.get("api_key")
            if api_key:
                request.state.api_key = api_key
 
        # Continue processing the request
        response = await call_next(request)
        return response