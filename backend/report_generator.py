from jinja2 import Template
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

class EnhancedReportGenerator:
    def __init__(self):
        self.template = self._load_template()
    
    def generate_html_report(self, test_results: List[TestResult], validation: Dict) -> str:
        """Generate comprehensive HTML report with visualizations"""
        
        # Generate charts
        charts = {
            'success_rate': self._create_success_chart(test_results),
            'execution_time': self._create_timing_chart(test_results),
            'reproducibility': self._create_reproducibility_chart(validation)
        }
        
        # Compile report data
        report_data = {
            'summary': self._calculate_summary(test_results),
            'detailed_results': self._format_detailed_results(test_results),
            'validation': validation,
            'charts': charts,
            'recommendations': self._generate_recommendations(test_results, validation),
            'timestamp': datetime.now().isoformat()
        }
        
        # Render HTML
        html_content = self.template.render(**report_data)
        
        # Save report
        report_path = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        return report_path
    
    def _create_success_chart(self, results: List[TestResult]) -> str:
        """Create success rate pie chart"""
        plt.figure(figsize=(8, 6))
        
        passed = sum(1 for r in results if r.status == "passed")
        failed = sum(1 for r in results if r.status == "failed")
        
        plt.pie([passed, failed], labels=['Passed', 'Failed'], 
                autopct='%1.1f%%', colors=['#28a745', '#dc3545'])
        plt.title('Test Success Rate')
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"
    
    def _generate_recommendations(self, results: List[TestResult], validation: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Analyze failure patterns
        failed_tests = [r for r in results if r.status == "failed"]
        if failed_tests:
            failure_rate = len(failed_tests) / len(results)
            if failure_rate > 0.3:
                recommendations.append(
                    f"High failure rate ({failure_rate:.1%}) detected. "
                    "Review application stability and test environment."
                )
        
        # Check reproducibility
        low_reproducibility = [
            tid for tid, score in validation.get('repeat_validation', {}).items()
            if score < 0.7
        ]
        if low_reproducibility:
            recommendations.append(
                f"{len(low_reproducibility)} tests have low reproducibility. "
                "Consider adding wait conditions or retry logic."
            )
        
        # Performance issues
        slow_tests = [r for r in results if r.execution_time > 30]
        if slow_tests:
            recommendations.append(
                f"{len(slow_tests)} tests took over 30 seconds. "
                "Optimize test steps or parallelize execution."
            )
        
        return recommendations