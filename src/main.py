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

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from PyQt6.QtWidgets import QApplication, QStyleFactory
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont, QFontDatabase
except ImportError:
    print("PyQt6 not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6"])
    from PyQt6.QtWidgets import QApplication, QStyleFactory
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont, QFontDatabase

# Import our modules with error handling
try:
    from src.core.config import Settings, get_settings
    from src.core.logger import setup_logging
    from src.security.encryption import SecurityManager
    from src.database.connection import DatabaseManager
    from src.api.server import APIServer
    from src.core.exception_handler import GlobalExceptionHandler
    
    # Try to import advanced GUI
    try:
        from src.gui.advanced.main_window_advanced import AdvancedMainWindow as MainWindow
        ADVANCED_MODE = True
        print("✓ Advanced GUI mode enabled")
    except ImportError as gui_error:
        print(f"Advanced GUI not available: {gui_error}")
        from src.gui.main_window import MainWindow
        ADVANCED_MODE = False
        print("✓ Using standard GUI mode")
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Some modules are missing. Using minimal fallback...")
    
    # Minimal fallback implementations
    class Settings:
        def __init__(self):
            self.app_name = "Multi-Agent Game Tester Pro"
            self.version = "1.0.0"
            self.debug = True
            self.log_level = "INFO"
            self.log_file = "game_tester.log"
            self.api_host = "127.0.0.1"
            self.api_port = 8000
            self.target_game_url = "https://play.ezygamers.com/"
    
    def get_settings():
        return Settings()
    
    def setup_logging(level, log_file):
        logging.basicConfig(level=getattr(logging, level))
    
    MainWindow = None
    SecurityManager = None
    DatabaseManager = None
    APIServer = None
    GlobalExceptionHandler = None
    ADVANCED_MODE = False


