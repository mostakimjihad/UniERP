# Functional Testing Guidelines

## Overview

Functional testing in UniERP focuses on testing the application from the user's perspective, ensuring that UI workflows, end-to-end scenarios, and business processes work correctly. This level of testing validates that the system meets user requirements and provides a seamless experience.

## Testing Framework Setup

### Functional Test Base Classes

```python
from odoo.tests import common, tagged
from odoo.tests.common import HttpCase, BrowserCase

# HttpCase - For HTTP request testing
class TestWebInterface(common.HttpCase):
    def setUp(self):
        super().setUp()
        # Setup HTTP test environment
        
    def test_web_page_access(self):
        """Test web page accessibility."""
        response = self.url_open('/web')
        self.assertEqual(response.status_code, 200)

# BrowserCase - For browser automation testing
class TestUserWorkflows(common.BrowserCase):
    def setUp(self):
        super().setUp()
        # Setup browser test environment
        
    def test_user_login_workflow(self):
        """Test complete user login workflow."""
        # Browser automation test
        pass
```

### Test Configuration

```python
# Functional test tags
@common.tagged('functional')     # Standard functional tests
@common.tagged('ui')           # UI-specific tests
@common.tagged('workflow')      # Workflow tests
@common.tagged('end-to-end')   # End-to-end scenarios
@common.tagged('slow')          # Time-consuming functional tests

# Test with specific browser
@common.tagged('chrome')
@common.tagged('firefox')
```

## Best Practices and Naming Conventions

### File Organization

```
addons/my_module/tests/
├── functional/
│   ├── __init__.py
│   ├── test_user_workflows.py     # User journey tests
│   ├── test_ui_components.py      # UI component tests
│   ├── test_form_validation.py   # Form validation tests
│   ├── test_navigation.py         # Navigation tests
│   └── test_end_to_end.py       # End-to-end scenarios
```

### Naming Conventions

```python
# Test class names
class TestUserLoginWorkflow(common.BrowserCase):  # Test + User + Action + Workflow
class TestSaleOrderCreation(common.BrowserCase):  # Test + Entity + Action
class TestInvoiceValidation(common.BrowserCase):  # Test + Entity + Validation

# Test method names
def test_complete_user_registration_flow(self):  # test_complete_user_action_flow
def test_product_search_and_add_to_cart(self):  # test_entity_action_and_action
def test_checkout_process_with_payment(self):  # test_process_with_condition
def test_invoice_generation_after_sale(self):  # test_entity_after_event
```

## Sample Test Cases and Code Examples

### User Workflow Testing

