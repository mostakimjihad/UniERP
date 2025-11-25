# CI/CD Pipeline Integration

## Overview

This document provides comprehensive CI/CD pipeline integration for UniERP testing, covering automated testing workflows, multi-environment strategies, parallel execution, and Docker containerization for consistent test environments.

## GitHub Actions Workflow Files

### Main CI/CD Pipeline

```yaml
# .github/workflows/ci-cd.yml
name: UniERP CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  release:
    types: [ published ]

env:
  PYTHON_VERSION: '3.10'
  NODE_VERSION: '18'
  POSTGRES_VERSION: '14'

jobs:
  # Code Quality Checks
  code-quality:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install flake8 pylint black isort pytest-cov
    
    - name: Run linting
      run: |
        flake8 odoo/ addons/ --max-line-length=120 --format=json > flake8-report.json
        pylint odoo/ --output=json:pylint_report.json || true
        black --check odoo/ addons/
        isort --check-only odoo/ addons/
    
    - name: Upload linting results
      uses: actions/upload-artifact@v3
      with:
        name: linting-reports
        path: |
          flake8-report.json
          pylint_report.json

  # Unit Tests
  unit-tests:
    name: Unit Tests
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:${{ env.POSTGRES_VERSION }}
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: unierp
          POSTGRES_DB: unierp_test
          POSTGRES_DB_HOST: localhost
          POSTGRES_DB_PORT: 5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-xdist
    
    - name: Run unit tests
      run: |
        ./unierp-bin -d unierp_test --test-enable --test-tags "+standard" --stop-after-init
    
    - name: Run tests with coverage
      run: |
        python3 -m pytest addons/*/tests/ \
          --cov=odoo \
          --cov-report=xml \
          --cov-report=html \
          --cov-report=term \
          --junitxml=pytest-results.xml
    
    - name: Upload coverage reports
      uses: actions/upload-artifact@v3
      with:
        name: coverage-reports
        path: |
          htmlcov/
          coverage.xml
          pytest-results.xml
    
    - name: Upload to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  # Integration Tests
  integration-tests:
    name: Integration Tests
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:${{ env.POSTGRES_VERSION }}
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: unierp
          POSTGRES_DB: unierp_integration_test
          POSTGRES_DB_HOST: localhost
          POSTGRES_DB_PORT: 5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run integration tests
      run: |
        ./unierp-bin -d unierp_integration_test \
          --test-enable \
          --test-tags "+integration" \
          --stop-after-init
    
    - name: Generate integration report
      run: |
        python3 -m pytest addons/*/tests/integration/ \
          --cov=odoo \
          --cov-report=xml \
          --junitxml=integration-results.xml
    
    - name: Upload integration results
      uses: actions/upload-artifact@v3
      with:
        name: integration-reports
        path: |
          integration-results.xml

  # Performance Tests
  performance-tests:
    name: Performance Tests
    runs-on: ubuntu-latest
    if: github.event_name == 'schedule' || contains(github.event.head_ref, 'performance')
    
    services:
      postgres:
        image: postgres:${{ env.POSTGRES_VERSION }}
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: unierp
          POSTGRES_DB: unierp_perf_test
          POSTGRES_DB_HOST: localhost
          POSTGRES_DB_PORT: 5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov locust
    
    - name: Run performance tests
      run: |
        ./unierp-bin -d unierp_perf_test \
          --test-enable \
          --test-tags "+performance" \
          --stop-after-init
    
    - name: Run load tests
      run: |
        locust -f tests/performance/locustfile.py \
          --host=http://localhost:8069 \
          --users=50 \
          --spawn-rate=5 \
          --run-time=60s \
          --html=performance-report.html
    
    - name: Upload performance results
      uses: actions/upload-artifact@v3
      with:
        name: performance-reports
        path: |
          performance-report.html

  # Security Tests
  security-tests:
    name: Security Tests
    runs-on: ubuntu-latest
    if: github.event_name == 'schedule' || contains(github.event.head_ref, 'security')
    
    services:
      postgres:
        image: postgres:${{ env.POSTGRES_VERSION }}
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: unierp
          POSTGRES_DB: unierp_security_test
          POSTGRES_DB_HOST: localhost
          POSTGRES_DB_PORT: 5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov bandit safety
    
    - name: Run security tests
      run: |
        ./unierp-bin -d unierp_security_test \
          --test-enable \
          --test-tags "+security" \
          --stop-after-init
    
    - name: Run security scan
      run: |
        bandit -r odoo/ -f json -o bandit-report.json
        safety check --json --output safety-report.json
    
    - name: Upload security results
      uses: actions/upload-artifact@v3
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json

  # Build and Deploy
  build-and-deploy:
    name: Build and Deploy
    runs-on: ubuntu-latest
    needs: [code-quality, unit-tests, integration-tests]
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Install build dependencies
      run: |
        pip install -r requirements.txt
        pip install buildozer twine
    
    - name: Build package
      run: |
        python3 setup.py sdist bdist_wheel
        buildozer --inspect
    
    - name: Deploy to staging
      run: |
        # Deploy to staging environment
        echo "Deploying to staging..."
        # Add deployment commands here
    
    - name: Run smoke tests
      run: |
        # Run smoke tests on staging
        ./scripts/run-smoke-tests.sh
```

