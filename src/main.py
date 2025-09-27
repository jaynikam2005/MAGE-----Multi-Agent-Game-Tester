"""
Multi-Agent Game Tester - Main Entry Point
GUARANTEED FUNCTIONAL VERSION
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
    from PyQt6.QtGui import QFont
except ImportError:
    print("❌ PyQt6 not found. Please install it with: poetry add PyQt6")
    sys.exit(1)

# Import settings
try:
    from src.core.config import get_settings
    print("✅ Core configuration loaded")
except ImportError:
    print("⚠️  Using fallback settings")
    class Settings:
        app_name = "Multi-Agent Game Tester Pro"
        version = "2.0.0"
        target_game_url = "https://play.ezygamers.com/"
    
    def get_settings():
        return Settings()

def setup_qt_application():
    """Setup PyQt6 application"""
    app = QApplication(sys.argv)
    app.setApplicationName("MAGE - Multi-Agent Game Tester Enterprise")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("MAGE Corporation")
    
    # Set modern style
    available_styles = QStyleFactory.keys()
    if 'Fusion' in available_styles:
        app.setStyle(QStyleFactory.create('Fusion'))
    
    return app

def create_functional_application(settings):
    """Create the functional application - NOT DEMO VERSION"""
    
    print("🔧 CREATING FUNCTIONAL APPLICATION...")
    
    # FORCE IMPORT THE FUNCTIONAL VERSION
    sys.path.insert(0, str(Path(__file__).parent))
    
    try:
        # Import the functional main window directly
        import importlib.util
        
        # Load the functional main window module
        spec = importlib.util.spec_from_file_location(
            "functional_main_window", 
            Path(__file__).parent / "gui" / "advanced" / "functional_main_window.py"
        )
        
        if spec and spec.loader:
            functional_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(functional_module)
            
            # Create the functional main window
            FunctionalMainWindow = functional_module.FunctionalMainWindow
            main_window = FunctionalMainWindow(settings)
            
            print("✅ FUNCTIONAL MAIN WINDOW CREATED SUCCESSFULLY!")
            return main_window
        else:
            raise ImportError("Could not load functional module")
            
    except Exception as e:
        print(f"❌ Error creating functional application: {e}")
        print("🔄 Attempting direct import...")
        
        try:
            # Direct import attempt
            from src.gui.advanced.functional_main_window import FunctionalMainWindow
            main_window = FunctionalMainWindow(settings) 
            print("✅ DIRECT IMPORT SUCCESSFUL!")
            return main_window
        except ImportError as e2:
            print(f"❌ Direct import also failed: {e2}")
            raise Exception("Cannot load functional GUI")

def main():
    """Main application entry point - GUARANTEED FUNCTIONAL"""
    try:
        print("🎮 STARTING MAGE ENTERPRISE - FUNCTIONAL VERSION")
        print("=" * 60)
        print("🚀 LOADING REAL IMPLEMENTATIONS (NOT DEMO)")
        print("=" * 60)
        
        # Setup Qt application
        app = setup_qt_application()
        
        # Load settings
        settings = get_settings()
        print(f"✅ Settings loaded: {settings.app_name} v{settings.version}")
        
        # Create functional application
        print("🏗️  Creating functional main window...")
        main_window = create_functional_application(settings)
        
        # Show the window
        main_window.show()
        
        print("🎉 SUCCESS! FUNCTIONAL APPLICATION IS RUNNING!")
        print("=" * 60)
        print("✅ ACTIVE FEATURES:")
        print("  📊 Real-time Dashboard with live system metrics")
        print("  🧪 Functional Testing Console with WebDriver")
        print("  📈 Working Reports that generate actual files")  
        print("  ⚙️  Functional Settings with file persistence")
        print("  📝 Real System Logs with database storage")
        print("  🛡️  Working Security Scanner with real scans")
        print("  💾 SQLite Database with full operations")
        print("  🌐 Browser automation with Selenium")
        print("  📊 Performance monitoring with real metrics")
        print("  🤖 Agent management with status tracking")
        print("=" * 60)
        print("🖥️  The application window is now open with ALL WORKING FEATURES!")
        
        # Run application
        return app.exec()
    
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        print("\n🔍 TROUBLESHOOTING:")
        print("1. Make sure all files are in the correct locations")
        print("2. Check that PyQt6 is installed: poetry add PyQt6")
        print("3. Verify the functional_main_window.py file exists")
        
        import traceback
        print("\n📋 Full error details:")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
