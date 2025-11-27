/* Copyright 2024 UniERP
 * License AGPL-3.0 or later
 */

odoo.define('web.HelpSidebar', function (require) {
    'useStrict': false,
    'core': require('web.core'),
    'rpc': require('web.rpc'),
];

var HelpSidebar = Widget.extend({
    template: 'web.HelpSidebar',
    events: {
        'click': '_onHelpClick',
        'toggle': '_onHelpToggle',
    },

    /**
     * @constructor
     * @param {Widget} parent
     * @param {Object} services
     */
    init: function (parent, services) {
        this._super(parent, services);
        this.helpData = {};
        this.isExpanded = false;
    },

    /**
     * @override
     */
    willStart: function () {
        this._super.apply(this, arguments);
        this._loadHelpContent();
    },

    /**
     * Load help content from UniERP help system
     * @private
     */
    _loadHelpContent: function () {
        var self = this;
        self._rpc({
            model: 'ir.help',
            method: 'search_read',
            args: [
                [['active', '=', true]],
                ['name', 'content', 'category', 'url']
            ],
            kwargs: {context: self.getSession().user_context}
        }).then(function (result) {
            if (result && result.length > 0) {
                self.helpData = {};
                result.forEach(function (help) {
                    self.helpData[help.name] = help;
                });
                self._renderHelpContent();
            }
        });
    },

    /**
     * Render help content in sidebar
     * @private
     */
    _renderHelpContent: function () {
        var self = this;
        var categories = self._organizeHelpByCategory();
        
        var $helpContainer = self.$('.o_help_content');
        $helpContainer.empty();
        
        // Render help categories
        Object.keys(categories).forEach(function (category) {
            var $category = $('<div class="o_help_category">')
                .append($('<h3 class="o_help_category_title">')
                    .text(category.title)
                    .append($('<button class="o_help_category_toggle fa fa-chevron-down">')
                        .on('click', function () {
                            self._toggleCategory(category.name);
                        })
                )
                .append($('<div class="o_help_category_content">'));
            
            // Render help items in category
            if (categories[category.name] && categories[category.name].items.length > 0) {
                categories[category.name].items.forEach(function (item) {
                    var $item = $('<div class="o_help_item">')
                        .append($('<h4 class="o_help_item_title">')
                            .text(item.title)
                            .append($('<a class="o_help_item_link" href="' + item.url + '" target="_blank">')
                                .text(item.content)
                        )
                        .append($('<div class="o_help_item_description">')
                            .text(item.description)
                        );
                    
                    $category.find('.o_help_category_content').append($item);
                });
            }
            
            $helpContainer.append($category);
        });
        
        // Add UniERP branding
        var $branding = $('<div class="o_help_branding">')
            .append($('<p class="o_help_branding_text">')
                .text('Powered by UniERP Help System')
            .append($('<a href="https://www.uslbd.com/help" target="_blank" class="o_help_branding_link">')
                .text('Visit UniERP Documentation')
            );
        
        $helpContainer.append($branding);
    },

    /**
     * Organize help content by category
     * @private
     * @returns {Object} Help content organized by category
     */
    _organizeHelpByCategory: function () {
        var self = this;
        return {
            'getting_started': {
                title: 'Getting Started',
                items: [
                    {
                        title: 'UniERP Overview',
                        content: 'Learn the basics of UniERP system',
                        url: 'https://www.uslbd.com/documentation/getting-started'
                    },
                    {
                        title: 'System Requirements',
                        content: 'Hardware and software requirements for UniERP',
                        url: 'https://www.uslbd.com/documentation/system-requirements'
                    },
                    {
                        title: 'Installation Guide',
                        content: 'Step-by-step installation instructions',
                        url: 'https://www.uslbd.com/documentation/installation'
                    }
                ]
            },
            'user_guide': {
                title: 'User Guide',
                items: [
                    {
                        title: 'Dashboard Navigation',
                        content: 'How to navigate the UniERP dashboard',
                        url: 'https://www.uslbd.com/documentation/dashboard'
                    },
                    {
                        title: 'Common Tasks',
                        content: 'Frequently performed operations',
                        url: 'https://www.uslbd.com/documentation/common-tasks'
                    },
                    {
                        title: 'Module Guides',
                        content: 'Documentation for all UniERP modules',
                        url: 'https://www.uslbd.com/documentation/modules'
                    }
                ]
            },
            'admin_guide': {
                title: 'Administrator Guide',
                items: [
                    {
                        title: 'System Configuration',
                        content: 'Configure UniERP system settings',
                        url: 'https://www.uslbd.com/documentation/configuration'
                    },
                    {
                        title: 'Security Setup',
                        content: 'Security and access control',
                        url: 'https://www.uslbd.com/documentation/security'
                    },
                    {
                        title: 'Backup & Recovery',
                        content: 'Data backup and recovery procedures',
                        url: 'https://www.uslbd.com/documentation/backup'
                    }
                ]
            },
            'troubleshooting': {
                title: 'Troubleshooting',
                items: [
                    {
                        title: 'Common Issues',
                        content: 'Solutions to frequent problems',
                        url: 'https://www.uslbd.com/documentation/common-issues'
                    },
                    {
                        title: 'Error Messages',
                        content: 'Understanding error codes',
                        url: 'https://www.uslbd.com/documentation/error-messages'
                    },
                    {
                        title: 'Contact Support',
                        content: 'Get help from UniERP team',
                        url: 'https://www.uslbd.com/support'
                    }
                ]
            },
            'search': {
                title: 'Search Help',
                items: [
                    {
                        title: 'Search Tips',
                        content: 'How to find help effectively',
                        url: 'https://www.uslbd.com/documentation/search-tips'
                    },
                    {
                        title: 'Advanced Search',
                        content: 'Using search operators and filters',
                        url: 'https://www.uslbd.com/documentation/advanced-search'
                    }
                ]
            }
        };
    },

    /**
     * Toggle help category expansion
     * @private
     * @param {String} categoryName
     */
    _toggleCategory: function (categoryName) {
        var self = this;
        var $category = self.$('.o_help_category[data-category="' + categoryName + '"]');
        var $content = $category.find('.o_help_category_content');
        
        if (self.isExpanded) {
            $content.slideUp();
            $category.find('.o_help_category_toggle').removeClass('fa-chevron-down').addClass('fa-chevron-up');
        } else {
            $content.slideDown();
            $category.find('.o_help_category_toggle').removeClass('fa-chevron-up').addClass('fa-chevron-down');
        }
        
        self.isExpanded = !self.isExpanded;
    },

    /**
     * Handle help item click
     * @private
     * @param {Event} event
     */
    _onHelpClick: function (event) {
        event.preventDefault();
        var $item = $(event.currentTarget).closest('.o_help_item');
        var url = $item.find('.o_help_item_link').attr('href');
        
        if (url && url !== '#') {
            // Track help usage for analytics
            this._rpc({
                model: 'ir.help.usage',
                method: 'create',
                args: [{
                    help_item: $item.find('.o_help_item_title').text(),
                    url: url,
                    user_id: this.getSession().user_id
                }]
            });
        }
    },
});

core.action_registry.add('help_sidebar', HelpSidebar);