### Parallel Testing Configuration

```yaml
# .github/workflows/parallel-tests.yml
name: Parallel Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  # Split tests into parallel jobs
  test-suite-1:
    name: Test Suite 1
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: unierp
          POSTGRES_DB: unierp_test_1
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run test subset 1
      run: |
        python3 -m pytest addons/*/tests/ \
          --cov=odoo \
          --cov-report=xml \
          --junitxml=test-results-1.xml \
          -k "test_account or test_sale or test_stock"
    
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: test-results-1
        path: test-results-1.xml

  test-suite-2:
    name: Test Suite 2
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: unierp
          POSTGRES_DB: unierp_test_2
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run test subset 2
      run: |
        python3 -m pytest addons/*/tests/ \
          --cov=odoo \
          --cov-report=xml \
          --junitxml=test-results-2.xml \
          -k "test_purchase or test_hr or test_project"
    
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: test-results-2
        path: test-results-2.xml

  # Merge results
  merge-results:
    name: Merge Test Results
    needs: [test-suite-1, test-suite-2]
    runs-on: ubuntu-latest
    
    steps:
    - name: Download all results
      uses: actions/download-artifact@v3
      with:
        path: test-results
        merge-multiple: true
    
    - name: Merge and upload
      run: |
        # Merge XML results
        python3 scripts/merge-test-results.py
    
    - name: Upload merged results
      uses: actions/upload-artifact@v3
      with:
        name: merged-test-results
        path: merged-test-results.xml
```

## Multi-Environment Testing Strategies

### Environment Configuration

```yaml
# .github/workflows/multi-environment.yml
name: Multi-Environment Testing

on:
  push:
    branches: [ main, develop, staging ]
  pull_request:
    branches: [ main ]

jobs:
  # Development environment tests
  test-development:
    name: Development Tests
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: ${{ secrets.DEV_DB_PASSWORD }}
          POSTGRES_USER: ${{ secrets.DEV_DB_USER }}
          POSTGRES_DB: ${{ secrets.DEV_DB_NAME }}
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up development environment
      run: |
        echo "Setting up development environment"
        # Development-specific setup
    
    - name: Run development tests
      run: |
        ./unierp-bin -d ${{ secrets.DEV_DB_NAME }} \
          --test-enable \
          --test-tags "+standard,+integration" \
          --stop-after-init

  # Staging environment tests
  test-staging:
    name: Staging Tests
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/staging'
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: ${{ secrets.STAGING_DB_PASSWORD }}
          POSTGRES_USER: ${{ secrets.STAGING_DB_USER }}
          POSTGRES_DB: ${{ secrets.STAGING_DB_NAME }}
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Deploy to staging
      run: |
        echo "Deploying to staging environment"
        # Deployment commands
    
    - name: Run staging tests
      run: |
        ./unierp-bin -d ${{ secrets.STAGING_DB_NAME }} \
          --test-enable \
          --test-tags "+functional,+end-to-end" \
          --stop-after-init
    
    - name: Run smoke tests
      run: |
        ./scripts/run-staging-smoke-tests.sh

  # Production environment tests
  test-production:
    name: Production Tests
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: ${{ secrets.PROD_DB_PASSWORD }}
          POSTGRES_USER: ${{ secrets.PROD_DB_USER }}
          POSTGRES_DB: ${{ secrets.PROD_DB_NAME }}
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Deploy to production
      run: |
        echo "Deploying to production environment"
        # Production deployment commands
    
    - name: Run production smoke tests
      run: |
        ./scripts/run-production-smoke-tests.sh
```

## Docker Containerization

### Dockerfile for Testing

