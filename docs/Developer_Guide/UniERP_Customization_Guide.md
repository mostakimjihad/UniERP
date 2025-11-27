# UniERP Customization Guide

## Overview

This comprehensive guide provides developers and administrators with detailed instructions for customizing UniERP to meet specific business requirements, covering UI customization, workflow modifications, and system extensions.

## Table of Contents

1. [Customization Overview](#customization-overview)
2. [UI Customization](#ui-customization)
3. [Workflow Customization](#workflow-customization)
4. [Report Customization](#report-customization)
5. [Field Customization](#field-customization)
6. [Module Customization](#module-customization)
7. [Theme Development](#theme-development)
8. [Security Customization](#security-customization)
9. [Integration Customization](#integration-customization)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

## Customization Overview

### Customization Layers

UniERP supports multiple customization layers:

1. **Configuration Changes**: System settings and parameters
2. **UI Customization**: User interface modifications
3. **Workflow Customization**: Business process adaptations
4. **Module Development**: Custom functionality extensions
5. **Theme Customization**: Visual appearance changes

### Customization Tools

- **System Parameters**: Configuration settings
- **Studio**: Visual customization tool
- **Developer Mode**: Advanced customization access
- **Custom Modules**: Extended functionality
- **Themes**: Appearance and layout changes

## UI Customization

### View Customization

#### Custom Form Views

```xml
<!-- Custom form view with additional fields -->
<record id="view_custom_partner_form" model="ir.ui.view">
    <field name="name">res.partner.form.custom</field>
    <field name="model">res.partner</field>
    <field name="inherit_id" ref="base.view_partner_form"/>
    <field name="arch" type="xml">
        <form string="Custom Partner">
            <xpath expr="//field[@name='name']" position="after">
                <field name="custom_field" string="Custom Field" 
                       optional="show"/>
            </xpath>
            <xpath expr="//sheet" position="inside">
                <group string="Custom Information">
                    <field name="custom_field"/>
                    <field name="another_custom_field"/>
                </group>
            </xpath>
        </form>
    </field>
</record>
```

#### Custom List Views

```xml
<!-- Custom tree view with additional columns -->
<record id="view_custom_partner_tree" model="ir.ui.view">
    <field name="name">res.partner.tree.custom</field>
    <field name="model">res.partner</field>
    <field name="inherit_id" ref="base.view_partner_tree"/>
    <field name="arch" type="xml">
        <tree string="Custom Partners">
            <xpath expr="//field[@name='display_name']" position="after">
                <field name="custom_field"/>
            </xpath>
        </tree>
    </field>
</record>
```

#### Custom Search Views

```xml
<!-- Custom search view with additional filters -->
<record id="view_custom_partner_search" model="ir.ui.view">
    <field name="name">res.partner.search.custom</field>
    <field name="model">res.partner</field>
    <field name="inherit_id" ref="base.view_partner_filter"/>
    <field name="arch" type="xml">
        <search string="Custom Partner Search">
            <xpath expr="//filter" position="inside">
                <filter string="Custom Filter" name="custom_filter" 
                        domain="[('custom_field', '=', True)]"/>
            </xpath>
        </search>
    </field>
</record>
```

### Menu Customization

#### Custom Menu Items

```xml
<!-- Custom menu structure -->
<menuitem id="menu_custom_root" name="Custom Module" 
                  parent="base.menu_custom" 
                  sequence="10"/>
<menuitem id="menu_custom_partners" name="Custom Partners" 
                  parent="menu_custom_root" 
                  action="action_custom_partners" 
                  sequence="10"/>
<menuitem id="menu_custom_reports" name="Custom Reports" 
                  parent="menu_custom_root" 
                  action="action_custom_reports" 
                  sequence="20"/>
```

#### Action Customization

```xml
<!-- Custom window actions -->
<record id="action_custom_partners" model="ir.actions.act_window">
    <field name="name">Custom Partners</field>
    <field name="res_model">res.partner</field>
    <field name="view_mode">tree,form</field>
    <field name="view_id" ref="view_custom_partner_tree"/>
    <field name="domain">[('custom_field', '=', True)]</field>
    <field name="context">{'default_custom_field': True}</field>
    <field name="help" type="html">
        <p class="oe_view_nocontent_create">
            Manage custom partner records with additional fields.
        </p>
    </field>
</record>
```

### CSS Customization

#### Custom Stylesheets

```xml
<!-- Custom assets -->
<record id="assets_custom" model="ir.asset">
    <field name="name">custom.assets</field>
    <field name="bundle">web.assets_backend</field>
    <field name="sequence">16</field>
    <field name="inherit_id" ref="web.assets_backend"/>
    <field name="arch" type="xml">
        <xpath expr="//link[last()]" position="after">
            <link rel="stylesheet" type="text/scss" href="/custom/static/src/scss/custom_styles.scss"/>
        </xpath>
    </field>
</record>
```

#### Custom SCSS

```scss
// static/src/scss/custom_styles.scss
.o_custom_module {
    .custom_field {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 4px;
        padding: 8px;
        margin-bottom: 16px;
    }
    
    .custom_button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        
        &:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        &:active {
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
    }
    
    .custom_form {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        padding: 24px;
        
        .o_group {
            margin-bottom: 20px;
        }
        
        .o_field {
            margin-bottom: 12px;
            
            .o_field_label {
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 4px;
            }
        }
    }
}
```

## Workflow Customization

### Automated Actions

#### Custom Server Actions

```xml
<!-- Custom server actions -->
<record id="action_custom_workflow" model="ir.actions.server">
    <field name="name">Custom Workflow Action</field>
    <field name="model_id" ref="model_custom_model"/>
    <field name="state">code</field>
    <field name="code">
# Custom workflow logic
for record in env['custom.model'].browse(env.context.get('active_ids', [])):
    if record.custom_field:
        # Process custom logic
        record.write({
            'processed': True,
            'processed_date': fields.Datetime.now()
        })
        
# Return action result
env['bus.bus'].sendone(
    'custom_workflow',
    {
        'type': 'success',
        'message': 'Custom workflow completed successfully',
        'record_id': record.id
    }
)
    </field>
    <field name="help" type="html">
        <p>Execute custom workflow on selected records.</p>
    </field>
</record>
```

### Workflow Transitions

#### Custom Workflow Definition

```xml
<!-- Custom workflow -->
<record id="workflow_custom" model="workflow">
    <field name="name">Custom Workflow</field>
    <field name="osv">custom.model</field>
    <field name="on_create">True</field>
    
    <!-- Workflow nodes -->
    <field name="node" eval="[
        {
            'kind': 'function',
            'name': 'draft',
            'action': '_draft_action',
            'flow_start': True
        },
        {
            'kind': 'function',
            'name': 'process',
            'action': '_process_action',
            'transition': 'draft_to_process'
        },
        {
            'kind': 'function',
            'name': 'done',
            'action': '_done_action',
            'transition': 'process_to_done'
        }
    ]"/>
    
    <!-- Workflow transitions -->
    <field name="transition" eval="[
        {
            'source': 'draft',
            'dest': 'process',
            'signal': 'process_draft',
            'condition': 'True'
        },
        {
            'source': 'process',
            'dest': 'done',
            'signal': 'process_done',
            'condition': 'True'
        }
    ]"/>
</record>
```

## Report Customization

### Custom Report Views

#### QWeb Report Templates

```xml
<!-- Custom report template -->
<template id="report_custom_partner_document">
    <t t-call="web.html_container">
        <t t-set="title">Custom Partner Report</t>
        <div class="header">
            <h2>Custom Partner Report</h2>
            <div class="company_info">
                <span t-esc="company.name"/>
                <span t-esc="company.partner_id.street"/>
                <span t-esc="company.partner_id.city"/>, 
                <span t-esc="company.partner_id.country_id.name"/>
            </div>
        </div>
        <div class="content">
            <t t-foreach="docs" t-as="doc">
                <div class="document">
                    <h3 t-esc="doc.name"/>
                    <div class="document_info">
                        <span><strong>Partner:</strong> <t t-esc="doc.partner_id.name"/></span>
                        <span><strong>Date:</strong> <t t-esc="doc.date"/></span>
                        <span><strong>Custom Field:</strong> <t t-esc="doc.custom_field"/></span>
                    </div>
                </div>
            </t>
        </div>
    </t>
</template>
```

#### Custom Report Actions

```xml
<!-- Custom report action -->
<record id="action_report_custom_partner" model="ir.actions.report">
    <field name="name">Custom Partner Report</field>
    <field name="model">custom.model</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">custom.partner_document</field>
    <field name="report_file">custom_partner_report.pdf</field>
    <field name="binding_model_id" ref="model_custom_model"/>
    <field name="binding_type">report</field>
    <field name="print_report_name">'Custom Partner Report'</field>
</record>
```

### Custom Report Paper Format

```xml
<!-- Custom paper format -->
<record id="paperformat_custom" model="report.paperformat">
    <field name="name">Custom Format</field>
    <field name="default" eval="True"/>
    <field name="format">A4</field>
    <field name="width">210</field>
    <field name="height">297</field>
    <field name="margin_top">20</field>
    <field name="margin_bottom">20</field>
    <field name="margin_left">20</field>
    <field name="margin_right">20</field>
    <field name="header_spacing">10</field>
    <field name="header_line" eval="False"/>
</record>
```

## Field Customization

### Custom Field Types

#### Computed Fields

```python
# models/custom_model.py
from odoo import models, fields, api

class CustomModel(models.Model):
    _name = 'custom.model'
    
    # Regular field
    regular_field = fields.Char(string='Regular Field')
    
    # Computed field
    @api.depends('regular_field')
    def _compute_computed_field(self):
        for record in self:
            if record.regular_field:
                record.computed_field = f'Computed: {record.regular_field}'
            else:
                record.computed_field = 'No regular field'
    
    computed_field = fields.Char(
        string='Computed Field',
        compute='_compute_computed_field',
        store=True,
        help='Automatically computed based on regular field'
    )
```

#### Related Fields

```python
class CustomModel(models.Model):
    # ... other fields ...
    
    # Related field
    related_partner_id = fields.Many2one(
        'res.partner',
        string='Related Partner',
        compute='_compute_related_partner',
        store=True,
        help='Related partner based on business logic'
    )
    
    @api.depends('other_field')
    def _compute_related_partner(self):
        for record in self:
            if record.other_field:
                # Find partner based on business logic
                partner = self.env['res.partner'].search([
                    ('custom_business_id', '=', record.other_field)
                ], limit=1)
                record.related_partner_id = partner.id if partner else False
```

#### Selection Fields

```python
class CustomModel(models.Model):
    # Selection field with dynamic options
    status = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ], string='Status', default='draft')
    
    # Dynamic selection based on configuration
    @api.model
    def _get_selection_options(self):
        options = [
            ('option1', 'Option 1'),
            ('option2', 'Option 2'),
        ]
        
        # Add custom options from system parameters
        custom_options = self.env['ir.config_parameter'].get_param('custom.selection_options', '')
        if custom_options:
            for option in custom_options.split(','):
                if ':' in option:
                    key, value = option.split(':', 1)
                    options.append((key.strip(), value.strip()))
        
        return options
    
    dynamic_field = fields.Selection(
        selection='_get_selection_options',
        string='Dynamic Field',
        help='Field with dynamic selection options'
    )
```

## Module Customization

### Inheriting Existing Models

#### Model Extension

```python
# models/res_partner_extension.py
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    # Add custom fields
    custom_field = fields.Char(
        string='Custom Field',
        help='Custom field for partner'
    )
    
    another_custom_field = fields.Boolean(
        string='Another Custom Field',
        default=False,
        help='Another custom field'
    )
    
    # Override methods
    def write(self, vals):
        # Custom validation logic
        if 'custom_field' in vals:
            vals['custom_field'] = vals['custom_field'].strip().title()
        
        # Call parent method
        return super(ResPartner, self).write(vals)
```

#### View Extension

```xml
<!-- Extend existing views -->
<record id="view_extended_partner_form" model="ir.ui.view">
    <field name="name">res.partner.form.extended</field>
    <field name="model">res.partner</field>
    <field name="inherit_id" ref="base.view_partner_form"/>
    <field name="arch" type="xml">
        <form string="Extended Partner Form">
            <xpath expr="//field[@name='phone']" position="after">
                <field name="custom_field" string="Custom Field" 
                       attrs="{'invisible': [('company_type', '=', 'person')]}"/>
            </xpath>
            <xpath expr="//sheet" position="inside">
                <group string="Custom Information">
                    <field name="custom_field"/>
                    <field name="another_custom_field"/>
                </group>
            </xpath>
        </form>
    </field>
</record>
```

## Theme Development

### Theme Structure

```
custom_theme/
├── __init__.py
├── __manifest__.py
├── static/
│   ├── src/
│   │   ├── scss/
│   │   │   ├── primary.scss
│   │   │   ├── variables.scss
│   │   │   └── components.scss
│   │   ├── js/
│   │   │   └── theme.js
│   │   └── img/
│   │       └── logo.png
│   └── description/
│       └── icon.png
├── views/
│   └── assets.xml
└── data/
    └── ir_ui_view.xml
```

### Theme Manifest

```python
# __manifest__.py
{
    'name': 'Custom UniERP Theme',
    'version': '16.0.1.0.0',
    'category': 'Theme',
    'summary': 'Custom theme for UniERP',
    'description': '''
        A custom theme that modifies the appearance of UniERP
        with custom colors, fonts, and layout.
    ''',
    'author': 'Your Name',
    'website': 'https://www.uslbd.com',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'views/assets.xml',
        'data/ir_ui_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_theme/static/src/scss/*.scss',
            'custom_theme/static/src/js/*.js',
        ],
        'web.assets_frontend': [
            'custom_theme/static/src/scss/*.scss',
        'custom_theme/static/src/js/*.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
```

### Custom SCSS Variables

```scss
// static/src/scss/variables.scss
:root {
    // Primary colors
    --unierp-primary: #00a650;
    --unierp-secondary: #6c757d;
    --unierp-success: #28a745;
    --unierp-warning: #ffc107;
    --unierp-danger: #dc3545;
    --unierp-info: #17a2b8;
    
    // Neutral colors
    --unierp-light: #f8f9fa;
    --unierp-dark: #343a40;
    --unierp-white: #ffffff;
    --unierp-gray: #6c757d;
    
    // Typography
    --unierp-font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --unierp-font-size-base: 0.875rem;
    --unierp-font-size-lg: 1.125rem;
    
    // Spacing
    --unierp-spacing-xs: 0.25rem;
    --unierp-spacing-sm: 0.5rem;
    --unierp-spacing-md: 1rem;
    --unierp-spacing-lg: 1.5rem;
    --unierp-spacing-xl: 3rem;
    
    // Border radius
    --unierp-border-radius: 0.375rem;
    --unierp-border-radius-lg: 0.5rem;
    
    // Shadows
    --unierp-shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
    --unierp-shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
    --unierp-shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}
```

### Custom Component Styles

```scss
// static/src/scss/components.scss
@import 'variables';

.o_unierp_theme {
    // Custom button styles
    .btn-primary {
        background-color: var(--unierp-primary);
        border-color: var(--unierp-primary);
        color: var(--unierp-white);
        
        &:hover {
            background-color: darken(var(--unierp-primary), 10%);
            border-color: darken(var(--unierp-primary), 10%);
        }
    }
    
    // Custom card styles
    .card {
        background-color: var(--unierp-white);
        border: 1px solid var(--unierp-gray);
        border-radius: var(--unierp-border-radius);
        box-shadow: var(--unierp-shadow-sm);
        
        .card-header {
            background-color: var(--unierp-light);
            border-bottom: 1px solid var(--unierp-gray);
            padding: var(--unierp-spacing-md);
        }
        
        .card-body {
            padding: var(--unierp-spacing-lg);
        }
    }
    
    // Custom form styles
    .form-control {
        border: 1px solid var(--unierp-gray);
        border-radius: var(--unierp-border-radius);
        padding: var(--unierp-spacing-sm) var(--unierp-spacing-md);
        font-family: var(--unierp-font-family);
        
        &:focus {
            border-color: var(--unierp-primary);
            box-shadow: 0 0 0 3px rgba(var(--unierp-primary), 0.1);
        }
    }
}
```

## Security Customization

### Custom Access Rights

```xml
<!-- security/custom_security.xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Custom access rights -->
    <record id="group_custom_user" model="res.groups">
        <field name="name">Custom User Group</field>
        <field name="comment">Users with access to custom functionality</field>
        <field name="category_id" ref="base.module_category_usability"/>
        <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
    </record>
    
    <!-- Custom access rules -->
    <record id="rule_custom_model" model="ir.rule">
        <field name="name">Custom Model Rule</field>
        <field name="model_id" ref="model_custom_model"/>
        <field name="domain_force">[('company_id', '=', user.company_id.id)]</field>
        <field name="groups" eval="[(4, ref('group_custom_user'))]"/>
        <field name="perm_read" eval="True"/>
        <field name="perm_write" eval="True"/>
        <field name="perm_create" eval="True"/>
        <field name="perm_unlink" eval="False"/>
    </record>
</odoo>
```

### Custom Record Rules

```xml
<!-- Custom record rules -->
<record id="rule_custom_model_restricted" model="ir.rule">
    <field name="name">Custom Model Restricted Rule</field>
    <field name="model_id" ref="model_custom_model"/>
    <field name="domain_force">[
        ('company_id', '=', user.company_id.id),
        '|',
        ('user_id', '=', user.id)
    ]</field>
    <field name="groups" eval="[(4, ref('group_custom_manager'))]"/>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="True"/>
    <field name="perm_create" eval="True"/>
    <field name="perm_unlink" eval="True"/>
</record>
```

## Integration Customization

### External API Integration

```python
# models/external_integration.py
from odoo import models, fields, api
import requests
import json

class ExternalIntegration(models.Model):
    _name = 'external.integration'
    _description = 'External API Integration Configuration'
    
    name = fields.Char(string='Integration Name', required=True)
    api_endpoint = fields.Char(string='API Endpoint', required=True)
    api_key = fields.Char(string='API Key', password=True)
    active = fields.Boolean(string='Active', default=True)
    last_sync = fields.Datetime(string='Last Synchronization')
    
    @api.model
    def sync_data(self):
        """Synchronize data with external API"""
        for integration in self.search([('active', '=', True)]]:
            try:
                response = requests.get(
                    integration.api_endpoint,
                    headers={'Authorization': f'Bearer {integration.api_key}'},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self._process_external_data(data, integration)
                    integration.write({
                        'last_sync': fields.Datetime.now()
                    })
                else:
                    integration.message_post(
                        f'Sync failed: {response.status_code}',
                        f'Error: {response.text}'
                    )
                    
            except Exception as e:
                integration.message_post(f'Sync error: {str(e)}')
    
    def _process_external_data(self, data, integration):
        """Process external data and create/update records"""
        # Custom processing logic here
        pass
```

### Webhook Integration

```python
# controllers/webhook_controller.py
from odoo import http
from odoo.http import request, json
import hmac
import hashlib

class WebhookController(http.Controller):
    
    @http.route('/webhook/external', type='json', auth='public', methods=['POST'])
    def handle_webhook(self):
        """Handle external webhook notifications"""
        # Verify webhook signature
        signature = request.httprequest.headers.get('X-Webhook-Signature')
        payload = request.jsonrequest
        
        if not self._verify_webhook_signature(payload, signature):
            return {'error': 'Invalid signature'}
        
        # Process webhook data
        event_type = payload.get('event')
        if event_type == 'order.created':
            self._handle_order_created(payload)
        elif event_type == 'order.updated':
            self._handle_order_updated(payload)
        
        return {'status': 'success'}
    
    def _verify_webhook_signature(self, payload, signature):
        """Verify webhook signature using HMAC"""
        secret = request.env['ir.config_parameter'].get_param('webhook.secret')
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            json.dumps(payload, sort_keys=True).encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
    
    def _handle_order_created(self, payload):
        """Handle order creation webhook"""
        order_data = payload.get('data', {})
        # Create or update order record
        request.env['sale.order'].create(order_data)
```

## Best Practices

### Customization Guidelines

1. **Use Inheritance**: Extend existing functionality rather than modifying core
2. **Follow Standards**: Maintain coding and documentation standards
3. **Test Thoroughly**: Test all customizations in development and staging
4. **Document Changes**: Maintain clear documentation of customizations
5. **Version Control**: Use proper version control for all customizations
6. **Backup Regularly**: Backup customizations before updates
7. **Security First**: Implement proper access controls and validation
8. **Performance Awareness**: Consider impact of customizations on performance

### Maintenance Considerations

1. **Update Compatibility**: Ensure customizations work with UniERP updates
2. **Dependency Management**: Track and update custom dependencies
3. **Database Impact**: Monitor database size and performance
4. **User Training**: Provide training for custom features
5. **Rollback Planning**: Have rollback procedures for failed customizations

## Troubleshooting

### Common Customization Issues

1. **View Inheritance Problems**
   - **Issue**: Custom views not appearing
   - **Solution**: Check XPath expressions and view inheritance chains
   - **Debug**: Enable developer mode to inspect view structure

2. **Field Access Errors**
   - **Issue**: Permission denied on custom fields
   - **Solution**: Verify access rights and group assignments
   - **Debug**: Check security rules and user groups

3. **Performance Issues**
   - **Issue**: Slow performance after customization
   - **Solution**: Review computed fields and database queries
   - **Debug**: Enable SQL logging and query analysis

4. **Theme Conflicts**
   - **Issue**: Custom styles not applying
   - **Solution**: Check asset loading order and CSS specificity
   - **Debug**: Inspect browser developer tools for CSS conflicts

### Debug Mode

Enable comprehensive debugging:

```bash
./odoo-bin -d unierp_dev --dev=reload,qweb,werkzeug,xml,sql
```

### Getting Help

- **Documentation**: https://www.uslbd.com/documentation/customization
- **Community**: https://www.uslbd.com/community/customization
- **Support**: https://www.uslbd.com/support/customization

---

This comprehensive customization guide provides developers with the knowledge and tools needed to successfully customize UniERP for specific business requirements while maintaining system integrity and following best practices.