```python
# addons/sale/tests/functional/test_customer_journey.py
from odoo.tests import common, tagged
from odoo.exceptions import UserError

@common.tagged('functional')
@common.tagged('end-to-end')
class TestCustomerJourney(common.BrowserCase):
    """Test complete customer journey from registration to purchase."""
    
    def setUp(self):
        super().setUp()
        # Create test user
        self.user = self.env['res.users'].create({
            'name': 'Test Customer',
            'login': 'test_customer',
            'password': 'customer123',
            'groups_id': [(6, 0, [self.ref('base.group_portal')])]
        })
    
    def test_complete_purchase_workflow(self):
        """Test complete purchase workflow."""
        # Step 1: User login
        self.browser_open('/web')
        self.fill_input('login', 'test_customer')
        self.fill_input('password', 'customer123')
        self.click('.btn-login')
        
        # Verify login successful
        self.assert_element_visible('.o_main_navbar')
        
        # Step 2: Browse products
        self.browser_open('/shop')
        self.assert_element_visible('.product-card')
        
        # Step 3: Add product to cart
        self.click('.product-card:first-child .add-to-cart')
        self.assert_element_visible('.cart-count')
        self.assert_text('.cart-count', '1')
        
        # Step 4: Proceed to checkout
        self.click('.proceed-to-checkout')
        self.assert_element_visible('.checkout-form')
        
        # Step 5: Fill shipping information
        self.fill_input('shipping_name', 'Test Customer')
        self.fill_input('shipping_email', 'customer@test.com')
        self.fill_input('shipping_phone', '+1234567890')
        self.fill_input('shipping_address', '123 Test Street')
        self.fill_input('shipping_city', 'Test City')
        self.select_option('shipping_country', 'US')
        
        # Step 6: Select payment method
        self.click('.payment-method-card')
        self.assert_element_visible('.payment-form')
        
        # Step 7: Complete payment
        self.fill_input('card_number', '4111111111111111')
        self.fill_input('card_expiry', '12/25')
        self.fill_input('card_cvc', '123')
        self.click('.confirm-payment')
        
        # Verify order confirmation
        self.assert_element_visible('.order-confirmation')
        self.assert_text('.order-number', 'SO')
    
    def test_user_registration_flow(self):
        """Test new user registration workflow."""
        # Navigate to registration
        self.browser_open('/web/signup')
        self.assert_element_visible('.signup-form')
        
        # Fill registration form
        self.fill_input('name', 'New User')
        self.fill_input('email', 'newuser@test.com')
        self.fill_input('login', 'newuser')
        self.fill_input('password', 'password123')
        self.fill_input('confirm_password', 'password123')
        
        # Submit registration
        self.click('.btn-signup')
        
        # Verify successful registration
        self.assert_element_visible('.success-message')
        self.assert_text('.success-message', 'Registration successful')
        
        # Verify login works
        self.browser_open('/web')
        self.fill_input('login', 'newuser')
        self.fill_input('password', 'password123')
        self.click('.btn-login')
        self.assert_element_visible('.o_main_navbar')
```

### UI Component Testing

```python
# addons/web/tests/functional/test_ui_components.py
@common.tagged('functional')
@common.tagged('ui')
class TestUIComponents(common.BrowserCase):
    """Test UI component functionality."""
    
    def test_navigation_menu_functionality(self):
        """Test main navigation menu."""
        self.browser_open('/web')
        
        # Test main menu items
        menu_items = [
            '.menu-sales',
            '.menu-purchases',
            '.menu-inventory',
            '.menu-accounting',
            '.menu-hr',
        ]
        
        for menu_item in menu_items:
            self.assert_element_visible(menu_item)
            
            # Click menu item
            self.click(menu_item)
            
            # Verify menu is active
            self.assert_element_visible(f'{menu_item}.active')
            
            # Verify submenu appears (if any)
            submenu = self.find_element(f'{menu_item} .submenu')
            if submenu:
                self.assert_element_visible(f'{menu_item} .submenu')
    
    def test_form_validation_realtime(self):
        """Test real-time form validation."""
        self.browser_open('/web/register')
        
        # Test required field validation
        self.click('.btn-submit')
        self.assert_element_visible('.error-message')
        self.assert_text('.error-message', 'Name is required')
        
        # Fill name and test email validation
        self.fill_input('name', 'Test User')
        self.click('.btn-submit')
        self.assert_text('.error-message', 'Email is required')
        
        # Fill invalid email
        self.fill_input('email', 'invalid-email')
        self.click('.btn-submit')
        self.assert_text('.error-message', 'Invalid email format')
        
        # Fill valid email
        self.fill_input('email', 'valid@test.com')
        self.click('.btn-submit')
        self.assert_element_not_visible('.error-message')
    
    def test_responsive_design(self):
        """Test responsive design across devices."""
        # Test desktop view
        self.browser_resize(1920, 1080)
        self.browser_open('/web')
        self.assert_element_visible('.desktop-navigation')
        
        # Test tablet view
        self.browser_resize(768, 1024)
        self.assert_element_not_visible('.desktop-navigation')
        self.assert_element_visible('.mobile-navigation')
        
        # Test mobile view
        self.browser_resize(375, 667)
        self.assert_element_not_visible('.desktop-navigation')
        self.assert_element_visible('.mobile-navigation')
        self.assert_element_visible('.hamburger-menu')
```

