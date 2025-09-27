"""
Military-Grade Security Manager
Advanced encryption, authentication, and security controls
"""

import os
import hashlib
import secrets
import base64
from typing import Optional, Dict, Any, Union
from datetime import datetime, timedelta
import jwt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from passlib.context import CryptContext
from passlib.hash import bcrypt
import structlog

from src.core.config import get_settings


class SecurityManager:
    """Military-grade security manager with advanced encryption"""
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = structlog.get_logger(__name__)
        
        # Password hashing context
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__rounds=14  # Higher rounds for better security
        )
        
        # Symmetric encryption
        self._fernet: Optional[Fernet] = None
        
        # Asymmetric encryption keys
        self._private_key: Optional[rsa.RSAPrivateKey] = None
        self._public_key: Optional[rsa.RSAPublicKey] = None
        
        # Session management
        self._active_sessions: Dict[str, Dict[str, Any]] = {}
        self._failed_attempts: Dict[str, Dict[str, Any]] = {}
    
    async def initialize(self) -> None:
        """Initialize security components"""
        try:
            self._setup_symmetric_encryption()
            self._setup_asymmetric_encryption()
            self.logger.info("Security manager initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize security manager: {e}")
            raise
    
    def _setup_symmetric_encryption(self) -> None:
        """Setup Fernet symmetric encryption"""
        if self.settings.encryption_key:
            key = self.settings.encryption_key.encode()
        else:
            key = Fernet.generate_key()
        
        self._fernet = Fernet(key)
    
    def _setup_asymmetric_encryption(self) -> None:
        """Setup RSA asymmetric encryption"""
        # Generate RSA key pair
        self._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096  # Military-grade key size
        )
        self._public_key = self._private_key.public_key()
    
    def hash_password(self, password: str) -> str:
        """Hash password with bcrypt and high rounds"""
        if len(password) < self.settings.password_min_length:
            raise ValueError(f"Password must be at least {self.settings.password_min_length} characters")
        
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def encrypt_data(self, data: Union[str, bytes]) -> str:
        """Encrypt data using Fernet symmetric encryption"""
        if isinstance(data, str):
            data = data.encode()
        
        encrypted = self._fernet.encrypt(data)
        return base64.b64encode(encrypted).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt data using Fernet symmetric encryption"""
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted = self._fernet.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            self.logger.error(f"Decryption failed: {e}")
            raise ValueError("Invalid encrypted data")
    
    def encrypt_rsa(self, data: Union[str, bytes]) -> str:
        """Encrypt data using RSA public key"""
        if isinstance(data, str):
            data = data.encode()
        
        # RSA can only encrypt small amounts of data
        max_chunk_size = (self._public_key.key_size // 8) - 2 * (hashes.SHA256().digest_size) - 2
        
        encrypted_chunks = []
        for i in range(0, len(data), max_chunk_size):
            chunk = data[i:i + max_chunk_size]
            encrypted_chunk = self._public_key.encrypt(
                chunk,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            encrypted_chunks.append(encrypted_chunk)
        
        return base64.b64encode(b''.join(encrypted_chunks)).decode()
    
    def decrypt_rsa(self, encrypted_data: str) -> str:
        """Decrypt data using RSA private key"""
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            chunk_size = self._private_key.key_size // 8
            
            decrypted_chunks = []
            for i in range(0, len(encrypted_bytes), chunk_size):
                chunk = encrypted_bytes[i:i + chunk_size]
                decrypted_chunk = self._private_key.decrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                decrypted_chunks.append(decrypted_chunk)
            
            return b''.join(decrypted_chunks).decode()
        except Exception as e:
            self.logger.error(f"RSA decryption failed: {e}")
            raise ValueError("Invalid RSA encrypted data")
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate cryptographically secure token"""
        return secrets.token_urlsafe(length)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.settings.access_token_expire_minutes
            )
        
        to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "access"})
        
        # Add security claims
        to_encode.update({
            "jti": self.generate_secure_token(),  # JWT ID for token tracking
            "nbf": datetime.utcnow(),  # Not before
            "iss": self.settings.app_name,  # Issuer
        })
        
        return jwt.encode(
            to_encode,
            self.settings.secret_key,
            algorithm=self.settings.algorithm
        )
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create JWT refresh token"""
        data = {
            "sub": user_id,
            "type": "refresh",
            "jti": self.generate_secure_token(),
            "iat": datetime.utcnow(),
            "iss": self.settings.app_name,
            "exp": datetime.utcnow() + timedelta(days=self.settings.refresh_token_expire_days)
        }
        
        return jwt.encode(
            data,
            self.settings.secret_key,
            algorithm=self.settings.algorithm
        )
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token,
                self.settings.secret_key,
                algorithms=[self.settings.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token has expired")
            return None
        except jwt.JWTError as e:
            self.logger.warning(f"JWT error: {e}")
            return None
    
    def create_session(self, user_id: str, ip_address: str, user_agent: str) -> str:
        """Create secure session"""
        session_id = self.generate_secure_token()
        session_data = {
            "user_id": user_id,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "is_active": True
        }
        
        self._active_sessions[session_id] = session_data
        self.logger.info(f"Session created for user {user_id}", extra={"session_id": session_id})
        
        return session_id
    
    def validate_session(self, session_id: str, ip_address: str, user_agent: str) -> bool:
        """Validate session security"""
        if session_id not in self._active_sessions:
            return False
        
        session = self._active_sessions[session_id]
        
        # Check if session is active
        if not session.get("is_active", False):
            return False
        
        # Check IP address consistency (optional, can be disabled for mobile users)
        if session["ip_address"] != ip_address:
            self.logger.warning(f"IP address mismatch for session {session_id}")
            # Could return False for strict security
        
        # Update last activity
        session["last_activity"] = datetime.utcnow()
        
        return True
    
    def invalidate_session(self, session_id: str) -> None:
        """Invalidate session"""
        if session_id in self._active_sessions:
            self._active_sessions[session_id]["is_active"] = False
            self.logger.info(f"Session invalidated: {session_id}")
    
    def check_rate_limit(self, identifier: str, action: str = "login") -> bool:
        """Check rate limiting for security actions"""
        current_time = datetime.utcnow()
        key = f"{identifier}:{action}"
        
        if key not in self._failed_attempts:
            self._failed_attempts[key] = {
                "count": 0,
                "last_attempt": current_time,
                "locked_until": None
            }
        
        attempt_data = self._failed_attempts[key]
        
        # Check if currently locked
        if attempt_data["locked_until"] and current_time < attempt_data["locked_until"]:
            return False
        
        # Reset if lockout period has expired
        if attempt_data["locked_until"] and current_time >= attempt_data["locked_until"]:
            attempt_data["count"] = 0
            attempt_data["locked_until"] = None
        
        return True
    
    def record_failed_attempt(self, identifier: str, action: str = "login") -> None:
        """Record failed security attempt"""
        current_time = datetime.utcnow()
        key = f"{identifier}:{action}"
        
        if key not in self._failed_attempts:
            self._failed_attempts[key] = {
                "count": 0,
                "last_attempt": current_time,
                "locked_until": None
            }
        
        attempt_data = self._failed_attempts[key]
        attempt_data["count"] += 1
        attempt_data["last_attempt"] = current_time
        
        # Lock if too many attempts
        if attempt_data["count"] >= self.settings.max_login_attempts:
            attempt_data["locked_until"] = current_time + timedelta(
                minutes=self.settings.lockout_duration_minutes
            )
            self.logger.warning(f"Account locked due to too many failed attempts: {identifier}")
    
    def generate_api_key(self, user_id: str, name: str) -> Dict[str, str]:
        """Generate API key for user"""
        key_id = self.generate_secure_token(16)
        api_key = self.generate_secure_token(32)
        
        # In production, store this in database
        key_data = {
            "key_id": key_id,
            "api_key": api_key,
            "user_id": user_id,
            "name": name,
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True
        }
        
        return key_data
    
    def derive_key_from_password(self, password: str, salt: Optional[bytes] = None) -> tuple:
        """Derive encryption key from password using PBKDF2"""
        if salt is None:
            salt = os.urandom(32)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,  # High iteration count for security
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def cleanup(self) -> None:
        """Cleanup security resources"""
        # Clear sensitive data
        self._active_sessions.clear()
        self._failed_attempts.clear()
        
        # Overwrite keys (defense in depth)
        if self._fernet:
            del self._fernet
        if self._private_key:
            del self._private_key
        if self._public_key:
            del self._public_key
        
        self.logger.info("Security manager cleanup completed")
    
    def get_public_key_pem(self) -> str:
        """Get public key in PEM format"""
        return self._public_key.public_key_pem().decode()
    
    def sign_data(self, data: Union[str, bytes]) -> str:
        """Sign data with private key"""
        if isinstance(data, str):
            data = data.encode()
        
        signature = self._private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return base64.b64encode(signature).decode()
    
    def verify_signature(self, data: Union[str, bytes], signature: str) -> bool:
        """Verify signature with public key"""
        if isinstance(data, str):
            data = data.encode()
        
        try:
            signature_bytes = base64.b64decode(signature.encode())
            self._public_key.verify(
                signature_bytes,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