```dockerfile
# Dockerfile.test
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    libldap2-dev \
    libsasl2-dev \
    libjpeg-dev \
    libpq-dev \
    libtiff5-dev \
    libwebp-dev \
    zlib1-dev \
    libffi-dev \
    libssl-dev \
    nodejs \
    npm

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir /tmp/ -r /tmp/requirements.txt

# Install Node.js dependencies
RUN npm install -g less less-plugin-clean-css

# Copy UniERP source code
COPY . /opt/unierp/
WORKDIR /opt/unierp/

# Create unierp user
RUN useradd --system --group unierp unierp || true
RUN chown -R unierp:unierp /opt/unierp

# Set entrypoint
ENTRYPOINT ["./unierp-bin"]
CMD ["-d", "unierp_test", "--test-enable", "--stop-after-init"]
```

### Docker Compose for Testing

```yaml
# docker-compose.test.yml
version: '3.8'

services:
  unierp-test:
    build:
      context: .
      dockerfile: Dockerfile.test
    container_name: unierp-test
    ports:
      - "8069:8069"
      - "8072:8072"
    environment:
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_USER=unierp
      - POSTGRES_PASSWORD=unierp
      - POSTGRES_DB=unierp_test
    depends_on:
      - postgres-test
    volumes:
      - ./addons:/opt/unierp/addons
      - ./odoo:/opt/unierp/odoo
      - unierp-test-data:/opt/unierp/filestore
    networks:
      - unierp-test-network

  postgres-test:
    image: postgres:14
    container_name: postgres-test
    environment:
      - POSTGRES_USER=unierp
      - POSTGRES_PASSWORD=unierp
      - POSTGRES_DB=unierp_test
      - POSTGRES_INITDB_ARGS=--encoding=UTF-8 --lc-collate=C
    volumes:
      - postgres-test-data:/var/lib/postgresql/data
    networks:
      - unierp-test-network

  # Additional services for testing
  redis-test:
    image: redis:7
    container_name: redis-test
    ports:
      - "6379:6379"
    networks:
      - unierp-test-network

  elasticsearch-test:
    image: elasticsearch:8.8.0
    container_name: elasticsearch-test
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    networks:
      - unierp-test-network
```

### Test Scripts

```bash
#!/bin/bash
# scripts/run-docker-tests.sh
set -e

echo "Starting UniERP tests in Docker..."

# Build and start containers
docker-compose -f docker-compose.test.yml up -d --build

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

# Run database initialization
echo "Initializing test database..."
docker-compose exec unierp-test ./unierp-bin -d unierp_test -i base --without-demo=all --stop-after-init

# Run tests
echo "Running tests..."
docker-compose exec unierp-test ./unierp-bin -d unierp_test --test-enable --test-tags "+standard" --stop-after-init

# Collect test results
echo "Collecting test results..."
docker-compose cp unierp-test:/opt/unierp/test-results ./test-results

# Cleanup
echo "Cleaning up..."
docker-compose -f docker-compose.test.yml down -v

echo "Tests completed!"
```

## Database Initialization and Cleanup

### Database Setup Script

```bash
#!/bin/bash
# scripts/setup-test-database.sh
set -e

DB_NAME=${1:-"unierp_test"}
DB_USER=${2:-"unierp"}
DB_PASSWORD=${3:-"unierp"}

echo "Setting up test database: $DB_NAME"

# Create database user if not exists
sudo -u postgres psql -c "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER';" || \
    sudo -u postgres createuser --createdb --pwprompt $DB_USER

# Create database
sudo -u postgres createdb -O $DB_USER $DB_NAME

# Install extensions
sudo -u postgres psql -d $DB_NAME -c "
    CREATE EXTENSION IF NOT EXISTS \"pg_stat_statements\";
    CREATE EXTENSION IF NOT EXISTS \"pg_stat_activity\";
"

echo "Database setup completed!"
```

### Database Cleanup Script

```bash
#!/bin/bash
# scripts/cleanup-test-database.sh
set -e

DB_NAME=${1:-"unierp_test"}

echo "Cleaning up test database: $DB_NAME"

# Drop database
sudo -u postgres dropdb --if-exists $DB_NAME

echo "Database cleanup completed!"
```

## Test Result Reporting and Notification

### Test Result Processing

