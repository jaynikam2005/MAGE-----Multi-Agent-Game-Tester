"""
Modern UI Widgets with Advanced Styling
"""

from PyQt6.QtWidgets import QPushButton, QProgressBar, QFrame
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QBrush, QFont


class ModernButton(QPushButton):
    """Modern styled button with hover animations"""
    
    def __init__(self, text: str = "", primary: bool = False, danger: bool = False):
        super().__init__(text)
        self.primary = primary
        self.danger = danger
        self.setup_style()
    
    def setup_style(self):
        """Setup button styling"""
        base_style = """
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                transform: translateY(0px);
            }
            QPushButton:disabled {
                opacity: 0.6;
            }
        """
        
        if self.primary:
            style = base_style + """
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """
        elif self.danger:
            style = base_style + """
                QPushButton {
                    background-color: #f44336;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
            """
        else:
            style = base_style + """
                QPushButton {
                    background-color: #424242;
                    color: white;
                    border: 1px solid #666;
                }
                QPushButton:hover {
                    background-color: #616161;
                    border-color: #2196F3;
                }
            """
        
        self.setStyleSheet(style)


class ModernProgressBar(QProgressBar):
    """Modern styled progress bar"""
    
    def __init__(self):
        super().__init__()
        self.setup_style()
    
    def setup_style(self):
        """Setup progress bar styling"""
        self.setStyleSheet("""
            QProgressBar {
                border: 2px solid #424242;
                border-radius: 8px;
                text-align: center;
                background-color: #303030;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2196F3, stop:1 #21CBF3
                );
                border-radius: 6px;
                margin: 2px;
            }
        """)


class ModernCard(QFrame):
    """Modern card widget"""
    
    def __init__(self, title: str = ""):
        super().__init__()
        self.title = title
        self.setup_style()
    
    def setup_style(self):
        """Setup card styling"""
        self.setFrameStyle(QFrame.Shape.Box)
        self.setStyleSheet("""
            QFrame {
                background-color: #424242;
                border: 1px solid #666;
                border-radius: 12px;
                padding: 16px;
                margin: 8px;
            }
            QFrame:hover {
                border-color: #2196F3;
                box-shadow: 0 4px 8px rgba(33, 150, 243, 0.3);
            }
        """)
