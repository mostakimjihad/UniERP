# Contributing to UniERP

Thank you for your interest in contributing to UniERP! This document provides guidelines and information for contributors to ensure a smooth and effective collaboration process.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Submitting Issues](#submitting-issues)
5. [Feature Requests](#feature-requests)
6. [Pull Request Process](#pull-request-process)
7. [Coding Standards](#coding-standards)
8. [Testing Guidelines](#testing-guidelines)
9. [Documentation](#documentation)
10. [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:

- Gender, gender identity and expression
- Sexual orientation
- Disability
- Physical appearance
- Body size
- Race
- Age
- Religion
- Nationality

### Our Standards

Positive behavior that contributes to a healthy community includes:

- **🤝 Being respectful** of differing viewpoints and experiences
- **📚 Gracefully accepting** constructive criticism
- **🎯 Focusing** on what is best for the community
- **💡 Showing empathy** towards other community members
- **🤲 Helping** others learn and grow

Unacceptable behavior includes:

- **❌ Harassment** in any form
- **🚫 Derogatory comments** or personal attacks
- **📸 Public or private harassment**
- **🎭 Publishing** others' private information
- **🔫 Creating** an intimidating or hostile environment
- **🚫 Spamming** or disruptive behavior

### Enforcement

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned with this Code of Conduct.

#### Reporting Incidents

If you experience or witness unacceptable behavior, please report it:

- **Email**: conduct@unisoft.com.bd
- **Private Message**: Contact any project maintainer
- **Confidentiality**: All reports will be kept confidential

#### Consequences

Consequences for violating the Code of Conduct may include:

- Warning from project maintainers
- Temporary or permanent ban from the project
- Removal of contributions
- Reporting to appropriate authorities if necessary

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

1. **Git installed** and configured
2. **Python 3.10+** development environment
3. **PostgreSQL 14+** for local testing
4. **Basic knowledge** of Odoo/UniERP architecture
5. **Understanding** of our branching strategy

### Development Environment Setup

```bash
# 1. Fork the repository
# Visit https://github.com/unisoft/unierp and click "Fork"

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/unierp.git
cd unierp

# 3. Add upstream remote
git remote add upstream https://github.com/unisoft/unierp.git

# 4. Set up development environment
python3 -m venv dev-env
source dev-env/bin/activate
pip install -r requirements-dev.txt

# 5. Install pre-commit hooks
pre-commit install

# 6. Create development database
createdb unierp_dev

# 7. Configure local settings
cp etc/unierp.conf.example etc/unierp.conf
# Edit etc/unierp.conf with your local settings
```

### IDE Configuration

#### VS Code

Recommended extensions:
- Python
- Pylance
- GitLens
- Python Docstring Generator
- Better Comments

Settings (.vscode/settings.json):
```json
{
    "python.defaultInterpreterPath": "./dev-env/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": false,
    "editor.formatOnSave": true,
    "editor.rulers": [88, 120],
    "editor.wordWrap": "bounded"
}
```

#### PyCharm

Recommended settings:
- Python interpreter: dev-env/bin/python
- Code style: Black
- Inspection profile: PEP 8 + UniERP standards
- Version control: Git integration enabled

---

## Development Workflow

### 1. Create an Issue

Before starting work, create an issue to discuss your proposed change:

- **Bug fixes**: Create issue describing the bug
- **New features**: Create issue with feature proposal
- **Documentation**: Create issue describing documentation needs

### 2. Create a Branch

Follow our [branching strategy](github_docs/BRANCHING_STRATEGY.md):

```bash
# Sync with upstream
git fetch upstream
git checkout upstream/develop
git pull upstream develop

# Create feature branch
git checkout -b feature/BRAND-123-your-feature-name
```

### 3. Development Work

- **Small, focused commits**
- **Clear commit messages**
- **Regular testing**
- **Documentation updates**

### 4. Testing

- **Unit tests**: Write tests for new functionality
- **Integration tests**: Test module interactions
- **Manual testing**: Verify UI/UX changes
- **Performance testing**: Check for regressions

### 5. Submit Pull Request

- **Push to your fork**
- **Create pull request**
- **Fill out PR template**
- **Request code review**

---

## Submitting Issues

### Bug Reports

Use the bug report template below when reporting issues:

```markdown
## Bug Description
A clear and concise description of what the bug is.

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
A clear and concise description of what you expected to happen.

## Actual Behavior
A clear and concise description of what actually happened.

## Screenshots
If applicable, add screenshots to help explain your problem.

## Environment
- **UniERP Version**: [e.g. 1.0.0]
- **Operating System**: [e.g. Ubuntu 22.04]
- **Browser**: [e.g. Chrome 108.0]
- **Database**: [e.g. PostgreSQL 14]
- **Python Version**: [e.g. 3.10.6]

## Additional Context
Add any other context about the problem here.

## Possible Solution
If you have ideas for a solution, please describe them here.
```

### Feature Requests

Use the feature request template:

```markdown
## Feature Description
A clear and concise description of the feature you'd like to see added.

## Problem Statement
What problem does this feature solve? What pain point does it address?

## Proposed Solution
How do you envision this feature working?

## Alternatives Considered
What other approaches have you considered? Why are they not suitable?

## Additional Context
Add any other context, mockups, or examples about the feature request here.

## Priority
- [ ] High - Critical for business operations
- [ ] Medium - Important but not blocking
- [ ] Low - Nice to have
```

### Security Issues

For security vulnerabilities, please:

1. **Do NOT** open a public issue
2. **Email** security@unisoft.com.bd
3. **Include**:
   - Vulnerability description
   - Steps to reproduce
   - Potential impact
   - Any mitigation you've implemented

---

## Feature Requests

### Feature Request Process

1. **Check existing requests** to avoid duplicates
2. **Create detailed issue** with use case and requirements
3. **Gather community feedback** through comments
4. **Prioritization** by project maintainers
5. **Implementation** by team or community contributors

### Feature Request Template

```markdown
## Feature Request: [Brief Title]

### Use Case
Describe the specific business problem this feature solves.

### Current Workaround
How are users currently working around this limitation?

### Proposed Solution
Detailed description of the proposed feature implementation.

### Requirements
- [ ] Functional requirement 1
- [ ] Functional requirement 2
- [ ] Technical requirement 1
- [ ] UI/UX requirement 1

### Acceptance Criteria
- [ ] User can accomplish [specific task]
- [ ] System performs [specific function]
- [ ] Integration with [existing module]

### Mockups/Designs
If applicable, include mockups, wireframes, or designs.

### Additional Resources
Links to relevant documentation, examples, or references.
```

---

## Pull Request Process

### Pull Request Template

```markdown
## Description
Brief description of changes made in this PR.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes, code improvements)
- [ ] Performance improvements
- [ ] Security improvements

## Issue Reference
Fixes #BRAND-123
Closes #BRAND-456

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Performance testing completed (if applicable)
- [ ] Security testing completed (if applicable)

## Checklist
- [ ] Code follows project coding standards
- [ ] Self-review of the code
- [ ] Code is commented appropriately
- [ ] Documentation updated (if required)
- [ ] No hardcoded values
- [ ] Error handling implemented
- [ ] Branding compliance verified (no Odoo references)
- [ ] Tests added/updated
- [ ] All tests passing

## Screenshots/Videos
If applicable, include screenshots or videos demonstrating the changes.

## Additional Notes
Any additional information reviewers should know.
```

### Pull Request Guidelines

#### Before Submitting

1. **Search existing PRs** to avoid duplicates
2. **Ensure your branch is up-to-date** with develop
3. **Resolve all merge conflicts**
4. **Pass all automated checks**
5. **Complete the PR template**
6. **Add appropriate reviewers**

#### During Review

1. **Respond promptly** to review comments
2. **Address all feedback** before requesting re-review
3. **Keep discussions focused** and professional
4. **Update PR description** if scope changes
5. **Mark as ready** when all issues are resolved

#### After Merge

1. **Delete your feature branch** from your fork
2. **Update your local develop** branch
3. **Close related issues**
4. **Celebrate** your contribution! 🎉

### Review Process

#### Reviewer Responsibilities

1. **Thorough code review** for quality and correctness
2. **Check for compliance** with coding standards
3. **Verify functionality** meets requirements
4. **Test the changes** if possible
5. **Provide constructive feedback**
6. **Approve or request changes** promptly

#### Review Guidelines

- **Be constructive** and specific in feedback
- **Focus on the code**, not the person
- **Explain reasoning** behind suggestions
- **Acknowledge good work** and improvements
- **Ask questions** if anything is unclear

---

## Coding Standards

### Python Standards

#### Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with additional guidelines:

```python
# Import order
import os
import sys
from datetime import datetime

# Third-party imports
import requests
from flask import Flask

# Local imports
from odoo import models, fields, api
from odoo.exceptions import ValidationError

# Class definition
class UniERPModel(models.Model):
    """Brief description of the model."""
    
    _name = 'unierp.model'
    _description = 'Model Description'
    
    # Field definitions
    name = fields.Char(
        string='Name',
        required=True,
        help='Human-readable name of the record'
    )
    
    # Method definitions
    @api.model
    def create(self, vals):
        """Create a new record with validation."""
        if not vals.get('name'):
            raise ValidationError('Name is required')
        
        return super().create(vals)
    
    @api.depends('field1', 'field2')
    def _compute_computed_field(self):
        """Compute field based on dependencies."""
        for record in self:
            record.computed_field = record.field1 + record.field2
```

#### Naming Conventions

- **Classes**: PascalCase (e.g., `UniERPModel`)
- **Functions/Methods**: snake_case (e.g., `compute_total_amount`)
- **Variables**: snake_case (e.g., `total_amount`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_RETRY_ATTEMPTS`)
- **Private methods**: prefix with underscore (e.g., `_validate_data`)

#### Documentation Standards

```python
def calculate_discount(amount, percentage, max_discount=None):
    """
    Calculate discount amount with optional maximum limit.
    
    Args:
        amount (float): Original amount before discount
        percentage (float): Discount percentage (0-100)
        max_discount (float, optional): Maximum discount amount
    
    Returns:
        float: Calculated discount amount
    
    Raises:
        ValueError: If percentage is not between 0 and 100
    
    Example:
        >>> calculate_discount(100, 10, 5)
        5.0
    """
    if not 0 <= percentage <= 100:
        raise ValueError('Percentage must be between 0 and 100')
    
    discount = amount * (percentage / 100)
    if max_discount:
        discount = min(discount, max_discount)
    
    return discount
```

### JavaScript Standards

```javascript
// Use modern ES6+ syntax
import { Component, useState, useEffect } from '@odoo/owl';

/**
 * UniERP Component Description
 */
export class UniERPComponent extends Component {
    static template = 'unierp.ComponentTemplate';
    
    setup() {
        this.state = useState({
            isLoading: false,
            data: [],
            error: null,
        });
    }
    
    /**
     * Load data from API
     * @param {Object} params - API parameters
     */
    async loadData(params = {}) {
        this.state.isLoading = true;
        this.state.error = null;
        
        try {
            const response = await this.rpc('/unierp/api/data', params);
            this.state.data = response;
        } catch (error) {
            this.state.error = error.message;
            console.error('Failed to load data:', error);
        } finally {
            this.state.isLoading = false;
        }
    }
}
```

### XML Standards

```xml
<!-- Use proper indentation and comments -->
<odoo>
    <data>
        <!-- View definition -->
        <record id="view_unierp_form" model="ir.ui.view">
            <field name="name">unierp.form</field>
            <field name="model">unierp.model</field>
            <field name="arch" type="xml">
                <form string="UniERP Model">
                    <header>
                        <button name="action_validate" 
                                string="Validate" 
                                type="object" 
                                class="btn-primary"/>
                    </header>
                    <sheet>
                        <group>
                            <field name="name" required="1"/>
                            <field name="description"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>
        
        <!-- Menu item -->
        <menuitem id="menu_unierp_root"
                  name="UniERP"
                  sequence="10"
                  web_icon="unierp,static/description/icon.png"/>
        
        <menuitem id="menu_unierp_model"
                  name="Models"
                  parent="menu_unierp_root"
                  action="action_unierp_model"
                  sequence="10"/>
    </data>
</odoo>
```

### CSS/SCSS Standards

```scss
// Use SCSS variables for branding
$unierp-primary: #1a73e8;
$unierp-secondary: #34a853;
$unierp-danger: #ea4335;

// Component-specific styles
.o_unierp_component {
    font-family: 'Inter', -apple-system, sans-serif;
    
    &__header {
        background-color: $unierp-primary;
        color: white;
        padding: 1rem;
        
        &:hover {
            background-color: darken($unierp-primary, 10%);
        }
    }
    
    &__content {
        padding: 1.5rem;
        
        &--loading {
            opacity: 0.6;
            pointer-events: none;
        }
    }
    
    // Responsive design
    @media (max-width: 768px) {
        &__header {
            padding: 0.5rem;
        }
    }
}
```

### Branding Compliance

#### Required Replacements

| Original | Replacement |
|----------|------------|
| Odoo | UniERP |
| odoo | unierp |
| ODOO | UNIERP |
| odoo.com | uslbd.com |
| @odoo.com | @unisoft.com.bd |
| odoo S.A. | UniSoft Systems Ltd. |

#### Code Review Checklist

- [ ] No Odoo branding references in code
- [ ] All URLs point to uslbd.com
- [ ] Email addresses use unisoft.com.bd
- [ ] UniERP branding correctly applied
- [ ] License attribution maintained

---

## Testing Guidelines

### Test Structure

```python
import unittest
from odoo.tests import common
from odoo.exceptions import ValidationError

class TestUniERPModel(common.TransactionCase):
    """Test cases for UniERP Model."""
    
    at_install = False
    post_install = True
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.test_data = {
            'name': 'Test Record',
            'description': 'Test Description',
        }
    
    def test_create_record_valid_data(self):
        """Test creating record with valid data."""
        record = self.env['unierp.model'].create(self.test_data)
        
        self.assertEqual(record.name, self.test_data['name'])
        self.assertEqual(record.description, self.test_data['description'])
    
    def test_create_record_missing_name(self):
        """Test creating record without name raises error."""
        with self.assertRaises(ValidationError):
            self.env['unierp.model'].create({'description': 'Test'})
    
    def test_compute_field(self):
        """Test computed field calculation."""
        record = self.env['unierp.model'].create({
            'name': 'Test',
            'field1': 10,
            'field2': 20,
        })
        
        self.assertEqual(record.computed_field, 30)
    
    def tearDown(self):
        """Clean up test environment."""
        super().tearDown()
```

### Testing Requirements

#### Unit Tests

- **Coverage**: Minimum 80% line coverage
- **Isolation**: Each test should be independent
- **Assertions**: Clear and meaningful assertions
- **Setup/Teardown**: Proper resource management

#### Integration Tests

- **Module Interactions**: Test cross-module functionality
- **API Endpoints**: Test REST API functionality
- **Database Operations**: Test data integrity
- **User Workflows**: Test business processes

#### Performance Tests

- **Load Testing**: Test under concurrent load
- **Memory Usage**: Monitor memory consumption
- **Database Queries**: Optimize slow queries
- **Response Times**: Ensure acceptable performance

### Running Tests

```bash
# Run all tests
./unierp-bin -d test_db --test-enable --stop-after-init

# Run specific module tests
./unierp-bin -d test_db --test-enable --test-tags TestUniERPModel --stop-after-init

# Run with coverage
python3 -m pytest tests/ --cov=odoo --cov-report=html

# Run performance tests
python3 -m pytest tests/performance/ --benchmark-only
```

---

## Documentation

### Documentation Standards

#### Code Documentation

- **Docstrings** for all public functions and classes
- **Comments** for complex logic
- **Type hints** for function parameters and return values
- **Examples** for complex functions

#### User Documentation

- **User manuals** with step-by-step instructions
- **Screenshots** for UI workflows
- **Video tutorials** for complex processes
- **FAQ sections** for common questions

#### API Documentation

- **Endpoint descriptions** with parameters and responses
- **Authentication** requirements and examples
- **Error codes** and handling
- **Rate limiting** information

### Documentation Structure

```
docs/
├── user/
│   ├── user-manual.md
│   ├── quick-start.md
│   └── troubleshooting.md
├── developer/
│   ├── api-reference.md
│   ├── module-development.md
│   └── contributing.md
├── admin/
│   ├── installation.md
│   ├── configuration.md
│   └── security.md
└── assets/
    ├── images/
    ├── videos/
    └── diagrams/
```

---

## Community

### Communication Channels

#### Official Channels

- **📧 Email**: dev@unisoft.com.bd
- **💬 Slack**: [unierp-community.slack.com](https://unierp-community.slack.com)
- **🐛 Issues**: [GitHub Issues](https://github.com/unisoft/unierp/issues)
- **📖 Forums**: [community.unierp.uslbd.com](https://community.unierp.uslbd.com)

#### Social Media

- **🐦 Twitter**: [@UniERP_BD](https://twitter.com/UniERP_BD)
- **💼 LinkedIn**: [UniERP](https://linkedin.com/company/unierp)
- **📺 YouTube**: [UniERP Channel](https://youtube.com/c/unierp)

### Events

#### Community Meetings

- **Monthly Community Call**: Last Friday of each month
- **Office Hours**: First Thursday of each month
- **Annual Conference**: UniERP Summit (details announced)

#### Contributer Recognition

- **🏆 Monthly Spotlight**: Featured contributor
- **🎖️ Contributor Badges**: GitHub achievement badges
- **📝 Blog Features**: Contributor spotlights on our blog
- **🎁 Swag**: Annual contributor appreciation packages

### Getting Help

#### For Contributors

- **📚 Documentation**: [docs.uslbd.com/unierp](https://docs.uslbd.com/unierp)
- **💬 Community**: [community.unierp.uslbd.com](https://community.unierp.uslbd.com)
- **📧 Email**: dev@unisoft.com.bd

#### For Users

- **🎫 Support**: [support.uslbd.com](https://support.uslbd.com)
- **📚 Knowledge Base**: [kb.unierp.uslbd.com](https://kb.unierp.uslbd.com)
- **🎓 Training**: [training.unierp.uslbd.com](https://training.unierp.uslbd.com)

---

## Thank You!

Thank you for contributing to UniERP! Your contributions help make this project better for everyone.

### Recognition

All contributors will be acknowledged in:
- **README.md** contributors section
- **Release notes** for each version
- **Annual report** highlighting community contributions
- **Special recognition** for significant contributions

### Next Steps

After your first contribution:

1. **Join our community** channels
2. **Participate in discussions**
3. **Help other contributors**
4. **Share your experience**
5. **Consider becoming a maintainer**

---

## Contact

For questions about contributing:

- **📧 Email**: dev@unisoft.com.bd
- **💬 Slack**: #contributing channel
- **🐛 Issues**: Use "question" label

---

*This contributing guide is a living document and will be updated as our community grows and evolves.*

**Last Updated**: November 19, 2025  
**Version**: 1.0  
**Maintainers**: UniSoft Development Team
