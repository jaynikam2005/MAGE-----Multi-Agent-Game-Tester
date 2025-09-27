"""
GUI Module - Import the functional main window by default
"""

# Import the functional version by default
try:
    from src.gui.advanced.functional_main_window import FunctionalMainWindow as MainWindow
    FUNCTIONAL_GUI = True
    print("✅ Functional GUI module loaded")
except ImportError as e:
    print(f"⚠️  Functional GUI not available: {e}")
    # Fallback to basic implementation
    try:
        from src.gui.main_window import MainWindow
        FUNCTIONAL_GUI = False
        print("📋 Using basic GUI fallback")
    except ImportError:
        print("❌ No GUI implementation available")
        MainWindow = None
        FUNCTIONAL_GUI = False

__all__ = ['MainWindow', 'FUNCTIONAL_GUI']
