"""
Advanced Themes for Gaming Industry Desktop Application
Cyberpunk, Neon, and Futuristic Styling Systems
"""

from typing import Dict, Any
from PyQt6.QtGui import QColor


class AdvancedDarkTheme:
    """Professional dark theme for enterprise applications"""
    
    def __init__(self):
        self.colors = {
            'primary': '#0078D4',
            'primary_dark': '#005A9E',
            'secondary': '#40E0D0',
            'background': '#1E1E1E',
            'surface': '#2D2D2D',
            'surface_light': '#404040',
            'text_primary': '#FFFFFF',
            'text_secondary': '#B0B0B0',
            'accent': '#FF6B35',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'error': '#F44336',
            'border': '#404040',
            'shadow': 'rgba(0,0,0,0.3)'
        }
    
    def get_complete_stylesheet(self) -> str:
        """Get complete stylesheet for the theme"""
        
        return f"""
        /* Main Application Styling */
        QMainWindow {{
            background-color: {self.colors['background']};
            color: {self.colors['text_primary']};
            font-family: 'Segoe UI', 'Arial', sans-serif;
        }}
        
        QWidget {{
            background-color: {self.colors['background']};
            color: {self.colors['text_primary']};
        }}
        
        /* Menu Styling */
        QMenuBar {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.colors['surface']}, stop:1 {self.colors['background']});
            border-bottom: 2px solid {self.colors['primary']};
            padding: 4px;
            font-weight: bold;
        }}
        
        QMenuBar::item {{
            background: transparent;
            padding: 8px 16px;
            border-radius: 4px;
            margin: 2px;
        }}
        
        QMenuBar::item:selected {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.colors['primary']}, stop:1 {self.colors['primary_dark']});
        }}
        
        QMenu {{
            background-color: {self.colors['surface']};
            border: 2px solid {self.colors['border']};
            border-radius: 8px;
            padding: 6px;
        }}
        
        QMenu::item {{
            padding: 8px 20px;
            border-radius: 4px;
            margin: 2px;
        }}
        
        QMenu::item:selected {{
            background-color: {self.colors['primary']};
        }}
        
        /* Toolbar Styling */
        QToolBar {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.colors['surface_light']}, stop:1 {self.colors['surface']});
            border: none;
            spacing: 5px;
            padding: 8px;
        }}
        
        QToolButton {{
            background: transparent;
            border: 2px solid transparent;
            border-radius: 8px;
            padding: 8px 16px;
            margin: 2px;
            color: {self.colors['text_primary']};
            font-weight: bold;
        }}
        
        QToolButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.colors['primary']}, stop:1 {self.colors['primary_dark']});
            border-color: {self.colors['secondary']};
        }}
        
        /* Button Styling */
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.colors['surface_light']}, stop:1 {self.colors['surface']});
            border: 2px solid {self.colors['border']};
            border-radius: 8px;
            color: {self.colors['text_primary']};
            font-weight: bold;
            font-size: 14px;
            padding: 12px 24px;
            min-height: 20px;
        }}
        
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.colors['primary']}, stop:1 {self.colors['primary_dark']});
            border-color: {self.colors['secondary']};
        }}
        
        QPushButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.colors['primary_dark']}, stop:1 {self.colors['primary']});
        }}
        
        /* Input Controls */
        QLineEdit {{
            background-color: {self.colors['surface']};
            border: 2px solid {self.colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
            color: {self.colors['text_primary']};
        }}
        
        QLineEdit:focus {{
            border-color: {self.colors['primary']};
        }}
        
        QComboBox {{
            background-color: {self.colors['surface']};
            border: 2px solid {self.colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            min-width: 120px;
            color: {self.colors['text_primary']};
        }}
        
        QComboBox:focus {{
            border-color: {self.colors['primary']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 24px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {self.colors['surface']};
            border: 2px solid {self.colors['border']};
            selection-background-color: {self.colors['primary']};
            color: {self.colors['text_primary']};
        }}
        
        /* Checkbox Styling */
        QCheckBox {{
            spacing: 8px;
            color: {self.colors['text_primary']};
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {self.colors['border']};
            border-radius: 4px;
            background-color: {self.colors['surface']};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {self.colors['primary']};
            border-color: {self.colors['primary']};
        }}
        
        /* Slider Styling */
        QSlider::groove:horizontal {{
            border: none;
            height: 8px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {self.colors['surface']}, stop:1 {self.colors['surface_light']});
            border-radius: 4px;
        }}
        
        QSlider::handle:horizontal {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {self.colors['primary']}, stop:1 {self.colors['primary_dark']});
            border: 2px solid {self.colors['secondary']};
            width: 20px;
            height: 20px;
            margin: -6px 0;
            border-radius: 12px;
        }}
        
        QSlider::sub-page:horizontal {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {self.colors['primary']}, stop:1 {self.colors['secondary']});
            border-radius: 4px;
        }}
        
        /* Table Styling */
        QTableWidget {{
            background-color: {self.colors['surface']};
            border: 2px solid {self.colors['border']};
            border-radius: 8px;
            gridline-color: {self.colors['border']};
            selection-background-color: {self.colors['primary']};
            color: {self.colors['text_primary']};
        }}
        
        QHeaderView::section {{
            background-color: {self.colors['surface_light']};
            padding: 8px;
            border: none;
            border-bottom: 2px solid {self.colors['border']};
            font-weight: bold;
            color: {self.colors['text_primary']};
        }}
        
        /* Tree Widget */
        QTreeWidget {{
            background-color: {self.colors['surface']};
            border: 2px solid {self.colors['border']};
            border-radius: 8px;
            selection-background-color: {self.colors['primary']};
            color: {self.colors['text_primary']};
        }}
        
        QTreeWidget::item {{
            padding: 6px;
            border-bottom: 1px solid {self.colors['border']};
        }}
        
        QTreeWidget::item:selected {{
            background-color: {self.colors['primary']};
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 2px solid {self.colors['border']};
            border-radius: 8px;
            background-color: {self.colors['surface']};
        }}
        
        QTabBar::tab {{
            background-color: {self.colors['surface_light']};
            padding: 12px 20px;
            margin-right: 2px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            color: {self.colors['text_secondary']};
        }}
        
        QTabBar::tab:selected {{
            background-color: {self.colors['primary']};
            color: {self.colors['text_primary']};
        }}
        
        /* Progress Bar */
        QProgressBar {{
            border: 2px solid {self.colors['border']};
            border-radius: 8px;
            text-align: center;
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
            font-weight: bold;
        }}
        
        QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {self.colors['primary']}, stop:1 {self.colors['secondary']});
            border-radius: 6px;
            margin: 2px;
        }}
        
        /* Scroll Bars */
        QScrollBar:vertical {{
            background-color: {self.colors['surface']};
            width: 16px;
            border-radius: 8px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {self.colors['surface_light']};
            border-radius: 8px;
            min-height: 20px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {self.colors['primary']};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.colors['surface']}, stop:1 {self.colors['background']});
            border-top: 2px solid {self.colors['primary']};
            color: {self.colors['text_primary']};
        }}
        
        /* Dock Widgets */
        QDockWidget {{
            color: {self.colors['text_primary']};
            font-weight: bold;
        }}
        
        QDockWidget::title {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.colors['surface_light']}, stop:1 {self.colors['surface']});
            padding: 8px;
            border-radius: 4px;
        }}
        
        /* Text Edit */
        QTextEdit {{
            background-color: {self.colors['surface']};
            border: 2px solid {self.colors['border']};
            border-radius: 8px;
            color: {self.colors['text_primary']};
            padding: 8px;
            font-family: 'Consolas', monospace;
        }}
        
        QTextEdit:focus {{
            border-color: {self.colors['primary']};
        }}
        
        /* Group Box */
        QGroupBox {{
            font-weight: bold;
            border: 2px solid {self.colors['border']};
            border-radius: 8px;
            margin: 8px 0;
            padding-top: 16px;
            background-color: {self.colors['surface']};
            color: {self.colors['text_primary']};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 16px;
            padding: 0 8px;
            color: {self.colors['primary']};
        }}
        """


