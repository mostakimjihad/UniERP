# UniERP Module Development Guide

## Overview

This comprehensive guide provides developers with detailed instructions for creating custom modules for UniERP, covering development best practices, coding standards, and integration procedures.

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Module Structure](#module-structure)
3. [Creating a New Module](#creating-a-new-module)
4. [Module Manifest](#module-manifest)
5. [Model Development](#model-development)
6. [View Development](#view-development)
7. [Controller Development](#controller-development)
8. [Static Files Management](#static-files-management)
9. [Security Implementation](#security-implementation)
10. [Testing Your Module](#testing-your-module)
11. [Module Packaging](#module-packaging)
12. [Deployment Procedures](#deployment-procedures)
13. [Best Practices](#best-practices)
14. [Troubleshooting](#troubleshooting)

## Development Environment Setup

### Prerequisites

Before developing UniERP modules, ensure you have:

- **Python 3.8+** installed
- **PostgreSQL 12+** database server
- **Git** version control system
- **UniERP Server** development environment
- **Text Editor/IDE** with Python support

### Environment Configuration

```bash
# Clone UniERP repository
git clone https://github.com/unierp/unierp.git

# Set up virtual environment
python3 -m venv unierp-dev
source unierp-dev/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up database
createdb unierp_dev
```

### Development Tools

Recommended tools for UniERP module development:

- **PyCharm** or **VS Code** with Python extensions
- **pgAdmin** for database management
- **Postman** for API testing
- **Git** for version control

## Module Structure

### Basic Module Structure

```
my_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── my_model.py
├── views/
│   ├── my_model_views.xml
│   └── my_model_templates.xml
├── controllers/
│   ├── __init__.py
│   └── my_controller.py
├── static/
│   ├── src/
│   │   ├── js/
│   │   ├── css/
│   │   └── img/
│   └── description/
│       └── icon.png
├── data/
│   └── my_module_data.xml
├── demo/
│   └── my_module_demo.xml
├── security/
│   └── ir.model.access.csv
└── tests/
    ├── __init__.py
    └── test_my_module.py
```

### Directory Explanations

- **`__init__.py`**: Module initialization file
- **`__manifest__.py`**: Module manifest with metadata
- **`models/`**: Database model definitions
- **`views/`**: User interface definitions
- **`controllers/`**: Web controllers and routes
- **`static/`**: Static assets (JS, CSS, images)
- **`data/`**: Data files (XML, CSV)
- **`demo/`**: Demonstration data
- **`security/`**: Access control rules
- **`tests/`**: Unit and integration tests

## Creating a New Module

### Step 1: Create Module Directory

```bash
mkdir my_unierp_module
cd my_unierp_module
```

### Step 2: Initialize Module Structure

```bash
# Create necessary directories
mkdir models views controllers static data demo security tests

# Create initialization files
touch __init__.py
touch models/__init__.py
touch controllers/__init__.py
touch tests/__init__.py
```

### Step 3: Basic Module Files

Create the essential files for a functional module.

## Module Manifest

### Manifest File Structure

The `__manifest__.py` file contains module metadata:

```python
{
    'name': 'My UniERP Module',
    'version': '16.0.1.0.0',
    'category': 'Uncategorized',
    'summary': 'A custom module for UniERP',
    'description': '''
        This module provides custom functionality for UniERP users.
        It includes custom models, views, and business logic.
    ''',
    'author': 'Your Name',
    'website': 'https://www.uslbd.com',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/my_module_views.xml',
    ],
    'demo': [
        'demo/my_module_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/icon.png'],
}
```

### Manifest Fields Explained

- **`name`**: Human-readable module name
- **`version`**: Module version (follow semantic versioning)
- **`category`**: Module category for app store
- **`summary`**: Brief module description
- **`description`**: Detailed module description
- **`author`**: Module author information
- **`website`**: Author or company website
- **`license`**: License type (LGPL-3 recommended)
- **`depends`**: Required dependencies
- **`data`**: Data files to load
- **`demo`**: Demonstration data files
- **`installable`**: Whether module can be installed
- **`application`**: Whether module appears in app menu
- **`auto_install`**: Whether to auto-install

## Model Development

### Creating Models

Models define the data structure of your module:

```python
# models/my_model.py
from odoo import models, fields, api

class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Custom Model'
    _order = 'name asc'
    
    name = fields.Char(
        string='Name',
        required=True,
        help='Enter the name for this record'
    )
    
    description = fields.Text(
        string='Description',
        help='Detailed description of the record'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Enable or disable this record'
    )
    
    date_field = fields.Datetime(
        string='Date',
        default=fields.Datetime.now,
        help='Record creation date'
    )
    
    related_id = fields.Many2one(
        'res.partner',
        string='Related Partner',
        help='Link to customer/partner record'
    )
    
    @api.depends('name', 'description')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.name} - {record.description[:20]}"
    
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help='Computed display name'
    )
```

### Field Types

Common field types in UniERP:

- **`Char`**: Single line text
- **`Text`**: Multi-line text
- **`Integer`**: Whole numbers
- **`Float`**: Decimal numbers
- **`Boolean`**: True/False values
- **`Date`**: Date without time
- **`Datetime`**: Date and time
- **`Selection`**: Dropdown options
- **`Many2one`**: Many-to-one relationship
- **`One2many`**: One-to-many relationship
- **`Many2many`**: Many-to-many relationship

### Model Methods

Common model methods:

```python
class MyModel(models.Model):
    # ... field definitions ...
    
    @api.model
    def create(self, vals):
        # Override create method
        vals['name'] = vals.get('name', '').strip().title()
        return super(MyModel, self).create(vals)
    
    def write(self, vals):
        # Override write method
        if 'name' in vals:
            vals['name'] = vals['name'].strip().title()
        return super(MyModel, self).write(vals)
    
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name or len(record.name) < 3:
                raise models.ValidationError('Name must be at least 3 characters long')
    
    def action_method(self):
        # Custom action method
        self.write({'active': False})
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
```

## View Development

### Creating Views

Views define how models are displayed in the UI:

```xml
<!-- views/my_model_views.xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_my_model_tree" model="ir.ui.view">
        <field name="name">my.model.tree</field>
        <field name="model">my.model</field>
        <field name="arch" type="xml">
            <tree string="My Models">
                <field name="name"/>
                <field name="description"/>
                <field name="date_field"/>
                <field name="active"/>
            </tree>
        </field>
    </record>
    
    <record id="view_my_model_form" model="ir.ui.view">
        <field name="name">my.model.form</field>
        <field name="model">my.model</field>
        <field name="arch" type="xml">
            <form string="My Model">
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="description"/>
                        <field name="date_field"/>
                        <field name="related_id"/>
                    </group>
                    <group>
                        <field name="active"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>
    
    <record id="view_my_model_search" model="ir.ui.view">
        <field name="name">my.model.search</field>
        <field name="model">my.model</field>
        <field name="arch" type="xml">
            <search string="Search My Models">
                <field name="name"/>
                <field name="description"/>
                <filter name="active" string="Active" domain="[('active', '=', True)]"/>
                <separator/>
                <filter name="created_today" string="Created Today" 
                        domain="[('date_field', '>=', datetime.datetime.combine(context_today(), datetime.time(0,0)))]"/>
            </search>
        </field>
    </record>
    
    <!-- Window Actions -->
    <record id="action_my_model" model="ir.actions.act_window">
        <field name="name">My Models</field>
        <field name="res_model">my.model</field>
        <field name="view_mode">tree,form</field>
        <field name="view_id" ref="view_my_model_tree"/>
        <field name="help" type="html">
            <p class="oe_view_nocontent_create">
                Create and manage your custom records here.
            </p>
        </field>
    </record>
    
    <!-- Menu Items -->
    <menuitem id="menu_my_model_root" name="My Module" 
                  parent="base.menu_custom" 
                  sequence="10"/>
    <menuitem id="menu_my_model" name="My Models" 
                  parent="menu_my_model_root" 
                  action="action_my_model" 
                  sequence="10"/>
</odoo>
```

### View Types

- **`tree`**: List view for multiple records
- **`form`**: Detail view for single record
- **`search`**: Search and filter view
- **`kanban`**: Card-based view
- **`calendar`**: Calendar view
- **`graph`**: Chart view
- **`pivot`**: Pivot table view

## Controller Development

### Creating Web Controllers

Controllers handle HTTP requests and web functionality:

```python
# controllers/my_controller.py
from odoo import http
from odoo.http import request, content_disposition
import json

class MyController(http.Controller):
    
    @http.route('/my_module/data', type='json', auth='user')
    def get_my_data(self, **kwargs):
        """Return JSON data for my model"""
        records = request.env['my.model'].search([])
        data = []
        for record in records:
            data.append({
                'id': record.id,
                'name': record.name,
                'description': record.description,
                'date': record.date_field.strftime('%Y-%m-%d %H:%M:%S'),
            })
        return data
    
    @http.route('/my_module/form', type='http', auth='user', website=True)
    def my_form_page(self):
        """Render a custom form page"""
        return request.render('my_module.custom_form', {
            'user': request.env.user,
            'company': request.env.company,
        })
    
    @http.route('/my_module/export', type='http', auth='user')
    def export_data(self, **kwargs):
        """Export data as CSV"""
        records = request.env['my.model'].search([])
        csv_content = self._generate_csv(records)
        
        return request.make_response(
            csv_content,
            headers=[
                ('Content-Type', 'text/csv'),
                ('Content-Disposition', content_disposition('export.csv', 'csv')),
            ]
        )
    
    def _generate_csv(self, records):
        """Generate CSV content from records"""
        lines = ['Name,Description,Date\n']
        for record in records:
            lines.append(f'"{record.name}","{record.description}","{record.date_field}"\n')
        return ''.join(lines)
```

### Route Types

- **`type='json'`**: Returns JSON responses
- **`type='http'`**: Returns HTML responses
- **`auth='user'`**: Requires authenticated user
- **`auth='public'`**: Public access
- **`website=True`**: Website integration

## Static Files Management

### JavaScript Files

```javascript
// static/src/js/my_module.js
odoo.define('my_module.main', function (require) {
    "use strict";
    
    var core = require('web.core');
    var Widget = require('web.Widget');
    
    var MyWidget = Widget.extend({
        template: 'my_module.MyWidget',
        events: {
            'click .my_button': 'onButtonClick',
        },
        
        init: function (parent) {
            this._super.apply(this, arguments);
            this.title = 'My Custom Widget';
        },
        
        onButtonClick: function (ev) {
            ev.preventDefault();
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'my.model',
                views: [[false, 'form']],
                target: 'current',
            });
        },
    });
    
    core.action_registry.add('my_widget', MyWidget);
    
    return {
        'MyWidget': MyWidget,
    };
});
```

### CSS Files

```scss
// static/src/scss/my_module.scss
.o_my_module {
    .my_container {
        padding: 16px;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        background-color: #ffffff;
    }
    
    .my_button {
        background-color: #00a650;  /* UniERP primary color */
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        cursor: pointer;
        
        &:hover {
            background-color: #0088cc;
        }
        
        &:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
    }
    
    .my_form {
        .o_field {
            margin-bottom: 8px;
        }
        
        .o_field_label {
            font-weight: bold;
            color: #333333;
        }
    }
}
```

## Security Implementation

### Access Control

Create security rules in `security/ir.model.access.csv`:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model,base.group_user,1,1,1,0
access_my_model_manager,my.model,base.group_system,1,1,1,1
```

### Record Rules

Define record-level access rules:

```xml
<!-- security/my_model_security.xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="rule_my_model_company" model="ir.rule">
        <field name="name">My Model Company Rule</field>
        <field name="model_id" ref="model_my_model"/>
        <field name="domain_force">[('company_id', '=', user.company_id.id)]</field>
        <field name="groups" eval="[(4, ref('base.group_user'))]"/>
        <field name="perm_read" eval="True"/>
        <field name="perm_write" eval="True"/>
        <field name="perm_create" eval="True"/>
        <field name="perm_unlink" eval="False"/>
    </record>
</odoo>
```

## Testing Your Module

### Unit Tests

```python
# tests/test_my_module.py
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestMyModel(TransactionCase):
    
    def setUp(self):
        super(TestMyModel, self).setUp()
        self.MyModel = self.env['my.model']
    
    def test_create_my_model(self):
        """Test creating a new record"""
        record = self.MyModel.create({
            'name': 'Test Record',
            'description': 'Test Description',
        })
        self.assertTrue(record)
        self.assertEqual(record.name, 'Test Record')
    
    def test_name_constraint(self):
        """Test name validation constraint"""
        with self.assertRaises(ValidationError):
            self.MyModel.create({
                'name': 'AB',  # Too short
                'description': 'Test Description',
            })
    
    def test_compute_display_name(self):
        """Test computed display name"""
        record = self.MyModel.create({
            'name': 'Test Name',
            'description': 'Long Description Text',
        })
        expected = 'Test Name - Long Description Te'
        self.assertEqual(record.display_name, expected)
    
    def test_active_default(self):
        """Test default active value"""
        record = self.MyModel.create({
            'name': 'Test Record',
        })
        self.assertTrue(record.active)
```

### Integration Tests

```python
# tests/test_my_module_integration.py
from odoo.tests.common import HttpCase
import json

class TestMyModuleIntegration(HttpCase):
    
    def test_json_endpoint(self):
        """Test JSON endpoint functionality"""
        response = self.url_open('/my_module/data')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIsInstance(data, list)
    
    def test_web_page_access(self):
        """Test web page access control"""
        # Test unauthorized access
        response = self.url_open('/my_module/form')
        self.assertEqual(response.status_code, 200)  # Should redirect to login
        
        # Test authenticated access
        self.authenticate('admin', 'admin')
        response = self.url_open('/my_module/form')
        self.assertEqual(response.status_code, 200)
```

## Module Packaging

### Preparing for Distribution

1. **Update Version**: Increment version in `__manifest__.py`
2. **Update Changelog**: Add changes to `CHANGELOG.md`
3. **Test Thoroughly**: Run all tests
4. **Documentation**: Update README and docs
5. **Create Archive**: Package for distribution

### Version Management

```python
# __manifest__.py
{
    'version': '16.0.1.1.0',  # Increment version
    # ... other fields
}
```

### Creating Archive

```bash
# Create distribution archive
cd /path/to/my_module
tar -czf my_module-16.0.1.1.0.tar.gz \
    --exclude='.git*' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='tests' \
    .
```

## Deployment Procedures

### Local Deployment

```bash
# Install module in development
./odoo-bin -d unierp_dev -i my_module_path --update=my_module

# Update existing module
./odoo-bin -d unierp_dev -u my_module
```

### Production Deployment

1. **Backup Database**: Create full backup
2. **Test Environment**: Deploy to staging first
3. **Install Module**: Use app store or manual upload
4. **Verify Functionality**: Test all features
5. **Monitor Performance**: Check system impact

## Best Practices

### Code Quality

- **Follow PEP 8**: Python style guidelines
- **Use Meaningful Names**: Clear variable and function names
- **Document Code**: Comprehensive docstrings
- **Handle Exceptions**: Proper error handling
- **Validate Input**: Data validation and sanitization

### Performance Optimization

- **Database Indexing**: Add indexes for frequent queries
- **Batch Operations**: Use create/write in batches
- **Caching**: Implement appropriate caching
- **Lazy Loading**: Load data only when needed

### Security Considerations

- **Validate Input**: Sanitize all user input
- **Access Control**: Implement proper permissions
- **SQL Injection**: Use ORM methods, not raw SQL
- **XSS Prevention**: Escape output properly

## Troubleshooting

### Common Issues

1. **Module Not Visible**: Check `installable` and `application` flags
2. **Import Errors**: Verify `__init__.py` files
3. **Access Denied**: Check security rules and groups
4. **Performance Issues**: Review database queries and indexes
5. **Display Problems**: Check view arch syntax and CSS

### Debug Mode

Enable debug mode for development:

```bash
./odoo-bin -d unierp_dev --dev=reload,qweb,werkzeug,xml
```

### Getting Help

- **Documentation**: https://www.uslbd.com/documentation
- **Community**: https://www.uslbd.com/community
- **Support**: https://www.uslbd.com/support

---

This comprehensive module development guide provides the foundation for creating robust, secure, and efficient UniERP modules that follow established best practices and integrate seamlessly with the UniERP ecosystem.