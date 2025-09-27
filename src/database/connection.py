"""
Advanced Database Manager with Encryption and Connection Pooling
"""

import asyncio
from typing import Optional, Dict, Any, AsyncGenerator
from contextlib import asynccontextmanager
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import QueuePool
import structlog

from src.core.config import Settings
from src.security.encryption import SecurityManager

Base = declarative_base()


class DatabaseManager:
    """Advanced database manager with security and performance optimization"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.logger = structlog.get_logger(__name__)
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[async_sessionmaker] = None
        self._security_manager: Optional[SecurityManager] = None
    
    async def initialize(self) -> None:
        """Initialize database connection with advanced configuration"""
        try:
            # Create async engine with optimized settings
            self._engine = create_async_engine(
                self.settings.database_url,
                poolclass=QueuePool,
                pool_size=self.settings.db_pool_size,
                max_overflow=self.settings.db_max_overflow,
                pool_timeout=self.settings.db_pool_timeout,
                pool_recycle=self.settings.db_pool_recycle,
                pool_pre_ping=True,  # Validate connections before use
                echo=self.settings.debug,
                future=True,
                connect_args={
                    "server_settings": {
                        "jit": "off"  # Disable JIT for consistent performance
                    }
                }
            )
            
            # Create session factory
            self._session_factory = async_sessionmaker(
                bind=self._engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
                autocommit=False
            )
            
            # Test connection
            await self._test_connection()
            
            # Initialize database schema
            await self._initialize_schema()
            
            self.logger.info("Database manager initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            raise
    
    async def _test_connection(self) -> None:
        """Test database connection"""
        try:
            async with self._engine.begin() as conn:
                await conn.execute(sa.text("SELECT 1"))
            self.logger.info("Database connection test successful")
        except Exception as e:
            self.logger.error(f"Database connection test failed: {e}")
            raise
    
    async def _initialize_schema(self) -> None:
        """Initialize database schema"""
        try:
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            self.logger.info("Database schema initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize schema: {e}")
            raise
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session with automatic cleanup"""
        if not self._session_factory:
            raise RuntimeError("Database not initialized")
        
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Execute raw SQL query safely"""
        async with self.get_session() as session:
            result = await session.execute(sa.text(query), params or {})
            return result.fetchall()
    
    async def close(self) -> None:
        """Close database connections"""
        if self._engine:
            await self._engine.dispose()
            self.logger.info("Database connections closed")


# Database Models
class User(Base):
    """User model with enhanced security"""
    __tablename__ = "users"
    
    id = sa.Column(sa.String, primary_key=True)
    username = sa.Column(sa.String(50), unique=True, nullable=False)
    email = sa.Column(sa.String(255), unique=True, nullable=False)
    password_hash = sa.Column(sa.String(255), nullable=False)
    is_active = sa.Column(sa.Boolean, default=True)
    is_admin = sa.Column(sa.Boolean, default=False)
    created_at = sa.Column(sa.DateTime, default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    last_login = sa.Column(sa.DateTime)
    failed_login_attempts = sa.Column(sa.Integer, default=0)
    locked_until = sa.Column(sa.DateTime)


class TestSession(Base):
    """Test session model"""
    __tablename__ = "test_sessions"
    
    id = sa.Column(sa.String, primary_key=True)
    user_id = sa.Column(sa.String, sa.ForeignKey("users.id"))
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text)
    status = sa.Column(sa.String(50), default="pending")
    target_url = sa.Column(sa.String(500), nullable=False)
    test_config = sa.Column(sa.JSON)
    created_at = sa.Column(sa.DateTime, default=sa.func.now())
    started_at = sa.Column(sa.DateTime)
    completed_at = sa.Column(sa.DateTime)
    total_tests = sa.Column(sa.Integer, default=0)
    passed_tests = sa.Column(sa.Integer, default=0)
    failed_tests = sa.Column(sa.Integer, default=0)


class TestCase(Base):
    """Individual test case model"""
    __tablename__ = "test_cases"
    
    id = sa.Column(sa.String, primary_key=True)
    session_id = sa.Column(sa.String, sa.ForeignKey("test_sessions.id"))
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text)
    test_type = sa.Column(sa.String(50), nullable=False)
    priority = sa.Column(sa.Integer, default=5)
    status = sa.Column(sa.String(50), default="pending")
    test_data = sa.Column(sa.JSON)
    expected_result = sa.Column(sa.JSON)
    actual_result = sa.Column(sa.JSON)
    error_message = sa.Column(sa.Text)
    execution_time = sa.Column(sa.Float)
    created_at = sa.Column(sa.DateTime, default=sa.func.now())
    executed_at = sa.Column(sa.DateTime)


class TestArtifact(Base):
    """Test artifacts (screenshots, logs, etc.)"""
    __tablename__ = "test_artifacts"
    
    id = sa.Column(sa.String, primary_key=True)
    test_case_id = sa.Column(sa.String, sa.ForeignKey("test_cases.id"))
    artifact_type = sa.Column(sa.String(50), nullable=False)  # screenshot, log, network, dom
    file_path = sa.Column(sa.String(500), nullable=False)
    file_size = sa.Column(sa.Integer)
    mime_type = sa.Column(sa.String(100))
    metadata = sa.Column(sa.JSON)
    created_at = sa.Column(sa.DateTime, default=sa.func.now())


class AgentExecution(Base):
    """Agent execution tracking"""
    __tablename__ = "agent_executions"
    
    id = sa.Column(sa.String, primary_key=True)
    session_id = sa.Column(sa.String, sa.ForeignKey("test_sessions.id"))
    agent_type = sa.Column(sa.String(50), nullable=False)
    agent_name = sa.Column(sa.String(100), nullable=False)
    input_data = sa.Column(sa.JSON)
    output_data = sa.Column(sa.JSON)
    execution_time = sa.Column(sa.Float)
    status = sa.Column(sa.String(50), default="pending")
    error_message = sa.Column(sa.Text)
    created_at = sa.Column(sa.DateTime, default=sa.func.now())
    completed_at = sa.Column(sa.DateTime)