### Form Validation Testing

```python
# addons/base/tests/functional/test_form_validation.py
@common.tagged('functional')
class TestFormValidation(common.BrowserCase):
    """Test form validation across modules."""
    
    def test_partner_form_validation(self):
        """Test partner form validation."""
        self.browser_open('/web/partner/create')
        
        # Test empty required fields
        self.click('.btn-save')
        self.assert_element_visible('.error-name')
        self.assert_text('.error-name', 'This field is required')
        
        self.assert_element_visible('.error-email')
        self.assert_text('.error-email', 'This field is required')
        
        # Test invalid email format
        self.fill_input('name', 'Test Partner')
        self.fill_input('email', 'invalid-email')
        self.click('.btn-save')
        self.assert_text('.error-email', 'Invalid email format')
        
        # Test valid data
        self.fill_input('email', 'valid@test.com')
        self.click('.btn-save')
        self.assert_element_not_visible('.error-message')
        self.assert_element_visible('.success-message')
    
    def test_product_form_validation(self):
        """Test product form validation."""
        self.browser_open('/web/product/create')
        
        # Test negative price validation
        self.fill_input('name', 'Test Product')
        self.fill_input('list_price', '-100')
        self.click('.btn-save')
        self.assert_element_visible('.error-list_price')
        self.assert_text('.error-list_price', 'Price must be positive')
        
        # Test zero quantity validation
        self.fill_input('list_price', '100')
        self.fill_input('qty_available', '0')
        self.click('.btn-save')
        self.assert_element_visible('.error-qty_available')
        self.assert_text('.error-qty_available', 'Quantity must be greater than 0')
        
        # Test valid data
        self.fill_input('qty_available', '10')
        self.click('.btn-save')
        self.assert_element_not_visible('.error-message')
```

### End-to-End Scenario Testing

```python
# addons/sale_stock_account/tests/functional/test_sale_to_cash_flow.py
@common.tagged('functional')
@common.tagged('end-to-end')
class TestSaleToCashFlow(common.BrowserCase):
    """Test complete sales process from order to payment."""
    
    def setUp(self):
        super().setUp()
        # Setup test environment
        self._setup_test_products()
        self._setup_test_customer()
        self._setup_payment_methods()
    
    def test_complete_sales_workflow(self):
        """Test complete sales workflow."""
        # Step 1: Create sales order
        self.browser_open('/web/sale/orders')
        self.click('.btn-new-order')
        self.fill_input('partner_id', self.customer.name)
        self.fill_input('order_line_product_0', self.product_a.name)
        self.fill_input('order_line_quantity_0', '5')
        self.click('.btn-confirm-order')
        
        # Verify order created
        self.assert_element_visible('.order-header')
        self.assert_text('.order-state', 'Quotation')
        
        # Step 2: Confirm quotation
        self.click('.btn-confirm-quotation')
        self.assert_text('.order-state', 'Sales Order')
        
        # Step 3: Create delivery
        self.click('.btn-create-delivery')
        self.assert_element_visible('.delivery-form')
        self.click('.btn-confirm-delivery')
        
        # Verify delivery created
        self.assert_element_visible('.delivery-header')
        self.assert_text('.delivery-state', 'Confirmed')
        
        # Step 4: Validate delivery
        self.browser_open('/web/stock/picking')
        self.click('.delivery-row')
        self.click('.btn-validate')
        self.assert_text('.delivery-state', 'Done')
        
        # Step 5: Create invoice
        self.click('.btn-create-invoice')
        self.assert_element_visible('.invoice-form')
        self.click('.btn-validate-invoice')
        
        # Verify invoice created
        self.assert_element_visible('.invoice-header')
        self.assert_text('.invoice-state', 'Posted')
        
        # Step 6: Register payment
        self.click('.btn-register-payment')
        self.fill_input('payment_amount', '500.00')
        self.select_option('payment_method', 'cash')
        self.click('.btn-confirm-payment')
        
        # Verify payment registered
        self.assert_element_visible('.payment-header')
        self.assert_text('.payment-state', 'Paid')
        
        # Step 7: Verify complete workflow
        self.browser_open('/web/sale/orders/' + self.order_number)
        self.assert_text('.order-state', 'Paid')
        self.assert_element_visible('.workflow-complete-indicator')
```

