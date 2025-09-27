"""
Advanced Dashboard Widgets
Real-time monitoring and visualization components
"""

import sys
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QProgressBar, QFrame, QScrollArea, QGraphicsView, QGraphicsScene
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QRectF, QPointF
from PyQt6.QtGui import (
    QPainter, QColor, QBrush, QPen, QLinearGradient, QRadialGradient,
    QFont, QPainterPath, QPolygonF
)
import structlog


class RealTimeDashboard(QWidget):
    """Real-time dashboard with live metrics"""
    
    def __init__(self):
        super().__init__()
        self.logger = structlog.get_logger(__name__)
        self.init_ui()
        
    def init_ui(self):
        """Initialize dashboard UI"""
        
        layout = QGridLayout(self)
        
        # Key metrics cards
        self.create_metrics_cards(layout)
        
        # Live charts area
        self.create_live_charts(layout)
        
    def create_metrics_cards(self, layout):
        """Create animated metrics cards"""
        
        # Active Tests Card
        self.active_tests_card = MetricCard("Active Tests", "0", "🧪", "#4CAF50")
        layout.addWidget(self.active_tests_card, 0, 0)
        
        # Success Rate Card
        self.success_rate_card = MetricCard("Success Rate", "0%", "✅", "#2196F3")
        layout.addWidget(self.success_rate_card, 0, 1)
        
        # Performance Card
        self.performance_card = MetricCard("Performance", "Good", "⚡", "#FF9800")
        layout.addWidget(self.performance_card, 0, 2)
        
        # Security Card
        self.security_card = MetricCard("Security", "Protected", "🛡️", "#9C27B0")
        layout.addWidget(self.security_card, 0, 3)
    
    def create_live_charts(self, layout):
        """Create live chart widgets"""
        
        # System performance chart
        self.performance_chart = LiveLineChart("System Performance")
        layout.addWidget(self.performance_chart, 1, 0, 1, 2)
        
        # Test execution chart
        self.test_chart = LiveBarChart("Test Execution")
        layout.addWidget(self.test_chart, 1, 2, 1, 2)
    
    def update_data(self, data: Dict[str, Any]):
        """Update dashboard with new data"""
        
        # Update metric cards
        self.active_tests_card.update_value(str(data.get("active_tests", 0)))
        self.success_rate_card.update_value(f"{data.get('success_rate', 0):.1f}%")
        
        cpu_usage = data.get("cpu_usage", 0)
        if cpu_usage > 80:
            performance_text = "High Load"
        elif cpu_usage > 60:
            performance_text = "Moderate"
        else:
            performance_text = "Good"
        self.performance_card.update_value(performance_text)
        
        # Update charts
        self.performance_chart.add_data_point(data.get("cpu_usage", 0))
        self.test_chart.add_data_point(data.get("active_tests", 0))


class MetricCard(QWidget):
    """Animated metric card widget"""
    
    def __init__(self, title: str, value: str, icon: str, color: str):
        super().__init__()
        self.title = title
        self.value = value
        self.icon = icon
        self.color = QColor(color)
        self.init_ui()
        
    def init_ui(self):
        """Initialize metric card UI"""
        
        self.setMinimumSize(200, 120)
        self.setMaximumSize(300, 150)
        
        layout = QVBoxLayout(self)
        
        # Header with icon and title
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-weight: bold; color: #666;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Value display
        self.value_label = QLabel(self.value)
        self.value_label.setStyleSheet(f"""
            font-size: 36px;
            font-weight: bold;
            color: {self.color.name()};
            margin: 10px;
        """)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)
        
        # Apply card styling
        self.setStyleSheet(f"""
            MetricCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.1), stop:1 rgba(255,255,255,0.05));
                border: 2px solid rgba({self.color.red()},{self.color.green()},{self.color.blue()},0.3);
                border-radius: 12px;
                margin: 5px;
            }}
            MetricCard:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.15), stop:1 rgba(255,255,255,0.08));
                border-color: rgba({self.color.red()},{self.color.green()},{self.color.blue()},0.6);
            }}
        """)
    
    def update_value(self, new_value: str):
        """Update card value with animation"""
        self.value = new_value
        self.value_label.setText(new_value)
        
        # Add subtle glow effect on update
        self.setStyleSheet(self.styleSheet() + """
            MetricCard { border-color: rgba(255,255,255,0.8); }
        """)
        
        # Reset styling after animation
        QTimer.singleShot(200, self.reset_styling)
    
    def reset_styling(self):
        """Reset card styling after animation"""
        self.setStyleSheet(f"""
            MetricCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255,255,255,0.1), stop:1 rgba(255,255,255,0.05));
                border: 2px solid rgba({self.color.red()},{self.color.green()},{self.color.blue()},0.3);
                border-radius: 12px;
                margin: 5px;
            }}
        """)


