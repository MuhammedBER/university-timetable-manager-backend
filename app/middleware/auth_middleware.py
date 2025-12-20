import os
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.models.user import User
from app.database.db import SessionLocal
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to authenticate users for protected routes.
    Excludes authentication routes from verification.
    """
    
    # Routes that don't require authentication
    EXCLUDED_PATHS = {
        "/api/auth/login",
        "/api/auth/register",
        "/docs",
        "/redoc",
        "/openapi.json",
    }
    
    # Exact match paths (must match exactly)
    EXCLUDED_EXACT_PATHS = {
        "/",  # Only root endpoint, not everything starting with /
    }
    
    async def dispatch(self, request: Request, call_next):
        # Debug: Print the request path
        print(f"🔍 Middleware checking path: {request.url.path}")
        
        # Check if the path should be excluded from authentication
        if self._is_excluded_path(request.url.path):
            print(f"✅ Path excluded from auth: {request.url.path}")
            return await call_next(request)
        
        # Get the Authorization header
        auth_header = request.headers.get("Authorization")
        
        print(f"🔑 Authorization header: {auth_header}")
        
        if not auth_header:
            print(f"❌ Missing auth header for: {request.url.path}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing authorization header"}
            )
        
        # Extract token from "Bearer <token>"
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid authentication scheme"}
                )
        except ValueError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid authorization header format"}
            )
        
        # Verify token
        db = SessionLocal()
        try:
            # Decode JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = int(payload.get("sub"))
            
            if not user_id:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid token payload"}
                )
            
            # Verify user exists in database
            user = db.query(User).get(user_id)
            if not user:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "User not found"}
                )
            
            # Add user to request state for access in route handlers (optional)
            request.state.user = user
            request.state.user_id = user_id
            
        except JWTError as e:
            return JSONResponse(
                status_code=401,
                content={"detail": f"Invalid or expired token"}
            )
        except Exception as e:
            return JSONResponse(
                status_code=401,
                content={"detail": f"Authentication error: {str(e)}"}
            )
        finally:
            db.close()
        
        # Proceed with the request
        response = await call_next(request)
        return response
    
    def _is_excluded_path(self, path: str) -> bool:
        """Check if the path should be excluded from authentication"""
        # Check exact matches
        if path in self.EXCLUDED_EXACT_PATHS:
            return True
        
        # Check if path starts with any excluded path
        for excluded in self.EXCLUDED_PATHS:
            if path.startswith(excluded):
                return True
        
        return False