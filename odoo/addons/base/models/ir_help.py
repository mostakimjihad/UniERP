# Copyright 2024 UniERP
# License AGPL-3.0 or later

from odoo import models, fields, api, _

class IrHelp(models.Model):
    """UniERP Help System Model"""
    
    _name = 'ir.help'
    _description = 'UniERP Help System'
    _order = 'sequence, category'
    
    name = fields.Char(required=True, translate=True, help='Help item name')
    category = fields.Char(required=True, translate=True, help='Help category')
    sequence = fields.Integer(help='Display order for help items')
    content = fields.Html(translate=True, help='Help content with full HTML formatting')
    url = fields.Char(help='URL for external help resources')
    description = fields.Text(translate=True, help='Brief description of help item')
    active = fields.Boolean(default=True, help='Whether help item is active')
    is_context_help = fields.Boolean(default=False, help='Whether this is context-specific help')
    
    @api.model
    def _get_default_categories(self):
        """Get default help categories for UniERP"""
        return [
            {
                'name': 'getting_started',
                'title': 'Getting Started',
                'sequence': 10,
                'description': 'Learn the basics of UniERP system',
                'url': 'https://www.uslbd.com/documentation/getting-started'
            },
            {
                'name': 'user_guide',
                'title': 'User Guide',
                'sequence': 20,
                'description': 'How to use UniERP effectively',
                'url': 'https://www.uslbd.com/documentation/user-guide'
            },
            {
                'name': 'admin_guide',
                'title': 'Administrator Guide',
                'sequence': 30,
                'description': 'System administration and configuration',
                'url': 'https://www.uslbd.com/documentation/admin-guide'
            },
            {
                'name': 'troubleshooting',
                'title': 'Troubleshooting',
                'sequence': 40,
                'description': 'Solutions to common problems',
                'url': 'https://www.uslbd.com/documentation/troubleshooting'
            },
            {
                'name': 'search',
                'title': 'Search Help',
                'sequence': 50,
                'description': 'How to find help effectively',
                'url': 'https://www.uslbd.com/documentation/search-help'
            }
        ]
    
    @api.depends('config.parameter')
    def _get_help_url(self):
        """Get help URL from system parameters"""
        help_url = self.env['ir.config_parameter'].sudo().get_param('help_base_url', 'https://www.uslbd.com/help')
        return help_url
    
    @api.model
    def search_read(self, domain=None, limit=None):
        """Search help items based on domain"""
        domain = domain or []
        return self.search(domain)
    
    @api.model
    def get_help_content(self, category=None):
        """Get help content for specific category"""
        if category:
            help_items = self.search([('category', '=', category), ('active', '=', True)], order='sequence')
        else:
            help_items = self.search([('active', '=', True)], order='sequence')
        
        result = []
        for item in help_items:
            result.append({
                'id': item.id,
                'name': item.name,
                'content': item.content,
                'description': item.description,
                'url': item.url or self._get_help_url(),
                'category': item.category,
                'sequence': item.sequence
            })
        
        return result
    
    @api.model
    def get_context_help(self, model=None, res_id=None):
        """Get context help for specific model and record"""
        if not model or not res_id:
            return False
        
        # Look for context-specific help
        context_help = self.search([
            ('is_context_help', '=', True),
            ('model', '=', model),
            ('res_id', '=', res_id),
            ('active', '=', True)
        ])
        
        if context_help:
            return {
                'title': context_help.name,
                'content': context_help.content,
                'url': context_help.url
            }
        
        return False
    
    @api.model
    def mark_help_used(self, help_item_id):
        """Mark help item as used for analytics"""
        if help_item_id:
            help_item = self.browse(help_item_id)
            if help_item:
                # Track usage for analytics
                self._rpc({
                    model: 'ir.help.usage',
                    method: 'create',
                    args: [{
                        'help_item': help_item.id,
                        'user_id': self.env.user.id,
                        'access_time': fields.Datetime.now()
                    }]
                })
        return True
    
    @api.model
    def get_help_usage_stats(self, help_item_id=None):
        """Get usage statistics for help items"""
        domain = [('user_id', '=', self.env.user.id)]
        if help_item_id:
            domain.append(('help_item', '=', help_item_id))
        
        usage_records = self.env['ir.help.usage'].search(domain)
        
        result = {
            'total_views': len(usage_records),
            'unique_users': len(set(record.user_id for record in usage_records)),
            'most_viewed': help_item_id and max(usage_records, key=lambda x: x.help_item, default=None)
        }
        
        return result