class LiveLineChart(QWidget):
    """Live updating line chart"""
    
    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.data_points = []
        self.max_points = 50
        self.init_ui()
        
    def init_ui(self):
        """Initialize chart UI"""
        
        self.setMinimumSize(400, 200)
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Chart area
        self.chart_widget = QWidget()
        self.chart_widget.setMinimumHeight(150)
        layout.addWidget(self.chart_widget)
        
        # Styling
        self.setStyleSheet("""
            LiveLineChart {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 10px;
            }
        """)
    
    def add_data_point(self, value: float):
        """Add new data point and trigger repaint"""
        
        self.data_points.append(value)
        
        # Keep only max_points
        if len(self.data_points) > self.max_points:
            self.data_points.pop(0)
        
        self.chart_widget.update()
    
    def paintEvent(self, event):
        """Custom paint event for chart"""
        
        super().paintEvent(event)
        
        if not self.data_points:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get widget rect
        rect = self.chart_widget.rect()
        
        # Calculate scaling
        if len(self.data_points) > 1:
            max_value = max(self.data_points)
            min_value = min(self.data_points)
            value_range = max_value - min_value if max_value > min_value else 1
            
            # Draw grid
            self.draw_grid(painter, rect)
            
            # Draw line
            self.draw_line(painter, rect, min_value, value_range)
    
    def draw_grid(self, painter: QPainter, rect: QRectF):
        """Draw chart grid"""
        
        painter.setPen(QPen(QColor(255, 255, 255, 30), 1))
        
        # Horizontal lines
        for i in range(5):
            y = rect.top() + (rect.height() / 4) * i
            painter.drawLine(rect.left(), y, rect.right(), y)
        
        # Vertical lines
        for i in range(10):
            x = rect.left() + (rect.width() / 9) * i
            painter.drawLine(x, rect.top(), x, rect.bottom())
    
    def draw_line(self, painter: QPainter, rect: QRectF, min_value: float, value_range: float):
        """Draw data line"""
        
        # Create gradient brush
        gradient = QLinearGradient(0, rect.top(), 0, rect.bottom())
        gradient.setColorAt(0, QColor(0, 150, 255, 180))
        gradient.setColorAt(1, QColor(0, 150, 255, 50))
        
        # Draw area under curve
        path = QPainterPath()
        
        if self.data_points:
            # Start path
            first_x = rect.left()
            first_y = rect.bottom() - ((self.data_points[0] - min_value) / value_range) * rect.height()
            path.moveTo(first_x, rect.bottom())
            path.lineTo(first_x, first_y)
            
            # Add data points
            for i, value in enumerate(self.data_points):
                x = rect.left() + (i / (len(self.data_points) - 1)) * rect.width()
                y = rect.bottom() - ((value - min_value) / value_range) * rect.height()
                path.lineTo(x, y)
            
            # Close path
            path.lineTo(rect.right(), rect.bottom())
            path.lineTo(rect.left(), rect.bottom())
        
        painter.fillPath(path, QBrush(gradient))
        
        # Draw line
        painter.setPen(QPen(QColor(0, 150, 255), 2))
        if len(self.data_points) > 1:
            for i in range(len(self.data_points) - 1):
                x1 = rect.left() + (i / (len(self.data_points) - 1)) * rect.width()
                y1 = rect.bottom() - ((self.data_points[i] - min_value) / value_range) * rect.height()
                
                x2 = rect.left() + ((i + 1) / (len(self.data_points) - 1)) * rect.width()
                y2 = rect.bottom() - ((self.data_points[i + 1] - min_value) / value_range) * rect.height()
                
                painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))


