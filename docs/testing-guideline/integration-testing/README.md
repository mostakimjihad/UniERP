# Integration Testing Guidelines

## Overview

Integration testing in UniERP focuses on verifying that different modules, components, and systems work together correctly. This level of testing ensures that module interactions, database operations, and external integrations function as expected.

## Testing Framework Setup

### Integration Test Base Classes

```python
from odoo.tests import common, tagged
from odoo.tools import config

@common.tagged('integration')
class TestModuleIntegration(common.TransactionCase):
    """Test integration between modules."""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Setup shared integration environment
        cls.setup_integrated_modules()
    
    def setUp(self):
        super().setUp()
        # Reset environment for each test
        self.env.clear()
```

### Multi-Module Testing

```python
# Test integration between sale, stock, and account modules
@common.tagged('integration')
class TestSaleStockAccountIntegration(common.TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Install required modules
        cls.env['ir.module.module'].search([
            ('name', 'in', ['sale', 'stock', 'account'])
        ]).button_immediate_install()
```

## Best Practices and Naming Conventions

### File Organization

```
addons/my_module/tests/
├── integration/
│   ├── __init__.py
│   ├── test_sale_stock_integration.py
│   ├── test_account_integration.py
│   ├── test_api_integration.py
│   └── test_external_service_integration.py
```

### Naming Conventions

```python
# Integration test class names
class TestSaleStockIntegration(common.TransactionCase):  # Test + ModuleA + ModuleB + Integration
class TestAccountPaymentIntegration(common.TransactionCase):  # Test + ModuleA + ModuleB + Integration

# Integration test method names
def test_sale_order_creates_stock_move(self):  # test_action_creates_related_object
def test_invoice_payment_reconciliation(self):  # test_moduleA_moduleB_action
def test_external_api_order_sync(self):  # test_external_system_object_sync
```

## Sample Test Cases and Code Examples

### Module Integration Testing

```python
# addons/sale_stock/tests/integration/test_sale_stock_flow.py
from odoo.tests import common, tagged
from odoo.exceptions import UserError

@common.tagged('integration')
class TestSaleStockFlow(common.TransactionCase):
    """Test complete sale to stock flow integration."""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create test warehouse and locations
        cls.warehouse = cls.env['stock.warehouse'].create({
            'name': 'Test Warehouse',
            'code': 'TEST',
        })
        cls.location_stock = cls.warehouse.lot_stock_id
        cls.location_customer = cls.warehouse.lot_stock_id
        
        # Create test products
        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
            'type': 'product',
            'list_price': 100.0,
            'default_code': 'TEST001',
        })
        
        # Create test partner
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'customer@test.com',
        })
    
    def test_sale_order_creates_picking(self):
        """Test that confirming sale order creates stock picking."""
        # Create sale order
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [
                (0, 0, {
                    'product_id': self.product.id,
                    'product_uom_qty': 10.0,
                    'price_unit': 100.0,
                })
            ]
        })
        
        # Confirm sale order
        sale_order.action_confirm()
        
        # Verify picking was created
        pickings = self.env['stock.picking'].search([
            ('sale_id', '=', sale_order.id)
        ])
        self.assertEqual(len(pickings), 1)
        
        picking = pickings[0]
        self.assertEqual(picking.state, 'confirmed')
        self.assertEqual(picking.picking_type_id, self.warehouse.out_type_id)
    
    def test_picking_validation_updates_stock_levels(self):
        """Test that picking validation updates stock levels."""
        # Create initial stock
        self.env['stock.quant']._update_available_quantity(
            self.product, self.location_stock, 100.0
        )
        
        # Create and validate picking
        picking = self.env['stock.picking'].create({
            'picking_type_id': self.warehouse.out_type_id,
            'location_id': self.location_stock,
            'location_dest_id': self.location_customer,
            'move_ids': [
                (0, 0, {
                    'product_id': self.product.id,
                    'product_uom_qty': 20.0,
                    'location_id': self.location_stock,
                    'location_dest_id': self.location_customer,
                })
            ]
        })
        
        # Check stock before validation
        quant_before = self.env['stock.quant']._gather(self.product, self.location_stock)
        self.assertEqual(quant_before.quantity, 100.0)
        
        # Validate picking
        picking.button_validate()
        
        # Check stock after validation
        quant_after = self.env['stock.quant']._gather(self.product, self.location_stock)
        self.assertEqual(quant_after.quantity, 80.0)
    
    def test_invoice_creation_from_sale(self):
        """Test invoice creation from validated picking."""
        # Create and confirm sale order
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [
                (0, 0, {
                    'product_id': self.product.id,
                    'product_uom_qty': 5.0,
                    'price_unit': 100.0,
                })
            ]
        })
        sale_order.action_confirm()
        
        # Validate picking
        picking = sale_order.picking_ids[0]
        picking.button_validate()
        
        # Create invoice from picking
        wizard = self.env['stock.picking.backorder.confirmation'].create({
            'picking_id': picking.id,
        })
        wizard.with_context(
            button_validate_picking_ids=[picking.id]
        ).process_cancel_backorder()
        
        # Verify invoice was created
        invoices = self.env['account.move'].search([
            ('sale_order_id', '=', sale_order.id)
        ])
        self.assertEqual(len(invoices), 1)
        
        invoice = invoices[0]
        self.assertEqual(invoice.state, 'draft')
        self.assertEqual(invoice.partner_id, self.partner)
```

