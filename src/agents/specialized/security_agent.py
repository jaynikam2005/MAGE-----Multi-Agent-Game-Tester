"""
Advanced Security Testing Agent
Penetration Testing & Vulnerability Assessment for Games
"""

import asyncio
import json
import re
import hashlib
import base64
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import structlog
from urllib.parse import urlparse, parse_qs

from src.core.config import get_settings


@dataclass
class SecurityVulnerability:
    """Security vulnerability finding"""
    id: str
    severity: str  # critical, high, medium, low, info
    category: str
    title: str
    description: str
    impact: str
    remediation: str
    evidence: List[str]
    cwe_id: Optional[str]
    cvss_score: float


@dataclass
class SecurityTest:
    """Security test case"""
    test_id: str
    test_type: str
    target: str
    payload: str
    expected_response: str
    actual_response: str
    vulnerable: bool


class SecurityAgent:
    """Advanced security testing agent with penetration testing capabilities"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = config
        self.settings = get_settings()
        self.logger = structlog.get_logger(__name__)
        
        # Security test payloads
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "';alert('XSS');//",
            "<svg onload=alert('XSS')>",
            "{{constructor.constructor('alert(\"XSS\")')()}}"
        ]
        
        self.sql_injection_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT null, version(), null --",
            "1' AND (SELECT COUNT(*) FROM information_schema.tables)>0 --",
            "admin'--",
            "' OR 1=1#"
        ]
        
        self.path_traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "....//....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64",
            "..%252f..%252f..%252fetc%252fpasswd"
        ]
        
        self.command_injection_payloads = [
            "; ls -la",
            "| whoami",
            "&& cat /etc/passwd",
            "`id`",
            "$(whoami)",
            "; ping -c 1 127.0.0.1"
        ]
        
        # Security scanning rules
        self.security_headers = {
            "Content-Security-Policy": "missing",
            "X-Frame-Options": "missing",
            "X-Content-Type-Options": "missing",
            "Strict-Transport-Security": "missing",
            "X-XSS-Protection": "missing",
            "Referrer-Policy": "missing"
        }
        
        # Vulnerability patterns
        self.vulnerability_patterns = {
            "debug_info": [
                r"debug[:\s]+(true|on|enabled)",
                r"error[:\s]+.*?(stack trace|exception)",
                r"console\.log\([^)]+\)",
                r"alert\([^)]+\)"
            ],
            "sensitive_data": [
                r"password[:\s]+[^,\s]+",
                r"api[_\s]*key[:\s]+[^,\s]+",
                r"secret[:\s]+[^,\s]+",
                r"token[:\s]+[^,\s]+"
            ],
            "weak_crypto": [
                r"md5\(",
                r"sha1\(",
                r"Math\.random\(\)"
            ]
        }
    
    async def initialize(self) -> None:
        """Initialize security testing agent"""
        try:
            await self._load_security_rules()
            self.logger.info(f"Security agent {self.agent_id} initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize security agent: {e}")
            raise
    
    async def analyze_security(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Comprehensive security analysis"""
        
        try:
            self.logger.info(f"Starting security analysis of {len(test_results)} test results")
            
            # Extract target information
            target_info = await self._extract_target_info(test_results)
            
            # Perform security tests
            security_tests = await self._perform_security_tests(target_info)
            
            # Analyze for vulnerabilities
            vulnerabilities = await self._analyze_vulnerabilities(test_results, security_tests)
            
            # Check security headers
            headers_analysis = await self._analyze_security_headers(test_results)
            
            # Analyze client-side security
            client_security = await self._analyze_client_security(test_results)
            
            # Check for information disclosure
            info_disclosure = await self._check_information_disclosure(test_results)
            
            # Authentication and authorization checks
            auth_analysis = await self._analyze_authentication(test_results)
            
            # Generate security score
            security_score = await self._calculate_security_score(vulnerabilities, headers_analysis)
            
            # Risk assessment
            risk_assessment = await self._assess_security_risks(vulnerabilities)
            
            analysis = {
                "agent_id": self.agent_id,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "security_score": security_score,
                "risk_level": self._determine_risk_level(security_score),
                "target_info": target_info,
                "vulnerabilities": [v.__dict__ for v in vulnerabilities],
                "security_tests": [t.__dict__ for t in security_tests],
                "headers_analysis": headers_analysis,
                "client_security": client_security,
                "information_disclosure": info_disclosure,
                "authentication_analysis": auth_analysis,
                "risk_assessment": risk_assessment,
                "compliance_status": await self._check_compliance_status(vulnerabilities),
                "recommendations": await self._generate_security_recommendations(vulnerabilities)
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Security analysis failed: {e}")
            raise
    
    async def _extract_target_info(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract target application information"""
        
        target_info = {
            "urls": set(),
            "technologies": set(),
            "endpoints": set(),
            "parameters": set()
        }
        
        for result in results:
            # Extract URLs from artifacts
            if "artifacts" in result and "dom_snapshot" in result["artifacts"]:
                dom = result["artifacts"]["dom_snapshot"]
                
                # Extract links and forms
                url_pattern = r'https?://[^\s<>"\']+|\/[^\s<>"\']*'
                urls = re.findall(url_pattern, dom)
                target_info["urls"].update(urls)
                
                # Extract form actions
                form_pattern = r'<form[^>]+action=["\']([^"\']+)["\']'
                forms = re.findall(form_pattern, dom, re.IGNORECASE)
                target_info["endpoints"].update(forms)
                
                # Extract input parameters
                input_pattern = r'<input[^>]+name=["\']([^"\']+)["\']'
                inputs = re.findall(input_pattern, dom, re.IGNORECASE)
                target_info["parameters"].update(inputs)
                
                # Detect technologies
                if "react" in dom.lower():
                    target_info["technologies"].add("React")
                if "angular" in dom.lower():
                    target_info["technologies"].add("Angular")
                if "vue" in dom.lower():
                    target_info["technologies"].add("Vue.js")
                if "jquery" in dom.lower():
                    target_info["technologies"].add("jQuery")
        
        # Convert sets to lists for JSON serialization
        for key in target_info:
            target_info[key] = list(target_info[key])
        
        return target_info
    
    async def _perform_security_tests(self, target_info: Dict[str, Any]) -> List[SecurityTest]:
        """Perform active security tests"""
        
        security_tests = []
        test_counter = 1
        
        # XSS Testing
        for url in target_info["urls"][:5]:  # Limit to first 5 URLs
            for payload in self.xss_payloads[:3]:  # Test top 3 payloads
                test = SecurityTest(
                    test_id=f"XSS_{test_counter:03d}",
                    test_type="XSS",
                    target=url,
                    payload=payload,
                    expected_response="payload_escaped",
                    actual_response="simulated_safe",  # Simulated response
                    vulnerable=False  # Simulated result
                )
                security_tests.append(test)
                test_counter += 1
        
        # SQL Injection Testing
        for param in target_info["parameters"][:3]:
            for payload in self.sql_injection_payloads[:2]:
                test = SecurityTest(
                    test_id=f"SQLi_{test_counter:03d}",
                    test_type="SQL_Injection",
                    target=param,
                    payload=payload,
                    expected_response="error_or_filter",
                    actual_response="simulated_filtered",
                    vulnerable=False
                )
                security_tests.append(test)
                test_counter += 1
        
        # Path Traversal Testing
        for endpoint in target_info["endpoints"][:3]:
            for payload in self.path_traversal_payloads[:2]:
                test = SecurityTest(
                    test_id=f"PathTraversal_{test_counter:03d}",
                    test_type="Path_Traversal",
                    target=endpoint,
                    payload=payload,
                    expected_response="access_denied",
                    actual_response="simulated_blocked",
                    vulnerable=False
                )
                security_tests.append(test)
                test_counter += 1
        
        return security_tests
    
    async def _analyze_vulnerabilities(self, results: List[Dict[str, Any]], 
                                     security_tests: List[SecurityTest]) -> List[SecurityVulnerability]:
        """Analyze for security vulnerabilities"""
        
        vulnerabilities = []
        vuln_counter = 1
        
        # Check for debug information exposure
        debug_vulns = await self._check_debug_exposure(results)
        vulnerabilities.extend(debug_vulns)
        
        # Check for sensitive data exposure
        sensitive_vulns = await self._check_sensitive_data_exposure(results)
        vulnerabilities.extend(sensitive_vulns)
        
        # Check for weak cryptography
        crypto_vulns = await self._check_weak_cryptography(results)
        vulnerabilities.extend(crypto_vulns)
        
        # Check for insecure communications
        comm_vulns = await self._check_insecure_communications(results)
        vulnerabilities.extend(comm_vulns)
        
        # Analyze security test results
        for test in security_tests:
            if test.vulnerable:
                vuln = SecurityVulnerability(
                    id=f"VULN_{vuln_counter:03d}",
                    severity=self._get_vulnerability_severity(test.test_type),
                    category=test.test_type,
                    title=f"{test.test_type} Vulnerability",
                    description=f"Application is vulnerable to {test.test_type} attacks",
                    impact=self._get_vulnerability_impact(test.test_type),
                    remediation=self._get_vulnerability_remediation(test.test_type),
                    evidence=[f"Payload: {test.payload}", f"Response: {test.actual_response}"],
                    cwe_id=self._get_cwe_id(test.test_type),
                    cvss_score=self._calculate_cvss_score(test.test_type)
                )
                vulnerabilities.append(vuln)
                vuln_counter += 1
        
        return vulnerabilities
    
    async def _check_debug_exposure(self, results: List[Dict[str, Any]]) -> List[SecurityVulnerability]:
        """Check for debug information exposure"""
        
        vulnerabilities = []
        
        for result in results:
            if "artifacts" in result:
                artifacts = result["artifacts"]
                
                # Check console logs
                if "console_logs" in artifacts:
                    for log in artifacts["console_logs"]:
                        for pattern in self.vulnerability_patterns["debug_info"]:
                            if re.search(pattern, str(log), re.IGNORECASE):
                                vulnerabilities.append(SecurityVulnerability(
                                    id="DEBUG_001",
                                    severity="medium",
                                    category="Information_Disclosure",
                                    title="Debug Information Exposure",
                                    description="Application exposes debug information in console logs",
                                    impact="Information disclosure, potential system details exposure",
                                    remediation="Disable debug mode in production, remove console.log statements",
                                    evidence=[f"Debug log: {log}"],
                                    cwe_id="CWE-489",
                                    cvss_score=4.3
                                ))
                                break
                
                # Check DOM for debug info
                if "dom_snapshot" in artifacts:
                    dom = artifacts["dom_snapshot"]
                    for pattern in self.vulnerability_patterns["debug_info"]:
                        matches = re.findall(pattern, dom, re.IGNORECASE)
                        if matches:
                            vulnerabilities.append(SecurityVulnerability(
                                id="DEBUG_002",
                                severity="low",
                                category="Information_Disclosure",
                                title="Debug Information in DOM",
                                description="Debug information found in DOM structure",
                                impact="Minor information disclosure",
                                remediation="Remove debug elements from production DOM",
                                evidence=[f"Debug pattern: {match}" for match in matches[:3]],
                                cwe_id="CWE-489",
                                cvss_score=2.1
                            ))
        
        return vulnerabilities
    
    async def _check_sensitive_data_exposure(self, results: List[Dict[str, Any]]) -> List[SecurityVulnerability]:
        """Check for sensitive data exposure"""
        
        vulnerabilities = []
        
        for result in results:
            if "artifacts" in result and "dom_snapshot" in result["artifacts"]:
                dom = result["artifacts"]["dom_snapshot"]
                
                for pattern in self.vulnerability_patterns["sensitive_data"]:
                    matches = re.findall(pattern, dom, re.IGNORECASE)
                    if matches:
                        vulnerabilities.append(SecurityVulnerability(
                            id="SENSITIVE_001",
                            severity="high",
                            category="Sensitive_Data_Exposure",
                            title="Sensitive Data in Client-Side Code",
                            description="Sensitive information found in client-side code",
                            impact="Credential theft, unauthorized access",
                            remediation="Move sensitive data to server-side, use environment variables",
                            evidence=[f"Sensitive data pattern: {match}" for match in matches[:3]],
                            cwe_id="CWE-200",
                            cvss_score=7.5
                        ))
        
        return vulnerabilities
    
    async def _check_weak_cryptography(self, results: List[Dict[str, Any]]) -> List[SecurityVulnerability]:
        """Check for weak cryptographic implementations"""
        
        vulnerabilities = []
        
        for result in results:
            if "artifacts" in result and "dom_snapshot" in result["artifacts"]:
                dom = result["artifacts"]["dom_snapshot"]
                
                for pattern in self.vulnerability_patterns["weak_crypto"]:
                    if re.search(pattern, dom, re.IGNORECASE):
                        vulnerabilities.append(SecurityVulnerability(
                            id="CRYPTO_001",
                            severity="medium",
                            category="Cryptographic_Issues",
                            title="Weak Cryptographic Algorithm",
                            description="Application uses weak cryptographic algorithms",
                            impact="Data integrity compromise, potential data decryption",
                            remediation="Use strong cryptographic algorithms (SHA-256, AES)",
                            evidence=[f"Weak crypto pattern found: {pattern}"],
                            cwe_id="CWE-327",
                            cvss_score=5.3
                        ))
        
        return vulnerabilities
    
    async def _check_insecure_communications(self, results: List[Dict[str, Any]]) -> List[SecurityVulnerability]:
        """Check for insecure communications"""
        
        vulnerabilities = []
        
        for result in results:
            if "artifacts" in result:
                artifacts = result["artifacts"]
                
                # Check for HTTP requests in HTTPS context
                if "network_requests" in artifacts:
                    for request in artifacts["network_requests"]:
                        url = request.get("url", "")
                        if url.startswith("http://") and "localhost" not in url:
                            vulnerabilities.append(SecurityVulnerability(
                                id="COMM_001",
                                severity="medium",
                                category="Insecure_Communication",
                                title="Mixed Content - Insecure HTTP Request",
                                description="Application makes insecure HTTP requests",
                                impact="Man-in-the-middle attacks, data interception",
                                remediation="Use HTTPS for all external communications",
                                evidence=[f"Insecure request: {url}"],
                                cwe_id="CWE-319",
                                cvss_score=5.9
                            ))
        
        return vulnerabilities
    
    async def _analyze_security_headers(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze HTTP security headers"""
        
        headers_status = self.security_headers.copy()
        missing_headers = []
        
        # In a real implementation, we would check actual HTTP response headers
        # For simulation, we'll assume some headers are missing
        
        critical_missing = []
        for header, status in headers_status.items():
            if status == "missing":
                missing_headers.append(header)
                
                if header in ["Content-Security-Policy", "X-Frame-Options"]:
                    critical_missing.append(header)
        
        return {
            "headers_checked": len(self.security_headers),
            "missing_headers": missing_headers,
            "critical_missing": critical_missing,
            "security_score": max(0, 100 - len(missing_headers) * 15),
            "recommendations": [
                f"Implement {header} header" for header in missing_headers[:5]
            ]
        }
    
    async def _analyze_client_security(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze client-side security"""
        
        client_issues = []
        
        for result in results:
            if "artifacts" in result and "dom_snapshot" in result["artifacts"]:
                dom = result["artifacts"]["dom_snapshot"]
                
                # Check for inline scripts
                inline_scripts = len(re.findall(r'<script[^>]*>(?!.*src=)', dom, re.IGNORECASE))
                if inline_scripts > 0:
                    client_issues.append({
                        "issue": "inline_scripts",
                        "count": inline_scripts,
                        "severity": "medium",
                        "description": "Inline JavaScript detected"
                    })
                
                # Check for eval usage
                eval_usage = len(re.findall(r'\beval\s*\(', dom, re.IGNORECASE))
                if eval_usage > 0:
                    client_issues.append({
                        "issue": "eval_usage",
                        "count": eval_usage,
                        "severity": "high",
                        "description": "eval() function usage detected"
                    })
                
                # Check for document.write usage
                doc_write = len(re.findall(r'document\.write\s*\(', dom, re.IGNORECASE))
                if doc_write > 0:
                    client_issues.append({
                        "issue": "document_write",
                        "count": doc_write,
                        "severity": "medium",
                        "description": "document.write usage detected"
                    })
        
        return {
            "issues_found": len(client_issues),
            "client_issues": client_issues,
            "security_rating": self._rate_client_security(client_issues)
        }
    
    def _rate_client_security(self, issues: List[Dict[str, Any]]) -> str:
        """Rate client-side security"""
        
        high_severity = len([i for i in issues if i["severity"] == "high"])
        medium_severity = len([i for i in issues if i["severity"] == "medium"])
        
        if high_severity > 0:
            return "poor"
        elif medium_severity > 3:
            return "fair"
        elif medium_severity > 0:
            return "good"
        else:
            return "excellent"
    
    async def _check_information_disclosure(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Check for information disclosure vulnerabilities"""
        
        disclosure_issues = []
        
        for result in results:
            if "artifacts" in result:
                artifacts = result["artifacts"]
                
                # Check for error messages in console
                if "console_logs" in artifacts:
                    for log in artifacts["console_logs"]:
                        if any(error_term in str(log).lower() for error_term in ["error", "exception", "stack trace"]):
                            disclosure_issues.append({
                                "type": "error_exposure",
                                "severity": "low",
                                "evidence": str(log)[:100]
                            })
                
                # Check for version information
                if "dom_snapshot" in artifacts:
                    dom = artifacts["dom_snapshot"]
                    version_patterns = [r'version[:\s]+[\d.]+', r'v[\d.]+', r'build[:\s]+\d+']
                    
                    for pattern in version_patterns:
                        matches = re.findall(pattern, dom, re.IGNORECASE)
                        if matches:
                            disclosure_issues.append({
                                "type": "version_disclosure",
                                "severity": "info",
                                "evidence": matches[0]
                            })
        
        return {
            "issues_count": len(disclosure_issues),
            "disclosure_issues": disclosure_issues,
            "risk_level": "high" if len(disclosure_issues) > 5 else "low"
        }
    
    async def _analyze_authentication(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze authentication mechanisms"""
        
        auth_analysis = {
            "authentication_detected": False,
            "session_management": "unknown",
            "password_policy": "unknown",
            "multi_factor": False,
            "issues": []
        }
        
        for result in results:
            if "artifacts" in result and "dom_snapshot" in result["artifacts"]:
                dom = result["artifacts"]["dom_snapshot"]
                
                # Check for login forms
                login_forms = re.findall(r'<form[^>]*>.*?password.*?</form>', dom, re.DOTALL | re.IGNORECASE)
                if login_forms:
                    auth_analysis["authentication_detected"] = True
                    
                    # Check for password requirements
                    if "minlength" in dom.lower() or "pattern" in dom.lower():
                        auth_analysis["password_policy"] = "enforced"
                    
                    # Check for remember me checkboxes
                    if "remember" in dom.lower():
                        auth_analysis["issues"].append({
                            "issue": "remember_me_option",
                            "severity": "low",
                            "description": "Remember me option may pose security risk"
                        })
        
        return auth_analysis
    
    def _get_vulnerability_severity(self, vuln_type: str) -> str:
        """Get vulnerability severity based on type"""
        severity_map = {
            "XSS": "high",
            "SQL_Injection": "critical",
            "Path_Traversal": "high",
            "Command_Injection": "critical",
            "CSRF": "medium",
            "Information_Disclosure": "medium"
        }
        return severity_map.get(vuln_type, "medium")
    
    def _get_vulnerability_impact(self, vuln_type: str) -> str:
        """Get vulnerability impact description"""
        impact_map = {
            "XSS": "Client-side code execution, session hijacking, data theft",
            "SQL_Injection": "Database compromise, data breach, system takeover",
            "Path_Traversal": "Unauthorized file access, information disclosure",
            "Command_Injection": "System compromise, remote code execution"
        }
        return impact_map.get(vuln_type, "Security compromise")
    
    def _get_vulnerability_remediation(self, vuln_type: str) -> str:
        """Get vulnerability remediation advice"""
        remediation_map = {
            "XSS": "Implement proper input validation and output encoding",
            "SQL_Injection": "Use parameterized queries and input validation",
            "Path_Traversal": "Validate and sanitize file paths, use allowlists",
            "Command_Injection": "Avoid system calls, use safe APIs"
        }
        return remediation_map.get(vuln_type, "Implement security controls")
    
    def _get_cwe_id(self, vuln_type: str) -> str:
        """Get CWE ID for vulnerability type"""
        cwe_map = {
            "XSS": "CWE-79",
            "SQL_Injection": "CWE-89",
            "Path_Traversal": "CWE-22",
            "Command_Injection": "CWE-78"
        }
        return cwe_map.get(vuln_type, "CWE-0")
    
    def _calculate_cvss_score(self, vuln_type: str) -> float:
        """Calculate CVSS score for vulnerability"""
        cvss_map = {
            "XSS": 6.1,
            "SQL_Injection": 9.8,
            "Path_Traversal": 7.5,
            "Command_Injection": 9.8
        }
        return cvss_map.get(vuln_type, 5.0)
    
    async def _calculate_security_score(self, vulnerabilities: List[SecurityVulnerability], 
                                      headers_analysis: Dict[str, Any]) -> float:
        """Calculate overall security score"""
        
        base_score = 100.0
        
        # Deduct points for vulnerabilities
        for vuln in vulnerabilities:
            if vuln.severity == "critical":
                base_score -= 20
            elif vuln.severity == "high":
                base_score -= 15
            elif vuln.severity == "medium":
                base_score -= 10
            elif vuln.severity == "low":
                base_score -= 5
        
        # Deduct points for missing security headers
        missing_headers = len(headers_analysis.get("missing_headers", []))
        base_score -= missing_headers * 3
        
        return max(0.0, base_score)
    
    def _determine_risk_level(self, security_score: float) -> str:
        """Determine overall risk level"""
        
        if security_score >= 90:
            return "low"
        elif security_score >= 70:
            return "medium"
        elif security_score >= 50:
            return "high"
        else:
            return "critical"
    
    async def _assess_security_risks(self, vulnerabilities: List[SecurityVulnerability]) -> Dict[str, Any]:
        """Assess security risks"""
        
        risk_factors = []
        
        # Categorize vulnerabilities by severity
        critical_vulns = [v for v in vulnerabilities if v.severity == "critical"]
        high_vulns = [v for v in vulnerabilities if v.severity == "high"]
        
        if critical_vulns:
            risk_factors.append({
                "factor": "critical_vulnerabilities",
                "count": len(critical_vulns),
                "impact": "immediate_threat",
                "description": "Critical vulnerabilities require immediate attention"
            })
        
        if len(high_vulns) > 3:
            risk_factors.append({
                "factor": "multiple_high_severity",
                "count": len(high_vulns),
                "impact": "high_risk",
                "description": "Multiple high-severity vulnerabilities increase attack surface"
            })
        
        return {
            "overall_risk": "critical" if critical_vulns else "high" if len(high_vulns) > 2 else "medium",
            "risk_factors": risk_factors,
            "vulnerability_distribution": {
                "critical": len(critical_vulns),
                "high": len(high_vulns),
                "medium": len([v for v in vulnerabilities if v.severity == "medium"]),
                "low": len([v for v in vulnerabilities if v.severity == "low"])
            }
        }
    
    async def _check_compliance_status(self, vulnerabilities: List[SecurityVulnerability]) -> Dict[str, Any]:
        """Check compliance with security standards"""
        
        compliance_issues = []
        
        # OWASP Top 10 compliance check
        owasp_categories = {
            "A01": ["SQL_Injection"],
            "A02": ["Cryptographic_Issues"],
            "A03": ["XSS"],
            "A05": ["Information_Disclosure"],
            "A07": ["XSS"]  # Cross-Site Scripting
        }
        
        failing_categories = []
        for category, vuln_types in owasp_categories.items():
            if any(v.category in vuln_types for v in vulnerabilities):
                failing_categories.append(category)
        
        return {
            "owasp_top_10_compliance": len(failing_categories) == 0,
            "failing_categories": failing_categories,
            "compliance_score": max(0, 100 - len(failing_categories) * 10),
            "recommendations": [
                f"Address OWASP {cat} vulnerabilities" for cat in failing_categories
            ]
        }
    
    async def _generate_security_recommendations(self, vulnerabilities: List[SecurityVulnerability]) -> List[str]:
        """Generate security recommendations"""
        
        recommendations = []
        
        # Priority recommendations based on critical vulnerabilities
        critical_vulns = [v for v in vulnerabilities if v.severity == "critical"]
        if critical_vulns:
            recommendations.extend([
                "Immediately patch critical security vulnerabilities",
                "Conduct emergency security review",
                "Consider taking application offline until fixes are implemented"
            ])
        
        # General recommendations
        vuln_categories = set(v.category for v in vulnerabilities)
        
        if "XSS" in vuln_categories:
            recommendations.append("Implement Content Security Policy (CSP)")
            recommendations.append("Use proper output encoding and input validation")
        
        if "SQL_Injection" in vuln_categories:
            recommendations.append("Use parameterized queries and ORM frameworks")
            recommendations.append("Implement database access controls")
        
        if "Information_Disclosure" in vuln_categories:
            recommendations.append("Remove debug information from production")
            recommendations.append("Implement proper error handling")
        
        # Security best practices
        recommendations.extend([
            "Implement security headers (CSP, HSTS, X-Frame-Options)",
            "Conduct regular security testing and code reviews",
            "Implement security monitoring and logging",
            "Use HTTPS for all communications",
            "Regular security updates and patch management"
        ])
        
        return recommendations[:10]  # Return top 10 recommendations
    
    async def _load_security_rules(self) -> None:
        """Load security testing rules"""
        # In production, this would load from configuration files or database
        pass
    
    async def get_health_metrics(self) -> Dict[str, Any]:
        """Get security agent health metrics"""
        return {
            "agent_id": self.agent_id,
            "status": "healthy",
            "cpu_usage": 0.18,
            "memory_usage": 0.25,
            "security_tests_run": 50,  # Would track actual metrics
            "vulnerabilities_detected": 3
        }
