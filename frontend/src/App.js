import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = 'http://localhost:8000/api';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [status, setStatus] = useState('idle');
  const [progress, setProgress] = useState(0);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  // Start new test session
  const startTesting = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/sessions/create`, {
        game_url: 'https://play.ezygamers.com/',
        test_count: 20,
        top_k: 10
      });
      
      setSessionId(response.data.session_id);
      setStatus('running');
      
      // Start polling for status
      pollStatus(response.data.session_id);
    } catch (error) {
      console.error('Failed to start testing:', error);
      setLoading(false);
    }
  };

  // Poll session status
  const pollStatus = async (id) => {
    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`${API_URL}/sessions/${id}`);
        setStatus(response.data.status);
        setProgress(response.data.progress || 0);
        
        if (response.data.status === 'completed') {
          clearInterval(interval);
          fetchReport(id);
        } else if (response.data.status === 'failed') {
          clearInterval(interval);
          setLoading(false);
        }
      } catch (error) {
        console.error('Failed to fetch status:', error);
        clearInterval(interval);
        setLoading(false);
      }
    }, 2000); // Poll every 2 seconds
  };

  // Fetch final report
  const fetchReport = async (id) => {
    try {
      const response = await axios.get(`${API_URL}/sessions/${id}/report`);
      setReport(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch report:', error);
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Multi-Agent Game Tester</h1>
        <p>Automated Testing for EzyGamers Number Puzzle</p>
      </header>
      
      <main className="App-main">
        {!sessionId && (
          <div className="start-section">
            <button 
              onClick={startTesting} 
              disabled={loading}
              className="start-button"
            >
              Start Testing
            </button>
          </div>
        )}
        
        {sessionId && !report && (
          <div className="progress-section">
            <h2>Test Session: {sessionId}</h2>
            <p>Status: {status}</p>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${progress}%` }}
              />
            </div>
            <p>{progress}% Complete</p>
          </div>
        )}
        
        {report && (
          <div className="report-section">
            <h2>Test Report</h2>
            <div className="summary">
              <h3>Summary</h3>
              <ul>
                <li>Total Tests: {report.summary.total_tests}</li>
                <li>Executed: {report.summary.executed_tests}</li>
                <li>Passed: {report.summary.passed}</li>
                <li>Failed: {report.summary.failed}</li>
                <li>Success Rate: {report.summary.success_rate.toFixed(2)}%</li>
              </ul>
            </div>
            
            <div className="test-results">
              <h3>Test Results</h3>
              <table>
                <thead>
                  <tr>
                    <th>Test ID</th>
                    <th>Status</th>
                    <th>Execution Time</th>
                    <th>Reproducibility</th>
                    <th>Artifacts</th>
                  </tr>
                </thead>
                <tbody>
                  {report.test_results.map(result => (
                    <tr key={result.test_case_id}>
                      <td>{result.test_case_id}</td>
                      <td className={`status-${result.status}`}>
                        {result.status}
                      </td>
                      <td>{result.execution_time.toFixed(2)}s</td>
                      <td>{(result.reproducibility_score * 100).toFixed(0)}%</td>
                      <td>
                        <button onClick={() => viewArtifacts(result.artifacts)}>
                          View
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            
            <div className="validation">
              <h3>Validation Results</h3>
              <pre>{JSON.stringify(report.validation, null, 2)}</pre>
            </div>
            
            <div className="recommendations">
              <h3>Recommendations</h3>
              <ul>
                {report.recommendations?.map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </div>
            
            <button 
              onClick={() => downloadReport(report)}
              className="download-button"
            >
              Download Full Report
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;