### Database Integration Testing

```python
# addons/base/tests/integration/test_database_integration.py
@common.tagged('integration')
class TestDatabaseIntegration(common.TransactionCase):
    """Test database-level integrations."""
    
    def test_foreign_key_constraints(self):
        """Test foreign key constraints between models."""
        # Create partner
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })
        
        # Create company with partner
        company = self.env['res.company'].create({
            'name': 'Test Company',
            'partner_id': partner.id,
        })
        
        # Try to delete partner (should fail due to FK)
        with self.assertRaises(Exception):
            partner.unlink()
        
        # Should work after deleting company
        company.unlink()
        partner.unlink()  # Should work now
    
    def test_cascade_deletion(self):
        """Test cascade deletion behavior."""
        # Create partner with contacts
        partner = self.env['res.partner'].create({
            'name': 'Test Company',
            'is_company': True,
        })
        
        contact1 = self.env['res.partner'].create({
            'name': 'Contact 1',
            'parent_id': partner.id,
        })
        contact2 = self.env['res.partner'].create({
            'name': 'Contact 2',
            'parent_id': partner.id,
        })
        
        # Delete company (should cascade delete contacts)
        partner.unlink()
        
        # Verify contacts are deleted
        remaining_contacts = self.env['res.partner'].search([
            ('parent_id', '=', partner.id)
        ])
        self.assertEqual(len(remaining_contacts), 0)
    
    def test_database_transactions_rollback(self):
        """Test transaction rollback on errors."""
        # Start with clean state
        initial_count = self.env['res.partner'].search_count([])
        
        # Create partner
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })
        
        # Verify creation
        after_create_count = self.env['res.partner'].search_count([])
        self.assertEqual(after_create_count, initial_count + 1)
        
        # Force error to test rollback
        with self.assertRaises(Exception):
            # This should rollback the entire transaction
            self.env.cr.execute("SELECT invalid_function()")
        
        # Verify rollback - partner should not exist
        after_rollback_count = self.env['res.partner'].search_count([])
        self.assertEqual(after_rollback_count, initial_count)
```

### API Integration Testing

```python
# addons/api/tests/integration/test_rest_api.py
from odoo.tests import common, tagged
from odoo.http import request
import json

@common.tagged('integration')
@common.tagged('external')
class TestRestAPIIntegration(common.TransactionCase):
    """Test REST API integration with external systems."""
    
    def setUp(self):
        super().setUp()
        # Create API user
        self.api_user = self.env['res.users'].create({
            'name': 'API User',
            'login': 'api_user',
            'password': 'api_password',
            'groups_id': [(6, 0, [self.ref('base.group_portal')])]
        })
    
    def test_api_authentication(self):
        """Test API authentication endpoint."""
        # Test authentication
        auth_response = self.url_open(
            '/api/authenticate',
            data={
                'login': 'api_user',
                'password': 'api_password',
                'db': self.env.cr.dbname
            },
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(auth_response.status_code, 200)
        auth_data = json.loads(auth_response.content)
        self.assertIn('session_id', auth_data)
    
    def test_api_create_partner(self):
        """Test creating partner via API."""
        # Authenticate first
        session_id = self._authenticate_api()
        
        # Create partner via API
        create_response = self.url_open(
            '/api/partner',
            data=json.dumps({
                'name': 'API Partner',
                'email': 'api@example.com',
                'is_company': False,
            }),
            headers={
                'Content-Type': 'application/json',
                'X-Openerp-Session-Id': session_id
            }
        )
        
        self.assertEqual(create_response.status_code, 200)
        create_data = json.loads(create_response.content)
        self.assertIn('id', create_data)
        
        # Verify partner was created in database
        partner = self.env['res.partner'].browse(create_data['id'])
        self.assertEqual(partner.name, 'API Partner')
        self.assertEqual(partner.email, 'api@example.com')
    
    def test_api_error_handling(self):
        """Test API error handling."""
        # Test invalid data
        error_response = self.url_open(
            '/api/partner',
            data=json.dumps({
                'name': '',  # Invalid empty name
                'email': 'invalid-email',  # Invalid email
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(error_response.status_code, 400)
        error_data = json.loads(error_response.content)
        self.assertIn('error', error_data)
        self.assertIn('name', error_data['error']['fields'])
    
    def _authenticate_api(self):
        """Helper method for API authentication."""
        auth_response = self.url_open(
            '/api/authenticate',
            data={
                'login': 'api_user',
                'password': 'api_password',
                'db': self.env.cr.dbname
            },
            headers={'Content-Type': 'application/json'}
        )
        auth_data = json.loads(auth_response.content)
        return auth_data.get('session_id')
```

