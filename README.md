# MAGE (Multi-Agent Game Testing Environment)

## Overview
Production-grade desktop application for automated testing of web-based games using multi-agent architecture.

## Features
- 20+ test case generation using LangChain
- Smart test ranking and selection
- Multi-agent test execution framework
- Comprehensive artifact capture (screenshots, DOM, console logs, network)
- Cross-agent validation system
- Structured reporting (JSON + HTML)

## Tech Stack
- Backend: FastAPI (Python 3.11+)
- Frontend: Electron.js + React + TailwindCSS
- Multi-Agent Framework: LangChain
- Browser Automation: Playwright
- Security: AES-256 encryption, RBAC, audit logging
- Testing: Pytest (backend), Jest (frontend)
- Packaging: PyInstaller + Electron Builder

## Prerequisites
- Python 3.11+
- Node.js 18+
- Poetry for Python dependency management
- npm for JavaScript dependency management

## Installation

### Backend Setup
```bash
# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install

# Set up environment
cp .env.example .env
# Edit .env with your settings

# Install Playwright browsers
poetry run playwright install chromium

# Run backend
poetry run python src/main.py
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run in development mode
npm run dev

# Build desktop app
npm run build
```

## Security Features
- End-to-end encryption for data at rest and in transit
- Role-based access control
- Comprehensive audit logging
- Code signing for released binaries
- Secure dependency management

## Development
- Follow clean code principles
- Use Black + Flake8 for Python code formatting
- Use ESLint + Prettier for JavaScript code formatting
- Write tests for new features
- Update documentation as needed

## Testing
```bash
# Backend tests
poetry run pytest

# Frontend tests
cd frontend && npm test
```

## Building Desktop App
```bash
# Build backend binary
poetry run pyinstaller src/main.spec

# Build frontend
cd frontend && npm run build

# Create installers
npm run dist
```

## Project Structure
```
mage/
├── backend/
│   ├── src/
│   │   ├── agents/         # Multi-agent system
│   │   ├── api/           # FastAPI routes
│   │   ├── core/         # Core functionality
│   │   └── tests/        # Backend tests
│   └── pyproject.toml    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # Frontend services
│   │   └── styles/       # TailwindCSS styles
│   └── package.json     # JS dependencies
├── .github/             # GitHub Actions
└── README.md           # This file
```

## Contributing
1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
MIT License
