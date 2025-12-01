# Unit Testing Guidelines

## Overview

Unit testing in UniERP focuses on testing individual components, methods, and business logic in isolation. This ensures that each part of the system works correctly before integration with other components.

## Testing Framework Setup

### Base Test Classes

UniERP uses Odoo's built-in testing framework with these base classes:

```python
from odoo.tests import common, tagged

# TransactionCase - Each test runs in its own transaction
class TestMyModel(common.TransactionCase):
    def setUp(self):
        super().setUp()
        # Setup test data
    
    def test_method(self):
        # Test implementation
        pass

# SingleTransactionCase - All tests share one transaction
class TestMyModelSingle(common.SingleTransactionCase):
    def setUpClass(cls):
        super().setUpClass()
        # Setup shared data
```

### Test Configuration

```python
# Test tags for categorization
@common.tagged('standard')  # Standard tests
@common.tagged('slow')      # Performance tests
@common.tagged('external')   # Tests requiring external services

# Test with specific user
@common.users('base.user_admin')
def test_admin_functionality(self):
    # Test as admin user
    pass

# No retry for flaky tests
@common.no_retry
def test_network_operation(self):
    # Network-dependent test
    pass
```

## Best Practices and Naming Conventions

### File Organization

```
addons/my_module/
├── tests/
│   ├── __init__.py          # Test imports
│   ├── common.py            # Shared test utilities
│   ├── test_models.py       # Model tests
│   ├── test_methods.py      # Method tests
│   └── test_business_logic.py  # Business logic tests
```

### Naming Conventions

```python
# Test class names
class TestResPartner(common.TransactionCase):  # Test + ModelName
class TestInvoiceLine(common.TransactionCase):  # Test + ModelName

# Test method names
def test_create_partner_valid_data(self):  # test_action_condition
def test_create_partner_missing_name_raises_error(self):  # test_action_condition_expected_result
def test_compute_total_amount(self):  # test_compute_field_name
def test_onchange_partner_id(self):  # test_onchange_field_name
```

### Test Structure (Arrange-Act-Assert)

```python
def test_create_invoice_with_valid_data(self):
    """Test creating invoice with valid data."""
    # Arrange
    invoice_data = {
        'partner_id': self.partner_a.id,
        'invoice_line_ids': [
            (0, 0, {
                'product_id': self.product_a.id,
                'quantity': 2.0,
                'price_unit': 100.0,
            })
        ]
    }
    
    # Act
    invoice = self.env['account.move'].create(invoice_data)
    
    # Assert
    self.assertEqual(invoice.state, 'draft')
    self.assertEqual(len(invoice.invoice_line_ids), 1)
    self.assertEqual(invoice.amount_total, 200.0)
```

## Sample Test Cases and Code Examples

### Model Testing

```python
# addons/account/tests/test_invoice.py
from odoo.tests import common, tagged
from odoo.exceptions import ValidationError

@common.tagged('standard')
class TestAccountMove(common.TransactionCase):
    
    def setUp(self):
        super().setUp()
        # Create test data
        self.partner_a = self.env['res.partner'].create({
            'name': 'Test Partner A',
            'email': 'test@example.com',
        })
        self.product_a = self.env['product.product'].create({
            'name': 'Test Product A',
            'list_price': 100.0,
        })
    
    def test_create_invoice_basic(self):
        """Test basic invoice creation."""
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_a.id,
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.product_a.id,
                    'quantity': 1.0,
                    'price_unit': 100.0,
                })
            ]
        })
        
        self.assertEqual(invoice.state, 'draft')
        self.assertEqual(invoice.partner_id, self.partner_a)
        self.assertEqual(len(invoice.invoice_line_ids), 1)
    
    def test_invoice_amount_computation(self):
        """Test invoice amount computation."""
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_a.id,
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.product_a.id,
                    'quantity': 2.0,
                    'price_unit': 50.0,
                })
            ]
        })
        
        # Trigger computation
        invoice._compute_amount()
        
        self.assertEqual(invoice.amount_untaxed, 100.0)
        self.assertEqual(invoice.amount_tax, 0.0)
        self.assertEqual(invoice.amount_total, 100.0)
    
    def test_create_invoice_without_partner_raises_error(self):
        """Test that creating invoice without partner raises error."""
        with self.assertRaises(ValidationError):
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                # Missing partner_id
                'invoice_line_ids': []
            })
```

### Method Testing

