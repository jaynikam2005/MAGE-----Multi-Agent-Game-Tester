# MAGE - Multi-Agent Game Tester

MAGE is an advanced automated testing framework that uses multiple AI agents to test web-based games. It employs LangChain for test planning and execution, with a focus on comprehensive testing and result validation.

## Features

- 🤖 Multi-agent architecture for distributed testing
- 🧪 Automatic test case generation using LangChain
- 📊 Comprehensive test reporting with artifacts
- 🔄 Cross-validation and reproducibility checks
- 🚀 FastAPI backend with React frontend
- 📈 Grafana monitoring integration

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/jaynikam2005/MAGE---Multi-Agent-Game-Tester.git
cd MAGE---Multi-Agent-Game-Tester
```

2. Set up environment:
```bash
cp .env.template .env
# Edit .env with your configurations
```

3. Start with Docker:
```bash
docker-compose up -d
```

4. Access:
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Monitoring: http://localhost:3001

## Architecture

The system consists of multiple specialized agents:
- PlannerAgent: Generates test cases
- RankerAgent: Prioritizes test cases
- ExecutorAgent: Runs the tests
- AnalyzerAgent: Validates results
- OrchestratorAgent: Coordinates all agents

## Development

1. Install dependencies:
```bash
poetry install
```

2. Run tests:
```bash
poetry run pytest
```

## Security

- JWT authentication
- Rate limiting
- CORS protection
- Input validation
- Secure headers

## License

MIT License