class NeonTheme(AdvancedDarkTheme):
    """Neon-style theme with glowing effects"""
    
    def __init__(self):
        super().__init__()
        self.colors.update({
            'primary': '#00FF88',
            'primary_dark': '#00CC66',
            'secondary': '#FF0088',
            'background': '#0A0A0A',
            'surface': '#1A1A2E',
            'surface_light': '#16213E',
            'accent': '#FF6B35',
            'neon_glow': 'rgba(0,255,136,0.5)',
            'neon_shadow': 'rgba(0,255,136,0.3)'
        })
    
    def get_complete_stylesheet(self) -> str:
        """Get neon-enhanced stylesheet"""
        
        base_style = super().get_complete_stylesheet()
        
        neon_additions = f"""
        
        /* Neon Enhancements */
        QPushButton {{
            text-shadow: 0 0 10px {self.colors['neon_glow']};
            border: 2px solid {self.colors['primary']};
        }}
        
        QPushButton:hover {{
            box-shadow: 0 0 20px {self.colors['neon_glow']};
            text-shadow: 0 0 15px {self.colors['neon_glow']};
        }}
        
        QLineEdit:focus {{
            box-shadow: 0 0 15px {self.colors['neon_glow']};
        }}
        
        QSlider::handle:horizontal {{
            box-shadow: 0 0 10px {self.colors['neon_glow']};
        }}
        
        QTabBar::tab:selected {{
            box-shadow: 0 0 15px {self.colors['neon_glow']};
        }}
        
        /* Neon Text Effects */
        QLabel {{
            text-shadow: 0 0 5px {self.colors['neon_shadow']};
        }}
        
        QMenuBar::item:selected {{
            text-shadow: 0 0 10px {self.colors['neon_glow']};
        }}
        """
        
        return base_style + neon_additions