```python
# addons/sale/tests/test_sale_order.py
@common.tagged('standard')
class TestSaleOrderMethods(common.TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })
    
    def test_action_confirm(self):
        """Test order confirmation action."""
        # Initial state
        self.assertEqual(self.order.state, 'draft')
        
        # Confirm order
        self.order.action_confirm()
        
        # Verify state change
        self.assertEqual(self.order.state, 'sale')
        self.assertTrue(self.order.date_order)
    
    def test_compute_amount_total(self):
        """Test total amount computation."""
        # Add order lines
        self.order.write({
            'order_line': [
                (0, 0, {
                    'product_id': self.product_a.id,
                    'product_uom_qty': 2,
                    'price_unit': 100.0,
                }),
                (0, 0, {
                    'product_id': self.product_b.id,
                    'product_uom_qty': 1,
                    'price_unit': 50.0,
                })
            ]
        })
        
        # Trigger computation
        self.order._compute_amount_total()
        
        self.assertEqual(self.order.amount_total, 250.0)
    
    def test_onchange_partner_id(self):
        """Test onchange partner_id updates fiscal position."""
        # Create partner with fiscal position
        partner_fp = self.env['res.partner'].create({
            'name': 'Partner with FP',
            'property_account_position_id': self.fiscal_position.id,
        })
        
        # Trigger onchange
        result = self.order.onchange_partner_id(partner_fp.id)
        
        self.assertEqual(
            result['value']['fiscal_position_id'],
            self.fiscal_position.id
        )
```

### Business Logic Testing

```python
# addons/stock/tests/test_inventory.py
@common.tagged('standard')
class TestInventoryLogic(common.TransactionCase):
    
    def test_inventory_valuation_computation(self):
        """Test inventory valuation computation."""
        # Create products with different costing methods
        product_fifo = self.env['product.product'].create({
            'name': 'FIFO Product',
            'cost_method': 'fifo',
            'standard_price': 100.0,
        })
        
        product_average = self.env['product.product'].create({
            'name': 'Average Product',
            'cost_method': 'average',
            'standard_price': 100.0,
        })
        
        # Receive inventory
        self.env['stock.picking'].create({
            'picking_type_id': self.picking_type_in.id,
            'move_ids': [
                (0, 0, {
                    'product_id': product_fifo.id,
                    'product_uom_qty': 10,
                    'price_unit': 80.0,
                }),
                (0, 0, {
                    'product_id': product_average.id,
                    'product_uom_qty': 10,
                    'price_unit': 120.0,
                })
            ]
        }).button_validate()
        
        # Check valuation
        self.assertEqual(product_fifo.standard_price, 80.0)
        self.assertEqual(product_average.standard_price, 120.0)
    
    def test_reservation_logic(self):
        """Test stock reservation logic."""
        # Create product with limited stock
        product = self.env['product.product'].create({
            'name': 'Limited Product',
            'type': 'product',
            'qty_available': 5.0,
        })
        
        # Create sale order for 3 units
        order1 = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [
                (0, 0, {
                    'product_id': product.id,
                    'product_uom_qty': 3.0,
                })
            ]
        })
        order1.action_confirm()
        
        # Create sale order for 4 units (should fail)
        order2 = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [
                (0, 0, {
                    'product_id': product.id,
                    'product_uom_qty': 4.0,
                })
            ]
        })
        
        # First order should reserve 3 units
        self.assertEqual(product.virtual_available, 2.0)
        
        # Second order should not have enough stock
        order2.action_confirm()
        self.assertEqual(order2.state, 'sale')
        self.assertEqual(product.virtual_available, -2.0)  # Over-reserved
```

## Test Data Management Strategies

### Fixtures

```python
# addons/my_module/tests/common.py
from odoo.tests import common
from odoo import new_test_user

class TestCommon(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Create test users
        cls.user_admin = new_test_user(
            cls.env, 'test_admin', 
            'base.group_user,base.group_partner_manager'
        )
        cls.user_demo = new_test_user(
            cls.env, 'test_demo', 
            'base.group_user'
        )
        
        # Create common test data
        cls.partner_customer = cls.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'customer@test.com',
            'customer_rank': 1,
        })
        cls.partner_supplier = cls.env['res.partner'].create({
            'name': 'Test Supplier',
            'email': 'supplier@test.com',
            'supplier_rank': 1,
        })
        
        # Create test products
        cls.product_service = cls.env['product.product'].create({
            'name': 'Test Service',
            'type': 'service',
            'list_price': 100.0,
        })
        cls.product_storable = cls.env['product.product'].create({
            'name': 'Test Storable',
            'type': 'product',
            'list_price': 50.0,
        })
    
    def setUp(self):
        super().setUp()
        # Reset environment for each test
        self.env.clear()
```

### Data Factories

```python
# addons/my_module/tests/factories.py
class PartnerFactory:
    @staticmethod
    def create(env, **kwargs):
        defaults = {
            'name': 'Test Partner',
            'email': 'test@example.com',
            'is_company': False,
        }
        defaults.update(kwargs)
        return env['res.partner'].create(defaults)

class ProductFactory:
    @staticmethod
    def create(env, **kwargs):
        defaults = {
            'name': 'Test Product',
            'type': 'product',
            'list_price': 100.0,
            'standard_price': 80.0,
        }
        defaults.update(kwargs)
        return env['product.product'].create(defaults)

# Usage in tests
def test_with_factory(self):
    partner = PartnerFactory.create(self.env, name='Custom Partner')
    product = ProductFactory.create(self.env, list_price=200.0)
```

### Mocking External Dependencies

