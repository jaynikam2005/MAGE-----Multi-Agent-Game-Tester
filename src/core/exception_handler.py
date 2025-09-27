"""
Global Exception Handler
"""

import sys
import traceback
from typing import Any, Type
import structlog
from PyQt6.QtWidgets import QMessageBox, QApplication


class GlobalExceptionHandler:
    """Global exception handler for the application"""
    
    def __init__(self):
        self.logger = structlog.get_logger(__name__)
    
    def handle_exception(self, exc_type: Type[BaseException], 
                        exc_value: BaseException, exc_traceback: Any) -> None:
        """Handle unhandled exceptions"""
        if issubclass(exc_type, KeyboardInterrupt):
            # Handle Ctrl+C gracefully
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        # Log the exception
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.logger.error(f"Unhandled exception: {error_msg}")
        
        # Show error dialog
        app = QApplication.instance()
        if app:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Unexpected Error")
            msg.setText("An unexpected error occurred.")
            msg.setDetailedText(error_msg)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        
        # Call the default handler
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
