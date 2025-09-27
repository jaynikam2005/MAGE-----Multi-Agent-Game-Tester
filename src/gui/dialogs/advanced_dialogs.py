"""
Advanced Dialog Classes
Specialized dialogs for system information, performance profiling, security scanning
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QPushButton, QLabel, QTextEdit, QProgressBar, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem,
    QGroupBox, QFrame, QScrollArea, QSplitter, QDialogButtonBox,
    QLineEdit, QSpinBox, QCheckBox, QComboBox, QSlider
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot, QThread, QRunnable, QThreadPool
from PyQt6.QtGui import QFont, QPixmap, QIcon


class PerformanceProfilerDialog(QDialog):
    """Performance profiler dialog with real-time analysis"""
    
    def __init__(self, performance_data, parent=None):
        super().__init__(parent)
        
        self.performance_data = performance_data
        self.setWindowTitle("⚡ Performance Profiler")
        self.setMinimumSize(800, 600)
        self.init_ui()
        self.analyze_performance_data()
    
    def init_ui(self):
        """Initialize profiler UI"""
        
        layout = QVBoxLayout(self)
        
        # Performance Analysis Tabs
        self.tabs = QTabWidget()
        
        # CPU Analysis Tab
        cpu_tab = self.create_cpu_analysis_tab()
        self.tabs.addTab(cpu_tab, "🖥️ CPU Analysis")
        
        # Memory Analysis Tab
        memory_tab = self.create_memory_analysis_tab()
        self.tabs.addTab(memory_tab, "💾 Memory Analysis")
        
        # Response Time Tab
        response_tab = self.create_response_analysis_tab()
        self.tabs.addTab(response_tab, "⚡ Response Time")
        
        # Recommendations Tab
        recommendations_tab = self.create_recommendations_tab()
        self.tabs.addTab(recommendations_tab, "💡 Recommendations")
        
        layout.addWidget(self.tabs)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close |
            QDialogButtonBox.StandardButton.Save
        )
        button_box.accepted.connect(self.save_profile)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: white;
            }
            QTabWidget::pane {
                border: 2px solid #404040;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background: #404040;
                padding: 8px 16px;
                margin-right: 2px;
                color: white;
            }
            QTabBar::tab:selected {
                background: #0078d4;
            }
            QTextEdit {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                color: #00ff00;
                font-family: 'Consolas', monospace;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 16px;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                color: #0078d4;
            }
        """)
    
    def create_cpu_analysis_tab(self):
        """Create CPU analysis tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # CPU Statistics
        stats_group = QGroupBox("📊 CPU Statistics")
        stats_layout = QGridLayout(stats_group)
        
        if self.performance_data:
            cpu_values = [p.cpu_usage for p in self.performance_data]
            avg_cpu = sum(cpu_values) / len(cpu_values)
            max_cpu = max(cpu_values)
            min_cpu = min(cpu_values)
            
            stats_layout.addWidget(QLabel("Average CPU Usage:"), 0, 0)
            stats_layout.addWidget(QLabel(f"{avg_cpu:.1f}%"), 0, 1)
            
            stats_layout.addWidget(QLabel("Peak CPU Usage:"), 1, 0)
            stats_layout.addWidget(QLabel(f"{max_cpu:.1f}%"), 1, 1)
            
            stats_layout.addWidget(QLabel("Minimum CPU Usage:"), 2, 0)
            stats_layout.addWidget(QLabel(f"{min_cpu:.1f}%"), 2, 1)
            
            stats_layout.addWidget(QLabel("Data Points:"), 3, 0)
            stats_layout.addWidget(QLabel(str(len(cpu_values))), 3, 1)
        
        layout.addWidget(stats_group)
        
        # CPU Analysis Details
        analysis_group = QGroupBox("🔍 CPU Analysis")
        analysis_layout = QVBoxLayout(analysis_group)
        
        self.cpu_analysis = QTextEdit()
        self.cpu_analysis.setReadOnly(True)
        analysis_layout.addWidget(self.cpu_analysis)
        
        layout.addWidget(analysis_group)
        
        return widget
    
    def create_memory_analysis_tab(self):
        """Create memory analysis tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Memory Statistics
        stats_group = QGroupBox("💾 Memory Statistics")
        stats_layout = QGridLayout(stats_group)
        
        if self.performance_data:
            memory_values = [p.memory_usage for p in self.performance_data]
            avg_memory = sum(memory_values) / len(memory_values)
            max_memory = max(memory_values)
            min_memory = min(memory_values)
            
            stats_layout.addWidget(QLabel("Average Memory Usage:"), 0, 0)
            stats_layout.addWidget(QLabel(f"{avg_memory:.1f}%"), 0, 1)
            
            stats_layout.addWidget(QLabel("Peak Memory Usage:"), 1, 0)
            stats_layout.addWidget(QLabel(f"{max_memory:.1f}%"), 1, 1)
            
            stats_layout.addWidget(QLabel("Minimum Memory Usage:"), 2, 0)
            stats_layout.addWidget(QLabel(f"{min_memory:.1f}%"), 2, 1)
        
        layout.addWidget(stats_group)
        
        # Memory Analysis Details
        analysis_group = QGroupBox("🔍 Memory Analysis")
        analysis_layout = QVBoxLayout(analysis_group)
        
        self.memory_analysis = QTextEdit()
        self.memory_analysis.setReadOnly(True)
        analysis_layout.addWidget(self.memory_analysis)
        
        layout.addWidget(analysis_group)
        
        return widget
    
    def create_response_analysis_tab(self):
        """Create response time analysis tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Response Time Statistics
        stats_group = QGroupBox("⚡ Response Time Statistics")
        stats_layout = QGridLayout(stats_group)
        
        if self.performance_data:
            response_values = [p.response_time_ms for p in self.performance_data]
            avg_response = sum(response_values) / len(response_values)
            max_response = max(response_values)
            min_response = min(response_values)
            
            stats_layout.addWidget(QLabel("Average Response Time:"), 0, 0)
            stats_layout.addWidget(QLabel(f"{avg_response:.1f}ms"), 0, 1)
            
            stats_layout.addWidget(QLabel("Slowest Response:"), 1, 0)
            stats_layout.addWidget(QLabel(f"{max_response:.1f}ms"), 1, 1)
            
            stats_layout.addWidget(QLabel("Fastest Response:"), 2, 0)
            stats_layout.addWidget(QLabel(f"{min_response:.1f}ms"), 2, 1)
        
        layout.addWidget(stats_group)
        
        # Response Analysis Details
        analysis_group = QGroupBox("🔍 Response Time Analysis")
        analysis_layout = QVBoxLayout(analysis_group)
        
        self.response_analysis = QTextEdit()
        self.response_analysis.setReadOnly(True)
        analysis_layout.addWidget(self.response_analysis)
        
        layout.addWidget(analysis_group)
        
        return widget
    
    def create_recommendations_tab(self):
        """Create recommendations tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        recommendations_group = QGroupBox("💡 Performance Recommendations")
        recommendations_layout = QVBoxLayout(recommendations_group)
        
        self.recommendations = QTextEdit()
        self.recommendations.setReadOnly(True)
        recommendations_layout.addWidget(self.recommendations)
        
        layout.addWidget(recommendations_group)
        
        return widget
    
    def analyze_performance_data(self):
        """Analyze performance data and populate tabs"""
        
        if not self.performance_data:
            self.cpu_analysis.setText("No performance data available for analysis.")
            self.memory_analysis.setText("No performance data available for analysis.")
            self.response_analysis.setText("No performance data available for analysis.")
            self.recommendations.setText("No recommendations available without performance data.")
            return
        
        # CPU Analysis
        cpu_values = [p.cpu_usage for p in self.performance_data]
        avg_cpu = sum(cpu_values) / len(cpu_values)
        
        cpu_analysis_text = f"""
🖥️ CPU Performance Analysis

📊 Statistical Summary:
• Average CPU Usage: {avg_cpu:.1f}%
• Peak CPU Usage: {max(cpu_values):.1f}%
• CPU Usage Variance: {self.calculate_variance(cpu_values):.2f}

📈 Performance Trends:
• High CPU periods: {len([c for c in cpu_values if c > 80])} data points
• Moderate CPU periods: {len([c for c in cpu_values if 50 < c <= 80])} data points
• Low CPU periods: {len([c for c in cpu_values if c <= 50])} data points

🎯 CPU Efficiency Score: {self.calculate_cpu_score(avg_cpu)}/100
        """.strip()
        
        self.cpu_analysis.setText(cpu_analysis_text)
        
        # Memory Analysis
        memory_values = [p.memory_usage for p in self.performance_data]
        avg_memory = sum(memory_values) / len(memory_values)
        
        memory_analysis_text = f"""
💾 Memory Performance Analysis

📊 Statistical Summary:
• Average Memory Usage: {avg_memory:.1f}%
• Peak Memory Usage: {max(memory_values):.1f}%
• Memory Usage Variance: {self.calculate_variance(memory_values):.2f}

📈 Memory Trends:
• High memory periods: {len([m for m in memory_values if m > 80])} data points
• Moderate memory periods: {len([m for m in memory_values if 50 < m <= 80])} data points
• Low memory periods: {len([m for m in memory_values if m <= 50])} data points

🎯 Memory Efficiency Score: {self.calculate_memory_score(avg_memory)}/100
        """.strip()
        
        self.memory_analysis.setText(memory_analysis_text)
        
        # Response Time Analysis
        response_values = [p.response_time_ms for p in self.performance_data]
        avg_response = sum(response_values) / len(response_values)
        
        response_analysis_text = f"""
⚡ Response Time Analysis

📊 Statistical Summary:
• Average Response Time: {avg_response:.1f}ms
• Slowest Response: {max(response_values):.1f}ms
• Fastest Response: {min(response_values):.1f}ms
• Response Time Variance: {self.calculate_variance(response_values):.2f}

📈 Response Trends:
• Slow responses (>200ms): {len([r for r in response_values if r > 200])} data points
• Moderate responses (100-200ms): {len([r for r in response_values if 100 < r <= 200])} data points
• Fast responses (<100ms): {len([r for r in response_values if r <= 100])} data points

🎯 Response Time Score: {self.calculate_response_score(avg_response)}/100
        """.strip()
        
        self.response_analysis.setText(response_analysis_text)
        
        # Generate Recommendations
        recommendations = self.generate_recommendations(avg_cpu, avg_memory, avg_response)
        self.recommendations.setText(recommendations)
    
    def calculate_variance(self, values):
        """Calculate variance of values"""
        if not values:
            return 0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5  # Standard deviation
    
    def calculate_cpu_score(self, avg_cpu):
        """Calculate CPU efficiency score"""
        if avg_cpu < 30:
            return 100
        elif avg_cpu < 50:
            return 85
        elif avg_cpu < 70:
            return 70
        elif avg_cpu < 85:
            return 50
        else:
            return 25
    
    def calculate_memory_score(self, avg_memory):
        """Calculate memory efficiency score"""
        if avg_memory < 40:
            return 100
        elif avg_memory < 60:
            return 85
        elif avg_memory < 75:
            return 70
        elif avg_memory < 85:
            return 50
        else:
            return 25
    
    def calculate_response_score(self, avg_response):
        """Calculate response time score"""
        if avg_response < 50:
            return 100
        elif avg_response < 100:
            return 85
        elif avg_response < 200:
            return 70
        elif avg_response < 500:
            return 50
        else:
            return 25
    
    def generate_recommendations(self, avg_cpu, avg_memory, avg_response):
        """Generate performance recommendations"""
        
        recommendations = "💡 Performance Optimization Recommendations\n\n"
        
        # CPU Recommendations
        if avg_cpu > 80:
            recommendations += "🔥 CRITICAL - CPU Usage:\n"
            recommendations += "• Consider upgrading CPU or reducing workload\n"
            recommendations += "• Profile CPU-intensive operations\n"
            recommendations += "• Implement CPU usage optimization\n\n"
        elif avg_cpu > 60:
            recommendations += "⚠️ WARNING - CPU Usage:\n"
            recommendations += "• Monitor CPU-intensive processes\n"
            recommendations += "• Consider optimizing algorithms\n\n"
        else:
            recommendations += "✅ CPU Usage: Within optimal range\n\n"
        
        # Memory Recommendations
        if avg_memory > 85:
            recommendations += "🔥 CRITICAL - Memory Usage:\n"
            recommendations += "• Immediate memory optimization required\n"
            recommendations += "• Check for memory leaks\n"
            recommendations += "• Consider increasing RAM\n\n"
        elif avg_memory > 70:
            recommendations += "⚠️ WARNING - Memory Usage:\n"
            recommendations += "• Monitor memory consumption\n"
            recommendations += "• Optimize data structures\n\n"
        else:
            recommendations += "✅ Memory Usage: Within optimal range\n\n"
        
        # Response Time Recommendations
        if avg_response > 200:
            recommendations += "🔥 CRITICAL - Response Time:\n"
            recommendations += "• Optimize database queries\n"
            recommendations += "• Implement caching strategies\n"
            recommendations += "• Review network latency\n\n"
        elif avg_response > 100:
            recommendations += "⚠️ WARNING - Response Time:\n"
            recommendations += "• Consider performance optimizations\n"
            recommendations += "• Profile slow operations\n\n"
        else:
            recommendations += "✅ Response Time: Within optimal range\n\n"
        
        # General Recommendations
        recommendations += "🎯 General Optimization Tips:\n"
        recommendations += "• Enable performance monitoring alerts\n"
        recommendations += "• Schedule regular performance reviews\n"
        recommendations += "• Implement automated performance testing\n"
        recommendations += "• Consider load balancing for high traffic\n"
        recommendations += "• Update system drivers and software\n"
        
        return recommendations
    
    def save_profile(self):
        """Save performance profile to file"""
        
        try:
            profile_data = {
                "generated_at": datetime.now().isoformat(),
                "data_points": len(self.performance_data),
                "analysis": {
                    "cpu_analysis": self.cpu_analysis.toPlainText(),
                    "memory_analysis": self.memory_analysis.toPlainText(),
                    "response_analysis": self.response_analysis.toPlainText(),
                    "recommendations": self.recommendations.toPlainText()
                }
            }
            
            # Save to reports directory
            reports_dir = Path("reports/profiles")
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            profile_file = reports_dir / f"performance_profile_{timestamp}.json"
            
            with open(profile_file, 'w') as f:
                json.dump(profile_data, f, indent=2)
            
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Profile Saved", f"Performance profile saved to:\n{profile_file}")
            
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Save Failed", f"Error saving performance profile: {str(e)}")