## Test Data Management Strategies

### Functional Test Fixtures

```python
# addons/common/tests/functional_fixtures.py
from odoo.tests import common

class FunctionalTestCommon(common.BrowserCase):
    """Common fixtures for functional tests."""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Setup realistic test data
        cls._setup_company_data()
        cls._setup_user_hierarchy()
        cls._setup_product_catalog()
        cls._setup_business_scenarios()
    
    @classmethod
    def _setup_company_data(cls):
        """Setup realistic company data."""
        cls.company = cls.env['res.company'].create({
            'name': 'Test Company Ltd.',
            'email': 'info@testcompany.com',
            'phone': '+1234567890',
            'website': 'www.testcompany.com',
            'currency_id': cls.env.ref('base.USD'),
        })
        
        # Create departments
        cls.departments = cls.env['hr.department'].create([
            {'name': 'Sales', 'company_id': cls.company.id},
            {'name': 'Marketing', 'company_id': cls.company.id},
            {'name': 'Finance', 'company_id': cls.company.id},
        ])
    
    @classmethod
    def _setup_user_hierarchy(cls):
        """Setup realistic user hierarchy."""
        # Create different user roles
        cls.admin_user = cls.env['res.users'].create({
            'name': 'Admin User',
            'login': 'admin',
            'password': 'admin123',
            'groups_id': [(6, 0, [cls.ref('base.group_system')])]
        })
        
        cls.manager_user = cls.env['res.users'].create({
            'name': 'Manager User',
            'login': 'manager',
            'password': 'manager123',
            'groups_id': [(6, 0, [cls.ref('base.group_manager')])]
        })
        
        cls.employee_users = cls.env['res.users'].create([
            {
                'name': 'Employee User 1',
                'login': 'employee1',
                'password': 'emp123',
                'groups_id': [(6, 0, [cls.ref('base.group_user')])]
            },
            {
                'name': 'Employee User 2',
                'login': 'employee2',
                'password': 'emp123',
                'groups_id': [(6, 0, [cls.ref('base.group_user')])]
            }
        ])
```

### Test Data Factories

```python
# addons/my_module/tests/functional/factories.py
class BusinessScenarioFactory:
    """Factory for creating business test scenarios."""
    
    @staticmethod
    def create_sales_scenario(env, **kwargs):
        """Create complete sales scenario."""
        defaults = {
            'customer': {
                'name': 'Test Customer',
                'email': 'customer@test.com',
                'phone': '+1234567890',
            },
            'products': [
                {
                    'name': 'Test Product A',
                    'price': 100.0,
                    'quantity': 2.0,
                }
            ],
            'payment_method': 'bank_transfer',
            'delivery_method': 'delivery_carrier',
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create_purchase_scenario(env, **kwargs):
        """Create complete purchase scenario."""
        defaults = {
            'supplier': {
                'name': 'Test Supplier',
                'email': 'supplier@test.com',
            },
            'products': [
                {
                    'name': 'Raw Material A',
                    'price': 50.0,
                    'quantity': 10.0,
                }
            ],
            'payment_terms': 'net_30',
        }
        defaults.update(kwargs)
        return defaults
```

## Coverage Requirements and Reporting

### Functional Coverage Targets

| Functional Area | Minimum Coverage | Target Coverage |
|----------------|------------------|-----------------|
| User Workflows | 85% | 95% |
| UI Components | 80% | 90% |
| Form Validation | 90% | 100% |
| Navigation | 85% | 95% |
| End-to-End Scenarios | 80% | 90% |
| Mobile Responsiveness | 85% | 95% |

