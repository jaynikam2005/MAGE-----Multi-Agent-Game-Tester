"""
Advanced Report Generation System
PDF, HTML, JSON, Excel report generation
"""

import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import uuid

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️  ReportLab not available. Install with: pip install reportlab")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("⚠️  Pandas not available. Install with: pip install pandas")

class ReportGenerator:
    """Advanced report generation system"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.reports_dir / "pdf").mkdir(exist_ok=True)
        (self.reports_dir / "html").mkdir(exist_ok=True)
        (self.reports_dir / "json").mkdir(exist_ok=True)
        (self.reports_dir / "excel").mkdir(exist_ok=True)
        (self.reports_dir / "csv").mkdir(exist_ok=True)
    
    def generate_comprehensive_report(self, test_results: List[Any], 
                                    performance_data: List[Any],
                                    security_data: List[Any],
                                    format: str = "html") -> str:
        """Generate comprehensive test report"""
        
        report_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report_data = {
            "report_id": report_id,
            "generated_at": datetime.now().isoformat(),
            "report_type": "Comprehensive Test Report",
            "summary": self._generate_summary(test_results, performance_data, security_data),
            "test_results": [self._serialize_result(r) for r in test_results],
            "performance_analysis": self._analyze_performance_data(performance_data),
            "security_analysis": self._analyze_security_data(security_data),
            "recommendations": self._generate_recommendations(test_results, performance_data, security_data)
        }
        
        if format.lower() == "pdf":
            return self._generate_pdf_report(report_data, f"comprehensive_report_{timestamp}")
        elif format.lower() == "html":
            return self._generate_html_report(report_data, f"comprehensive_report_{timestamp}")
        elif format.lower() == "json":
            return self._generate_json_report(report_data, f"comprehensive_report_{timestamp}")
        elif format.lower() == "excel":
            return self._generate_excel_report(report_data, f"comprehensive_report_{timestamp}")
        else:
            return self._generate_html_report(report_data, f"comprehensive_report_{timestamp}")
    
    def generate_performance_report(self, performance_data: List[Any], format: str = "html") -> str:
        """Generate performance-specific report"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_data = {
            "report_type": "Performance Analysis Report",
            "generated_at": datetime.now().isoformat(),
            "analysis": self._analyze_performance_data(performance_data),
            "recommendations": self._generate_performance_recommendations(performance_data)
        }
        
        if format.lower() == "pdf":
            return self._generate_pdf_report(report_data, f"performance_report_{timestamp}")
        elif format.lower() == "html":
            return self._generate_html_report(report_data, f"performance_report_{timestamp}")
        else:
            return self._generate_html_report(report_data, f"performance_report_{timestamp}")
    
    def generate_security_report(self, security_data: List[Any], format: str = "html") -> str:
        """Generate security assessment report"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_data = {
            "report_type": "Security Assessment Report",
            "generated_at": datetime.now().isoformat(),
            "analysis": self._analyze_security_data(security_data),
            "recommendations": self._generate_security_recommendations(security_data)
        }
        
        if format.lower() == "pdf":
            return self._generate_pdf_report(report_data, f"security_report_{timestamp}")
        elif format.lower() == "html":
            return self._generate_html_report(report_data, f"security_report_{timestamp}")
        else:
            return self._generate_html_report(report_data, f"security_report_{timestamp}")
    
    def _generate_html_report(self, data: Dict[str, Any], filename: str) -> str:
        """Generate HTML report"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{data.get('report_type', 'Test Report')}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    border-bottom: 3px solid #0078d4;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    color: #0078d4;
                    margin: 0;
                    font-size: 2.5em;
                }}
                .header p {{
                    color: #666;
                    font-size: 1.1em;
                    margin: 10px 0;
                }}
                .summary {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    border-left: 5px solid #28a745;
                }}
                .metric {{
                    display: inline-block;
                    background: #0078d4;
                    color: white;
                    padding: 15px 25px;
                    margin: 10px;
                    border-radius: 8px;
                    text-align: center;
                    min-width: 150px;
                }}
                .metric h3 {{
                    margin: 0 0 10px 0;
                    font-size: 2em;
                }}
                .metric p {{
                    margin: 0;
                    font-size: 0.9em;
                    opacity: 0.9;
                }}
                .section {{
                    margin: 30px 0;
                }}
                .section h2 {{
                    color: #0078d4;
                    border-bottom: 2px solid #e9ecef;
                    padding-bottom: 10px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #e9ecef;
                }}
                th {{
                    background-color: #0078d4;
                    color: white;
                    font-weight: bold;
                }}
                tr:hover {{
                    background-color: #f8f9fa;
                }}
                .success {{ color: #28a745; font-weight: bold; }}
                .warning {{ color: #ffc107; font-weight: bold; }}
                .danger {{ color: #dc3545; font-weight: bold; }}
                .recommendations {{
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .recommendations h3 {{
                    color: #856404;
                    margin-top: 0;
                }}
                .recommendations ul {{
                    margin: 0;
                    padding-left: 20px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #e9ecef;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎮 {data.get('report_type', 'Test Report')}</h1>
                    <p>Generated on {datetime.fromisoformat(data['generated_at']).strftime('%B %d, %Y at %H:%M:%S')}</p>
                    <p>MAGE - Multi-Agent Game Tester Enterprise</p>
                </div>
        """
        
        # Add summary if available
        if 'summary' in data:
            summary = data['summary']
            html_content += f"""
                <div class="summary">
                    <h2>📊 Executive Summary</h2>
                    <div style="text-align: center;">
                        <div class="metric">
                            <h3>{summary.get('total_tests', 0)}</h3>
                            <p>Total Tests</p>
                        </div>
                        <div class="metric">
                            <h3>{summary.get('success_rate', 0):.1f}%</h3>
                            <p>Success Rate</p>
                        </div>
                        <div class="metric">
                            <h3>{summary.get('avg_performance_score', 0):.1f}</h3>
                            <p>Avg Performance</p>
                        </div>
                        <div class="metric">
                            <h3>{summary.get('security_score', 0):.1f}</h3>
                            <p>Security Score</p>
                        </div>
                    </div>
                </div>
            """
        
        # Add test results table
        if 'test_results' in data and data['test_results']:
            html_content += """
                <div class="section">
                    <h2>🧪 Test Results</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Test ID</th>
                                <th>Type</th>
                                <th>Status</th>
                                <th>Score</th>
                                <th>Duration</th>
                                <th>Timestamp</th>
                            </tr>
                        </thead>
                        <tbody>
            """
            
            for result in data['test_results']:
                status_class = 'success' if result['success'] else 'danger'
                html_content += f"""
                    <tr>
                        <td>{result['test_id'][:12]}...</td>
                        <td>{result['test_type']}</td>
                        <td><span class="{status_class}">{result['status']}</span></td>
                        <td>{result['score']:.1f}</td>
                        <td>{result['duration_ms']}ms</td>
                        <td>{datetime.fromisoformat(result['start_time']).strftime('%H:%M:%S')}</td>
                    </tr>
                """
            
            html_content += """
                        </tbody>
                    </table>
                </div>
            """
        
        # Add performance analysis
        if 'performance_analysis' in data:
            perf = data['performance_analysis']
            html_content += f"""
                <div class="section">
                    <h2>⚡ Performance Analysis</h2>
                    <div class="summary">
                        <p><strong>Average CPU Usage:</strong> {perf.get('avg_cpu_usage', 0):.1f}%</p>
                        <p><strong>Average Memory Usage:</strong> {perf.get('avg_memory_usage', 0):.1f}%</p>
                        <p><strong>Average Response Time:</strong> {perf.get('avg_response_time', 0):.1f}ms</p>
                        <p><strong>Performance Grade:</strong> <span class="success">{perf.get('grade', 'N/A')}</span></p>
                    </div>
                </div>
            """
        
        # Add security analysis
        if 'security_analysis' in data:
            sec = data['security_analysis']
            html_content += f"""
                <div class="section">
                    <h2>🛡️ Security Analysis</h2>
                    <div class="summary">
                        <p><strong>Security Score:</strong> {sec.get('security_score', 0):.1f}/100</p>
                        <p><strong>Threat Level:</strong> <span class="warning">{sec.get('threat_level', 'Unknown')}</span></p>
                        <p><strong>Vulnerabilities Found:</strong> {sec.get('vulnerabilities_count', 0)}</p>
                        <p><strong>Last Scan:</strong> {sec.get('last_scan', 'Never')}</p>
                    </div>
                </div>
            """
        
        # Add recommendations
        if 'recommendations' in data and data['recommendations']:
            html_content += """
                <div class="recommendations">
                    <h3>💡 Recommendations</h3>
                    <ul>
            """
            for rec in data['recommendations']:
                html_content += f"<li>{rec}</li>"
            
            html_content += """
                    </ul>
                </div>
            """
        
        html_content += """
                <div class="footer">
                    <p>Generated by MAGE - Multi-Agent Game Tester Enterprise</p>
                    <p>© 2025 MAGE Corporation. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Save HTML report
        report_path = self.reports_dir / "html" / f"{filename}.html"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(report_path)
    
    def _generate_json_report(self, data: Dict[str, Any], filename: str) -> str:
        """Generate JSON report"""
        report_path = self.reports_dir / "json" / f"{filename}.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        
        return str(report_path)
    
    def _generate_excel_report(self, data: Dict[str, Any], filename: str) -> str:
        """Generate Excel report"""
        if not PANDAS_AVAILABLE:
            print("⚠️  Pandas not available. Generating CSV instead.")
            return self._generate_csv_report(data, filename)
        
        report_path = self.reports_dir / "excel" / f"{filename}.xlsx"
        
        with pd.ExcelWriter(report_path, engine='xlsxwriter') as writer:
            # Summary sheet
            if 'summary' in data:
                summary_df = pd.DataFrame([data['summary']])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Test results sheet
            if 'test_results' in data and data['test_results']:
                results_df = pd.DataFrame(data['test_results'])
                results_df.to_excel(writer, sheet_name='Test Results', index=False)
        
        return str(report_path)
    
    def _generate_csv_report(self, data: Dict[str, Any], filename: str) -> str:
        """Generate CSV report"""
        report_path = self.reports_dir / "csv" / f"{filename}.csv"
        
        if 'test_results' in data and data['test_results']:
            with open(report_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['test_id', 'test_type', 'status', 'success', 'score', 'duration_ms', 'start_time']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for result in data['test_results']:
                    row = {field: result.get(field, '') for field in fieldnames}
                    writer.writerow(row)
        
        return str(report_path)
    
    def _generate_summary(self, test_results, performance_data, security_data) -> Dict[str, Any]:
        """Generate report summary"""
        if not test_results:
            return {}
        
        total_tests = len(test_results)
        successful_tests = sum(1 for r in test_results if r.success)
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        avg_score = sum(r.score for r in test_results) / total_tests if total_tests > 0 else 0
        avg_duration = sum(r.duration_ms for r in test_results) / total_tests if total_tests > 0 else 0
        
        # Performance summary
        avg_performance_score = avg_score if test_results else 0
        
        # Security summary  
        security_score = security_data[0].security_score if security_data else 85.0
        
        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "success_rate": success_rate,
            "avg_score": avg_score,
            "avg_duration_ms": avg_duration,
            "avg_performance_score": avg_performance_score,
            "security_score": security_score
        }
    
    def _analyze_performance_data(self, performance_data) -> Dict[str, Any]:
        """Analyze performance data"""
        if not performance_data:
            return {}
        
        cpu_values = [p.cpu_usage for p in performance_data if hasattr(p, 'cpu_usage')]
        memory_values = [p.memory_usage for p in performance_data if hasattr(p, 'memory_usage')]
        response_values = [p.response_time_ms for p in performance_data if hasattr(p, 'response_time_ms')]
        
        avg_cpu = sum(cpu_values) / len(cpu_values) if cpu_values else 0
        avg_memory = sum(memory_values) / len(memory_values) if memory_values else 0
        avg_response = sum(response_values) / len(response_values) if response_values else 0
        
        # Performance grade
        if avg_cpu < 50 and avg_memory < 60 and avg_response < 100:
            grade = "Excellent"
        elif avg_cpu < 70 and avg_memory < 75 and avg_response < 200:
            grade = "Good"
        elif avg_cpu < 85 and avg_memory < 85 and avg_response < 500:
            grade = "Fair"
        else:
            grade = "Poor"
        
        return {
            "avg_cpu_usage": avg_cpu,
            "avg_memory_usage": avg_memory, 
            "avg_response_time": avg_response,
            "grade": grade,
            "total_measurements": len(performance_data)
        }
    
    def _analyze_security_data(self, security_data) -> Dict[str, Any]:
        """Analyze security data"""
        if not security_data:
            return {
                "security_score": 85.0,
                "threat_level": "LOW",
                "vulnerabilities_count": 0,
                "last_scan": "Never"
            }
        
        latest_scan = security_data[-1]
        return {
            "security_score": latest_scan.security_score,
            "threat_level": latest_scan.threat_level,
            "vulnerabilities_count": latest_scan.vulnerabilities_found,
            "last_scan": latest_scan.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _generate_recommendations(self, test_results, performance_data, security_data) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if test_results:
            success_rate = sum(1 for r in test_results if r.success) / len(test_results) * 100
            if success_rate < 90:
                recommendations.append("Improve test success rate by addressing failing test cases")
            
            avg_score = sum(r.score for r in test_results) / len(test_results)
            if avg_score < 80:
                recommendations.append("Focus on improving overall test scores through optimization")
        
        if performance_data:
            cpu_values = [p.cpu_usage for p in performance_data if hasattr(p, 'cpu_usage')]
            if cpu_values and sum(cpu_values) / len(cpu_values) > 80:
                recommendations.append("Consider CPU optimization - high average CPU usage detected")
        
        if security_data:
            latest_scan = security_data[-1]
            if latest_scan.security_score < 80:
                recommendations.append("Address security vulnerabilities to improve security score")
            if latest_scan.vulnerabilities_found > 0:
                recommendations.append(f"Fix {latest_scan.vulnerabilities_found} security vulnerabilities found")
        
        # General recommendations
        recommendations.extend([
            "Regular performance monitoring and optimization",
            "Implement automated security scanning",
            "Consider increasing test coverage for better reliability"
        ])
        
        return recommendations
    
    def _serialize_result(self, result) -> Dict[str, Any]:
        """Serialize test result for report"""
        return {
            "test_id": result.test_id,
            "test_type": result.test_type,
            "status": result.status,
            "success": result.success,
            "score": result.score,
            "duration_ms": result.duration_ms,
            "start_time": result.start_time.isoformat(),
            "end_time": result.end_time.isoformat(),
            "details": result.details
        }
    
    def get_available_reports(self) -> List[Dict[str, str]]:
        """Get list of available reports"""
        reports = []
        
        for format_dir in ['html', 'pdf', 'json', 'excel', 'csv']:
            format_path = self.reports_dir / format_dir
            if format_path.exists():
                for report_file in format_path.glob('*'):
                    if report_file.is_file():
                        reports.append({
                            'name': report_file.stem,
                            'format': format_dir.upper(),
                            'path': str(report_file),
                            'size': f"{report_file.stat().st_size / 1024:.1f} KB",
                            'created': datetime.fromtimestamp(report_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                        })
        
        return sorted(reports, key=lambda x: x['created'], reverse=True)
