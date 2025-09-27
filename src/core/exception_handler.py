"""
Minimal Exception Handler
"""

import sys
import traceback
import logging
from typing import Any, Type


class GlobalExceptionHandler:
    """Minimal global exception handler"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def handle_exception(self, exc_type: Type[BaseException], 
                        exc_value: BaseException, exc_traceback: Any) -> None:
        """Handle unhandled exceptions"""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        # Log the exception
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.logger.error(f"Unhandled exception: {error_msg}")
        
        # Call the default handler
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
