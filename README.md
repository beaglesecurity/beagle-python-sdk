# Beagle Python SDK

[![PyPI version](https://badge.fury.io/py/beagle-sdk.svg)](https://badge.fury.io/py/beagle-sdk)
[![Python Support](https://img.shields.io/pypi/pyversions/beagle-sdk.svg)](https://pypi.org/project/beagle-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready Python SDK for the Beagle v3 API. This SDK provides easy access to all Beagle security testing and vulnerability assessment endpoints.

## Features

- 🔒 **Secure Authentication** - Built-in API key authentication with automatic retry logic
- 🚀 **Comprehensive API Coverage** - Full support for all Beagle v3 API endpoints
- 📊 **Project Management** - Create, manage, and monitor security projects
- 🛡️ **Application Testing** - Start, stop, and monitor security tests
- 📈 **Results & Analytics** - Retrieve test results in JSON or PDF format
- 🎣 **Webhook Support** - Configure webhooks for real-time notifications
- ⚡ **Production Ready** - Robust error handling, rate limiting, and retry logic
- 🐍 **Python 3.7+** - Compatible with modern Python versions

## Installation

```bash
pip install beagle-sdk
```

## Quick Start

```python
from beagle_sdk import BeagleClient

# Initialize the client
client = BeagleClient(api_key="your-api-key-here")

# List all projects
projects = client.projects.list()
print(f"Found {len(projects['data'])} projects")

# Get a specific project
project = client.projects.get("project-uuid-here")
print(f"Project: {project['name']}")

# List applications under a project
applications = client.applications.list(project_key="project-uuid-here")

# Start a security test
test_result = client.testing.start("application-token-here")
result_token = test_result['result_token']

# Check test status
status = client.testing.get_status("application-token-here", result_token)
print(f"Test status: {status['status']}")

# Get test results when complete
results = client.results.get_json("application-token-here", result_token)

# Download PDF report
pdf_path = client.results.download_pdf("application-token-here", result_token)
print(f"Report saved to: {pdf_path}")
```

## API Reference

### Client Initialization

```python
from beagle_sdk import BeagleClient

client = BeagleClient(
    api_key="your-api-key",
    base_url="https://api.beagle.security",  # Optional, uses production by default
    timeout=30,  # Optional, request timeout in seconds
    max_retries=3  # Optional, maximum number of retries
)
```

### Projects

```python
# List all projects
projects = client.projects.list()

# Search projects
projects = client.projects.list(search="my-project")

# Get a specific project
project = client.projects.get("project-uuid")

# Create a new project
project_data = {
    "name": "My Security Project",
    "description": "Project for security testing"
}
new_project = client.projects.create(project_data)

# Update a project
updated_project = client.projects.update(project_data)

# Delete a project
client.projects.delete("project-uuid")

# Get project webhook
webhook = client.projects.get_webhook("project-uuid")

# Create project webhook
webhook_data = {"url": "https://example.com/webhook"}
client.projects.create_webhook("project-uuid", webhook_data)

# Get project summary and analytics
summary = client.projects.get_summary("project-uuid")
criticality_count = client.projects.get_open_count_by_criticality("project-uuid")
score = client.projects.get_score("cvss", "project-uuid")
trend = client.projects.get_score_trend("cvss", "project-uuid")
```

### Applications

```python
# List all applications
applications = client.applications.list()

# List applications with pagination
applications = client.applications.list(page=0, count=20)

# List applications under a project
applications = client.applications.list(project_key="project-uuid")

# Search applications
applications = client.applications.list(search="web-app", importance="high")

# Get application details
app = client.applications.get("application-token")

# Create a new application
app_data = {
    "name": "My Web App",
    "url": "https://example.com",
    "project_key": "project-uuid"
}
new_app = client.applications.create(app_data)

# Update an application
updated_app = client.applications.update(app_data)

# Delete an application
client.applications.delete("application-token")

# Get domain signature
signature = client.applications.get_signature("application-token")

# Verify signature
verification = client.applications.verify_signature("application-token", signature_data)

# Application webhooks
webhook = client.applications.get_webhook("application-token")
client.applications.create_webhook("application-token", webhook_data)
client.applications.delete_webhook("application-token")

# Application analytics
summary = client.applications.get_summary("application-token")
criticality = client.applications.get_open_count_by_criticality("application-token")
score = client.applications.get_score("application-token", "cvss")
```

### Security Testing

```python
# Start a test
test_config = {"scan_type": "full", "max_duration": 3600}
test_result = client.testing.start("application-token", test_config)
result_token = test_result['result_token']

# Check test status
status = client.testing.get_status("application-token", result_token)

# Control test execution
client.testing.pause("application-token")
client.testing.resume("application-token")
client.testing.stop("application-token")

# Get test sessions
sessions = client.testing.get_sessions("application-token", page=0, count=10)

# Get all running sessions
running_sessions = client.testing.get_running_sessions()
```

### Results & Reports

```python
# Get latest test results in JSON format
results = client.results.get_json("application-token")

# Get results for a specific test session
results = client.results.get_json("application-token", "result-token")

# Download PDF report
pdf_data = client.results.get_pdf("application-token", "result-token")

# Save PDF report to file
pdf_path = client.results.download_pdf(
    "application-token", 
    "result-token", 
    output_path="security-report.pdf"
)
```

## Error Handling

The SDK provides comprehensive error handling with specific exception types:

```python
from beagle_sdk import (
    BeagleClient,
    BeagleAPIError,
    BeagleAuthenticationError,
    BeagleValidationError,
    BeagleNotFoundError,
    BeagleRateLimitError
)

client = BeagleClient(api_key="your-api-key")

try:
    projects = client.projects.list()
except BeagleAuthenticationError:
    print("Invalid API key or authentication failed")
except BeagleRateLimitError:
    print("Rate limit exceeded, please wait before retrying")
except BeagleNotFoundError:
    print("Resource not found")
except BeagleValidationError as e:
    print(f"Validation error: {e}")
except BeagleAPIError as e:
    print(f"API error: {e}")
```

## Configuration

### Environment Variables

You can set your API key using environment variables:

```bash
export BEAGLE_API_KEY="your-api-key"
```

```python
import os
from beagle_sdk import BeagleClient

# API key will be read from BEAGLE_API_KEY environment variable
client = BeagleClient(api_key=os.getenv('BEAGLE_API_KEY'))
```

### Timeouts and Retries

```python
client = BeagleClient(
    api_key="your-api-key",
    timeout=60,  # 60 second timeout
    max_retries=5  # Retry up to 5 times
)
```

## Development

### Setting up for development

```bash
# Clone the repository
git clone https://github.com/beagle-security/beagle-python-sdk
cd beagle-python-sdk

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
flake8 beagle_sdk/
black --check beagle_sdk/

# Type checking
mypy beagle_sdk/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=beagle_sdk --cov-report=html

# Run specific test file
pytest tests/test_client.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 Email: support@beagle.security
- 📖 Documentation: https://docs.beagle.security
- 🐛 Issues: https://github.com/beagle-security/beagle-python-sdk/issues

## Changelog

### v1.0.0 (2024-01-XX)
- Initial release
- Full Beagle v3 API support
- Comprehensive error handling
- Production-ready features