```python
# scripts/process-test-results.py
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

class TestResultProcessor:
    """Process and analyze test results."""
    
    def __init__(self, results_dir):
        self.results_dir = results_dir
        self.results = []
    
    def process_junit_results(self):
        """Process JUnit XML results."""
        for filename in os.listdir(self.results_dir):
            if filename.endswith('.xml'):
                filepath = os.path.join(self.results_dir, filename)
                tree = ET.parse(filepath)
                root = tree.getroot()
                
                for testcase in root.findall('.//testcase'):
                    result = {
                        'name': testcase.get('name'),
                        'classname': testcase.get('classname'),
                        'time': float(testcase.get('time', 0)),
                        'failure': None,
                    }
                    
                    failure = testcase.find('failure')
                    if failure is not None:
                        result['failure'] = {
                            'message': failure.get('message'),
                            'type': failure.get('type'),
                        }
                    
                    self.results.append(result)
    
    def generate_summary(self):
        """Generate test summary."""
        total_tests = len(self.results)
        failed_tests = len([r for r in self.results if r['failure']])
        passed_tests = total_tests - failed_tests
        
        total_time = sum(r['time'] for r in self.results)
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': passed_tests / total_tests if total_tests > 0 else 0,
            'total_time': total_time,
            'average_time': total_time / total_tests if total_tests > 0 else 0,
        }
        
        return summary
    
    def save_summary(self, output_file):
        """Save summary to file."""
        summary = self.generate_summary()
        
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Test summary saved to {output_file}")

# Usage
if __name__ == '__main__':
    processor = TestResultProcessor('test-results')
    processor.process_junit_results()
    summary = processor.generate_summary()
    processor.save_summary('test-summary.json')
```

### Notification Configuration

```yaml
# .github/workflows/notifications.yml
name: Test Notifications

on:
  workflow_run:
    workflows: ["ci-cd.yml"]
  workflow_conclusion:
    types: [success, failure, neutral]

jobs:
  notify-success:
    name: Notify Success
    if: github.event_name == 'workflow_conclusion' && github.event.conclusion == 'success'
    runs-on: ubuntu-latest
    
    steps:
    - name: Send success notification
      uses: 8398a7/action-slack@v3
      with:
        status: success
        channel: '#ci-cd'
        text: |
          ✅ UniERP CI/CD Pipeline Succeeded!
          
          *Build:* ${{ github.sha }}
          *Branch:* ${{ github.ref }}
          *Author:* ${{ github.actor }}
          
          View results: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
  
  notify-failure:
    name: Notify Failure
    if: github.event_name == 'workflow_conclusion' && github.event.conclusion == 'failure'
    runs-on: ubuntu-latest
    
    steps:
    - name: Send failure notification
      uses: 8398a7/action-slack@v3
      with:
        status: failure
        channel: '#ci-cd'
        text: |
          ❌ UniERP CI/CD Pipeline Failed!
          
          *Build:* ${{ github.sha }}
          *Branch:* ${{ github.ref }}
          *Author:* ${{ github.actor }}
          *Error:* Check the logs for details
          
          View results: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

## Running CI/CD Pipeline

### Local Development

```bash
# Run full CI/CD pipeline locally
./scripts/run-local-ci.sh

# Run specific jobs
./scripts/run-local-ci.sh --job=unit-tests
./scripts/run-local-ci.sh --job=integration-tests
./scripts/run-local-ci.sh --job=security-tests
```

### Production Deployment

```bash
# Deploy to production
./scripts/deploy-production.sh

# Rollback production
./scripts/rollback-production.sh
```

## Common Pitfalls and Solutions

### Test Environment Isolation

```yaml
# Problem: Tests interfere with each other
jobs:
  test-1:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        run: ./run-tests.sh  # Modifies shared state
  
  test-2:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        run: ./run-tests.sh  # Affected by test-1

# Solution: Use isolated environments
jobs:
  test-1:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: test_db_1
    steps:
      - name: Run tests
        run: ./run-tests.sh
  
  test-2:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: test_db_2
    steps:
      - name: Run tests
        run: ./run-tests.sh
```

### Resource Optimization

```yaml
# Problem: CI/CD pipeline is slow
jobs:
  slow-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        run: ./run-all-tests.sh  # Takes 30 minutes

# Solution: Optimize with caching and parallelization
jobs:
  fast-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        test-group: [unit, integration, functional]
    steps:
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      
      - name: Run tests
        run: ./run-${{ matrix.test-group }}-tests.sh
```

### Security in CI/CD

```yaml
# Problem: Exposing secrets in logs
jobs:
  insecure-job:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests with secrets
        run: |
          echo "Running tests with ${{ secrets.DB_PASSWORD }}"  # Bad!
        ./run-tests.sh ${{ secrets.DB_PASSWORD }}

# Solution: Use secure secret handling
jobs:
  secure-job:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests securely
        run: |
          echo "Running tests..."
          ./run-tests.sh  # Secrets passed via environment
        env:
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
```

---

*For specific testing methodologies, see: [Unit Testing](../unit-testing/README.md), [Integration Testing](../integration-testing/README.md), [Functional Testing](../functional-testing/README.md), [Performance Testing](../performance-testing/README.md), [Security Testing](../security-testing/README.md)*