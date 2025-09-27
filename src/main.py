"""
Multi-Agent Game Tester - Main Entry Point
Advanced Desktop Application with Military-Grade Security
"""

import sys
import asyncio
import logging
from pathlib import Path
from typing import Optional
import signal
import os

from PyQt6.QtWidgets import QApplication, QStyleFactory
from PyQt6.QtCore import QDir, qmlRegisterType
from PyQt6.QtGui import QFont, QFontDatabase

from src.core.config import Settings, get_settings
from src.core.logger import setup_logging
from src.gui.main_window import MainWindow
from src.security.encryption import SecurityManager
from src.database.connection import DatabaseManager
from src.api.server import APIServer
from src.core.exception_handler import GlobalExceptionHandler


class ApplicationBootstrap:
    """Advanced application bootstrap with security and performance optimization"""
    
    def __init__(self):
        self.settings: Optional[Settings] = None
        self.app: Optional[QApplication] = None
        self.main_window: Optional[MainWindow] = None
        self.api_server: Optional[APIServer] = None
        self.security_manager: Optional[SecurityManager] = None
        self.db_manager: Optional[DatabaseManager] = None
        self.logger = logging.getLogger(__name__)
        
    async def initialize_security(self) -> None:
        """Initialize military-grade security components"""
        try:
            self.security_manager = SecurityManager()
            await self.security_manager.initialize()
            self.logger.info("Security manager initialized successfully")
        except Exception as e:
            self.logger.critical(f"Failed to initialize security: {e}")
            raise SystemExit(1)
    
    async def initialize_database(self) -> None:
        """Initialize encrypted database connection"""
        try:
            self.db_manager = DatabaseManager(self.settings)
            await self.db_manager.initialize()
            self.logger.info("Database manager initialized successfully")
        except Exception as e:
            self.logger.critical(f"Failed to initialize database: {e}")
            raise SystemExit(1)
    
    def setup_qt_application(self) -> None:
        """Setup PyQt6 application with advanced styling"""
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Multi-Agent Game Tester Pro")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("GameTester Corp")
        
        # Set modern style
        self.app.setStyle(QStyleFactory.create('Fusion'))
        
        # Load custom fonts
        font_db = QFontDatabase()
        font_path = Path(__file__).parent / "gui" / "assets" / "fonts"
        if font_path.exists():
            for font_file in font_path.glob("*.ttf"):
                font_db.addApplicationFont(str(font_file))
        
        # Set application font
        font = QFont("Segoe UI", 10)
        self.app.setFont(font)
        
    async def start_api_server(self) -> None:
        """Start FastAPI server in background"""
        try:
            self.api_server = APIServer(
                self.settings, 
                self.db_manager, 
                self.security_manager
            )
            await self.api_server.start()
            self.logger.info(f"API server started on port {self.settings.api_port}")
        except Exception as e:
            self.logger.error(f"Failed to start API server: {e}")
    
    def setup_signal_handlers(self) -> None:
        """Setup graceful shutdown handlers"""
        def signal_handler(signum, frame):
            self.logger.info(f"Received signal {signum}, shutting down gracefully...")
            self.shutdown()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def initialize_gui(self) -> None:
        """Initialize main GUI window"""
        try:
            self.main_window = MainWindow(
                self.settings,
                self.db_manager,
                self.security_manager,
                self.api_server
            )
            self.main_window.show()
            self.logger.info("GUI initialized successfully")
        except Exception as e:
            self.logger.critical(f"Failed to initialize GUI: {e}")
            raise SystemExit(1)
    
    def shutdown(self) -> None:
        """Graceful application shutdown"""
        self.logger.info("Initiating graceful shutdown...")
        
        if self.api_server:
            asyncio.create_task(self.api_server.stop())
        
        if self.db_manager:
            asyncio.create_task(self.db_manager.close())
        
        if self.security_manager:
            self.security_manager.cleanup()
        
        if self.app:
            self.app.quit()
        
        self.logger.info("Shutdown complete")
    
    async def run(self) -> int:
        """Main application runner"""
        try:
            # Load configuration
            self.settings = get_settings()
            
            # Setup logging
            setup_logging(self.settings.log_level, self.settings.log_file)
            self.logger.info("Starting Multi-Agent Game Tester Pro")
            
            # Initialize components
            await self.initialize_security()
            await self.initialize_database()
            
            # Setup Qt application
            self.setup_qt_application()
            self.setup_signal_handlers()
            
            # Start backend services
            await self.start_api_server()
            
            # Initialize GUI
            await self.initialize_gui()
            
            # Install global exception handler
            exception_handler = GlobalExceptionHandler()
            sys.excepthook = exception_handler.handle_exception
            
            # Run application
            return self.app.exec()
            
        except Exception as e:
            self.logger.critical(f"Application startup failed: {e}")
            return 1
        finally:
            self.shutdown()


async def main() -> int:
    """Async main entry point"""
    bootstrap = ApplicationBootstrap()
    return await bootstrap.run()


def sync_main() -> None:
    """Synchronous entry point for Poetry scripts"""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    return_code = asyncio.run(main())
    sys.exit(return_code)


if __name__ == "__main__":
    sync_main()
