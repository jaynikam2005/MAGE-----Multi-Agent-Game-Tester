"""
Enterprise-Grade Configuration Management
Advanced Gaming Industry Focus with Military-Grade Security
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from functools import lru_cache
from enum import Enum

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestingMode(str, Enum):
    """Advanced testing modes"""
    PERFORMANCE = "performance"
    STRESS = "stress"
    LOAD = "load"
    AI_BEHAVIOR = "ai_behavior"
    GRAPHICS = "graphics"
    NETWORK = "network"
    SECURITY = "security"
    ACCESSIBILITY = "accessibility"
    CHAOS = "chaos"
    VR_AR = "vr_ar"


class GameGenre(str, Enum):
    """Supported game genres"""
    ACTION = "action"
    RPG = "rpg"
    STRATEGY = "strategy"
    PUZZLE = "puzzle"
    SIMULATION = "simulation"
    RACING = "racing"
    SPORTS = "sports"
    MMORPG = "mmorpg"
    BATTLE_ROYALE = "battle_royale"
    MOBILE = "mobile"


class Platform(str, Enum):
    """Gaming platforms"""
    PC = "pc"
    CONSOLE_PS5 = "ps5"
    CONSOLE_XBOX = "xbox"
    MOBILE_IOS = "ios"
    MOBILE_ANDROID = "android"
    WEB = "web"
    VR = "vr"
    AR = "ar"
    CLOUD = "cloud"


class AdvancedSettings(BaseSettings):
    """Enterprise gaming industry configuration with advanced features"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application Metadata
    app_name: str = "MAGE - Multi-Agent Game Tester Enterprise"
    version: str = "2.0.0"
    build_number: str = "20250928"
    codename: str = "Phoenix"
    debug: bool = False
    environment: str = Field(default="enterprise", description="deployment environment")
    
    # Enterprise Licensing
    enterprise_license_key: str = Field(default="", description="Enterprise license")
    max_concurrent_users: int = 50
    max_test_sessions: int = 100
    license_expiry: Optional[str] = None
    
    # Advanced API Configuration
    api_host: str = "0.0.0.0"  # Bind to all interfaces for enterprise
    api_port: int = 8000
    api_workers: int = 8  # Increased for enterprise load
    api_reload: bool = False
    enable_swagger: bool = True
    enable_metrics: bool = True
    
    # Database - Enterprise Grade
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "mage_enterprise"
    db_user: str = "mage_admin"
    db_password: str = Field(default="", description="Database password")
    db_pool_size: int = 50  # Enterprise pool size
    db_max_overflow: int = 100
    db_pool_timeout: int = 30
    db_pool_recycle: int = 3600
    
    # Redis Cluster Configuration
    redis_cluster_nodes: List[str] = ["localhost:7001", "localhost:7002", "localhost:7003"]
    redis_password: Optional[str] = None
    redis_ssl: bool = True
    redis_sentinel_service: str = "mage-redis"
    
    # Advanced Security
    secret_key: str = Field(default="", description="JWT secret")
    encryption_algorithm: str = "AES-256-GCM"
    key_derivation_iterations: int = 100000
    session_timeout_minutes: int = 60
    max_failed_attempts: int = 3
    account_lockout_duration: int = 900  # 15 minutes
    
    # Multi-Factor Authentication
    enable_2fa: bool = True
    totp_issuer: str = "MAGE Enterprise"
    backup_codes_count: int = 10
    
    # AI & Machine Learning
    openai_api_key: str = Field(default="", description="OpenAI API key")
    openai_model: str = "gpt-4-turbo-preview"
    claude_api_key: str = Field(default="", description="Anthropic Claude API key")
    gemini_api_key: str = Field(default="", description="Google Gemini API key")
    
    # Advanced AI Configuration
    ai_temperature: float = 0.7
    ai_max_tokens: int = 8000
    ai_context_window: int = 32000
    enable_ai_memory: bool = True
    ai_reasoning_chains: bool = True
    
    # Game Testing Configuration
    supported_genres: List[GameGenre] = [
        GameGenre.ACTION, GameGenre.RPG, GameGenre.PUZZLE, 
        GameGenre.STRATEGY, GameGenre.SIMULATION
    ]
    supported_platforms: List[Platform] = [
        Platform.PC, Platform.WEB, Platform.MOBILE_ANDROID, Platform.MOBILE_IOS
    ]
    default_testing_modes: List[TestingMode] = [
        TestingMode.PERFORMANCE, TestingMode.AI_BEHAVIOR, TestingMode.GRAPHICS
    ]
    
    # Advanced Browser Configuration
    browser_pool_size: int = 10
    enable_browser_clustering: bool = True
    browser_types: List[str] = ["chromium", "firefox", "webkit", "edge"]
    headless_ratio: float = 0.8  # 80% headless, 20% headed
    
    # Performance Testing
    max_virtual_users: int = 1000
    ramp_up_duration: int = 300  # 5 minutes
    test_duration: int = 3600    # 1 hour
    performance_thresholds: Dict[str, float] = {
        "response_time_95th": 2000,  # ms
        "throughput_rps": 100,       # requests per second
        "error_rate": 0.01,          # 1%
        "memory_usage": 0.85,        # 85% of available
        "cpu_usage": 0.80            # 80% of available
    }
    
    # Graphics Testing
    enable_gpu_testing: bool = True
    target_fps: int = 60
    min_fps_threshold: int = 30
    resolution_profiles: List[str] = [
        "1920x1080", "2560x1440", "3840x2160", "1366x768"
    ]
    graphics_quality_levels: List[str] = ["low", "medium", "high", "ultra"]
    
    # AI Behavior Testing
    ai_complexity_levels: List[str] = ["basic", "intermediate", "advanced", "expert"]
    behavior_tree_depth: int = 8
    decision_tree_nodes: int = 1000
    pathfinding_algorithms: List[str] = ["A*", "Dijkstra", "JPS", "Hierarchical"]
    
    # Network Testing
    network_simulation_profiles: List[str] = [
        "3G", "4G", "5G", "WiFi", "Ethernet", "Poor", "Offline"
    ]
    latency_profiles: Dict[str, int] = {
        "excellent": 20,    # ms
        "good": 50,
        "fair": 100,
        "poor": 200,
        "terrible": 500
    }
    
    # Cloud Integration
    aws_access_key: str = Field(default="", description="AWS access key")
    aws_secret_key: str = Field(default="", description="AWS secret key")
    aws_region: str = "us-west-2"
    gcp_project_id: str = Field(default="", description="GCP project ID")
    azure_subscription_id: str = Field(default="", description="Azure subscription")
    
    # Gaming Platform Integration
    steam_api_key: str = Field(default="", description="Steam API key")
    epic_client_id: str = Field(default="", description="Epic Games client ID")
    xbox_app_id: str = Field(default="", description="Xbox Live app ID")
    playstation_client_id: str = Field(default="", description="PlayStation client ID")
    
    # Advanced Analytics
    enable_telemetry: bool = True
    analytics_endpoint: str = "https://analytics.mage-enterprise.com"
    enable_heatmaps: bool = True
    enable_session_replay: bool = True
    retention_days: int = 90
    
    # Machine Learning Pipeline
    ml_model_registry: str = "mlflow"
    enable_auto_ml: bool = True
    model_retraining_interval: int = 24  # hours
    feature_store_endpoint: str = ""
    
    # Real-time Monitoring
    prometheus_endpoint: str = "http://localhost:9090"
    grafana_endpoint: str = "http://localhost:3000"
    alertmanager_endpoint: str = "http://localhost:9093"
    enable_distributed_tracing: bool = True
    
    # File Storage - Enterprise
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    test_data_dir: Path = Field(default_factory=lambda: Path("data/test_data"))
    ml_models_dir: Path = Field(default_factory=lambda: Path("data/models"))
    screenshots_dir: Path = Field(default_factory=lambda: Path("artifacts/screenshots"))
    videos_dir: Path = Field(default_factory=lambda: Path("artifacts/videos"))
    performance_data_dir: Path = Field(default_factory=lambda: Path("data/performance"))
    
    # Logging - Enterprise Grade
    log_level: str = "INFO"
    enable_structured_logging: bool = True
    log_format: str = "json"
    log_rotation_size: str = "100MB"
    log_retention_days: int = 30
    enable_log_shipping: bool = True
    elasticsearch_endpoint: str = ""
    
    # Advanced Agent Configuration
    max_agents_per_session: int = 20
    agent_memory_limit: str = "2GB"
    agent_cpu_limit: float = 2.0
    enable_agent_clustering: bool = True
    agent_fault_tolerance: bool = True
    
    # Specialized Agent Types
    planner_agent_config: Dict[str, Any] = {
        "temperature": 0.8,
        "max_planning_depth": 10,
        "enable_reasoning": True,
        "memory_size": "1GB"
    }
    
    executor_agent_config: Dict[str, Any] = {
        "temperature": 0.3,
        "parallel_execution": True,
        "max_retries": 3,
        "timeout_seconds": 300
    }
    
    analyzer_agent_config: Dict[str, Any] = {
        "temperature": 0.4,
        "enable_ml_analysis": True,
        "confidence_threshold": 0.85,
        "deep_analysis": True
    }
    
    # Game-Specific Configuration
    unity_integration: bool = True
    unreal_integration: bool = True
    godot_integration: bool = True
    custom_engine_support: bool = True
    
    # VR/AR Testing
    enable_vr_testing: bool = True
    vr_headsets: List[str] = ["Quest 2", "Quest 3", "PICO 4", "Valve Index"]
    ar_devices: List[str] = ["HoloLens 2", "Magic Leap 2", "ARCore", "ARKit"]
    
    # Blockchain & Web3 Gaming
    enable_web3_testing: bool = True
    ethereum_rpc_url: str = ""
    polygon_rpc_url: str = ""
    solana_rpc_url: str = ""
    
    @field_validator("secret_key", "encryption_key")
    @classmethod
    def generate_secure_keys(cls, v: str) -> str:
        """Generate cryptographically secure keys"""
        if not v:
            import secrets
            return secrets.token_urlsafe(32)
        return v
    
    @field_validator("test_data_dir", "ml_models_dir", "screenshots_dir", "videos_dir", "performance_data_dir")
    @classmethod
    def create_directories(cls, v: Path) -> Path:
        """Ensure all required directories exist"""
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL"""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @property
    def redis_cluster_url(self) -> str:
        """Construct Redis Cluster connection URL"""
        nodes = ",".join(self.redis_cluster_nodes)
        return f"redis-cluster://{nodes}"


@lru_cache()
def get_settings() -> AdvancedSettings:
    """Get cached advanced settings instance"""
    return AdvancedSettings()
