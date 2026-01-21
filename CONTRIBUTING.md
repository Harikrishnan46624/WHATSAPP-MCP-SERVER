# Contributing to WhatsApp MCP Server

Thank you for your interest in contributing to the WhatsApp MCP Server! This document provides guidelines and information to help you contribute effectively to the project.

## 🚀 Getting Started

### Development Setup

1. **Fork and Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/whatsapp-mcp-server.git
   cd whatsapp-mcp-server
   ```

2. **Set up Python Environment:**
   ```bash
   # Using uv (recommended)
   uv venv
   uv pip install -e .

   # Or using pip
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your MCP_API_TOKEN for testing
   ```

4. **Run the Server:**
   ```bash
   python server.py
   ```

### Development Workflow

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure tests pass:
   ```bash
   # Run tests if available
   pytest

   # Format code
   black .
   isort .
   ```

3. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

4. Push and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## 🧪 Testing

- Write tests for new features
- Ensure all existing tests pass
- Test both unit and integration scenarios

## 📝 Code Style

This project follows standard Python formatting:

- **Formatting**: Black
- **Import sorting**: isort
- **Linting**: flake8
- **Type hints**: mypy (recommended)

Run formatting before committing:
```bash
black .
isort .
flake8 .
```

## 🔄 Pull Request Process

1. **Title**: Use conventional commit format (e.g., `feat:`, `fix:`, `docs:`)
2. **Description**: Clearly describe what changes and why
3. **Tests**: Include tests for new functionality
4. **Documentation**: Update README/docs if needed

## 🎯 Good First Issues

These are beginner-friendly issues to help you get started with contributing:

### Production Error Handling & Logging
- Implement structured logging throughout the application
- Add error handling for WhatsApp API failures
- Create retry mechanisms for transient errors

### Multi-tenant Session Management
- Design and implement session isolation for multiple clients
- Add session cleanup and expiration logic
- Ensure proper credential management per session

### Rate Limiting & Retry Logic
- Implement rate limiting for WhatsApp API calls
- Add exponential backoff for failed requests
- Handle API quota exceeded scenarios

### Health Checks & Metrics Endpoint
- Add health check endpoint for monitoring
- Implement metrics collection (response times, error rates)
- Create Prometheus-compatible metrics output

## 🤝 Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. Please be respectful and constructive in all interactions.

## 📞 Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions and ideas
- **Documentation**: Check the README.md for detailed setup instructions

## 📋 Commit Message Guidelines

Use conventional commits:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Example: `feat: add rate limiting for WhatsApp API calls`

Thank you for contributing to make WhatsApp MCP Server better! 🎉
