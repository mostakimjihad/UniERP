# Copyright 2024 UniERP
# License AGPL-3.0 or later

from odoo import http, request
from odoo.addons.base.models.ir_help import IrHelp

import json


class HelpController(http.Controller):
    """UniERP Help System Controller"""
    
    @http.route('/help/search', type='json', auth='user', methods=['POST'], csrf=False)
    def search_help(self, **kwargs):
        """Search UniERP help content"""
        query = kwargs.get('query', '').strip()
        limit = int(kwargs.get('limit', 10))
        
        if not query:
            return {'error': 'Query parameter is required'}
        
        help_records = request.env['ir.help'].search([
            ('name', 'ilike', query),
            ('active', '=', True)
        ], limit=limit)
        
        results = []
        for help_item in help_records:
            results.append({
                'id': help_item.id,
                'name': help_item.name,
                'content': help_item.content,
                'url': help_item.url or self._get_help_url(),
                'description': help_item.description,
                'category': help_item.category
            })
        
        return {
            'success': True,
            'results': results,
            'total': len(help_records)
        }
    
    @http.route('/help/content/<int:help_id>', type='json', auth='user', methods=['GET'], csrf=False)
    def get_help_content(self, help_id):
        """Get specific UniERP help content"""
        help_item = request.env['ir.help'].browse(help_id)
        
        if not help_item or not help_item.active:
            return {'error': 'Help item not found'}
        
        # Mark help as used for analytics
        help_item.sudo().mark_help_used()
        
        return {
            'success': True,
            'help': {
                'id': help_item.id,
                'name': help_item.name,
                'content': help_item.content,
                'url': help_item.url or self._get_help_url(),
                'description': help_item.description,
                'category': help_item.category,
                'sequence': help_item.sequence
            }
        }
    
    @http.route('/help/categories', type='json', auth='user', methods=['GET'], csrf=False)
    def get_help_categories(self):
        """Get UniERP help categories"""
        categories = request.env['ir.help']._get_default_categories()
        
        return {
            'success': True,
            'categories': categories
        }
    
    @http.route('/help/context/<string:model>/<int:res_id>', type='json', auth='user', methods=['GET'], csrf=False)
    def get_context_help(self, model, res_id):
        """Get context help for specific model and record"""
        help_item = request.env['ir.help'].get_context_help(model, res_id)
        
        if not help_item:
            return {'error': 'Context help not found'}
        
        return {
            'success': True,
            'help': {
                'title': help_item.name,
                'content': help_item.content,
                'url': help_item.url or self._get_help_url()
            }
        }
    
    def _get_help_url(self):
        """Get help base URL from system parameters"""
        help_url = request.env['ir.config_parameter'].sudo().get_param('help_base_url', 'https://www.uslbd.com/help')
        return help_url