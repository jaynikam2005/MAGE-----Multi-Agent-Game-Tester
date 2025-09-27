"""
Main GUI Window - Advanced PyQt6 Desktop Interface
"""

import sys
from typing import Optional, Dict, Any
from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QTextEdit, QProgressBar, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem,
    QGroupBox, QFrame, QSplitter, QScrollArea, QStatusBar,
    QMenuBar, QToolBar, QMessageBox, QFileDialog, QDialog,
    QLineEdit, QSpinBox, QCheckBox, QComboBox, QSlider,
    QApplication, QHeaderView
)
from PyQt6.QtCore import (
    Qt, QThread, QTimer, pyqtSignal, pyqtSlot, QSize, QRect,
    QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
)
from PyQt6.QtGui import (
    QIcon, QPixmap, QFont, QPalette, QColor, QAction,
    QPainter, QBrush, QLinearGradient, QMovie
)
import structlog

from src.core.config import Settings
from src.security.encryption import SecurityManager
from src.database.connection import DatabaseManager
from src.api.server import APIServer
from src.gui.widgets.modern_widgets import ModernButton, ModernCard, ModernProgressBar
from src.gui.styles.dark_theme import DarkTheme


class TestExecutionThread(QThread):
    """Background thread for test execution"""
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    test_completed = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, test_config: Dict[str, Any]):
        super().__init__()
        self.test_config = test_config
        self.logger = structlog.get_logger(__name__)
        self._is_running = False
    
    def run(self):
        """Execute tests in background"""
        self._is_running = True
        try:
            # Simulate test execution
            total_steps = 100
            for i in range(total_steps):
                if not self._is_running:
                    break
                
                # Simulate work
                self.msleep(50)
                
                # Update progress
                progress = int((i + 1) / total_steps * 100)
                self.progress_updated.emit(progress)
                self.status_updated.emit(f"Executing test step {i + 1}/{total_steps}")
            
            # Simulate completion
            if self._is_running:
                result = {"status": "completed", "tests_run": 10, "passed": 8, "failed": 2}
                self.test_completed.emit(result)
                self.status_updated.emit("Test execution completed successfully")
                
        except Exception as e:
            self.error_occurred.emit(str(e))
            self.logger.error(f"Test execution failed: {e}")
    
    def stop(self):
        """Stop test execution"""
        self._is_running = False


