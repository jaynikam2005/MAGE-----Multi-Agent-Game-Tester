from typing import List
from pydantic import BaseSettings

class SecuritySettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS512"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: List[str]
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60
    MIN_PASSWORD_LENGTH: int = 12
    PASSWORD_REGEX: str = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{12,}$"
    CSRF_TOKEN_SECRET: str
    SECURE_HEADERS = {
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
        "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    
    class Config:
        env_file = ".env"