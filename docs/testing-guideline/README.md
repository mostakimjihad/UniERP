# UniERP Testing Guidelines

## Overview

This comprehensive testing guideline provides structured approaches for testing UniERP, an enterprise resource planning system built on Odoo 19 Community Edition. The guidelines cover all aspects of testing from unit tests to security assessments, ensuring high-quality, reliable software delivery.

## Testing Strategy

UniERP follows a multi-layered testing approach:

1. **Unit Testing**: Test individual components, methods, and business logic
2. **Integration Testing**: Verify module interactions and database operations
3. **Functional Testing**: Validate UI workflows and end-to-end scenarios
4. **Performance Testing**: Ensure system performs under load
5. **Security Testing**: Identify and mitigate vulnerabilities

## Quick Start Guide

### For New Developers

1. **Set up test environment**:
   ```bash
   # Create test database
   createdb unierp_test -O unierp
   
   # Install dependencies
   pip3 install -r requirements.txt
   ```

2. **Run all tests**:
   ```bash
   ./unierp-bin -d unierp_test --test-enable --stop-after-init
   ```

3. **Run specific module tests**:
   ```bash
   ./unierp-bin -d unierp_test --test-enable --test-tags TestModuleName --stop-after-init
   ```

4. **Run with coverage**:
   ```bash
   python3 -m pytest tests/ --cov=odoo --cov-report=html
   ```

### Test Execution Commands

| Purpose | Command | Description |
|---------|----------|-------------|
| Run all tests | `./unierp-bin -d test_db --test-enable --stop-after-init` | Execute entire test suite |
| Run specific tests | `./unierp-bin -d test_db --test-tags "+standard" --stop-after-init` | Run standard test suite |
| Run module tests | `./unierp-bin -d test_db --test-enable -i module_name --stop-after-init` | Test specific module |
| Run with coverage | `python3 -m pytest tests/ --cov=odoo --cov-report=html` | Generate coverage report |
| Run performance tests | `python3 -m pytest tests/performance/ --benchmark-only` | Execute performance benchmarks |

## Testing Framework

UniERP uses **Odoo's built-in testing framework** based on Python's unittest module with Odoo-specific extensions:

- **Base Classes**: `odoo.tests.common.TransactionCase`, `odoo.tests.common.SingleTransactionCase`
- **Test Discovery**: Automatic discovery in `addons/*/tests/` directories
- **Test Tags**: Categorize and filter tests (`+standard`, `-slow`, `:TestClass.test_method`)
- **Database Transactions**: Each test runs in isolated transaction
- **Fixtures**: Common test setup utilities

## Documentation Structure

```
docs/testing-guideline/
├── README.md                          # This file - overview and quick start
├── unit-testing/                      # Unit testing methodology and examples
├── integration-testing/                 # Integration testing approach
├── functional-testing/                  # UI and end-to-end testing
├── performance-testing/                 # Load testing and optimization
├── security-testing/                   # Security assessment procedures
└── ci-cd-integration/                 # CI/CD pipeline configuration
```

## Testing Best Practices

### General Guidelines

1. **Test Isolation**: Each test should be independent and not rely on other tests
2. **Descriptive Names**: Use clear, descriptive test method names
3. **Arrange-Act-Assert**: Structure tests with clear setup, execution, and verification
4. **Test Coverage**: Maintain minimum 80% line coverage
5. **Test Data**: Use fixtures for consistent test data
6. **Error Testing**: Test both positive and negative scenarios

### Code Quality

- Follow PEP 8 coding standards
- Use meaningful variable names
- Add docstrings for test methods
- Keep tests simple and focused
- Avoid test logic duplication

## Troubleshooting Common Issues

### Database Connection Issues

**Problem**: Tests fail to connect to database
```bash
# Solution: Check database configuration
psql -h localhost -U unierp -d unierp_test -c "SELECT 1;"
```

**Problem**: Permission denied errors
```bash
# Solution: Grant proper permissions
sudo -u postgres psql -c "ALTER USER unierp CREATEDB;"
```

### Test Discovery Issues

**Problem**: Tests not being discovered
```bash
# Solution: Check file structure
find addons/ -name "test_*.py" -o -name "tests" -type d
```

**Problem**: Import errors in tests
```python
# Solution: Ensure proper imports
from odoo.tests import common, tagged
from odoo.exceptions import ValidationError
```

### Performance Issues

**Problem**: Tests running slowly
```bash
# Solution: Run with specific tags
./unierp-bin -d test_db --test-tags "+standard,-slow" --stop-after-init
```

**Problem**: Memory issues during testing
```bash
# Solution: Limit test parallelization
./unierp-bin -d test_db --test-enable --workers 0 --stop-after-init
```

## Coverage Requirements

- **Minimum Coverage**: 80% line coverage for all modules
- **Critical Modules**: 90% coverage required
- **New Features**: 95% coverage before merge
- **Coverage Reports**: Generated automatically in CI/CD

## Test Categories

### Standard Tests (`+standard`)
- Basic functionality tests
- Model validation tests
- API endpoint tests
- Form processing tests

### Slow Tests (`+slow`)
- Performance benchmarks
- Large dataset tests
- Integration tests with external systems
- End-to-end workflows

### External Tests (`+external`)
- Third-party integration tests
- Web service tests
- Email sending tests
- Payment gateway tests

## Links to Documentation Sections

- [Unit Testing](unit-testing/README.md) - Component-level testing
- [Integration Testing](integration-testing/README.md) - Module interaction testing
- [Functional Testing](functional-testing/README.md) - UI and workflow testing
- [Performance Testing](performance-testing/README.md) - Load and optimization testing
- [Security Testing](security-testing/README.md) - Vulnerability assessment
- [CI/CD Integration](ci-cd-integration/README.md) - Automated testing pipelines

## Getting Help

### Internal Resources
- **Documentation**: [UniERP Developer Portal](https://docs.uslbd.com)
- **Issue Tracking**: [GitHub Issues](https://github.com/unisoft/unierp/issues)
- **Team Chat**: [Internal Slack](#testing-channel)

### External Resources
- **Odoo Testing Guide**: [Official Documentation](https://www.odoo.com/documentation/master/developer/misc/test.html)
- **Python Testing**: [pytest documentation](https://docs.pytest.org/)
- **Best Practices**: [Testing Best Practices](https://docs.python.org/3/library/unittest.html)

## Contributing to Testing Guidelines

To contribute improvements to these testing guidelines:

1. Fork the repository
2. Create feature branch: `git checkout -b improve-testing-docs`
3. Make your changes
4. Add tests for your changes
5. Submit pull request with description

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-25 | Initial comprehensive testing guidelines |

---

*This testing guideline is maintained by the UniSoft Systems Ltd. development team. For questions or suggestions, contact dev@unisoft.com.bd*