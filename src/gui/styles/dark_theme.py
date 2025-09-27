"""
Dark Theme Stylesheet
"""


class DarkTheme:
    """Modern dark theme for the application"""
    
    @staticmethod
    def get_stylesheet() -> str:
        """Get complete dark theme stylesheet"""
        return """
        /* Main Application */
        QMainWindow {
            background-color: #212121;
            color: #FFFFFF;
        }
        
        QWidget {
            background-color: #212121;
            color: #FFFFFF;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        /* Menu Bar */
        QMenuBar {
            background-color: #303030;
            border-bottom: 1px solid #424242;
            padding: 4px;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 8px 12px;
            border-radius: 4px;
        }
        
        QMenuBar::item:selected {
            background-color: #2196F3;
        }
        
        QMenu {
            background-color: #424242;
            border: 1px solid #666;
            border-radius: 8px;
            padding: 4px;
        }
        
        QMenu::item {
            padding: 8px 16px;
            border-radius: 4px;
        }
        
        QMenu::item:selected {
            background-color: #2196F3;
        }
        
        /* Tool Bar */
        QToolBar {
            background-color: #303030;
            border: none;
            spacing: 3px;
            padding: 4px;
        }
        
        QToolButton {
            background-color: transparent;
            border: none;
            border-radius: 6px;
            padding: 8px;
            margin: 2px;
        }
        
        QToolButton:hover {
            background-color: #424242;
        }
        
        QToolButton:pressed {
            background-color: #2196F3;
        }
        
        /* Status Bar */
        QStatusBar {
            background-color: #303030;
            border-top: 1px solid #424242;
        }
        
        /* Frames and Group Boxes */
        QFrame {
            border: 1px solid #424242;
            border-radius: 8px;
            background-color: #303030;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #424242;
            border-radius: 8px;
            margin: 8px 0;
            padding-top: 16px;
            background-color: #303030;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 16px;
            padding: 0 8px;
            color: #2196F3;
        }
        
        /* Input Controls */
        QLineEdit {
            border: 2px solid #424242;
            border-radius: 6px;
            padding: 8px 12px;
            background-color: #212121;
            font-size: 14px;
        }
        
        QLineEdit:focus {
            border-color: #2196F3;
        }
        
        QSpinBox {
            border: 2px solid #424242;
            border-radius: 6px;
            padding: 8px;
            background-color: #212121;
        }
        
        QSpinBox:focus {
            border-color: #2196F3;
        }
        
        QComboBox {
            border: 2px solid #424242;
            border-radius: 6px;
            padding: 8px 12px;
            background-color: #212121;
            min-width: 120px;
        }
        
        QComboBox:focus {
            border-color: #2196F3;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 24px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #FFFFFF;
        }
        
        QComboBox QAbstractItemView {
            background-color: #424242;
            border: 1px solid #666;
            selection-background-color: #2196F3;
        }
        
        /* Check Boxes */
        QCheckBox {
            spacing: 8px;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid #424242;
            border-radius: 4px;
            background-color: #212121;
        }
        
        QCheckBox::indicator:checked {
            background-color: #2196F3;
            border-color: #2196F3;
        }
        
        /* Sliders */
        QSlider::groove:horizontal {
            border: 1px solid #424242;
            height: 8px;
            background-color: #212121;
            border-radius: 4px;
        }
        
        QSlider::handle:horizontal {
            background-color: #2196F3;
            border: 1px solid #1976D2;
            width: 20px;
            margin: -6px 0;
            border-radius: 10px;
        }
        
        QSlider::sub-page:horizontal {
            background-color: #2196F3;
            border-radius: 4px;
        }
        
        /* Text Areas */
        QTextEdit {
            border: 2px solid #424242;
            border-radius: 8px;
            background-color: #212121;
            padding: 8px;
            font-family: 'Consolas', monospace;
        }
        
        QTextEdit:focus {
            border-color: #2196F3;
        }
        
        /* Tables */
        QTableWidget {
            border: 1px solid #424242;
            border-radius: 8px;
            background-color: #212121;
            gridline-color: #424242;
            selection-background-color: #2196F3;
        }
        
        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid #424242;
        }
        
        QHeaderView::section {
            background-color: #303030;
            padding: 8px;
            border: none;
            border-bottom: 1px solid #424242;
            font-weight: bold;
        }
        
        /* Tree Widget */
        QTreeWidget {
            border: 1px solid #424242;
            border-radius: 8px;
            background-color: #212121;
            selection-background-color: #2196F3;
        }
        
        QTreeWidget::item {
            padding: 4px 8px;
            border-bottom: 1px solid #424242;
        }
        
        QTreeWidget::item:selected {
            background-color: #2196F3;
        }
        
        /* Tab Widget */
        QTabWidget::pane {
            border: 1px solid #424242;
            border-radius: 8px;
            background-color: #303030;
        }
        
        QTabBar::tab {
            background-color: #424242;
            padding: 12px 20px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }
        
        QTabBar::tab:selected {
            background-color: #2196F3;
        }
        
        QTabBar::tab:hover {
            background-color: #616161;
        }
        
        /* Scroll Bars */
        QScrollBar:vertical {
            background-color: #303030;
            width: 16px;
            border-radius: 8px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #424242;
            border-radius: 8px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #666;
        }
        
        QScrollBar:horizontal {
            background-color: #303030;
            height: 16px;
            border-radius: 8px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #424242;
            border-radius: 8px;
            min-width: 20px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #666;
        }
        
        /* Tooltips */
        QToolTip {
            background-color: #424242;
            color: #FFFFFF;
            border: 1px solid #666;
            border-radius: 6px;
            padding: 8px;
            font-size: 12px;
        }
        
        /* Splitter */
        QSplitter::handle {
            background-color: #424242;
        }
        
        QSplitter::handle:horizontal {
            width: 4px;
        }
        
        QSplitter::handle:vertical {
            height: 4px;
        }
        """
