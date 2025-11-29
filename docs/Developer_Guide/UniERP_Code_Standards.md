# UniERP Code Standards

## Overview

This comprehensive guide establishes coding standards and best practices for UniERP development, ensuring code quality, maintainability, and consistency across all modules and customizations.

## Table of Contents

1. [General Principles](#general-principles)
2. [Python Standards](#python-standards)
3. [JavaScript Standards](#javascript-standards)
4. [XML Standards](#xml-standards)
5. [CSS/SCSS Standards](#cssscss-standards)
6. [Database Standards](#database-standards)
7. [Security Standards](#security-standards)
8. [Testing Standards](#testing-standards)
9. [Documentation Standards](#documentation-standards)
10. [Version Control](#version-control)
11. [Code Review Process](#code-review-process)

## General Principles

### Code Quality Goals

- **Readability**: Code should be easy to understand and modify
- **Maintainability**: Code should be easy to maintain and extend
- **Performance**: Code should be efficient and scalable
- **Security**: Code should be secure and protect against vulnerabilities
- **Consistency**: Code should follow established patterns and conventions

### Development Philosophy

1. **Simplicity**: Favor simple solutions over complex ones
2. **Clarity**: Write code that clearly expresses intent
3. **Modularity**: Break complex problems into smaller, reusable components
4. **Testability**: Write code that can be easily tested
5. **Documentation**: Document non-obvious code and complex logic

## Python Standards

### Code Style

#### Formatting

```python
# Use 4 spaces for indentation
def my_function(param1, param2):
    if param1 and param2:
        return param1 + param2

# Maximum line length: 88 characters
long_variable_name = (
    "This is a very long string that exceeds "
    "the maximum line length limit"
)

# Use trailing commas in multi-line constructs
my_list = [
    "item1",
    "item2",
    "item3",
]

# Use spaces around operators
if condition and other_condition:
    result = value1 + value2
else:
    result = value3
```

#### Naming Conventions

```python
# Variables and functions: snake_case
user_name = "John Doe"
def calculate_total_price(items):
    return sum(item.price for item in items)

# Classes: PascalCase
class ProductManager:
    def __init__(self):
        self.products = []
    
    def add_product(self, product):
        self.products.append(product)

# Constants: UPPER_CASE
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.unierp.com"

# Private methods: underscore prefix
class MyClass:
    def __init__(self):
        self._private_data = {}
    
    def public_method(self):
        return self._private_helper()
    
    def _private_helper(self):
        return "private data"
```

#### Import Organization

```python
# Standard library imports first
import os
import sys
import json
import logging
from datetime import datetime, timedelta

# Third-party imports second
import requests
import pandas as pd
from external_library import SomeClass

# Local imports third
from .models import my_model
from .utils import helper_function

# Avoid wildcard imports
# Bad: from models import *
# Good: from models import specific_model, another_model
```

#### Docstring Standards

```python
def complex_function(param1, param2):
    """
    Perform complex operation on provided parameters.
    
    Args:
        param1 (str): First parameter for the operation
        param2 (int): Second parameter for the operation
    
    Returns:
        bool: True if operation successful, False otherwise
    
    Raises:
        ValueError: If parameters are invalid
        ConnectionError: If external service unavailable
    
    Example:
        >>> result = complex_function("test", 42)
        >>> print(result)
        True
    """
    # Implementation here
    pass

class MyClass:
    """
    A class that represents a custom business entity.
    
    Attributes:
        name (str): The name of the entity
        value (float): The numerical value associated with the entity
        active (bool): Whether the entity is currently active
    
    Methods:
        calculate_total(): Calculate total value including related entities
        validate(): Validate entity data and return validation results
    """
    
    def __init__(self, name, value, active=True):
        self.name = name
        self.value = value
        self.active = active
```

#### Exception Handling

```python
import logging

logger = logging.getLogger(__name__)

class CustomError(Exception):
    """Base exception for custom module errors"""
    pass

class ValidationError(CustomError):
    """Raised when data validation fails"""
    pass

def risky_operation():
    try:
        # Potentially failing operation
        result = external_api_call()
        return result
    except ConnectionError as e:
        logger.error(f"Connection failed: {e}")
        raise
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
```

### Python Best Practices

#### Environment Variables

```python
import os
from odoo import api, fields, models

class ConfigurableModel(models.Model):
    _name = 'configurable.model'
    
    # Use environment variables for configuration
    api_key = fields.Char(
        string='API Key',
        default=lambda self: os.getenv('UNIERP_API_KEY', ''),
        help='API key for external integration'
    )
    
    debug_mode = fields.Boolean(
        string='Debug Mode',
        default=lambda self: os.getenv('UNIERP_DEBUG', 'False') == 'True',
        help='Enable debug logging'
    )
```

#### Context Management

```python
from odoo import api

class ContextAwareModel(models.Model):
    _name = 'context.aware.model'
    
    @api.model
    def create(self, vals):
        # Ensure context is preserved
        if self.env.context.get('from_webhook', False):
            vals['auto_process'] = True
        
        return super(ContextAwareModel, self).create(vals)
    
    @api.multi
    def write(self, vals):
        # Use context for conditional logic
        if self.env.context.get('skip_validation', False):
            return super(ContextAwareModel, self).write(vals)
        
        # Perform validation
        return self._validate_and_write(vals)
    
    def _validate_and_write(self, vals):
        # Custom validation logic
        return super(ContextAwareModel, self).write(vals)
```

#### Database Operations

```python
from odoo import api, fields, models

class EfficientModel(models.Model):
    _name = 'efficient.model'
    
    # Use CRUD operations efficiently
    @api.model
    def bulk_create(self, records_list):
        """Bulk create for better performance"""
        records = []
        for record_data in records_list:
            records.append((0, 0, {
                'name': record_data['name'],
                'value': record_data['value'],
            }))
        
        return self.browse([rec.id for rec in self.create(records)])
    
    # Use search efficiently
    @api.model
    def get_active_records(self, limit=100):
        """Efficient search with proper indexing"""
        return self.search([
            ('active', '=', True)
        ], limit=limit, order='create_date desc')
```

## JavaScript Standards

### Code Style

#### Formatting

```javascript
// Use 2 spaces for indentation
function calculateTotal(items) {
    let total = 0;
    
    for (const item of items) {
        total += item.price;
    }
    
    return total;
}

// Use trailing commas
const config = {
    apiUrl: 'https://api.unierp.com',
    timeout: 30000,
    retryAttempts: 3,
};

// Use spaces around operators
if (condition && otherCondition) {
    doSomething();
} else {
    doSomethingElse();
}
```

#### Naming Conventions

```javascript
// Variables and functions: camelCase
const userName = 'john_doe';
const maxRetryAttempts = 3;

function calculateTotalPrice(items) {
    return items.reduce((total, item) => total + item.price, 0);
}

// Classes: PascalCase
class ProductManager {
    constructor() {
        this.products = [];
    }
    
    addProduct(product) {
        this.products.push(product);
    }
}

// Constants: UPPER_CASE
const API_BASE_URL = 'https://api.unierp.com';
const DEFAULT_TIMEOUT = 30000;

// Private methods: underscore prefix
class MyClass {
    constructor() {
        this._privateData = {};
    }
    
    publicMethod() {
        return this._privateHelper();
    }
    
    _privateHelper() {
        return 'private data';
    }
}
```

#### Module Definition

```javascript
// Use AMD module definition
odoo.define('my_module.main', function (require) {
    "use strict";
    
    var core = require('web.core');
    var Widget = require('web.Widget');
    var ajax = require('web.ajax');
    
    var MyWidget = Widget.extend({
        // Widget implementation
    });
    
    core.action_registry.add('my_widget', MyWidget);
    
    return {
        MyWidget: MyWidget,
    };
});

// ES6 module export (if applicable)
export default {
    MyWidget,
    helperFunction,
};
```

#### Error Handling

```javascript
// Use promises for async operations
function fetchData(url) {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Fetch failed:', error);
            throw error;
        });
}

// Use try-catch for synchronous operations
function processData(data) {
    try {
        const result = complexOperation(data);
        return result;
    } catch (error) {
        console.error('Processing failed:', error);
        return null;
    }
}
```

## XML Standards

### Structure and Formatting

```xml
<!-- Proper XML declaration -->
<?xml version="1.0" encoding="utf-8"?>

<!-- Use proper indentation (4 spaces) -->
<odoo>
    <record id="view_my_form" model="ir.ui.view">
        <field name="name">my.model.form</field>
        <field name="model">my.model</field>
        <field name="arch" type="xml">
            <form string="My Model">
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="description"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
```

#### Naming Conventions

```xml
<!-- View IDs: descriptive and unique -->
<record id="view_custom_partner_form" model="ir.ui.view"/>
<record id="action_custom_partners" model="ir.actions.act_window"/>
<record id="menu_custom_root" model="ir.ui.menu"/>

<!-- Field names: descriptive snake_case -->
<field name="custom_field_name"/>
<field name="related_partner_id"/>
<field name="is_active_flag"/>

<!-- Menu items: descriptive hierarchy -->
<menuitem id="menu_custom_root" name="Custom Module"/>
<menuitem id="menu_custom_items" name="Custom Items" parent="menu_custom_root"/>
```

#### XPath Expressions

```xml
<!-- Use specific XPath expressions -->
<xpath expr="//field[@name='name']" position="after">
    <field name="custom_field" string="Custom Field"/>
</xpath>

<xpath expr="//sheet" position="inside">
    <group string="Custom Information">
        <field name="custom_field"/>
    </group>
</xpath>

<!-- Avoid overly broad expressions -->
<!-- Bad: xpath="//field" -->
<!-- Good: xpath="//field[@name='specific_field']" -->
```

## CSS/SCSS Standards

### Organization and Structure

```scss
// Use proper file organization
@import 'variables';
@import 'mixins';
@import 'components';

// Group related styles
.o_unierp_module {
    // Component styles here
    
    .component {
        // Component-specific styles
    }
    
    .variant {
        // Variant styles
    }
}

// Use meaningful class names
.customer_form {
    // Customer form styles
}

.product_list {
    // Product list styles
}
```

#### Naming Conventions

```scss
// Use kebab-case for class names
.custom-component {
    // Component styles
}

.custom-component--modifier {
    // Component variant
}

.custom-component__element {
    // Component element
}

// Use meaningful variable names
$primary-color: #00a650;
$secondary-color: #6c757d;
$border-radius: 4px;
$font-size-base: 0.875rem;

// Use SCSS variables for consistency
.button {
    background-color: $primary-color;
    border-radius: $border-radius;
    font-size: $font-size-base;
}
```

#### Responsive Design

```scss
// Use mobile-first approach
.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 16px;
    
    @media (min-width: 768px) {
        padding: 0 24px;
    }
    
    @media (min-width: 1024px) {
        padding: 0 32px;
    }
}

// Use flexible units
.flex-container {
    display: flex;
    gap: 1rem;
    
    .flex-item {
        flex: 1;
        min-width: 0;
    }
}
```

## Database Standards

### Naming Conventions

```sql
-- Table names: snake_case, plural
CREATE TABLE res_partner (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Column names: snake_case, descriptive
ALTER TABLE res_partner 
ADD COLUMN custom_field_name VARCHAR(100);

-- Index names: descriptive pattern
CREATE INDEX idx_res_partner_name ON res_partner(name);
CREATE INDEX idx_res_partner_email ON res_partner(email);
```

### Query Optimization

```sql
-- Use specific columns in WHERE clauses
-- Bad: SELECT * FROM res_partner WHERE UPPER(name) LIKE '%TEST%'
-- Good: SELECT id, name FROM res_partner WHERE name ILIKE '%test%'

-- Use appropriate indexes
-- Ensure indexes exist for frequently queried columns
EXPLAIN ANALYZE SELECT * FROM res_partner WHERE active = TRUE;

-- Use LIMIT for large result sets
SELECT * FROM large_table ORDER BY create_date DESC LIMIT 1000;

-- Use JOINs efficiently
SELECT p.name, p.price 
FROM product p 
JOIN sale_order_line sol ON p.id = sol.product_id 
WHERE sol.order_id = %s;
```

### Data Integrity

```sql
-- Use proper constraints
ALTER TABLE res_partner 
ADD CONSTRAINT res_partner_email_check 
CHECK (email ~* '^[^@]+@[^@]+\.[^@]+$');

-- Use foreign key constraints
ALTER TABLE sale_order_line 
ADD CONSTRAINT sol_product_id_fkey 
FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE RESTRICT;

-- Use appropriate data types
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(50) NOT NULL,
    user_id INTEGER REFERENCES res_users(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Security Standards

### Input Validation

```python
from odoo import api, fields, models

class SecureModel(models.Model):
    _name = 'secure.model'
    
    @api.model
    def create(self, vals):
        # Validate input data
        if 'email' in vals:
            if not self._validate_email(vals['email']):
                raise models.ValidationError('Invalid email format')
        
        if 'amount' in vals:
            try:
                amount = float(vals['amount'])
                if amount < 0:
                    raise models.ValidationError('Amount must be positive')
            except ValueError:
                raise models.ValidationError('Invalid amount format')
        
        return super(SecureModel, self).create(vals)
    
    def _validate_email(self, email):
        """Validate email format using regex"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
```

### Access Control

```python
from odoo import api, fields, models

class AccessControlledModel(models.Model):
    _name = 'access.controlled.model'
    
    # Use proper access groups
    @api.model
    def create(self, vals):
        if not self.env.user.has_group('base.group_system'):
            raise models.AccessError('Insufficient permissions')
        
        return super(AccessControlledModel, self).create(vals)
    
    # Implement record rules
    def check_access_rights(self, operation):
        """Check if current user can perform operation"""
        if operation == 'read':
            return self.env.user.has_group('base.group_user')
        elif operation == 'write':
            return self.env.user.has_group('base.group_manager')
        return False
```

### SQL Injection Prevention

```python
# Always use ORM methods
# Bad: Direct SQL execution
env.cr.execute(f"SELECT * FROM res_partner WHERE name = '{user_input}'")

# Good: Parameterized queries with ORM
partners = env['res.partner'].search([
    ('name', '=', user_input)
])

# If direct SQL is necessary, use proper parameterization
# Bad: env.cr.execute(f"UPDATE res_partner SET name = '{name}' WHERE id = {id}")
# Good: env.cr.execute("UPDATE res_partner SET name = %s WHERE id = %s", [name, id])
```

## Testing Standards

### Test Structure

```python
# Organize tests logically
class TestMyModel(TransactionCase):
    
    def setUp(self):
        super(TestMyModel, self).setUp()
        self.MyModel = self.env['my.model']
    
    def test_create_valid_record(self):
        """Test creating a valid record"""
        record = self.MyModel.create({
            'name': 'Test Record',
            'value': 42,
        })
        self.assertTrue(record)
        self.assertEqual(record.name, 'Test Record')
        self.assertEqual(record.value, 42)
    
    def test_create_invalid_record(self):
        """Test creating an invalid record"""
        with self.assertRaises(ValidationError):
            self.MyModel.create({
                'name': '',  # Invalid: empty name
                'value': -1,  # Invalid: negative value
            })
    
    def tearDown(self):
        super(TestMyModel, self).tearDown()
```

### Test Coverage

```python
# Aim for high test coverage
# Test all public methods
# Test edge cases
# Test error conditions
# Test data validation
# Test permissions
# Target: 90%+ code coverage
```

### Test Data Management

```python
# Use consistent test data
TEST_PARTNER_DATA = {
    'name': 'Test Partner',
    'email': 'test@example.com',
    'phone': '+1234567890',
    'is_company': True,
}

# Use factories for complex objects
class TestPartnerFactory:
    @staticmethod
    def create_partner(env, **kwargs):
        data = TEST_PARTNER_DATA.copy()
        data.update(kwargs)
        return env['res.partner'].create(data)
```

## Documentation Standards

### Code Documentation

```python
def complex_function(param1, param2):
    """
    Perform complex operation on provided parameters.
    
    This function handles the following scenarios:
    - Standard operation with valid parameters
    - Edge case with boundary values
    - Error conditions with appropriate exceptions
    
    Args:
        param1 (str): First parameter for the operation
        param2 (int): Second parameter for the operation
    
    Returns:
        dict: Result containing operation status and data
    
    Raises:
        ValueError: If parameters are invalid
        ConnectionError: If external service unavailable
    
    Example:
        >>> result = complex_function("test", 42)
        >>> print(result)
        {'status': 'success', 'data': {...}}
    """
    # Implementation
    pass
```

### Comment Standards

```python
# Use clear, concise comments
def calculate_discount(price, discount_rate):
    # Apply discount rate to price
    discounted_price = price * (1 - discount_rate)
    return discounted_price

# Explain complex logic
def process_order(order_data):
    """
    Process order data through multiple validation steps.
    
    1. Validate customer information
    2. Check product availability
    3. Calculate pricing and discounts
    4. Apply business rules
    """
    # Implementation
    pass

# TODO comments with actionable items
# TODO: Implement currency conversion support
# TODO: Add multi-language support
# FIXME: Temporary workaround for performance issue
```

## Version Control

### Commit Standards

```bash
# Use descriptive commit messages
git commit -m "feat: Add custom field validation

- Implement email format validation using regex
- Add unit tests for validation logic
- Update documentation with examples"

# Use conventional commits
# feat: New feature
# fix: Bug fix
# docs: Documentation changes
# style: Code formatting changes
# refactor: Code refactoring
# test: Test additions
# chore: Maintenance tasks
```

### Branch Strategy

```bash
# Use feature branches for development
git checkout -b feature/custom-validation
git checkout -b fix/email-validation-bug
git checkout -b docs/api-updates

# Use descriptive branch names
feature/user-permissions-enhancement
fix/database-connection-leak
docs/upgrade-procedure-update
refactor/performance-optimization
```

### Code Review Process

1. **Self-Review**: Review own code before submission
2. **Peer Review**: At least one team member reviews changes
3. **Automated Checks**: Run linting and testing tools
4. **Documentation**: Ensure code is properly documented
5. **Testing**: Verify tests pass and coverage is adequate

---

This comprehensive code standards guide provides developers with established best practices and conventions for creating high-quality, maintainable, and secure UniERP modules and customizations.