class SecurityScannerDialog(QDialog):
    """Security scanner dialog with real scanning capabilities"""
    
    def __init__(self, security_scanner, parent=None):
        super().__init__(parent)
        
        self.security_scanner = security_scanner
        self.setWindowTitle("🛡️ Security Scanner")
        self.setMinimumSize(900, 700)
        self.init_ui()
    
    def init_ui(self):
        """Initialize security scanner UI"""
        
        layout = QVBoxLayout(self)
        
        # Scan Configuration
        config_group = QGroupBox("🎯 Scan Configuration")
        config_layout = QFormLayout(config_group)
        
        self.target_url = QLineEdit("https://play.ezygamers.com/")
        config_layout.addRow("🌐 Target URL:", self.target_url)
        
        self.scan_depth = QComboBox()
        self.scan_depth.addItems(["Quick Scan", "Standard Scan", "Deep Scan"])
        self.scan_depth.setCurrentText("Standard Scan")
        config_layout.addRow("🔍 Scan Depth:", self.scan_depth)
        
        layout.addWidget(config_group)
        
        # Scan Controls
        controls_layout = QHBoxLayout()
        
        self.start_scan_btn = QPushButton("🚀 Start Security Scan")
        self.start_scan_btn.clicked.connect(self.start_security_scan)
        controls_layout.addWidget(self.start_scan_btn)
        
        self.stop_scan_btn = QPushButton("⏹️ Stop Scan")
        self.stop_scan_btn.clicked.connect(self.stop_security_scan)
        self.stop_scan_btn.setEnabled(False)
        controls_layout.addWidget(self.stop_scan_btn)
        
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Scan Progress
        self.scan_progress = QProgressBar()
        self.scan_progress.setVisible(False)
        layout.addWidget(self.scan_progress)
        
        # Results Tabs
        self.results_tabs = QTabWidget()
        
        # Scan Results Tab
        results_tab = self.create_results_tab()
        self.results_tabs.addTab(results_tab, "📊 Scan Results")
        
        # Vulnerabilities Tab
        vulns_tab = self.create_vulnerabilities_tab()
        self.results_tabs.addTab(vulns_tab, "⚠️ Vulnerabilities")
        
        # Recommendations Tab
        recommendations_tab = self.create_security_recommendations_tab()
        self.results_tabs.addTab(recommendations_tab, "💡 Recommendations")
        
        layout.addWidget(self.results_tabs)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close |
            QDialogButtonBox.StandardButton.Save
        )
        button_box.accepted.connect(self.save_scan_results)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: white;
            }
            QTabWidget::pane {
                border: 2px solid #404040;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background: #404040;
                padding: 8px 16px;
                margin-right: 2px;
                color: white;
            }
            QTabBar::tab:selected {
                background: #0078d4;
            }
            QTextEdit, QTableWidget {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                color: white;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 16px;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                color: #0078d4;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #404040, stop:1 #2d2d2d);
                border: 2px solid #555555;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #005a9e);
                border-color: #40e0d0;
            }
            QPushButton:disabled {
                background: #555555;
                color: #888888;
                border-color: #666666;
            }
        """)
    
    def create_results_tab(self):
        """Create scan results tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Scan Status
        self.scan_status = QLabel("🔄 Ready to scan")
        self.scan_status.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        layout.addWidget(self.scan_status)
        
        # Results Display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setFont(QFont('Consolas', 10))
        layout.addWidget(self.results_display)
        
        return widget
    
    def create_vulnerabilities_tab(self):
        """Create vulnerabilities tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Vulnerabilities Table
        self.vulnerabilities_table = QTableWidget()
        self.vulnerabilities_table.setColumnCount(4)
        self.vulnerabilities_table.setHorizontalHeaderLabels([
            "Severity", "Type", "Description", "Recommendation"
        ])
        self.vulnerabilities_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.vulnerabilities_table)
        
        return widget
    
    def create_security_recommendations_tab(self):
        """Create security recommendations tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.security_recommendations = QTextEdit()
        self.security_recommendations.setReadOnly(True)
        layout.addWidget(self.security_recommendations)
        
        return widget
    
    @pyqtSlot()
    def start_security_scan(self):
        """Start security scan"""
        
        target_url = self.target_url.text().strip()
        
        if not target_url:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Invalid Input", "Please enter a target URL.")
            return
        
        # Update UI for scanning state
        self.start_scan_btn.setEnabled(False)
        self.stop_scan_btn.setEnabled(True)
        self.scan_progress.setVisible(True)
        self.scan_progress.setValue(0)
        
        self.scan_status.setText("🔍 Scanning in progress...")
        self.scan_status.setStyleSheet("color: #ff9800; font-size: 14px; font-weight: bold; padding: 10px;")
        
        # Clear previous results
        self.results_display.clear()
        self.vulnerabilities_table.setRowCount(0)
        
        # Start scan in thread
        self.scan_worker = SecurityScanWorker(self.security_scanner, target_url)
        self.scan_worker.progress.connect(self.update_scan_progress)
        self.scan_worker.result.connect(self.on_scan_completed)
        self.scan_worker.error.connect(self.on_scan_error)
        
        QThreadPool.globalInstance().start(self.scan_worker)
    
    @pyqtSlot()
    def stop_security_scan(self):
        """Stop security scan"""
        
        self.start_scan_btn.setEnabled(True)
        self.stop_scan_btn.setEnabled(False)
        self.scan_progress.setVisible(False)
        
        self.scan_status.setText("⏹️ Scan stopped by user")
        self.scan_status.setStyleSheet("color: #ff6b6b; font-size: 14px; font-weight: bold; padding: 10px;")
    
    @pyqtSlot(int)
    def update_scan_progress(self, progress):
        """Update scan progress"""
        self.scan_progress.setValue(progress)
    
    @pyqtSlot(object)
    def on_scan_completed(self, scan_result):
        """Handle scan completion"""
        
        # Update UI
        self.start_scan_btn.setEnabled(True)
        self.stop_scan_btn.setEnabled(False)
        self.scan_progress.setVisible(False)
        
        self.scan_status.setText("✅ Scan completed successfully")
        self.scan_status.setStyleSheet("color: #4CAF50; font-size: 14px; font-weight: bold; padding: 10px;")
        
        # Display results
        self.display_scan_results(scan_result)
        
        # Populate vulnerabilities table
        self.populate_vulnerabilities_table(scan_result.details)
        
        # Generate recommendations
        self.generate_security_recommendations(scan_result)
    
    @pyqtSlot(str)
    def on_scan_error(self, error_message):
        """Handle scan error"""
        
        self.start_scan_btn.setEnabled(True)
        self.stop_scan_btn.setEnabled(False)
        self.scan_progress.setVisible(False)
        
        self.scan_status.setText(f"❌ Scan failed: {error_message}")
        self.scan_status.setStyleSheet("color: #ff0000; font-size: 14px; font-weight: bold; padding: 10px;")
        
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Scan Failed", f"Security scan failed:\n{error_message}")
    
    def display_scan_results(self, scan_result):
        """Display scan results"""
        
        results_text = f"""
🛡️ Security Scan Results
{'='*50}

🎯 Target: {self.target_url.text()}
📅 Scan Date: {scan_result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
🆔 Scan ID: {scan_result.scan_id}

📊 Summary:
• Security Score: {scan_result.security_score:.1f}/100
• Threat Level: {scan_result.threat_level}
• Vulnerabilities Found: {scan_result.vulnerabilities_found}

🔍 Detailed Analysis:
        """.strip()
        
        for detail in scan_result.details:
            results_text += f"""
• {detail['type']} ({detail['severity']})
  Description: {detail['description']}
  Recommendation: {detail['recommendation']}
"""
        
        self.results_display.setText(results_text)
    
    def populate_vulnerabilities_table(self, vulnerabilities):
        """Populate vulnerabilities table"""
        
        self.vulnerabilities_table.setRowCount(len(vulnerabilities))
        
        for row, vuln in enumerate(vulnerabilities):
            # Severity
            severity_item = QTableWidgetItem(vuln['severity'])
            if vuln['severity'] == 'HIGH':
                severity_item.setBackground(QColor(244, 67, 54, 100))  # Red
            elif vuln['severity'] == 'MEDIUM':
                severity_item.setBackground(QColor(255, 193, 7, 100))  # Orange
            else:
                severity_item.setBackground(QColor(76, 175, 80, 100))  # Green
            
            self.vulnerabilities_table.setItem(row, 0, severity_item)
            self.vulnerabilities_table.setItem(row, 1, QTableWidgetItem(vuln['type']))
            self.vulnerabilities_table.setItem(row, 2, QTableWidgetItem(vuln['description']))
            self.vulnerabilities_table.setItem(row, 3, QTableWidgetItem(vuln['recommendation']))
        
        self.vulnerabilities_table.resizeColumnsToContents()
    
    def generate_security_recommendations(self, scan_result):
        """Generate security recommendations"""
        
        recommendations = f"""
💡 Security Recommendations
{'='*40}

🎯 Overall Security Score: {scan_result.security_score:.1f}/100
🚨 Threat Level: {scan_result.threat_level}

📋 Immediate Actions Required:
"""
        
        if scan_result.threat_level == "HIGH":
            recommendations += """
🔥 CRITICAL SECURITY ISSUES DETECTED:
• Address all HIGH severity vulnerabilities immediately
• Implement emergency security measures
• Consider taking system offline until issues are resolved
• Conduct thorough security audit
"""
        elif scan_result.threat_level == "MEDIUM":
            recommendations += """
⚠️ MODERATE SECURITY CONCERNS:
• Address medium severity vulnerabilities within 7 days
• Implement additional security monitoring
• Update security policies and procedures
• Schedule regular security scans
"""
        else:
            recommendations += """
✅ GOOD SECURITY POSTURE:
• Maintain current security practices
• Continue regular security monitoring
• Keep systems and software updated
• Schedule quarterly security reviews
"""
        
        recommendations += """

🛡️ General Security Best Practices:
• Implement multi-factor authentication
• Use HTTPS for all communications
• Regular security patches and updates
• Employee security awareness training
• Implement intrusion detection systems
• Regular backup and disaster recovery testing
• Network segmentation and access controls
• Regular security audits and penetration testing

🔍 Monitoring Recommendations:
• Set up real-time security monitoring
• Configure security alert notifications
• Implement log analysis and SIEM solutions
• Regular vulnerability assessments
• Automated security scanning schedules
"""
        
        self.security_recommendations.setText(recommendations.strip())
    
    def save_scan_results(self):
        """Save scan results to file"""
        
        try:
            # Create results data
            results_data = {
                "scan_id": getattr(self, 'current_scan_id', 'unknown'),
                "target_url": self.target_url.text(),
                "scan_date": datetime.now().isoformat(),
                "results": self.results_display.toPlainText(),
                "recommendations": self.security_recommendations.toPlainText()
            }
            
            # Save to file
            reports_dir = Path("reports/security")
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            results_file = reports_dir / f"security_scan_{timestamp}.json"
            
            with open(results_file, 'w') as f:
                json.dump(results_data, f, indent=2)
            
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Results Saved", f"Security scan results saved to:\n{results_file}")
            
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Save Failed", f"Error saving scan results: {str(e)}")


