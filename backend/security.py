from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional

class SecurityManager:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = "HS256"
        self.bearer = HTTPBearer()
        
    def create_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(hours=24))
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())):
        """Verify JWT token"""
        token = credentials.credentials
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

# Input validation and sanitization
class InputValidator:
    @staticmethod
    def sanitize_url(url: str) -> str:
        """Sanitize and validate URL"""
        allowed_domains = ["play.ezygamers.com"]
        from urllib.parse import urlparse
        
        parsed = urlparse(url)
        if parsed.hostname not in allowed_domains:
            raise ValueError(f"URL must be from allowed domains: {allowed_domains}")
        
        return url
    
    @staticmethod
    def validate_test_count(count: int) -> int:
        """Validate test count limits"""
        if count < 1 or count > 50:
            raise ValueError("Test count must be between 1 and 50")
        return count

# Rate limiting
from fastapi import Request
from collections import defaultdict
from datetime import datetime
import time

class RateLimiter:
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed"""
        now = time.time()
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]
        
        # Check limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        self.requests[client_id].append(now)
        return True