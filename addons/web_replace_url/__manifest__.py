# Copyright 2018 Simone Orsi - Camptocamp SA
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
{
    "name": "UniERP URL Replace",
    'version': '19.0.3',
    "author": "UniERP",
    'support': 'support@unierp.com',
    "summary": "URL Replace link for UniERP",
    "description":"UniERP Replace odoo in hyperlink",
    "category": "Extra Tools",
    "license": "LGPL-3",
	'images': ['static/description/main_banner.png'],
    "depends": ["web",'base'],
    "application": False,
    "installable": True,
    "data": [
          'data/data.xml',
          'views/ir_config_parameter_views.xml'
      ],
    "assets": {
        "web.assets_backend": [
            "web_replace_url/static/src/**/*",
        ],
    },
    "installable": True,
    'uninstall_hook': '_uninstall_cleanup',
    'auto_install': True,
    'post_init_hook': '_post_init_hook',
}