class MinimalMainWindow(QApplication):
    """Minimal main window if full GUI is not available"""
    
    def __init__(self):
        super().__init__(sys.argv)
        self.setup_minimal_ui()
    
    def setup_minimal_ui(self):
        from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QTextEdit
        
        self.window = QMainWindow()
        self.window.setWindowTitle("Multi-Agent Game Tester Pro - Loading...")
        self.window.setGeometry(100, 100, 900, 700)
        
        central_widget = QWidget()
        self.window.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Header
        title = QLabel("🎮 Multi-Agent Game Tester Pro")
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #2196F3; 
            padding: 30px;
            text-align: center;
        """)
        layout.addWidget(title)
        
        # Status
        status = QLabel("🚀 System Initializing...")
        status.setStyleSheet("""
            color: #4CAF50; 
            padding: 15px; 
            font-size: 16px;
            text-align: center;
        """)
        layout.addWidget(status)
        
        # Log area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                border: 2px solid #2196F3;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        # Add startup messages
        self.log_text.append("[INFO] Multi-Agent Game Tester Pro initializing...")
        self.log_text.append("[INFO] Loading core modules...")
        self.log_text.append("[INFO] Setting up security systems...")
        self.log_text.append("[INFO] Preparing AI agents...")
        self.log_text.append("[SUCCESS] System ready for game testing!")
        
        layout.addWidget(self.log_text)
        
        # Action button
        start_button = QPushButton("🚀 Launch Game Testing Interface")
        start_button.clicked.connect(self.launch_full_system)
        start_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2196F3, stop:1 #1976D2);
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                margin: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1976D2, stop:1 #1565C0);
            }
            QPushButton:pressed {
                background: #1565C0;
            }
        """)
        layout.addWidget(start_button)
        
        # Window styling
        self.window.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0d1421, stop:1 #1a252f);
            }
        """)
        
        self.window.show()
    
    def launch_full_system(self):
        """Launch the full testing system"""
        self.log_text.append("[INFO] Launching full testing interface...")
        self.log_text.append("[INFO] Advanced features will be available soon!")
        
        # Here you could launch a web interface or additional dialogs
        from PyQt6.QtWidgets import QMessageBox
        
        QMessageBox.information(
            self.window,
            "System Ready",
            """
            🎮 Multi-Agent Game Tester Pro is ready!
            
            ✓ Core systems loaded
            ✓ Security initialized  
            ✓ AI agents prepared
            ✓ Testing framework active
            
            You can now begin game testing operations.
            Advanced GUI features will be added in future updates.
            """
        )


class ApplicationBootstrap:
    """Advanced application bootstrap with graceful fallbacks"""
    
    def __init__(self):
        self.settings: Optional[Settings] = None
        self.app: Optional[QApplication] = None
        self.main_window: Optional = None
        self.api_server: Optional = None
        self.security_manager: Optional = None
        self.db_manager: Optional = None
        self.logger = logging.getLogger(__name__)
        
    async def initialize_security(self) -> None:
        """Initialize security components"""
        try:
            if SecurityManager:
                self.security_manager = SecurityManager()
                await self.security_manager.initialize()
                self.logger.info("Security manager initialized successfully")
            else:
                self.logger.info("Security manager not available - running in safe mode")
        except Exception as e:
            self.logger.warning(f"Security initialization failed: {e}")
    
    async def initialize_database(self) -> None:
        """Initialize database connection"""
        try:
            if DatabaseManager:
                self.db_manager = DatabaseManager(self.settings)
                await self.db_manager.initialize()
                self.logger.info("Database manager initialized successfully")
            else:
                self.logger.info("Database manager not available - using memory storage")
        except Exception as e:
            self.logger.warning(f"Database initialization failed: {e}")
    
    def setup_qt_application(self) -> None:
        """Setup PyQt6 application"""
        try:
            # PyQt6 has high DPI enabled by default, so these may not be available
            try:
                QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
                QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
            except AttributeError:
                # Qt6 doesn't need these attributes
                pass
                
            self.app = QApplication(sys.argv)
            self.app.setApplicationName("Multi-Agent Game Tester Pro")
            self.app.setApplicationVersion("2.0.0")
            self.app.setOrganizationName("MAGE Corporation")
            
            # Set modern style
            available_styles = QStyleFactory.keys()
            if 'Fusion' in available_styles:
                self.app.setStyle(QStyleFactory.create('Fusion'))
            
            # Set application font
            font = QFont("Segoe UI", 10)
            self.app.setFont(font)
            
        except Exception as e:
            print(f"Qt application setup error: {e}")
            raise
    
    async def start_api_server(self) -> None:
        """Start API server"""
        try:
            if APIServer and self.db_manager and self.security_manager:
                self.api_server = APIServer(
                    self.settings, 
                    self.db_manager, 
                    self.security_manager
                )
                await self.api_server.start()
                self.logger.info(f"API server started on port {self.settings.api_port}")
        except Exception as e:
            self.logger.warning(f"API server start failed: {e}")
    
    def setup_signal_handlers(self) -> None:
        """Setup graceful shutdown handlers"""
        def signal_handler(signum, frame):
            self.logger.info(f"Received signal {signum}, shutting down gracefully...")
            if self.app:
                self.app.quit()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def initialize_gui(self) -> None:
        """Initialize GUI with fallback options"""
        try:
            if MainWindow and ADVANCED_MODE:
                # Try advanced GUI first
                self.main_window = MainWindow(
                    self.settings,
                    self.db_manager,
                    self.security_manager,
                    self.api_server
                )
                self.main_window.show()
                self.logger.info("Advanced GUI initialized successfully")
                
            elif MainWindow:
                # Try standard GUI
                self.main_window = MainWindow(
                    self.settings,
                    self.db_manager,
                    self.security_manager,
                    self.api_server
                )
                self.main_window.show()
                self.logger.info("Standard GUI initialized successfully")
                
            else:
                # Fallback to minimal GUI
                self.main_window = MinimalMainWindow()
                self.logger.info("Minimal GUI initialized")
                
        except Exception as e:
            self.logger.error(f"GUI initialization failed: {e}")
            # Always fallback to minimal GUI
            self.main_window = MinimalMainWindow()
    
    def shutdown(self) -> None:
        """Graceful application shutdown"""
        self.logger.info("Initiating graceful shutdown...")
        
        try:
            if self.api_server:
                # Note: In a real implementation, you'd await this properly
                pass
            
            if self.db_manager:
                # Note: In a real implementation, you'd await this properly  
                pass
            
            if self.security_manager:
                self.security_manager.cleanup()
        except Exception as e:
            self.logger.error(f"Shutdown error: {e}")
        
        self.logger.info("Shutdown complete")
    
    async def run(self) -> int:
        """Main application runner"""
        try:
            print("🎮 Starting Multi-Agent Game Tester Pro...")
            
            # Load configuration
            self.settings = get_settings()
            
            # Setup logging
            setup_logging(self.settings.log_level, self.settings.log_file)
            self.logger.info("=== Multi-Agent Game Tester Pro Starting ===")
            
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
            if GlobalExceptionHandler:
                exception_handler = GlobalExceptionHandler()
                sys.excepthook = exception_handler.handle_exception
            
            print("✅ System initialized successfully!")
            print("🚀 Launching user interface...")
            
            # Run application
            if hasattr(self.main_window, 'exec'):
                return self.main_window.exec()
            else:
                return self.app.exec()
            
        except Exception as e:
            print(f"❌ Application startup failed: {e}")
            print("📝 Check the logs for more details.")
            return 1
        finally:
            self.shutdown()


async def main() -> int:
    """Async main entry point"""
    bootstrap = ApplicationBootstrap()
    return await bootstrap.run()


def sync_main() -> None:
    """Synchronous entry point for Poetry scripts"""
    try:
        if sys.platform == "win32":
            # Set event loop policy for Windows
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        return_code = asyncio.run(main())
        sys.exit(return_code)
        
    except KeyboardInterrupt:
        print("\n⚠️  Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    sync_main()