class MainWindow(QMainWindow):
    """Modern main window with advanced UI"""
    
    def __init__(self, settings: Settings, db_manager: DatabaseManager, 
                 security_manager: SecurityManager, api_server: APIServer):
        super().__init__()
        
        self.settings = settings
        self.db_manager = db_manager
        self.security_manager = security_manager
        self.api_server = api_server
        self.logger = structlog.get_logger(__name__)
        
        # UI Components
        self.central_widget = None
        self.status_bar = None
        self.progress_bar = None
        self.test_thread: Optional[TestExecutionThread] = None
        
        # Animation groups
        self.animation_group = QParallelAnimationGroup()
        
        # Initialize UI
        self.init_ui()
        self.apply_theme()
        self.setup_animations()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Multi-Agent Game Tester Pro v1.0")
        self.setMinimumSize(1400, 900)
        self.resize(1600, 1000)
        
        # Center window on screen
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2, 
                 (screen.height() - self.height()) // 2)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Create main content
        content_splitter = self.create_main_content()
        main_layout.addWidget(content_splitter)
        
        # Create status bar
        self.create_status_bar()
        
        self.logger.info("Main window UI initialized")
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu('File')
        
        new_action = QAction('New Test Session', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_test_session)
        file_menu.addAction(new_action)
        
        open_action = QAction('Open Session', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_session)
        file_menu.addAction(open_action)
        
        save_action = QAction('Save Session', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_session)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Test Menu
        test_menu = menubar.addMenu('Test')
        
        start_action = QAction('Start Testing', self)
        start_action.setShortcut('F5')
        start_action.triggered.connect(self.start_testing)
        test_menu.addAction(start_action)
        
        stop_action = QAction('Stop Testing', self)
        stop_action.setShortcut('F6')
        stop_action.triggered.connect(self.stop_testing)
        test_menu.addAction(stop_action)
        
        # View Menu
        view_menu = menubar.addMenu('View')
        
        logs_action = QAction('Show Logs', self)
        logs_action.triggered.connect(self.show_logs)
        view_menu.addAction(logs_action)
        
        reports_action = QAction('Show Reports', self)
        reports_action.triggered.connect(self.show_reports)
        view_menu.addAction(reports_action)
        
        # Help Menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create main toolbar"""
        toolbar = self.addToolBar('Main')
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        
        # New Session
        new_action = QAction('New', self)
        new_action.setToolTip('Create new test session')
        new_action.triggered.connect(self.new_test_session)
        toolbar.addAction(new_action)
        
        # Start Testing
        start_action = QAction('Start', self)
        start_action.setToolTip('Start test execution')
        start_action.triggered.connect(self.start_testing)
        toolbar.addAction(start_action)
        
        # Stop Testing
        stop_action = QAction('Stop', self)
        stop_action.setToolTip('Stop test execution')
        stop_action.triggered.connect(self.stop_testing)
        toolbar.addAction(stop_action)
        
        toolbar.addSeparator()
        
        # Settings
        settings_action = QAction('Settings', self)
        settings_action.setToolTip('Application settings')
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)
    
    def create_header(self) -> QWidget:
        """Create header section"""
        header = QFrame()
        header.setFrameStyle(QFrame.Shape.Box)
        header.setMaximumHeight(120)
        
        layout = QHBoxLayout(header)
        
        # Logo/Title section
        title_section = QVBoxLayout()
        
        title = QLabel("Multi-Agent Game Tester Pro")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2196F3; padding: 5px;")
        
        subtitle = QLabel("Advanced AI-Powered Game Testing Platform")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #666; padding: 2px;")
        
        title_section.addWidget(title)
        title_section.addWidget(subtitle)
        
        # Status section
        status_section = QVBoxLayout()
        status_section.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.connection_status = QLabel("🔒 Secure Connection Active")
        self.connection_status.setStyleSheet("color: #4CAF50; font-weight: bold;")
        
        self.agent_status = QLabel("🤖 5 Agents Ready")
        self.agent_status.setStyleSheet("color: #2196F3;")
        
        status_section.addWidget(self.connection_status)
        status_section.addWidget(self.agent_status)
        
        layout.addLayout(title_section)
        layout.addStretch()
        layout.addLayout(status_section)
        
        return header
    
    def create_main_content(self) -> QSplitter:
        """Create main content area"""
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Configuration & Control
        left_panel = self.create_control_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Results & Monitoring
        right_panel = self.create_results_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([400, 1000])
        
        return splitter
    
    def create_control_panel(self) -> QWidget:
        """Create left control panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.Box)
        panel.setMaximumWidth(450)
        
        layout = QVBoxLayout(panel)
        
        # Test Configuration
        config_group = QGroupBox("Test Configuration")
        config_layout = QVBoxLayout(config_group)
        
        # Target URL
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("Target URL:"))
        self.url_input = QLineEdit(self.settings.target_game_url)
        url_layout.addWidget(self.url_input)
        config_layout.addLayout(url_layout)
        
        # Number of tests
        tests_layout = QHBoxLayout()
        tests_layout.addWidget(QLabel("Test Cases:"))
        self.test_count = QSpinBox()
        self.test_count.setRange(1, 100)
        self.test_count.setValue(20)
        tests_layout.addWidget(self.test_count)
        config_layout.addLayout(tests_layout)
        
        # Browser selection
        browser_layout = QHBoxLayout()
        browser_layout.addWidget(QLabel("Browser:"))
        self.browser_combo = QComboBox()
        self.browser_combo.addItems(["Chromium", "Firefox", "WebKit"])
        browser_layout.addWidget(self.browser_combo)
        config_layout.addLayout(browser_layout)
        
        # Advanced options
        self.headless_check = QCheckBox("Headless Mode")
        self.headless_check.setChecked(True)
        config_layout.addWidget(self.headless_check)
        
        self.parallel_check = QCheckBox("Parallel Execution")
        self.parallel_check.setChecked(True)
        config_layout.addWidget(self.parallel_check)
        
        layout.addWidget(config_group)
        
        # Agent Configuration
        agent_group = QGroupBox("Agent Configuration")
        agent_layout = QVBoxLayout(agent_group)
        
        # Temperature slider
        temp_layout = QVBoxLayout()
        temp_layout.addWidget(QLabel("AI Temperature:"))
        self.temperature_slider = QSlider(Qt.Orientation.Horizontal)
        self.temperature_slider.setRange(0, 100)
        self.temperature_slider.setValue(70)
        self.temperature_label = QLabel("0.7")
        self.temperature_slider.valueChanged.connect(
            lambda v: self.temperature_label.setText(f"{v/100:.1f}")
        )
        temp_layout.addWidget(self.temperature_slider)
        temp_layout.addWidget(self.temperature_label)
        agent_layout.addLayout(temp_layout)
        
        layout.addWidget(agent_group)
        
        # Control Buttons
        button_layout = QVBoxLayout()
        
        self.start_button = ModernButton("🚀 Start Testing", primary=True)
        self.start_button.clicked.connect(self.start_testing)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = ModernButton("⏹️ Stop Testing", danger=True)
        self.stop_button.clicked.connect(self.stop_testing)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        self.generate_report_button = ModernButton("📊 Generate Report")
        self.generate_report_button.clicked.connect(self.generate_report)
        button_layout.addWidget(self.generate_report_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        return panel
    
    def create_results_panel(self) -> QWidget:
        """Create right results panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.Box)
        
        layout = QVBoxLayout(panel)
        
        # Progress section
        progress_group = QGroupBox("Execution Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = ModernProgressBar()
        self.progress_label = QLabel("Ready to start testing...")
        
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addWidget(progress_group)
        
        # Tab widget for results
        self.results_tabs = QTabWidget()
        
        # Test Cases Tab
        self.test_cases_tab = self.create_test_cases_tab()
        self.results_tabs.addTab(self.test_cases_tab, "Test Cases")
        
        # Agents Tab
        self.agents_tab = self.create_agents_tab()
        self.results_tabs.addTab(self.agents_tab, "Agents")
        
        # Logs Tab
        self.logs_tab = self.create_logs_tab()
        self.results_tabs.addTab(self.logs_tab, "Logs")
        
        # Reports Tab
        self.reports_tab = self.create_reports_tab()
        self.results_tabs.addTab(self.reports_tab, "Reports")
        
        layout.addWidget(self.results_tabs)
        
        return panel
    
    def create_test_cases_tab(self) -> QWidget:
        """Create test cases tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Test cases table
        self.test_cases_table = QTableWidget()
        self.test_cases_table.setColumnCount(6)
        self.test_cases_table.setHorizontalHeaderLabels([
            "ID", "Name", "Type", "Status", "Result", "Duration"
        ])
        
        # Set column widths
        header = self.test_cases_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.test_cases_table)
        
        return widget
    
    def create_agents_tab(self) -> QWidget:
        """Create agents monitoring tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Agents tree
        self.agents_tree = QTreeWidget()
        self.agents_tree.setHeaderLabels(["Agent", "Status", "Tasks", "Performance"])
        
        # Add sample agents
        agents = [
            ("PlannerAgent", "Active", "3/5", "98.5%"),
            ("RankerAgent", "Active", "2/3", "97.2%"),
            ("ExecutorAgent-1", "Busy", "1/1", "99.1%"),
            ("ExecutorAgent-2", "Idle", "0/1", "98.8%"),
            ("AnalyzerAgent", "Active", "2/4", "96.9%"),
            ("OrchestratorAgent", "Active", "1/1", "99.5%")
        ]
        
        for name, status, tasks, perf in agents:
            item = QTreeWidgetItem([name, status, tasks, perf])
            # Color code by status
            if status == "Active":
                item.setBackground(1, QColor(76, 175, 80, 50))
            elif status == "Busy":
                item.setBackground(1, QColor(255, 193, 7, 50))
            else:
                item.setBackground(1, QColor(158, 158, 158, 50))
            
            self.agents_tree.addTopLevelItem(item)
        
        layout.addWidget(self.agents_tree)
        
        return widget
    
    def create_logs_tab(self) -> QWidget:
        """Create logs tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        
        # Add sample logs
        sample_logs = [
            "2025-09-28 01:48:00 - INFO - Security manager initialized successfully",
            "2025-09-28 01:48:01 - INFO - Database connection established",
            "2025-09-28 01:48:02 - INFO - PlannerAgent started",
            "2025-09-28 01:48:03 - INFO - Test case generation in progress...",
            "2025-09-28 01:48:05 - INFO - Generated 25 candidate test cases",
            "2025-09-28 01:48:06 - INFO - RankerAgent ranking test cases...",
            "2025-09-28 01:48:08 - INFO - Selected top 10 test cases for execution"
        ]
        
        self.log_text.setText("\n".join(sample_logs))
        
        layout.addWidget(self.log_text)
        
        return widget
    
    def create_reports_tab(self) -> QWidget:
        """Create reports tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Reports list
        self.reports_table = QTableWidget()
        self.reports_table.setColumnCount(4)
        self.reports_table.setHorizontalHeaderLabels([
            "Timestamp", "Session", "Status", "Actions"
        ])
        
        layout.addWidget(self.reports_table)
        
        return widget
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add permanent widgets
        self.status_bar.addWidget(QLabel("Ready"))
        self.status_bar.addPermanentWidget(QLabel("🔒 Secure"))
        self.status_bar.addPermanentWidget(QLabel("📊 v1.0.0"))
    
    def apply_theme(self):
        """Apply dark theme"""
        theme = DarkTheme()
        self.setStyleSheet(theme.get_stylesheet())
    
    def setup_animations(self):
        """Setup UI animations"""
        # Progress bar pulse animation
        self.progress_animation = QPropertyAnimation(self.progress_bar, b"value")
        self.progress_animation.setDuration(1000)
        self.progress_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
    
    # Slot methods
    @pyqtSlot()
    def new_test_session(self):
        """Create new test session"""
        self.log_text.append("Creating new test session...")
        self.status_bar.showMessage("New test session created", 3000)
    
    @pyqtSlot()
    def open_session(self):
        """Open existing session"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Session", "", "JSON Files (*.json)"
        )
        if filename:
            self.log_text.append(f"Opening session: {filename}")
    
    @pyqtSlot()
    def save_session(self):
        """Save current session"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Session", "", "JSON Files (*.json)"
        )
        if filename:
            self.log_text.append(f"Saving session: {filename}")
    
    @pyqtSlot()
    def start_testing(self):
        """Start test execution"""
        if self.test_thread and self.test_thread.isRunning():
            return
        
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        # Create test configuration
        test_config = {
            "url": self.url_input.text(),
            "test_count": self.test_count.value(),
            "browser": self.browser_combo.currentText(),
            "headless": self.headless_check.isChecked(),
            "parallel": self.parallel_check.isChecked(),
            "temperature": self.temperature_slider.value() / 100
        }
        
        # Start test thread
        self.test_thread = TestExecutionThread(test_config)
        self.test_thread.progress_updated.connect(self.update_progress)
        self.test_thread.status_updated.connect(self.update_status)
        self.test_thread.test_completed.connect(self.on_test_completed)
        self.test_thread.error_occurred.connect(self.on_test_error)
        self.test_thread.start()
        
        self.log_text.append("Starting test execution...")
    
    @pyqtSlot()
    def stop_testing(self):
        """Stop test execution"""
        if self.test_thread:
            self.test_thread.stop()
            self.test_thread.wait()
        
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setValue(0)
        
        self.log_text.append("Test execution stopped")
        self.update_status("Test execution stopped")
    
    @pyqtSlot(int)
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    @pyqtSlot(str)
    def update_status(self, message):
        """Update status message"""
        self.progress_label.setText(message)
        self.status_bar.showMessage(message, 5000)
    
    @pyqtSlot(dict)
    def on_test_completed(self, result):
        """Handle test completion"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        message = f"Tests completed: {result['tests_run']} run, {result['passed']} passed, {result['failed']} failed"
        self.log_text.append(message)
        
        # Show completion dialog
        QMessageBox.information(self, "Test Completed", message)
    
    @pyqtSlot(str)
    def on_test_error(self, error):
        """Handle test error"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setValue(0)
        
        self.log_text.append(f"Error: {error}")
        QMessageBox.critical(self, "Test Error", f"An error occurred: {error}")
    
    @pyqtSlot()
    def generate_report(self):
        """Generate test report"""
        self.log_text.append("Generating comprehensive test report...")
        QMessageBox.information(self, "Report Generated", "Test report has been generated successfully!")
    
    @pyqtSlot()
    def show_settings(self):
        """Show settings dialog"""
        QMessageBox.information(self, "Settings", "Settings dialog would open here")
    
    @pyqtSlot()
    def show_logs(self):
        """Show logs dialog"""
        self.results_tabs.setCurrentWidget(self.logs_tab)
    
    @pyqtSlot()
    def show_reports(self):
        """Show reports dialog"""
        self.results_tabs.setCurrentWidget(self.reports_tab)
    
    @pyqtSlot()
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self, 
            "About Multi-Agent Game Tester Pro",
            """
            <h3>Multi-Agent Game Tester Pro v1.0.0</h3>
            <p>Advanced AI-Powered Game Testing Platform</p>
            <p>Built with military-grade security and cutting-edge AI technology.</p>
            <p><b>Features:</b></p>
            <ul>
                <li>Multi-agent AI testing system</li>
                <li>Advanced security encryption</li>
                <li>Real-time monitoring and reporting</li>
                <li>Cross-platform compatibility</li>
            </ul>
            <p>© 2025 GameTester Corp. All rights reserved.</p>
            """
        )
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.test_thread and self.test_thread.isRunning():
            reply = QMessageBox.question(
                self, 
                "Confirm Exit",
                "Tests are still running. Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.test_thread.stop()
                self.test_thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
