"""
Configuration Management with Advanced Security
"""

import os
from pathlib import Path
from typing import Optional, List
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with security-first approach"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid"
    )
    
    # Application
    app_name: str = "Multi-Agent Game Tester Pro"
    version: str = "1.0.0"
    debug: bool = False
    environment: str = Field(default="production", description="Environment: development, staging, production")
    
    # API Configuration
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    api_workers: int = 4
    api_reload: bool = False
    
    # Database Configuration
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "game_tester_pro"
    db_user: str = "postgres"
    db_password: str = Field(default="", description="Database password")
    db_pool_size: int = 20
    db_max_overflow: int = 30
    db_pool_timeout: int = 30
    db_pool_recycle: int = 3600
    
    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    redis_ssl: bool = False
    
    # Security Configuration
    secret_key: str = Field(default="", description="Secret key for encryption")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    password_min_length: int = 12
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 30
    
    # Encryption
    encryption_key: Optional[str] = Field(default=None, description="Fernet encryption key")
    use_encryption: bool = True
    
    # OpenAI Configuration
    openai_api_key: str = Field(default="", description="OpenAI API key")
    openai_model: str = "gpt-4-turbo-preview"
    openai_max_tokens: int = 4000
    openai_temperature: float = 0.7
    
    # LangChain Configuration
    langchain_tracing: bool = False
    langchain_project: str = "game-tester-agents"
    
    # Web Testing Configuration
    browser_headless: bool = True
    browser_timeout: int = 30000
    page_load_timeout: int = 60000
    element_timeout: int = 10000
    screenshot_quality: int = 90
    
    # Selenium Grid
    selenium_grid_url: Optional[str] = None
    selenium_implicit_wait: int = 10
    selenium_page_load_timeout: int = 60
    
    # Playwright Configuration
    playwright_browser: str = "chromium"  # chromium, firefox, webkit
    playwright_viewport_width: int = 1920
    playwright_viewport_height: int = 1080
    playwright_user_agent: Optional[str] = None
    
    # File Storage
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path("data"))
    log_dir: Path = Field(default_factory=lambda: Path("logs"))
    reports_dir: Path = Field(default_factory=lambda: Path("reports"))
    artifacts_dir: Path = Field(default_factory=lambda: Path("artifacts"))
    temp_dir: Path = Field(default_factory=lambda: Path("temp"))
    
    # Logging Configuration
    log_level: str = "INFO"
    log_file: str = "game_tester.log"
    log_max_size: int = 10 * 1024 * 1024  # 10MB
    log_backup_count: int = 5
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Performance Configuration
    max_concurrent_tests: int = 10
    test_timeout_minutes: int = 30
    retry_attempts: int = 3
    retry_delay_seconds: int = 5
    
    # Agent Configuration
    planner_agent_temperature: float = 0.8
    ranker_agent_temperature: float = 0.5
    executor_agent_temperature: float = 0.3
    analyzer_agent_temperature: float = 0.4
    orchestrator_agent_temperature: float = 0.6
    
    # Monitoring
    metrics_enabled: bool = True
    metrics_port: int = 9090
    health_check_interval: int = 30
    
    # Target Game Configuration
    target_game_url: str = "https://play.ezygamers.com/"
    game_type: str = "number_puzzle"
    supported_languages: List[str] = ["English", "हिन्दी", "ಕನ್ನಡ", "தமிழ்", "తెలుగు"]
    
    @field_validator("secret_key", "encryption_key")
    @classmethod
    def generate_keys_if_empty(cls, v: str) -> str:
        """Generate secure keys if not provided"""
        if not v:
            import secrets
            return secrets.token_urlsafe(32)
        return v
    
    @field_validator("data_dir", "log_dir", "reports_dir", "artifacts_dir", "temp_dir")
    @classmethod
    def create_directories(cls, v: Path) -> Path:
        """Ensure directories exist"""
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    @property
    def database_url(self) -> str:
        """Construct database URL"""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @property
    def redis_url(self) -> str:
        """Construct Redis URL"""
        password_part = f":{self.redis_password}@" if self.redis_password else ""
        protocol = "rediss" if self.redis_ssl else "redis"
        return f"{protocol}://{password_part}{self.redis_host}:{self.redis_port}/{self.redis_db}"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