class LiveBarChart(QWidget):
    """Live updating bar chart"""
    
    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.data_points = []
        self.max_bars = 10
        self.init_ui()
        
    def init_ui(self):
        """Initialize bar chart UI"""
        
        self.setMinimumSize(400, 200)
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Chart area
        self.chart_widget = QWidget()
        self.chart_widget.setMinimumHeight(150)
        layout.addWidget(self.chart_widget)
        
        # Styling
        self.setStyleSheet("""
            LiveBarChart {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 10px;
            }
        """)
    
    def add_data_point(self, value: float):
        """Add new data point"""
        
        self.data_points.append(value)
        
        # Keep only max_bars
        if len(self.data_points) > self.max_bars:
            self.data_points.pop(0)
        
        self.chart_widget.update()
    
    def paintEvent(self, event):
        """Custom paint event for bar chart"""
        
        super().paintEvent(event)
        
        if not self.data_points:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get widget rect
        rect = self.chart_widget.rect()
        
        if self.data_points:
            max_value = max(self.data_points) if max(self.data_points) > 0 else 1
            
            # Draw bars
            bar_width = rect.width() / len(self.data_points)
            
            for i, value in enumerate(self.data_points):
                bar_height = (value / max_value) * rect.height()
                
                x = rect.left() + i * bar_width
                y = rect.bottom() - bar_height
                
                # Create gradient for bar
                gradient = QLinearGradient(0, y, 0, rect.bottom())
                gradient.setColorAt(0, QColor(0, 255, 150, 200))
                gradient.setColorAt(1, QColor(0, 255, 150, 100))
                
                # Draw bar
                painter.fillRect(x + 2, y, bar_width - 4, bar_height, QBrush(gradient))
                
                # Draw bar outline
                painter.setPen(QPen(QColor(0, 255, 150), 1))
                painter.drawRect(x + 2, y, bar_width - 4, bar_height)


class PerformanceGraphs(QWidget):
    """Advanced performance monitoring graphs"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize performance graphs"""
        
        layout = QVBoxLayout(self)
        
        # CPU Usage Graph
        self.cpu_graph = LiveLineChart("CPU Usage (%)")
        layout.addWidget(self.cpu_graph)
        
        # Memory Usage Graph
        self.memory_graph = LiveLineChart("Memory Usage (%)")
        layout.addWidget(self.memory_graph)
        
        # Network Activity Graph
        self.network_graph = LiveLineChart("Network Activity")
        layout.addWidget(self.network_graph)
    
    def update_graphs(self, performance_data: List[Dict[str, Any]]):
        """Update all performance graphs"""
        
        if performance_data:
            latest = performance_data[-1]
            
            self.cpu_graph.add_data_point(latest.get("cpu_usage", 0))
            self.memory_graph.add_data_point(latest.get("memory_usage", 0))
            
            # Simulate network activity
            network_activity = np.random.uniform(10, 90)
            self.network_graph.add_data_point(network_activity)


