from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import APIKeyHeader
from fastapi import Query
from fastapi import Request
from jose import JWTError, jwt

SECRET_KEY = "rida_kee_secret_key"
ALGORITHM = "HS256"

# Use HTTPBearer for proper Swagger UI integration
bearer_scheme = HTTPBearer()

def api_key_dependency(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    request: Request = None,
):
    """
    Validate JWT token from Authorization header.
    """
    try:
        # Get token from Bearer credentials
        token = credentials.credentials
        
        # Decode and validate token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_role = payload.get("role")
        
        if user_role is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )

        if user_role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions"
            )
            
        return payload
        
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )  