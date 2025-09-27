import React, { useState, useEffect } from 'react';
import { ChakraProvider, Box, VStack, HStack, Button, Text, Input, Select, Progress, useToast, Table, Thead, Tbody, Tr, Th, Td, Badge } from '@chakra-ui/react';

const API_BASE_URL = 'http://localhost:8000/api/v2';

function App() {
  const [targetUrl, setTargetUrl] = useState('https://play.ezygamers.com/');
  const [executionId, setExecutionId] = useState(null);
  const [executionStatus, setExecutionStatus] = useState(null);
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  const generateTestPlan = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/generate-plan`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ target_url: targetUrl })
      });

      if (!response.ok) throw new Error('Failed to generate test plan');

      const data = await response.json();
      const executionResponse = await fetch(`${API_BASE_URL}/execute-plan`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ test_cases: data.test_cases })
      });

      if (!executionResponse.ok) throw new Error('Failed to start execution');

      const executionData = await executionResponse.json();
      setExecutionId(executionData.execution_id);
      startStatusPolling(executionData.execution_id);

      toast({
        title: 'Test plan generated and execution started',
        status: 'success',
        duration: 3000,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: error.message,
        status: 'error',
        duration: 3000,
      });
    } finally {
      setLoading(false);
    }
  };

  const startStatusPolling = (id) => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/execution-status/${id}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        const status = await response.json();
        setExecutionStatus(status);

        if (status.status === 'COMPLETED') {
          clearInterval(interval);
          fetchReports();
        }
      } catch (error) {
        console.error('Status polling error:', error);
        clearInterval(interval);
      }
    }, 5000);
  };

  const fetchReports = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/reports`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      setReports(data);
    } catch (error) {
      console.error('Error fetching reports:', error);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  return (
    <ChakraProvider>
      <Box p={8}>
        <VStack spacing={6} align="stretch">
          <HStack>
            <Input
              value={targetUrl}
              onChange={(e) => setTargetUrl(e.target.value)}
              placeholder="Enter target URL"
              flex={1}
            />
            <Button
              colorScheme="blue"
              onClick={generateTestPlan}
              isLoading={loading}
              loadingText="Generating..."
            >
              Generate & Execute Tests
            </Button>
          </HStack>

          {executionStatus && (
            <Box borderWidth={1} borderRadius="lg" p={4}>
              <Text fontSize="lg" mb={2}>Execution Status</Text>
              <Progress
                value={(executionStatus.completed_tests / executionStatus.total_tests) * 100}
                size="lg"
                colorScheme="green"
                mb={2}
              />
              <Text>{`${executionStatus.completed_tests} / ${executionStatus.total_tests} tests completed`}</Text>
              <Badge colorScheme={executionStatus.status === 'COMPLETED' ? 'green' : 'yellow'}>
                {executionStatus.status}
              </Badge>
            </Box>
          )}

          <Box>
            <Text fontSize="xl" mb={4}>Test Reports</Text>
            <Table variant="simple">
              <Thead>
                <Tr>
                  <Th>ID</Th>
                  <Th>Date</Th>
                  <Th>Success Rate</Th>
                  <Th>Actions</Th>
                </Tr>
              </Thead>
              <Tbody>
                {reports.map((report) => (
                  <Tr key={report.id}>
                    <Td>{report.id}</Td>
                    <Td>{new Date(report.timestamp).toLocaleString()}</Td>
                    <Td>
                      {((report.successful_tests / report.total_tests) * 100).toFixed(1)}%
                    </Td>
                    <Td>
                      <Button
                        size="sm"
                        onClick={() => window.open(`${API_BASE_URL}/reports/${report.id}`)}
                      >
                        View Details
                      </Button>
                    </Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </Box>
        </VStack>
      </Box>
    </ChakraProvider>
  );
}

export default App;