class SecurityMonitor(QWidget):
    """Security monitoring dashboard"""
    
    def __init__(self):
        super().__init__()
        self.security_events = []
        self.init_ui()
        
    def init_ui(self):
        """Initialize security monitor UI"""
        
        layout = QVBoxLayout(self)
        
        # Security status header
        header = QLabel("🛡️ Security Monitor")
        header.setStyleSheet("font-size: 16px; font-weight: bold; color: #2196F3; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Security metrics
        metrics_layout = QGridLayout()
        
        # Threat Level
        self.threat_level = SecurityMetric("Threat Level", "LOW", "#4CAF50")
        metrics_layout.addWidget(self.threat_level, 0, 0)
        
        # Active Scans
        self.active_scans = SecurityMetric("Active Scans", "3", "#FF9800")
        metrics_layout.addWidget(self.active_scans, 0, 1)
        
        # Vulnerabilities
        self.vulnerabilities = SecurityMetric("Vulnerabilities", "0", "#4CAF50")
        metrics_layout.addWidget(self.vulnerabilities, 1, 0)
        
        # Last Scan
        self.last_scan = SecurityMetric("Last Scan", "2m ago", "#9C27B0")
        metrics_layout.addWidget(self.last_scan, 1, 1)
        
        layout.addLayout(metrics_layout)
        
        # Recent events
        events_label = QLabel("Recent Security Events:")
        events_label.setStyleSheet("font-weight: bold; margin-top: 10px; margin-bottom: 5px;")
        layout.addWidget(events_label)
        
        self.events_area = QScrollArea()
        self.events_widget = QWidget()
        self.events_layout = QVBoxLayout(self.events_widget)
        self.events_area.setWidget(self.events_widget)
        self.events_area.setWidgetResizable(True)
        self.events_area.setMaximumHeight(150)
        layout.addWidget(self.events_area)
        
        # Add some sample events
        self.add_security_event("INFO", "Security scan completed successfully")
        self.add_security_event("WARNING", "Unusual network activity detected")
        self.add_security_event("INFO", "Firewall rules updated")
    
    def add_security_event(self, level: str, message: str):
        """Add security event to monitor"""
        
        event_widget = SecurityEvent(level, message, datetime.now())
        self.events_layout.insertWidget(0, event_widget)  # Add to top
        
        # Keep only last 10 events
        while self.events_layout.count() > 10:
            item = self.events_layout.takeAt(self.events_layout.count() - 1)
            if item.widget():
                item.widget().deleteLater()


class SecurityMetric(QWidget):
    """Individual security metric widget"""
    
    def __init__(self, title: str, value: str, color: str):
        super().__init__()
        self.title = title
        self.value = value
        self.color = color
        self.init_ui()
        
    def init_ui(self):
        """Initialize security metric UI"""
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-size: 10px; color: #666; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Value
        value_label = QLabel(self.value)
        value_label.setStyleSheet(f"font-size: 18px; color: {self.color}; font-weight: bold;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        
        # Styling
        self.setStyleSheet(f"""
            SecurityMetric {{
                background: rgba(255,255,255,0.05);
                border: 1px solid {self.color};
                border-radius: 6px;
                padding: 8px;
                margin: 2px;
            }}
        """)
        
        self.setMinimumSize(80, 60)


class SecurityEvent(QWidget):
    """Individual security event widget"""
    
    def __init__(self, level: str, message: str, timestamp: datetime):
        super().__init__()
        self.level = level
        self.message = message
        self.timestamp = timestamp
        self.init_ui()
        
    def init_ui(self):
        """Initialize security event UI"""
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        
        # Level indicator
        level_colors = {
            "INFO": "#4CAF50",
            "WARNING": "#FF9800", 
            "ERROR": "#F44336",
            "CRITICAL": "#9C27B0"
        }
        
        level_label = QLabel(self.level)
        level_label.setStyleSheet(f"""
            background: {level_colors.get(self.level, '#666')};
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 9px;
            font-weight: bold;
        """)
        level_label.setMaximumWidth(60)
        layout.addWidget(level_label)
        
        # Message
        message_label = QLabel(self.message)
        message_label.setStyleSheet("font-size: 10px; color: #ddd;")
        layout.addWidget(message_label)
        
        # Timestamp
        time_label = QLabel(self.timestamp.strftime("%H:%M:%S"))
        time_label.setStyleSheet("font-size: 9px; color: #888;")
        time_label.setMaximumWidth(50)
        layout.addWidget(time_label)
        
        # Event styling
        self.setStyleSheet("""
            SecurityEvent {
                background: rgba(255,255,255,0.03);
                border-radius: 3px;
                margin: 1px;
            }
            SecurityEvent:hover {
                background: rgba(255,255,255,0.08);
            }
        """)


class AgentVisualization(QWidget):
    """Agent network visualization widget"""
    
    def __init__(self):
        super().__init__()
        self.agents = {}
        self.init_ui()
        
    def init_ui(self):
        """Initialize agent visualization"""
        
        self.setMinimumSize(300, 200)
        
        # Styling
        self.setStyleSheet("""
            AgentVisualization {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(20,20,40,0.8), stop:1 rgba(40,40,80,0.8));
                border: 1px solid rgba(100,150,255,0.3);
                border-radius: 8px;
            }
        """)
    
    def update_agents(self, agent_data: Dict[str, Dict[str, Any]]):
        """Update agent visualization"""
        
        self.agents = agent_data
        self.update()
    
    def paintEvent(self, event):
        """Custom paint event for agent visualization"""
        
        super().paintEvent(event)
        
        if not self.agents:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        center = rect.center()
        
        # Draw agent nodes
        agent_positions = {}
        angle_step = 360 / len(self.agents) if self.agents else 0
        radius = min(rect.width(), rect.height()) * 0.3
        
        for i, (agent_id, data) in enumerate(self.agents.items()):
            angle = i * angle_step
            x = center.x() + radius * np.cos(np.radians(angle))
            y = center.y() + radius * np.sin(np.radians(angle))
            
            agent_positions[agent_id] = QPointF(x, y)
            
            # Draw agent node
            status_colors = {
                "active": QColor(76, 175, 80),
                "busy": QColor(255, 193, 7),
                "idle": QColor(158, 158, 158)
            }
            
            color = status_colors.get(data.get("status", "idle"), QColor(158, 158, 158))
            
            # Node glow effect
            gradient = QRadialGradient(x, y, 20)
            gradient.setColorAt(0, color)
            gradient.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 0))
            
            painter.setBrush(QBrush(gradient))
            painter.setPen(QPen(color, 2))
            painter.drawEllipse(QPointF(x, y), 15, 15)
            
            # Agent label
            painter.setPen(QPen(QColor(255, 255, 255), 1))
            painter.setFont(QFont("Arial", 8, QFont.Weight.Bold))
            painter.drawText(x - 20, y + 25, agent_id.split('_')[0])
        
        # Draw connections between agents
        painter.setPen(QPen(QColor(100, 150, 255, 100), 1))
        
        agent_list = list(agent_positions.items())
        for i, (agent1, pos1) in enumerate(agent_list):
            for j, (agent2, pos2) in enumerate(agent_list[i+1:], i+1):
                painter.drawLine(pos1, pos2)


