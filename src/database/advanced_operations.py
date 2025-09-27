"""
Advanced Database Operations
Comprehensive SQLite operations with optimization and analytics
"""

import sqlite3
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import logging

from src.core.implementations import TestResult, PerformanceMetrics, SecurityScanResult


class AdvancedDatabaseManager:
    """Advanced database manager with comprehensive operations"""
    
    def __init__(self, db_path: str = "data/mage_enterprise.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        
        # Initialize database with all tables
        self.init_advanced_database()
    
    def init_advanced_database(self):
        """Initialize comprehensive database schema"""
        
        with sqlite3.connect(self.db_path) as conn:
            # Enable foreign keys
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
            
            # Test Sessions Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS test_sessions (
                    session_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    config TEXT,
                    results_summary TEXT,
                    total_tests INTEGER DEFAULT 0,
                    successful_tests INTEGER DEFAULT 0,
                    avg_score REAL DEFAULT 0.0,
                    duration_ms INTEGER DEFAULT 0
                )
            """)
            
            # Test Results Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS test_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_id TEXT UNIQUE NOT NULL,
                    session_id TEXT,
                    test_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    start_time TIMESTAMP NOT NULL,
                    end_time TIMESTAMP NOT NULL,
                    duration_ms INTEGER NOT NULL,
                    success BOOLEAN NOT NULL,
                    score REAL NOT NULL,
                    details TEXT,
                    performance_data TEXT,
                    errors TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES test_sessions (session_id)
                )
            """)
            
            # Performance Metrics Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_id TEXT,
                    test_id TEXT,
                    cpu_usage REAL NOT NULL,
                    memory_usage REAL NOT NULL,
                    disk_io REAL DEFAULT 0,
                    network_io REAL DEFAULT 0,
                    gpu_usage REAL DEFAULT 0,
                    fps INTEGER DEFAULT 0,
                    response_time_ms REAL NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES test_sessions (session_id),
                    FOREIGN KEY (test_id) REFERENCES test_results (test_id)
                )
            """)
            
            # Security Scans Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS security_scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_id TEXT UNIQUE NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    target_url TEXT NOT NULL,
                    threat_level TEXT NOT NULL,
                    vulnerabilities_found INTEGER DEFAULT 0,
                    security_score REAL NOT NULL,
                    details TEXT,
                    scan_duration_ms INTEGER DEFAULT 0,
                    session_id TEXT,
                    FOREIGN KEY (session_id) REFERENCES test_sessions (session_id)
                )
            """)
            
            # System Events Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS system_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    event_type TEXT NOT NULL,
                    severity TEXT DEFAULT 'INFO',
                    message TEXT NOT NULL,
                    details TEXT,
                    session_id TEXT,
                    FOREIGN KEY (session_id) REFERENCES test_sessions (session_id)
                )
            """)
            
            # User Settings Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    setting_key TEXT NOT NULL,
                    setting_value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(category, setting_key)
                )
            """)
            
            # Agent Status Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tasks_completed INTEGER DEFAULT 0,
                    tasks_failed INTEGER DEFAULT 0,
                    cpu_usage REAL DEFAULT 0,
                    memory_usage REAL DEFAULT 0,
                    config TEXT,
                    session_id TEXT,
                    FOREIGN KEY (session_id) REFERENCES test_sessions (session_id)
                )
            """)
            
            # Reports Table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_id TEXT UNIQUE NOT NULL,
                    report_type TEXT NOT NULL,
                    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    file_path TEXT NOT NULL,
                    file_size INTEGER DEFAULT 0,
                    format TEXT NOT NULL,
                    session_id TEXT,
                    parameters TEXT,
                    FOREIGN KEY (session_id) REFERENCES test_sessions (session_id)
                )
            """)
            
            # Create indexes for performance
            self.create_performance_indexes()
            
            self.logger.info("Advanced database schema initialized")
    
    def create_performance_indexes(self):
        """Create database indexes for better performance"""
        
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_test_results_session ON test_results(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_test_results_type ON test_results(test_type)",
            "CREATE INDEX IF NOT EXISTS idx_test_results_timestamp ON test_results(start_time)",
            "CREATE INDEX IF NOT EXISTS idx_performance_timestamp ON performance_metrics(timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_performance_session ON performance_metrics(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_security_timestamp ON security_scans(timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_system_events_timestamp ON system_events(timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_system_events_type ON system_events(event_type)",
            "CREATE INDEX IF NOT EXISTS idx_agent_status_name ON agent_status(agent_name)"
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            for index_sql in indexes:
                try:
                    conn.execute(index_sql)
                except sqlite3.Error as e:
                    self.logger.warning(f"Index creation warning: {e}")
    
    def save_test_session_advanced(self, session_id: str, name: str, config: Dict[str, Any]) -> bool:
        """Save test session with advanced tracking"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO test_sessions 
                    (session_id, name, config, updated_at) 
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """, (session_id, name, json.dumps(config)))
                
                # Log system event
                self.log_system_event("session_created", "INFO", f"Test session created: {name}", {"session_id": session_id})
                
            return True
            
        except sqlite3.Error as e:
            self.logger.error(f"Error saving test session: {e}")
            return False
    
    def save_test_result_advanced(self, result: TestResult, session_id: str) -> bool:
        """Save test result with advanced metrics"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Insert test result
                conn.execute("""
                    INSERT OR REPLACE INTO test_results 
                    (test_id, session_id, test_type, status, start_time, end_time, 
                     duration_ms, success, score, details, performance_data, errors)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    result.test_id, session_id, result.test_type, result.status,
                    result.start_time, result.end_time, result.duration_ms,
                    result.success, result.score, json.dumps(result.details),
                    json.dumps(result.performance_metrics), json.dumps(result.errors)
                ))
                
                # Update session statistics
                self.update_session_statistics(session_id)
                
                # Save performance metrics if available
                if result.performance_metrics:
                    self.save_performance_metrics_for_test(result.test_id, session_id, result.performance_metrics)
                
            return True
            
        except sqlite3.Error as e:
            self.logger.error(f"Error saving test result: {e}")
            return False
    
    def save_performance_metrics_for_test(self, test_id: str, session_id: str, metrics: Dict[str, Any]):
        """Save detailed performance metrics for a test"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO performance_metrics 
                    (session_id, test_id, cpu_usage, memory_usage, disk_io, 
                     network_io, gpu_usage, fps, response_time_ms)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_id, test_id,
                    metrics.get('cpu_usage', 0),
                    metrics.get('memory_usage', 0),
                    metrics.get('disk_io', 0),
                    metrics.get('network_io', 0),
                    metrics.get('gpu_usage', 0),
                    metrics.get('fps', 0),
                    metrics.get('response_time_ms', 0)
                ))
                
        except sqlite3.Error as e:
            self.logger.error(f"Error saving performance metrics: {e}")
    
    def save_security_scan(self, scan_result: SecurityScanResult, session_id: str = None) -> bool:
        """Save security scan results"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO security_scans 
                    (scan_id, target_url, threat_level, vulnerabilities_found, 
                     security_score, details, session_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    scan_result.scan_id, 
                    scan_result.details[0].get('url', 'unknown') if scan_result.details else 'unknown',
                    scan_result.threat_level,
                    scan_result.vulnerabilities_found,
                    scan_result.security_score,
                    json.dumps(scan_result.details),
                    session_id
                ))
                
            return True
            
        except sqlite3.Error as e:
            self.logger.error(f"Error saving security scan: {e}")
            return False
    
    def update_session_statistics(self, session_id: str):
        """Update session statistics after test completion"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Calculate session statistics
                stats = conn.execute("""
                    SELECT 
                        COUNT(*) as total_tests,
                        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_tests,
                        AVG(score) as avg_score,
                        SUM(duration_ms) as total_duration
                    FROM test_results 
                    WHERE session_id = ?
                """, (session_id,)).fetchone()
                
                if stats:
                    conn.execute("""
                        UPDATE test_sessions 
                        SET total_tests = ?, successful_tests = ?, avg_score = ?, 
                            duration_ms = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE session_id = ?
                    """, (stats[0], stats[1], stats[2] or 0, stats[3] or 0, session_id))
                
        except sqlite3.Error as e:
            self.logger.error(f"Error updating session statistics: {e}")
    
    def get_session_analytics(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive session analytics"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Basic session info
                session_info = conn.execute("""
                    SELECT * FROM test_sessions WHERE session_id = ?
                """, (session_id,)).fetchone()
                
                if not session_info:
                    return {}
                
                # Test type breakdown
                test_breakdown = conn.execute("""
                    SELECT test_type, COUNT(*) as count, AVG(score) as avg_score,
                           SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count
                    FROM test_results 
                    WHERE session_id = ? 
                    GROUP BY test_type
                """, (session_id,)).fetchall()
                
                # Performance trends
                perf_trends = conn.execute("""
                    SELECT timestamp, cpu_usage, memory_usage, response_time_ms
                    FROM performance_metrics 
                    WHERE session_id = ? 
                    ORDER BY timestamp
                """, (session_id,)).fetchall()
                
                # Error analysis
                error_analysis = conn.execute("""
                    SELECT test_type, errors
                    FROM test_results 
                    WHERE session_id = ? AND errors != '[]' AND errors IS NOT NULL
                """, (session_id,)).fetchall()
                
                return {
                    "session_info": {
                        "session_id": session_info[0],
                        "name": session_info[1],
                        "created_at": session_info[2],
                        "total_tests": session_info[6],
                        "successful_tests": session_info[7],
                        "avg_score": session_info[8],
                        "duration_ms": session_info[9]
                    },
                    "test_breakdown": [
                        {
                            "test_type": row[0],
                            "count": row[1],
                            "avg_score": row[2],
                            "success_rate": (row[3] / row[1]) * 100 if row[1] > 0 else 0
                        }
                        for row in test_breakdown
                    ],
                    "performance_trends": [
                        {
                            "timestamp": row[0],
                            "cpu_usage": row[1],
                            "memory_usage": row[2],
                            "response_time_ms": row[3]
                        }
                        for row in perf_trends
                    ],
                    "error_analysis": [
                        {
                            "test_type": row[0],
                            "errors": json.loads(row[1]) if row[1] else []
                        }
                        for row in error_analysis
                    ]
                }
                
        except sqlite3.Error as e:
            self.logger.error(f"Error getting session analytics: {e}")
            return {}
    
    def get_performance_trends(self, days: int = 7) -> Dict[str, Any]:
        """Get performance trends over specified days"""
        
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            with sqlite3.connect(self.db_path) as conn:
                # Daily performance averages
                daily_perf = conn.execute("""
                    SELECT DATE(timestamp) as date,
                           AVG(cpu_usage) as avg_cpu,
                           AVG(memory_usage) as avg_memory,
                           AVG(response_time_ms) as avg_response_time,
                           COUNT(*) as measurement_count
                    FROM performance_metrics 
                    WHERE timestamp >= ? 
                    GROUP BY DATE(timestamp)
                    ORDER BY date
                """, (cutoff_date,)).fetchall()
                
                # Test success trends
                daily_tests = conn.execute("""
                    SELECT DATE(start_time) as date,
                           COUNT(*) as total_tests,
                           SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_tests,
                           AVG(score) as avg_score
                    FROM test_results 
                    WHERE start_time >= ? 
                    GROUP BY DATE(start_time)
                    ORDER BY date
                """, (cutoff_date,)).fetchall()
                
                return {
                    "performance_trends": [
                        {
                            "date": row[0],
                            "avg_cpu": row[1],
                            "avg_memory": row[2],
                            "avg_response_time": row[3],
                            "measurements": row[4]
                        }
                        for row in daily_perf
                    ],
                    "test_trends": [
                        {
                            "date": row[0],
                            "total_tests": row[1],
                            "successful_tests": row[2],
                            "success_rate": (row[2] / row[1]) * 100 if row[1] > 0 else 0,
                            "avg_score": row[3]
                        }
                        for row in daily_tests
                    ]
                }
                
        except sqlite3.Error as e:
            self.logger.error(f"Error getting performance trends: {e}")
            return {}
    
    def log_system_event(self, event_type: str, severity: str, message: str, details: Dict[str, Any] = None, session_id: str = None):
        """Log system events for monitoring"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO system_events 
                    (event_type, severity, message, details, session_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (event_type, severity, message, json.dumps(details) if details else None, session_id))
                
        except sqlite3.Error as e:
            self.logger.error(f"Error logging system event: {e}")
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health metrics"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Recent system events
                recent_events = conn.execute("""
                    SELECT event_type, severity, COUNT(*) as count
                    FROM system_events 
                    WHERE timestamp >= datetime('now', '-24 hours')
                    GROUP BY event_type, severity
                    ORDER BY count DESC
                """).fetchall()
                
                # Database statistics
                db_stats = conn.execute("""
                    SELECT 
                        (SELECT COUNT(*) FROM test_sessions) as total_sessions,
                        (SELECT COUNT(*) FROM test_results) as total_tests,
                        (SELECT COUNT(*) FROM performance_metrics) as total_metrics,
                        (SELECT COUNT(*) FROM security_scans) as total_scans
                """).fetchone()
                
                # Recent performance averages
                recent_perf = conn.execute("""
                    SELECT AVG(cpu_usage), AVG(memory_usage), AVG(response_time_ms)
                    FROM performance_metrics 
                    WHERE timestamp >= datetime('now', '-1 hour')
                """).fetchone()
                
                return {
                    "recent_events": [
                        {
                            "event_type": row[0],
                            "severity": row[1],
                            "count": row[2]
                        }
                        for row in recent_events
                    ],
                    "database_stats": {
                        "total_sessions": db_stats[0],
                        "total_tests": db_stats[1],
                        "total_metrics": db_stats[2],
                        "total_scans": db_stats[3]
                    },
                    "recent_performance": {
                        "avg_cpu": recent_perf[0] or 0,
                        "avg_memory": recent_perf[1] or 0,
                        "avg_response_time": recent_perf[2] or 0
                    } if recent_perf else {}
                }
                
        except sqlite3.Error as e:
            self.logger.error(f"Error getting system health: {e}")
            return {}
    
    def cleanup_old_data(self, days_to_keep: int = 30) -> bool:
        """Clean up old data to maintain database performance"""
        
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            with sqlite3.connect(self.db_path) as conn:
                # Clean old performance metrics
                deleted_metrics = conn.execute("""
                    DELETE FROM performance_metrics 
                    WHERE timestamp < ?
                """, (cutoff_date,)).rowcount
                
                # Clean old system events
                deleted_events = conn.execute("""
                    DELETE FROM system_events 
                    WHERE timestamp < ?
                """, (cutoff_date,)).rowcount
                
                # Vacuum database
                conn.execute("VACUUM")
                
                self.logger.info(f"Cleaned up {deleted_metrics} performance metrics and {deleted_events} system events")
                return True
                
        except sqlite3.Error as e:
            self.logger.error(f"Error cleaning up old data: {e}")
            return False
    
    def export_session_data(self, session_id: str) -> Dict[str, Any]:
        """Export complete session data for backup or analysis"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get session info
                session = conn.execute("SELECT * FROM test_sessions WHERE session_id = ?", (session_id,)).fetchone()
                
                # Get all test results
                tests = conn.execute("SELECT * FROM test_results WHERE session_id = ?", (session_id,)).fetchall()
                
                # Get performance metrics
                metrics = conn.execute("SELECT * FROM performance_metrics WHERE session_id = ?", (session_id,)).fetchall()
                
                # Get security scans
                scans = conn.execute("SELECT * FROM security_scans WHERE session_id = ?", (session_id,)).fetchall()
                
                # Get system events
                events = conn.execute("SELECT * FROM system_events WHERE session_id = ?", (session_id,)).fetchall()
                
                return {
                    "session": session,
                    "test_results": tests,
                    "performance_metrics": metrics,
                    "security_scans": scans,
                    "system_events": events,
                    "exported_at": datetime.now().isoformat()
                }
                
        except sqlite3.Error as e:
            self.logger.error(f"Error exporting session data: {e}")
            return {}