### Test Categories

```python
# Standard functional tests
@common.tagged('functional')
@common.tagged('standard')
class TestStandardFunctionality(common.BrowserCase):
    """Core functional tests."""
    pass

# UI-specific tests
@common.tagged('functional')
@common.tagged('ui')
class TestUIComponents(common.BrowserCase):
    """UI component tests."""
    pass

# Workflow tests
@common.tagged('functional')
@common.tagged('workflow')
class TestWorkflows(common.BrowserCase):
    """Business workflow tests."""
    pass

# End-to-end tests
@common.tagged('functional')
@common.tagged('end-to-end')
class TestEndToEndScenarios(common.BrowserCase):
    """Complete user journey tests."""
    pass

# Slow functional tests
@common.tagged('functional')
@common.tagged('slow')
class TestPerformanceFunctional(common.BrowserCase):
    """Time-consuming functional tests."""
    pass
```

## Running Functional Tests

### Command Line

```bash
# Run all functional tests
./unierp-bin -d test_db --test-enable --test-tags "+functional" --stop-after-init

# Run UI-specific tests
./unierp-bin -d test_db --test-enable --test-tags "+functional,+ui" --stop-after-init

# Run workflow tests
./unierp-bin -d test_db --test-enable --test-tags "+functional,+workflow" --stop-after-init

# Run end-to-end tests
./unierp-bin -d test_db --test-enable --test-tags "+functional,+end-to-end" --stop-after-init
```

### Browser Configuration

```python
# Configure browser for tests
class TestWithCustomBrowser(common.BrowserCase):
    def setUp(self):
        super().setUp()
        # Configure browser settings
        self.browser_size = (1920, 1080)
        self.browser_user_agent = 'UniERP-Test/1.0'
        self.browser_timeout = 30
```

## Common Pitfalls and Solutions

### Browser Automation Issues

```python
# Problem: Tests fail due to timing issues
def test_dynamic_content(self):
    self.click('.load-more-button')
    self.assert_element_visible('.dynamic-content')  # Might fail!

# Solution: Use waits
def test_dynamic_content(self):
    self.click('.load-more-button')
    self.wait_for_element('.dynamic-content')  # Wait for element
    self.assert_element_visible('.dynamic-content')

# Alternative: Use explicit waits
def test_dynamic_content(self):
    self.click('.load-more-button')
    self.wait_for_ajax()
    self.assert_element_visible('.dynamic-content')
```

### Test Data Management

```python
# Problem: Tests interfere with each other
def test_a_creates_user(self):
    self.env['res.users'].create({'name': 'User A'})

def test_b_expects_clean_state(self):
    # User A still exists!
    users = self.env['res.users'].search([('name', 'ilike', 'User%')])
    self.assertEqual(len(users), 1)  # Fails!

# Solution: Use proper cleanup
def setUp(self):
    super().setUp()
    # Clean up test data
    self.env['res.users'].search([
        ('login', 'like', 'test_%')
    ]).unlink()

def tearDown(self):
    super().tearDown()
    # Additional cleanup
    self.env.cr.commit()
```

### Cross-Browser Compatibility

```python
# Problem: Tests only work in one browser
@common.tagged('chrome')
class TestChromeOnly(common.BrowserCase):
    pass  # Only tests Chrome

# Solution: Test multiple browsers
@common.tagged('chrome')
class TestChromeFeatures(common.BrowserCase):
    """Chrome-specific features."""
    pass

@common.tagged('firefox')
class TestFirefoxFeatures(common.BrowserCase):
    """Firefox-specific features."""
    pass

@common.tagged('safari')
class TestSafariFeatures(common.BrowserCase):
    """Safari-specific features."""
    pass
```

---

*For specific testing methodologies, see: [Unit Testing](../unit-testing/README.md), [Integration Testing](../integration-testing/README.md), [Performance Testing](../performance-testing/README.md), [Security Testing](../security-testing/README.md)*