class SecurityScanWorker(QRunnable):
    """Worker for security scanning"""
    
    def __init__(self, security_scanner, target_url):
        super().__init__()
        self.security_scanner = security_scanner
        self.target_url = target_url
        self.signals = SecurityScanSignals()
    
    @property
    def progress(self):
        return self.signals.progress
    
    @property
    def result(self):
        return self.signals.result
    
    @property
    def error(self):
        return self.signals.error
    
    def run(self):
        """Run security scan"""
        
        try:
            # Create event loop for async scanner
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Simulate progress updates
            for i in range(0, 101, 10):
                self.signals.progress.emit(i)
                if i < 100:
                    import time
                    time.sleep(0.2)
            
            # Run actual scan
            result = loop.run_until_complete(
                self.security_scanner.run_security_scan(self.target_url)
            )
            
            self.signals.result.emit(result)
            loop.close()
            
        except Exception as e:
            self.signals.error.emit(str(e))


class SecurityScanSignals(QObject):
    """Signals for security scan worker"""
    progress = pyqtSignal(int)
    result = pyqtSignal(object)
    error = pyqtSignal(str)


# Continue with more dialog classes...
# [Should I continue with SystemInfoDialog, AboutDialog, TestResultDetailsDialog, etc.?]
# Continue from previous advanced_dialogs.py