class TestProgressVisualizer(QWidget):
    """Test progress visualization with animations"""
    
    def __init__(self):
        super().__init__()
        self.progress_value = 0
        self.is_animated = False
        self.init_ui()
        
        # Animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        
    def init_ui(self):
        """Initialize progress visualizer"""
        
        self.setMinimumHeight(80)
        
        layout = QVBoxLayout(self)
        
        # Progress info
        info_layout = QHBoxLayout()
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        info_layout.addWidget(self.status_label)
        
        info_layout.addStretch()
        
        self.progress_label = QLabel("0%")
        self.progress_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        info_layout.addWidget(self.progress_label)
        
        layout.addLayout(info_layout)
        
        # Custom progress bar area
        self.progress_area = QWidget()
        self.progress_area.setMinimumHeight(40)
        layout.addWidget(self.progress_area)
        
        # Styling
        self.setStyleSheet("""
            TestProgressVisualizer {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 10px;
            }
        """)
    
    def start_progress_animation(self):
        """Start progress animation"""
        
        self.is_animated = True
        self.animation_timer.start(50)  # 50ms updates
        self.status_label.setText("Testing in Progress...")
        self.status_label.setStyleSheet("font-weight: bold; color: #FF9800;")
    
    def stop_progress_animation(self):
        """Stop progress animation"""
        
        self.is_animated = False
        self.animation_timer.stop()
        self.status_label.setText("Completed")
        self.status_label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        self.progress_value = 100
        self.progress_label.setText("100%")
        self.update()
    
    def update_animation(self):
        """Update animation frame"""
        
        if self.is_animated and self.progress_value < 95:
            # Simulate progress
            self.progress_value += np.random.uniform(0.1, 1.0)
            self.progress_value = min(self.progress_value, 95)
            
            self.progress_label.setText(f"{self.progress_value:.1f}%")
            self.update()
    
    def paintEvent(self, event):
        """Custom paint event for progress visualization"""
        
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get progress area rect
        rect = self.progress_area.rect()
        
        if rect.width() <= 0 or rect.height() <= 0:
            return
        
        # Background
        painter.setBrush(QBrush(QColor(50, 50, 50, 100)))
        painter.setPen(QPen(QColor(100, 100, 100), 1))
        painter.drawRoundedRect(rect, 10, 10)
        
        # Progress fill
        if self.progress_value > 0:
            progress_width = (self.progress_value / 100.0) * rect.width()
            progress_rect = QRectF(rect.x(), rect.y(), progress_width, rect.height())
            
            # Gradient fill
            gradient = QLinearGradient(0, rect.y(), 0, rect.y() + rect.height())
            if self.is_animated:
                gradient.setColorAt(0, QColor(255, 193, 7, 200))  # Orange when active
                gradient.setColorAt(1, QColor(255, 152, 0, 200))
            else:
                gradient.setColorAt(0, QColor(76, 175, 80, 200))  # Green when complete
                gradient.setColorAt(1, QColor(56, 142, 60, 200))
            
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(progress_rect, 10, 10)
            
            # Animated shine effect
            if self.is_animated:
                shine_pos = (self.progress_value / 100.0) * rect.width()
                shine_gradient = QLinearGradient(shine_pos - 20, rect.y(), shine_pos + 20, rect.y())
                shine_gradient.setColorAt(0, QColor(255, 255, 255, 0))
                shine_gradient.setColorAt(0.5, QColor(255, 255, 255, 100))
                shine_gradient.setColorAt(1, QColor(255, 255, 255, 0))
                
                painter.setBrush(QBrush(shine_gradient))
                shine_rect = QRectF(shine_pos - 10, rect.y(), 20, rect.height())
                painter.drawRect(shine_rect)