```python
from unittest.mock import patch, MagicMock
from odoo.tests import common

@common.tagged('standard')
class TestExternalIntegration(common.TransactionCase):
    
    @patch('requests.post')
    def test_api_call_success(self, mock_post):
        """Test successful API call with mocked response."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'success'}
        mock_post.return_value = mock_response
        
        # Call method that uses requests.post
        result = self.env['my.model'].call_external_api({'data': 'test'})
        
        # Verify API was called
        mock_post.assert_called_once_with(
            'https://api.example.com/endpoint',
            json={'data': 'test'},
            headers={'Content-Type': 'application/json'}
        )
        
        # Verify result processing
        self.assertTrue(result)
    
    @patch('odoo.addons.my_module.models.time.time')
    def test_time_dependent_method(self, mock_time):
        """Test method with time dependency."""
        mock_time.return_value = 1609459200  # Fixed timestamp
        
        result = self.env['my.model'].get_time_based_value()
        
        self.assertEqual(result, '2021-01-01')
```

## Coverage Requirements and Reporting

### Coverage Targets

| Component Type | Minimum Coverage | Target Coverage |
|----------------|------------------|-----------------|
| Core Models | 85% | 95% |
| Business Logic | 90% | 98% |
| API Methods | 95% | 100% |
| Utility Functions | 80% | 90% |
| New Features | 95% | 100% |

### Running Coverage Reports

```bash
# Generate HTML coverage report
python3 -m pytest tests/ --cov=odoo --cov-report=html --cov-report=term

# Generate XML coverage for CI
python3 -m pytest tests/ --cov=odoo --cov-report=xml

# Coverage for specific module
python3 -m pytest addons/my_module/tests/ --cov=addons/my_module --cov-report=html
```

### Coverage Configuration

```ini
# .coveragerc
[run]
source = odoo
omit = 
    */tests/*
    */migrations/*
    */__pycache__/*
    */venv/*
    setup.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError

[html]
directory = htmlcov
```

## Running Unit Tests

### Command Line

```bash
# Run all unit tests
./unierp-bin -d test_db --test-enable --test-tags "+standard" --stop-after-init

# Run specific module tests
./unierp-bin -d test_db --test-enable --test-tags "TestAccountMove" --stop-after-init

# Run tests with coverage
python3 -m pytest addons/my_module/tests/ --cov=addons/my_module --cov-report=html

# Run tests with verbose output
./unierp-bin -d test_db --test-enable --test-tags "+standard" --stop-after-init --log-level=debug
```

### Within IDE

```python
# Run single test file
python3 -m pytest addons/my_module/tests/test_models.py -v

# Run specific test method
python3 -m pytest addons/my_module/tests/test_models.py::TestAccountMove::test_create_invoice -v

# Run with debugging
python3 -m pytest addons/my_module/tests/test_models.py -v -s --pdb
```

## Common Pitfalls and Solutions

### Database Transaction Issues

```python
# Problem: Test data persists between tests
def test_a(self):
    self.env['my.model'].create({'name': 'Test A'})

def test_b(self):
    # Test A's data is still here!
    records = self.env['my.model'].search([])
    self.assertEqual(len(records), 1)  # Fails!

# Solution: Use TransactionCase
class TestMyModel(common.TransactionCase):
    # Each test runs in separate transaction
    def test_a(self):
        self.env['my.model'].create({'name': 'Test A'})
    
    def test_b(self):
        # Clean environment
        records = self.env['my.model'].search([])
        self.assertEqual(len(records), 0)  # Passes!
```

### Test Data Conflicts

```python
# Problem: Tests interfere with each other
def test_create_record(self):
    record = self.env['my.model'].create({'name': 'Test'})
    # Record ID might vary between runs

# Solution: Use deterministic data
def test_create_record(self):
    record = self.env['my.model'].create({
        'name': f'Test_{self.id}',  # Unique per test
        'code': 'TEST001',  # Fixed code
    })
    self.assertEqual(record.code, 'TEST001')
```

### Performance Issues

```python
# Problem: Tests are slow due to large datasets
def test_large_dataset(self):
    # Creating 1000 records in test
    for i in range(1000):
        self.env['my.model'].create({'name': f'Record {i}'})

# Solution: Use smaller datasets or mock
@common.tagged('slow')  # Mark as slow test
def test_large_dataset(self):
    # Use realistic but smaller datasets
    for i in range(10):  # Still tests logic
        self.env['my.model'].create({'name': f'Record {i}'})
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
# .github/workflows/unit-tests.yml
name: Unit Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run unit tests
      run: |
        ./unierp-bin -d test_db --test-enable --test-tags "+standard" --stop-after-init
    
    - name: Generate coverage report
      run: |
        python3 -m pytest tests/ --cov=odoo --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

*For specific testing methodologies, see: [Integration Testing](../integration-testing/README.md), [Functional Testing](../functional-testing/README.md), [Performance Testing](../performance-testing/README.md), [Security Testing](../security-testing/README.md)*