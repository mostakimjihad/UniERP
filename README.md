# UniERP - Enterprise Resource Planning System

<div align="center">

![UniERP Logo](https://github.com/mostakimjihad/UniERP/blob/master/github_docs/img/UniERP.png)

**Empowering Business Excellence Through Integrated ERP Solutions**

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3.0-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Based on Odoo 19.0](https://img.shields.io/badge/Based%20on-Odoo%2019.0-green.svg)](https://www.odoo.com/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/unisoft/unierp/actions)
[![Coverage](https://img.shields.io/badge/coverage-80%25-green.svg)](https://codecov.io/gh/unisoft/unierp)

[Website](https://uslbd.com) • [Documentation](https://docs.uslbd.com/unierp) • [Demo](https://demo.unierp.uslbd.com) • [Support](https://support.uslbd.com)

</div>

## Executive Summary

**UniERP** is a comprehensive Enterprise Resource Planning system developed by UniSoft Systems Ltd. Built upon the robust foundation of Odoo 19 Community Edition, UniERP has been completely rebranded and customized to deliver a white-label ERP solution tailored for modern businesses.

> **License Compliance Notice:** UniERP is licensed under GNU Lesser General Public License v3.0 (LGPL-3.0) and maintains full compliance with Odoo's licensing requirements. See [LICENSE](LICENSE) file for complete license terms and attribution information.

### Key Differentiators

- **🎯 Complete Rebranding**: 100% removal of Odoo branding with professional UniERP identity
- **🔧 Full Functionality**: Preserves all powerful features of Odoo 19 Community Edition
- **🏢 Corporate Ready**: Enterprise-grade security, scalability, and compliance
- **🌐 Local Expertise**: Developed and supported by UniSoft Systems Ltd. in Bangladesh
- **📚 Comprehensive Documentation**: Complete user guides, admin manuals, and API documentation

## Key Features

### Core Business Modules

| Module | Description | Status |
|--------|-------------|--------|
| **Sales Management** | Complete sales cycle from quotation to invoicing | ✅ |
| **CRM** | Customer relationship management and lead tracking | ✅ |
| **Accounting** | Financial management, reporting, and compliance | ✅ |
| **Inventory** | Multi-warehouse inventory control and valuation | ✅ |
| **Manufacturing** | Production planning, MRP, and quality control | ✅ |
| **HR Management** | Employee management, payroll, and attendance | ✅ |
| **Project Management** | Project planning, tasks, and time tracking | ✅ |
| **Purchase Management** | Procurement, vendor management, and receiving | ✅ |
| **Website Builder** | Drag-and-drop website creation and management | ✅ |
| **E-commerce** | Online store with payment integration | ✅ |

### Advanced Features

- **📊 Business Intelligence**: Advanced reporting and analytics dashboard
- **🔄 Workflow Automation**: Customizable business process automation
- **📱 Mobile Responsive**: Full mobile compatibility across all modules
- **🔗 API Integration**: RESTful API for third-party integrations
- **🌍 Multi-Company**: Support for multiple company structures
- **💳 Payment Gateways**: Integration with major payment providers
- **📧 Email Integration**: Seamless email marketing and communication
- **🔐 Security**: Role-based access control and audit trails

## Installation

### Prerequisites

#### System Requirements

- **Operating System**: Ubuntu 20.04+ / CentOS 8+ / Windows 10+
- **Python**: 3.10 or higher
- **Database**: PostgreSQL 14 or higher
- **Memory**: Minimum 4GB RAM (8GB+ recommended)
- **Storage**: Minimum 20GB free space
- **Processor**: 64-bit, 2+ cores recommended

#### Software Dependencies

```bash
# System packages
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev python3-venv
sudo apt-get install -y postgresql postgresql-server-dev-all
sudo apt-get install -y build-essential libxml2-dev libxslt1-dev libevent-dev
sudo apt-get install -y libsasl2-dev libldap2-dev libpq-dev libjpeg-dev
sudo apt-get install -y libzip-dev libssl-dev nodejs npm

# Python packages
pip3 install -r requirements.txt

# Node.js packages
npm install -g less less-plugin-clean-css
```

### Quick Start

#### Option 1: Docker Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/unisoft/unierp.git
cd unierp

# Build and run with Docker Compose
docker-compose up -d

# Access UniERP
open http://localhost:8069
```

#### Option 2: Manual Installation

```bash
# 1. Clone the repository
git clone https://github.com/unisoft/unierp.git
cd unierp

# 2. Create virtual environment
python3 -m venv unierp-env
source unierp-env/bin/activate

# 3. Install dependencies
pip3 install -r requirements.txt

# 4. Create database user
sudo -u postgres createuser --createdb --pwprompt unierp

# 5. Create database
sudo -u postgres createdb -O unierp unierp

# 6. Configure UniERP
cp etc/unierp.conf.example etc/unierp.conf
# Edit etc/unierp.conf with your database settings

# 7. Initialize database
./unierp-bin -d unierp -i base --without-demo=all

# 8. Start UniERP
./unierp-bin -c etc/unierp.conf
```

#### Option 3: Production Installation

For production deployment, please refer to our [Production Deployment Guide](https://docs.uslbd.com/unierp/deployment).

### Configuration

Create a configuration file at `/etc/unierp/unierp.conf`:

```ini
[options]
# Database settings
db_host = localhost
db_port = 5432
db_user = unierp
db_password = your_secure_password
db_maxconn = 64

# UniERP settings
addons_path = /opt/unierp/addons,/opt/unierp/custom_addons
data_dir = /var/lib/unierp
logfile = /var/log/unierp/unierp.log

# Web settings
xmlrpc_port = 8069
longpolling_port = 8072
workers = 4
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
limit_request = 8192
limit_time_cpu = 600
limit_time_real = 1200

# Email settings
email_from = noreply@uslbd.com
smtp_server = smtp.uslbd.com
smtp_port = 587
smtp_user = your_email@uslbd.com
smtp_password = your_email_password

# UniERP branding
unierp_system_name = UniERP
unierp_company_name = Your Company Name
unierp_website = https://uslbd.com
```

## Local Development Setup

### Development Environment

```bash
# 1. Clone the repository
git clone https://github.com/unisoft/unierp.git
cd unierp

# 2. Create development branch
git checkout -b feature/your-feature-name

# 3. Set up development environment
python3 -m venv dev-env
source dev-env/bin/activate
pip3 install -r requirements-dev.txt

# 4. Install pre-commit hooks
pip3 install pre-commit
pre-commit install

# 5. Create development database
createdb unierp_dev

# 6. Run UniERP in development mode
./unierp-bin -d unierp_dev --dev=reload,qweb,werkzeug,xml
```

### Development Tools

#### Code Quality

```bash
# Run linting
flake8 odoo/ addons/ --max-line-length=120
pylint odoo/ --disable=C0114,C0115

# Format code
black odoo/ addons/
isort odoo/ addons/

# Run tests
python3 -m pytest tests/ --cov=odoo --cov-report=html

# Security scan
bandit -r odoo/ -f json
```

#### Database Management

```bash
# Backup database
pg_dump -U unierp unierp_dev > backup.sql

# Restore database
psql -U unierp unierp_dev < backup.sql

# Update module
./unierp-bin -d unierp_dev -u module_name --stop-after-init
```

## Contributing

We welcome contributions to the UniERP project! Please read our [Contributing Guidelines](CONTRIBUTING.md) for detailed information on:

- Code of conduct
- Development workflow
- Pull request process
- Coding standards
- Testing requirements

### Quick Contribution Guide

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
4. **Push** to your fork (`git push origin feature/amazing-feature`)
5. **Create** a Pull Request

## Documentation

Comprehensive documentation is available at [docs.uslbd.com/unierp](https://docs.uslbd.com/unierp):

### User Documentation
- [User Manual](https://docs.uslbd.com/unierp/user-manual)
- [Quick Start Guide](https://docs.uslbd.com/unierp/quick-start)
- [Video Tutorials](https://docs.uslbd.com/unierp/videos)

### Developer Documentation
- [Developer Guide](https://docs.uslbd.com/unierp/developer-guide)
- [API Reference](https://docs.uslbd.com/unierp/api)
- [Module Development](https://docs.uslbd.com/unierp/module-development)
- [Database Schema](https://docs.uslbd.com/unierp/database-schema)

### Administrator Documentation
- [Installation Guide](https://docs.uslbd.com/unierp/installation)
- [Configuration Guide](https://docs.uslbd.com/unierp/configuration)
- [Backup and Recovery](https://docs.uslbd.com/unierp/backup)
- [Security Hardening](https://docs.uslbd.com/unierp/security)

## Support

### Professional Support

For professional support and services:

- **📧 Email**: support@unisoft.com.bd
- **📞 Phone**: +880-2-XXXXXXX
- **💬 Live Chat**: [support.uslbd.com](https://support.uslbd.com)
- **🎫 Help Desk**: [helpdesk.uslbd.com](https://helpdesk.uslbd.com)

### Community Support

- **💬 Forums**: [community.unierp.uslbd.com](https://community.unierp.uslbd.com)
- **🐛 Issues**: [GitHub Issues](https://github.com/unisoft/unierp/issues)
- **📖 Wiki**: [wiki.unierp.uslbd.com](https://wiki.unierp.uslbd.com)

### Support Levels

| Level | Response Time | Features |
|-------|---------------|----------|
| **Basic** | 48 hours | Email support, community forums |
| **Professional** | 24 hours | Priority email, phone support |
| **Enterprise** | 4 hours | 24/7 support, dedicated account manager |

## Roadmap

### Upcoming Releases

#### v1.1 (Q1 2026)
- Enhanced mobile application
- Advanced analytics dashboard
- Improved API performance
- Additional payment gateways

#### v1.2 (Q2 2026)
- AI-powered business insights
- Advanced workflow automation
- Multi-warehouse enhancements
- HR analytics module

#### v2.0 (Q4 2026)
- Complete UI/UX redesign
- Microservices architecture
- Advanced security features
- Cloud-native deployment

### Feature Requests

Submit feature requests and vote on existing ones at:
[feedback.unierp.uslbd.com](https://feedback.unierp.uslbd.com)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Attribution

UniERP is built on Odoo Community Edition
Copyright © 2004-2024 Odoo SA (https://www.odoo.com)
Licensed under LGPL v3

Modified and distributed by:
UniSoft Systems Ltd.
Copyright © 2025 UniSoft Systems Ltd.
https://uslbd.com

## Performance Benchmarks

### System Performance

| Metric | Value | Target |
|--------|--------|--------|
| Page Load Time | < 2 seconds | ✅ |
| Database Query Time | < 100ms | ✅ |
| Concurrent Users | 500+ | ✅ |
| Uptime | 99.9% | ✅ |
| API Response Time | < 500ms | ✅ |

### Hardware Requirements

| Users | CPU | RAM | Storage | Database |
|--------|------|-----|---------|----------|
| 1-10 | 2 cores | 4GB | 20GB | PostgreSQL 14 |
| 10-50 | 4 cores | 8GB | 50GB | PostgreSQL 14 |
| 50-200 | 8 cores | 16GB | 100GB | PostgreSQL 14 |
| 200+ | 16+ cores | 32GB+ | 500GB+ | PostgreSQL 14 |

## Security

### Security Features

- **🔐 Authentication**: Multi-factor authentication, SSO support
- **🛡️ Authorization**: Role-based access control, field-level security
- **🔒 Data Protection**: Encryption at rest and in transit
- **📋 Audit Trail**: Complete activity logging and monitoring
- **🚨 Threat Detection**: Real-time security monitoring
- **🔧 Security Hardening**: Regular security updates and patches

### Compliance

- **🏢 ISO 27001**: Information security management
- **🔒 GDPR**: Data protection and privacy compliance
- **💳 PCI DSS**: Payment card industry compliance
- **🏛️ SOC 2**: Service organization control compliance

## Integration Ecosystem

### Third-Party Integrations

| Category | Integrations | Status |
|----------|-------------|--------|
| **Payment Gateways** | Stripe, PayPal, bKash, Nagad | ✅ |
| **Shipping** | FedEx, DHL, UPS, Pathao | ✅ |
| **Accounting** | QuickBooks, Xero, Tally | ✅ |
| **Communication** | Twilio, SendGrid, Mailchimp | ✅ |
| **Analytics** | Google Analytics, Mixpanel, Hotjar | ✅ |
| **Storage** | AWS S3, Google Cloud, Azure | ✅ |

### API Access

Complete RESTful API documentation available at:
[api.unierp.uslbd.com/docs](https://api.unierp.uslbd.com/docs)

## About UniSoft Systems Ltd.

**UniSoft Systems Ltd.** is a leading software development company based in Dhaka, Bangladesh, specializing in enterprise solutions and digital transformation.

### Company Information

- **Founded**: 2015
- **Headquarters**: Dhaka, Bangladesh
- **Office**: 8,000 sq ft modern development center
- **Team**: 40+ Elite Engineers
- **Projects**: 150+ Projects Delivered
- **Certifications**: ISO 9001:2015, ISO 27001:2013

### Contact Information

- **Website**: https://uslbd.com
- **Email**: hello@unisoft.com.bd
- **Sales**: sales@unisoft.com.bd
- **Support**: support@unisoft.com.bd
- **Address**: 8,000 sq ft development center, Dhaka, Bangladesh

### Our Values

- **🎯 Excellence**: Commitment to quality and innovation
- **🤝 Integrity**: Ethical business practices and transparency
- **🚀 Innovation**: Continuous improvement and cutting-edge solutions
- **👥 Teamwork**: Collaborative approach to problem-solving
- **🌍 Impact**: Creating value for our customers and community

## Acknowledgments

- **Odoo SA** for the excellent Odoo Community Edition framework
- **Contributors** who have helped improve UniERP
- **Community** for valuable feedback and suggestions
- **Partners** who have integrated with UniERP

---

<div align="center">

**[🌐 Visit Website](https://uslbd.com)** • **[📚 View Documentation](https://docs.uslbd.com/unierp)** • **[🚀 Try Demo](https://demo.unierp.uslbd.com)** • **[💬 Contact Support](https://support.uslbd.com)**

Made with ❤️ by [UniSoft Systems Ltd.](https://uslbd.com)

</div>