### External Service Integration Testing

```python
# addons/payment_paypal/tests/integration/test_paypal_integration.py
from unittest.mock import patch, MagicMock
from odoo.tests import common, tagged

@common.tagged('integration')
@common.tagged('external')
class TestPayPalIntegration(common.TransactionCase):
    """Test PayPal payment gateway integration."""
    
    def setUp(self):
        super().setUp()
        self.payment_acquirer = self.env['payment.acquirer'].create({
            'name': 'PayPal',
            'provider': 'paypal',
            'paypal_email_account': 'test@example.com',
            'state': 'test',
        })
    
    @patch('requests.post')
    def test_paypal_payment_creation(self, mock_post):
        """Test PayPal payment creation flow."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 'PAY-12345',
            'state': 'approved',
        }
        mock_post.return_value = mock_response
        
        # Create payment transaction
        payment = self.env['payment.transaction'].create({
            'acquirer_id': self.payment_acquirer.id,
            'amount': 100.0,
            'currency_id': self.env.ref('base.USD'),
            'reference': 'TEST-001',
        })
        
        # Process payment
        payment.s2s_process()
        
        # Verify PayPal API was called
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[1]['url'], 'https://api.paypal.com/v1/payments/payment')
        self.assertIn('access_token', call_args[1]['data'])
        
        # Verify payment state
        self.assertEqual(payment.state, 'done')
        self.assertEqual(payment.acquirer_reference, 'PAY-12345')
    
    @patch('requests.post')
    def test_paypal_error_handling(self, mock_post):
        """Test PayPal error handling."""
        # Setup error response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'name': 'INVALID_RESOURCE',
            'message': 'Payment failed',
        }
        mock_post.return_value = mock_response
        
        # Create and process payment
        payment = self.env['payment.transaction'].create({
            'acquirer_id': self.payment_acquirer.id,
            'amount': 100.0,
            'currency_id': self.env.ref('base.USD'),
            'reference': 'TEST-002',
        })
        
        # Process payment (should handle error)
        payment.s2s_process()
        
        # Verify error handling
        self.assertEqual(payment.state, 'error')
        self.assertIn('INVALID_RESOURCE', payment.state_message)
```

## Test Data Management Strategies

### Integration Test Fixtures

```python
# addons/common/tests/integration_fixtures.py
from odoo.tests import common

class IntegrationTestCommon(common.TransactionCase):
    """Common fixtures for integration tests."""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Setup complete business scenario
        cls._setup_company_structure()
        cls._setup_products_and_categories()
        cls._setup_customers_and_suppliers()
        cls._setup_warehouse_structure()
    
    @classmethod
    def _setup_company_structure(cls):
        """Setup realistic company structure."""
        cls.company = cls.env['res.company'].create({
            'name': 'Test Company Ltd.',
            'email': 'info@testcompany.com',
            'currency_id': cls.env.ref('base.USD'),
        })
        
        # Create departments
        cls.sales_dept = cls.env['hr.department'].create({
            'name': 'Sales',
            'company_id': cls.company.id,
        })
        
        cls.finance_dept = cls.env['hr.department'].create({
            'name': 'Finance',
            'company_id': cls.company.id,
        })
    
    @classmethod
    def _setup_products_and_categories(cls):
        """Setup product hierarchy."""
        # Create categories
        cls.category_raw = cls.env['product.category'].create({
            'name': 'Raw Materials',
            'parent_id': False,
        })
        
        cls.category_finished = cls.env['product.category'].create({
            'name': 'Finished Goods',
            'parent_id': False,
        })
        
        # Create products with BOM
        cls.product_raw = cls.env['product.product'].create({
            'name': 'Raw Material A',
            'categ_id': cls.category_raw.id,
            'type': 'product',
            'list_price': 10.0,
        })
        
        cls.product_finished = cls.env['product.product'].create({
            'name': 'Finished Product A',
            'categ_id': cls.category_finished.id,
            'type': 'product',
            'list_price': 100.0,
        })
        
        # Create BOM
        cls.bom = cls.env['mrp.bom'].create({
            'product_tmpl_id': cls.product_finished.product_tmpl_id,
            'bom_line_ids': [
                (0, 0, {
                    'product_id': cls.product_raw.id,
                    'product_qty': 2.0,
                })
            ]
        })
```

