"""
FastAPI Server for Backend Services
"""

import asyncio
from typing import Optional
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import structlog

from src.core.config import Settings
from src.security.encryption import SecurityManager
from src.database.connection import DatabaseManager


class APIServer:
    """FastAPI server for backend services"""
    
    def __init__(self, settings: Settings, db_manager: DatabaseManager, 
                 security_manager: SecurityManager):
        self.settings = settings
        self.db_manager = db_manager
        self.security_manager = security_manager
        self.logger = structlog.get_logger(__name__)
        
        self.app = FastAPI(
            title="Multi-Agent Game Tester API",
            version="1.0.0",
            description="Advanced AI-Powered Game Testing Platform API"
        )
        
        self.server: Optional[uvicorn.Server] = None
        self.setup_middleware()
        self.setup_routes()
    
    def setup_middleware(self):
        """Setup FastAPI middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],  # React frontend
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/")
        async def root():
            return {"message": "Multi-Agent Game Tester API", "version": "1.0.0"}
        
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "timestamp": "2025-09-28T01:48:00Z"}
        
        @self.app.post("/test/start")
        async def start_test(test_config: dict):
            return {"message": "Test started", "session_id": "test-123"}
        
        @self.app.get("/test/status/{session_id}")
        async def get_test_status(session_id: str):
            return {"session_id": session_id, "status": "running", "progress": 45}
    
    async def start(self):
        """Start the API server"""
        config = uvicorn.Config(
            self.app,
            host=self.settings.api_host,
            port=self.settings.api_port,
            log_level="info"
        )
        self.server = uvicorn.Server(config)
        
        # Start server in background task
        asyncio.create_task(self.server.serve())
        self.logger.info(f"API server started on {self.settings.api_host}:{self.settings.api_port}")
    
    async def stop(self):
        """Stop the API server"""
        if self.server:
            self.server.should_exit = True
            self.logger.info("API server stopped")