class CyberpunkTheme(AdvancedDarkTheme):
    """Cyberpunk 2077 inspired theme"""
    
    def __init__(self):
        super().__init__()
        self.colors.update({
            'primary': '#FCEE09',
            'primary_dark': '#E6D200',
            'secondary': '#FF003C',
            'tertiary': '#00F5FF',
            'background': '#0F0F0F',
            'surface': '#1E1E1E',
            'surface_light': '#2E2E2E',
            'text_primary': '#FCEE09',
            'text_secondary': '#B0B0B0',
            'accent': '#FF003C',
            'cyber_pink': '#FF1493',
            'cyber_blue': '#00BFFF'
        })
    
    def get_complete_stylesheet(self) -> str:
        """Get cyberpunk-enhanced stylesheet"""
        
        base_style = super().get_complete_stylesheet()
        
        cyberpunk_additions = f"""
        
        /* Cyberpunk Enhancements */
        QMainWindow {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {self.colors['background']}, 
                stop:0.5 rgba(255,0,60,0.05), 
                stop:1 {self.colors['background']});
        }}
        
        QPushButton {{
            border: 2px solid {self.colors['primary']};
            color: {self.colors['primary']};
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {self.colors['secondary']}, stop:1 {self.colors['tertiary']});
            color: {self.colors['background']};
            border-color: {self.colors['cyber_pink']};
        }}
        
        QMenuBar {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {self.colors['background']}, 
                stop:0.5 rgba(252,238,9,0.1), 
                stop:1 {self.colors['background']});
            border-bottom: 3px solid {self.colors['primary']};
        }}
        
        QTabBar::tab:selected {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {self.colors['primary']}, stop:1 {self.colors['secondary']});
            color: {self.colors['background']};
        }}
        
        /* Cyberpunk Progress Bar */
        QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {self.colors['primary']}, 
                stop:0.5 {self.colors['secondary']}, 
                stop:1 {self.colors['tertiary']});
        }}
        
        /* Cyberpunk Scroll Bars */
        QScrollBar::handle:vertical:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {self.colors['cyber_pink']}, stop:1 {self.colors['cyber_blue']});
        }}
        
        /* Glitch Effects for Selected Items */
        QTreeWidget::item:selected {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {self.colors['primary']}, 
                stop:0.3 {self.colors['secondary']}, 
                stop:0.7 {self.colors['tertiary']}, 
                stop:1 {self.colors['primary']});
            color: {self.colors['background']};
        }}
        """
        
        return base_style + cyberpunk_additions