### Test Environment Isolation

```python
# Database isolation for integration tests
class IsolatedIntegrationTest(common.TransactionCase):
    
    def setUp(self):
        super().setUp()
        # Create isolated schema for test
        self.test_schema = f"test_schema_{self.id}"
        self.env.cr.execute(f"CREATE SCHEMA {self.test_schema}")
        self.env.cr.execute(f"SET search_path TO {self.test_schema}, public")
    
    def tearDown(self):
        super().tearDown()
        # Clean up test schema
        self.env.cr.execute(f"DROP SCHEMA {self.test_schema} CASCADE")
        self.env.cr.execute("RESET search_path")
```

## Coverage Requirements and Reporting

### Integration Coverage Targets

| Integration Type | Minimum Coverage | Target Coverage |
|-----------------|------------------|-----------------|
| Module Interactions | 80% | 95% |
| Database Operations | 85% | 98% |
| API Integrations | 90% | 100% |
| External Services | 85% | 95% |
| Workflow Integration | 80% | 90% |

### Integration Test Categories

```python
# Standard integration tests
@common.tagged('integration')
@common.tagged('standard')
class TestStandardIntegration(common.TransactionCase):
    """Core module interactions."""
    pass

# External integration tests
@common.tagged('integration')
@common.tagged('external')
class TestExternalIntegration(common.TransactionCase):
    """Third-party service integrations."""
    pass

# Performance integration tests
@common.tagged('integration')
@common.tagged('slow')
class TestPerformanceIntegration(common.TransactionCase):
    """Integration with performance impact."""
    pass
```

## Running Integration Tests

### Command Line

```bash
# Run all integration tests
./unierp-bin -d test_db --test-enable --test-tags "+integration" --stop-after-init

# Run specific integration tests
./unierp-bin -d test_db --test-enable --test-tags "+integration,+standard" --stop-after-init

# Run external integration tests
./unierp-bin -d test_db --test-enable --test-tags "+integration,+external" --stop-after-init

# Run with detailed logging
./unierp-bin -d test_db --test-enable --test-tags "+integration" --stop-after-init --log-level=debug
```

### Test Execution Order

```bash
# Run in specific order for dependencies
./unierp-bin -d test_db --test-enable --test-tags "TestBase,TestResUsers,TestResPartner" --stop-after-init

# Parallel execution (careful with dependencies)
./unierp-bin -d test_db --test-enable --test-tags "+integration" --stop-after-init --test-enable
```

## Common Pitfalls and Solutions

### Module Dependency Issues

```python
# Problem: Tests fail due to missing dependencies
def test_integration_without_dependencies(self):
    # This will fail if sale module not installed
    order = self.env['sale.order'].create({...})

# Solution: Ensure module installation
@classmethod
def setUpClass(cls):
    super().setUpClass()
    # Install required modules
    modules = cls.env['ir.module.module'].search([
        ('name', 'in', ['sale', 'stock', 'account'])
    ])
    for module in modules:
        if module.state != 'installed':
            module.button_immediate_install()
```

### Data Consistency Issues

```python
# Problem: Tests interfere with each other
def test_a_creates_data(self):
    self.env['my.model'].create({'name': 'Test A'})

def test_b_expects_clean_data(self):
    # Test A's data interferes
    records = self.env['my.model'].search([])
    self.assertEqual(len(records), 0)  # Fails!

# Solution: Use transactions or cleanup
def setUp(self):
    super().setUp()
    # Clean environment
    self.env['my.model'].search([]).unlink()

def tearDown(self):
    super().tearDown()
    # Additional cleanup
    self.env.cr.commit()
```

### External Service Dependencies

```python
# Problem: Tests fail when external service unavailable
def test_external_api_call(self):
    # This fails if API is down
    response = requests.get('https://api.external.com/data')

# Solution: Mock external services
@patch('requests.get')
def test_external_api_call(self, mock_get):
    mock_get.return_value.json.return_value = {'data': 'test'}
    # Test logic, not external service
```

---

*For specific testing methodologies, see: [Unit Testing](../unit-testing/README.md), [Functional Testing](../functional-testing/README.md), [Performance Testing](../performance-testing/README.md), [Security Testing](../security-testing/README.md)*