class SystemInfoDialog(QDialog):
    """System information dialog with comprehensive details"""
    
    def __init__(self, system_info, parent=None):
        super().__init__(parent)
        
        self.system_info = system_info
        self.setWindowTitle("💻 System Information")
        self.setMinimumSize(800, 600)
        self.init_ui()
        self.populate_system_info()
    
    def init_ui(self):
        """Initialize system info UI"""
        
        layout = QVBoxLayout(self)
        
        # System Info Tabs
        self.info_tabs = QTabWidget()
        
        # System Overview Tab
        overview_tab = self.create_overview_tab()
        self.info_tabs.addTab(overview_tab, "🖥️ Overview")
        
        # Hardware Tab
        hardware_tab = self.create_hardware_tab()
        self.info_tabs.addTab(hardware_tab, "⚙️ Hardware")
        
        # Network Tab
        network_tab = self.create_network_tab()
        self.info_tabs.addTab(network_tab, "🌐 Network")
        
        # Processes Tab
        processes_tab = self.create_processes_tab()
        self.info_tabs.addTab(processes_tab, "🔄 Processes")
        
        layout.addWidget(self.info_tabs)
        
        # Export and Close buttons
        button_layout = QHBoxLayout()
        
        export_btn = QPushButton("📤 Export System Info")
        export_btn.clicked.connect(self.export_system_info)
        button_layout.addWidget(export_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_system_info)
        button_layout.addWidget(refresh_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("❌ Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: white;
            }
            QTabWidget::pane {
                border: 2px solid #404040;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background: #404040;
                padding: 8px 16px;
                margin-right: 2px;
                color: white;
            }
            QTabBar::tab:selected {
                background: #0078d4;
            }
            QTextEdit, QTreeWidget, QTableWidget {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                color: white;
                font-family: 'Consolas', monospace;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #404040, stop:1 #2d2d2d);
                border: 2px solid #555555;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #005a9e);
                border-color: #40e0d0;
            }
        """)
    
    def create_overview_tab(self):
        """Create system overview tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.overview_display = QTextEdit()
        self.overview_display.setReadOnly(True)
        layout.addWidget(self.overview_display)
        
        return widget
    
    def create_hardware_tab(self):
        """Create hardware information tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.hardware_display = QTextEdit()
        self.hardware_display.setReadOnly(True)
        layout.addWidget(self.hardware_display)
        
        return widget
    
    def create_network_tab(self):
        """Create network information tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.network_display = QTextEdit()
        self.network_display.setReadOnly(True)
        layout.addWidget(self.network_display)
        
        return widget
    
    def create_processes_tab(self):
        """Create processes information tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Process table
        self.processes_table = QTableWidget()
        self.processes_table.setColumnCount(5)
        self.processes_table.setHorizontalHeaderLabels([
            "PID", "Name", "CPU %", "Memory %", "Status"
        ])
        self.processes_table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.processes_table)
        
        return widget
    
    def populate_system_info(self):
        """Populate system information"""
        
        # System Overview
        overview_text = f"""
💻 System Information Overview
{'='*50}

🖥️ Platform: {self.system_info.get('platform', 'Unknown')}
🐍 Python Version: {self.system_info.get('python_version', 'Unknown')}
🏗️ Architecture: {self.system_info.get('architecture', 'Unknown')}
🖨️ Processor: {self.system_info.get('processor', 'Unknown')}
🏠 Hostname: {self.system_info.get('hostname', 'Unknown')}
🔄 Running Processes: {self.system_info.get('running_processes', 0)}

⏰ Boot Time: {self.system_info.get('boot_time', 'Unknown')}
📅 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        self.overview_display.setText(overview_text)
        
        # Hardware Information
        memory_info = self.system_info.get('memory', {})
        hardware_text = f"""
⚙️ Hardware Information
{'='*40}

🖥️ CPU Information:
• CPU Cores: {self.system_info.get('cpu_count', 'Unknown')}
• CPU Frequency: {self.format_cpu_freq()}

💾 Memory Information:
• Total Memory: {self.format_bytes(memory_info.get('total', 0))}
• Available Memory: {self.format_bytes(memory_info.get('available', 0))}
• Used Memory: {self.format_bytes(memory_info.get('used', 0))}
• Memory Usage: {memory_info.get('percent', 0):.1f}%

💿 Disk Information:
{self.format_disk_info()}
        """.strip()
        
        self.hardware_display.setText(hardware_text)
        
        # Network Information
        network_text = "🌐 Network Information\n" + "="*40 + "\n\n"
        
        network_interfaces = self.system_info.get('network_interfaces', [])
        for interface in network_interfaces:
            network_text += f"🔗 Interface: {interface['name']}\n"
            for addr in interface['addresses']:
                network_text += f"  • {addr['family']}: {addr['address']}\n"
                if addr.get('netmask'):
                    network_text += f"    Netmask: {addr['netmask']}\n"
            network_text += "\n"
        
        self.network_display.setText(network_text)
        
        # Populate processes
        self.populate_processes()
    
    def format_cpu_freq(self):
        """Format CPU frequency information"""
        
        cpu_freq = self.system_info.get('cpu_freq')
        if cpu_freq:
            return f"{cpu_freq.get('current', 0):.1f} MHz (Max: {cpu_freq.get('max', 0):.1f} MHz)"
        return "Unknown"
    
    def format_bytes(self, bytes_value):
        """Format bytes to human readable format"""
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
    
    def format_disk_info(self):
        """Format disk usage information"""
        
        disk_info = self.system_info.get('disk_usage', {})
        if disk_info:
            return f"""• Total Disk Space: {self.format_bytes(disk_info.get('total', 0))}
• Used Disk Space: {self.format_bytes(disk_info.get('used', 0))}
• Free Disk Space: {self.format_bytes(disk_info.get('free', 0))}
• Disk Usage: {(disk_info.get('used', 0) / disk_info.get('total', 1)) * 100:.1f}%"""
        return "Disk information not available"
    
    def populate_processes(self):
        """Populate running processes"""
        
        try:
            import psutil
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            
            # Show top 50 processes
            self.processes_table.setRowCount(min(50, len(processes)))
            
            for row, proc in enumerate(processes[:50]):
                self.processes_table.setItem(row, 0, QTableWidgetItem(str(proc.get('pid', ''))))
                self.processes_table.setItem(row, 1, QTableWidgetItem(proc.get('name', '')))
                self.processes_table.setItem(row, 2, QTableWidgetItem(f"{proc.get('cpu_percent', 0):.1f}"))
                self.processes_table.setItem(row, 3, QTableWidgetItem(f"{proc.get('memory_percent', 0):.1f}"))
                self.processes_table.setItem(row, 4, QTableWidgetItem(proc.get('status', '')))
            
            self.processes_table.resizeColumnsToContents()
            
        except ImportError:
            # Fallback if psutil not available
            self.processes_table.setRowCount(1)
            self.processes_table.setItem(0, 0, QTableWidgetItem("N/A"))
            self.processes_table.setItem(0, 1, QTableWidgetItem("Process information not available"))
            self.processes_table.setItem(0, 2, QTableWidgetItem("N/A"))
            self.processes_table.setItem(0, 3, QTableWidgetItem("N/A"))
            self.processes_table.setItem(0, 4, QTableWidgetItem("N/A"))
    
    def refresh_system_info(self):
        """Refresh system information"""
        
        # Re-gather system info
        if hasattr(self.parent(), 'gather_system_info'):
            self.system_info = self.parent().gather_system_info()
            self.populate_system_info()
        
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Refreshed", "System information has been refreshed.")
    
    def export_system_info(self):
        """Export system information to file"""
        
        try:
            # Create export data
            export_data = {
                "exported_at": datetime.now().isoformat(),
                "system_info": self.system_info,
                "overview": self.overview_display.toPlainText(),
                "hardware": self.hardware_display.toPlainText(),
                "network": self.network_display.toPlainText()
            }
            
            # Save to file
            reports_dir = Path("reports/system")
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            export_file = reports_dir / f"system_info_{timestamp}.json"
            
            with open(export_file, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Export Complete", f"System information exported to:\n{export_file}")
            
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Export Failed", f"Error exporting system information: {str(e)}")


class AboutDialog(QDialog):
    """Enhanced about dialog with system and license information"""
    
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        
        self.settings = settings
        self.setWindowTitle("ℹ️ About MAGE Enterprise")
        self.setFixedSize(600, 500)
        self.init_ui()
    
    def init_ui(self):
        """Initialize about dialog UI"""
        
        layout = QVBoxLayout(self)
        
        # Header with logo placeholder
        header_layout = QVBoxLayout()
        
        # Application title
        title_label = QLabel("🎮 MAGE Enterprise")
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #0078d4;
            text-align: center;
            padding: 20px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Multi-Agent Game Tester Enterprise Edition")
        subtitle_label.setStyleSheet("""
            font-size: 16px;
            color: #666;
            text-align: center;
            padding-bottom: 10px;
        """)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        layout.addLayout(header_layout)
        
        # About content tabs
        self.about_tabs = QTabWidget()
        
        # Application Info Tab
        app_tab = self.create_app_info_tab()
        self.about_tabs.addTab(app_tab, "📱 Application")
        
        # System Info Tab
        system_tab = self.create_system_info_tab()
        self.about_tabs.addTab(system_tab, "💻 System")
        
        # License Tab
        license_tab = self.create_license_tab()
        self.about_tabs.addTab(license_tab, "📄 License")
        
        # Credits Tab
        credits_tab = self.create_credits_tab()
        self.about_tabs.addTab(credits_tab, "👨‍💻 Credits")
        
        layout.addWidget(self.about_tabs)
        
        # Close button
        close_btn = QPushButton("❌ Close")
        close_btn.clicked.connect(self.accept)
        close_btn.setDefault(True)
        layout.addWidget(close_btn)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                color: #333;
            }
            QTabWidget::pane {
                border: 2px solid #ccc;
                background-color: white;
            }
            QTabBar::tab {
                background: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #0078d4;
                color: white;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                color: #333;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #005a9e);
                border: none;
                color: white;
                font-weight: bold;
                padding: 10px 30px;
                border-radius: 6px;
                margin: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #106ebe, stop:1 #004578);
            }
        """)
    
    def create_app_info_tab(self):
        """Create application info tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        app_info = QTextEdit()
        app_info.setReadOnly(True)
        
        version = getattr(self.settings, 'version', '2.0.0')
        
        app_info_text = f"""
🚀 MAGE - Multi-Agent Game Tester Enterprise

📊 Version Information:
• Version: {version}
• Build: Enterprise Edition
• Release Date: January 2025
• Architecture: 64-bit

🎯 Key Features:
• Advanced Multi-Agent AI Testing System
• Real-time Performance Monitoring  
• Enterprise Security Scanning
• Comprehensive Analytics & Reporting
• Graphics & Visual Testing
• AI Behavior Analysis
• Advanced Dashboard & Visualization
• Complete Testing Automation

🏢 Product Information:
• Product Name: MAGE Enterprise
• Product Type: Gaming Industry Testing Solution
• Target Audience: Game Developers, QA Teams, Gaming Companies
• License Type: Enterprise Commercial License

🌟 What's New in v{version}:
• Enhanced multi-agent coordination
• Improved security scanning algorithms
• Advanced reporting capabilities
• Real-time performance profiling
• Enhanced UI/UX experience
• Better integration capabilities
        """.strip()
        
        app_info.setText(app_info_text)
        layout.addWidget(app_info)
        
        return widget
    
    def create_system_info_tab(self):
        """Create system info tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        system_info = QTextEdit()
        system_info.setReadOnly(True)
        
        import platform
        import sys
        
        system_info_text = f"""
💻 System Environment Information

🖥️ Operating System:
• Platform: {platform.platform()}
• System: {platform.system()}
• Release: {platform.release()}
• Version: {platform.version()}
• Machine: {platform.machine()}
• Processor: {platform.processor()}

🐍 Python Environment:
• Python Version: {sys.version}
• Python Executable: {sys.executable}
• Python Path: {sys.path[0]}

📦 Dependencies:
• PyQt6: Available
• Pydantic: Available
• AsyncIO: Available
• JSON: Available
• SQLite3: Available

🔧 Application Environment:
• Working Directory: {os.getcwd()}
• Configuration: Loaded Successfully
• Database: Initialized
• Logging: Active
• Security: Enabled

📁 Directory Structure:
• Reports: Available
• Logs: Available  
• Data: Available
• Configuration: Available
        """.strip()
        
        system_info.setText(system_info_text)
        layout.addWidget(system_info)
        
        return widget
    
    def create_license_tab(self):
        """Create license information tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        license_info = QTextEdit()
        license_info.setReadOnly(True)
        
        license_text = """
📄 MAGE Enterprise License Agreement

© 2025 MAGE Corporation. All Rights Reserved.

🏢 ENTERPRISE COMMERCIAL LICENSE

This software is licensed under the MAGE Enterprise Commercial License.

📋 License Terms:
• This software is provided under a commercial license
• Usage is restricted to licensed organizations
• Redistribution requires written permission
• Modification allowed for internal use only
• Reverse engineering is prohibited

🎯 Permitted Uses:
• Internal game testing and quality assurance
• Performance monitoring and optimization
• Security vulnerability assessment
• Automated testing integration
• Report generation and analysis

🚫 Restrictions:
• No redistribution without permission
• No commercial resale or sublicensing
• No removal of copyright notices
• No use in competing products

📞 Support & Contact:
• Technical Support: support@mage-corp.com
• Sales Inquiries: sales@mage-corp.com
• General Information: info@mage-corp.com
• Website: https://www.mage-corp.com

⚖️ Legal Notice:
This software is provided "as is" without warranty of any kind, either 
express or implied, including but not limited to the implied warranties 
of merchantability and fitness for a particular purpose.

For complete license terms and conditions, please refer to the full 
license agreement included with your purchase.
        """.strip()
        
        license_info.setText(license_text)
        layout.addWidget(license_info)
        
        return widget
    
    def create_credits_tab(self):
        """Create credits and acknowledgments tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        credits_info = QTextEdit()
        credits_info.setReadOnly(True)
        
        credits_text = """
👨‍💻 MAGE Enterprise Development Team

🏢 MAGE Corporation Development Team:
• Lead Architect & Developer
• Senior AI/ML Engineers
• Full-Stack Developers  
• Security Specialists
• QA & Testing Engineers
• UI/UX Designers
• DevOps Engineers

🛠️ Technologies & Frameworks:
• PyQt6 - Modern GUI Framework
• Python 3.12+ - Core Programming Language
• Pydantic - Data Validation & Settings
• SQLite - Embedded Database
• AsyncIO - Asynchronous Programming
• ReportLab - PDF Report Generation
• PSUtil - System Monitoring
• OpenAI API - AI Integration

🌟 Special Recognition:
• Gaming Industry Beta Testers
• Early Adopters & Feedback Providers
• Open Source Community Contributors
• Security Research Community
• Performance Testing Experts

📚 Third-Party Libraries:
• PyQt6 - GUI Framework (Riverbank Computing)
• Pydantic - Data Validation (Samuel Colvin)
• ReportLab - PDF Generation (ReportLab Ltd)
• PSUtil - System Monitoring (Giampaolo Rodola)
• Various other open source libraries

💝 Acknowledgments:
Thank you to all the developers, testers, and users who have contributed 
to making MAGE Enterprise the leading solution for game testing automation.

🌍 Community:
Join our community of game testing professionals:
• Discord: MAGE Enterprise Community
• GitHub: Enterprise Feature Requests
• Forums: Technical Discussions
• Newsletter: Product Updates

🚀 Future Development:
MAGE Enterprise continues to evolve with cutting-edge features and 
improvements based on user feedback and industry requirements.
        """.strip()
        
        credits_info.setText(credits_text)
        layout.addWidget(credits_info)
        
        return widget


class TestResultDetailsDialog(QDialog):
    """Detailed test result viewer dialog"""
    
    def __init__(self, test_result, parent=None):
        super().__init__(parent)
        
        self.test_result = test_result
        self.setWindowTitle(f"🔍 Test Details - {test_result.test_id}")
        self.setMinimumSize(700, 500)
        self.init_ui()
        self.populate_test_details()
    
    def init_ui(self):
        """Initialize test details UI"""
        
        layout = QVBoxLayout(self)
        
        # Test header info
        header_group = QGroupBox("📋 Test Information")
        header_layout = QGridLayout(header_group)
        
        header_layout.addWidget(QLabel("Test ID:"), 0, 0)
        header_layout.addWidget(QLabel(self.test_result.test_id), 0, 1)
        
        header_layout.addWidget(QLabel("Test Type:"), 0, 2)
        header_layout.addWidget(QLabel(self.test_result.test_type), 0, 3)
        
        header_layout.addWidget(QLabel("Status:"), 1, 0)
        status_label = QLabel(self.test_result.status)
        if self.test_result.success:
            status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        else:
            status_label.setStyleSheet("color: #f44336; font-weight: bold;")
        header_layout.addWidget(status_label, 1, 1)
        
        header_layout.addWidget(QLabel("Score:"), 1, 2)
        score_label = QLabel(f"{self.test_result.score:.1f}")
        if self.test_result.score >= 80:
            score_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        elif self.test_result.score >= 60:
            score_label.setStyleSheet("color: #FF9800; font-weight: bold;")
        else:
            score_label.setStyleSheet("color: #f44336; font-weight: bold;")
        header_layout.addWidget(score_label, 1, 3)
        
        header_layout.addWidget(QLabel("Duration:"), 2, 0)
        header_layout.addWidget(QLabel(f"{self.test_result.duration_ms} ms"), 2, 1)
        
        header_layout.addWidget(QLabel("Started:"), 2, 2)
        header_layout.addWidget(QLabel(self.test_result.start_time.strftime('%H:%M:%S')), 2, 3)
        
        layout.addWidget(header_group)
        
        # Details tabs
        self.details_tabs = QTabWidget()
        
        # Test Details Tab
        details_tab = self.create_test_details_tab()
        self.details_tabs.addTab(details_tab, "📊 Details")
        
        # Performance Metrics Tab
        metrics_tab = self.create_metrics_tab()
        self.details_tabs.addTab(metrics_tab, "⚡ Performance")
        
        # Errors Tab
        errors_tab = self.create_errors_tab()
        self.details_tabs.addTab(errors_tab, "❌ Errors")
        
        layout.addWidget(self.details_tabs)
        
        # Close button
        close_btn = QPushButton("❌ Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: white;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #404040;
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 16px;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                color: #0078d4;
            }
            QTabWidget::pane {
                border: 2px solid #404040;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background: #404040;
                padding: 8px 16px;
                margin-right: 2px;
                color: white;
            }
            QTabBar::tab:selected {
                background: #0078d4;
            }
            QTextEdit {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                color: white;
                font-family: 'Consolas', monospace;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #404040, stop:1 #2d2d2d);
                border: 2px solid #555555;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #005a9e);
                border-color: #40e0d0;
            }
        """)
    
    def create_test_details_tab(self):
        """Create test details tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.details_display = QTextEdit()
        self.details_display.setReadOnly(True)
        layout.addWidget(self.details_display)
        
        return widget
    
    def create_metrics_tab(self):
        """Create performance metrics tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.metrics_display = QTextEdit()
        self.metrics_display.setReadOnly(True)
        layout.addWidget(self.metrics_display)
        
        return widget
    
    def create_errors_tab(self):
        """Create errors tab"""
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.errors_display = QTextEdit()
        self.errors_display.setReadOnly(True)
        layout.addWidget(self.errors_display)
        
        return widget
    
    def populate_test_details(self):
        """Populate test result details"""
        
        # Test Details
        details_text = f"""
📊 Test Execution Details
{'='*40}

🆔 Test Identification:
• Test ID: {self.test_result.test_id}
• Test Type: {self.test_result.test_type}
• Status: {self.test_result.status}
• Success: {'✅ Yes' if self.test_result.success else '❌ No'}

⏱️ Timing Information:
• Start Time: {self.test_result.start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
• End Time: {self.test_result.end_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
• Duration: {self.test_result.duration_ms} milliseconds
• Execution Speed: {'Fast' if self.test_result.duration_ms < 1000 else 'Moderate' if self.test_result.duration_ms < 5000 else 'Slow'}

📈 Performance Score:
• Overall Score: {self.test_result.score:.2f}/100
• Grade: {self.calculate_grade(self.test_result.score)}

🔍 Test Configuration:
        """.strip()
        
        # Add details from test result
        if self.test_result.details:
            for key, value in self.test_result.details.items():
                details_text += f"• {key.replace('_', ' ').title()}: {value}\n"
        
        self.details_display.setText(details_text)
        
        # Performance Metrics
        metrics_text = "⚡ Performance Metrics\n" + "="*30 + "\n\n"
        
        if self.test_result.performance_metrics:
            for metric, value in self.test_result.performance_metrics.items():
                if isinstance(value, (int, float)):
                    metrics_text += f"• {metric.replace('_', ' ').title()}: {value:.2f}\n"
                else:
                    metrics_text += f"• {metric.replace('_', ' ').title()}: {value}\n"
        else:
            metrics_text += "No performance metrics collected for this test."
        
        self.metrics_display.setText(metrics_text)
        
        # Errors
        errors_text = "❌ Error Information\n" + "="*25 + "\n\n"
        
        if self.test_result.errors:
            for i, error in enumerate(self.test_result.errors, 1):
                errors_text += f"Error #{i}: {error}\n\n"
        else:
            errors_text += "✅ No errors occurred during test execution."
        
        self.errors_display.setText(errors_text)
    
    def calculate_grade(self, score):
        """Calculate letter grade from score"""
        
        if score >= 90:
            return "A+ (Excellent)"
        elif score >= 80:
            return "A (Very Good)"
        elif score >= 70:
            return "B (Good)"
        elif score >= 60:
            return "C (Fair)"
        elif score >= 50:
            return "D (Poor)"
        else:
            return "F (Failed)"
