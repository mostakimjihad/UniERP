# UniERP Upgrade Procedures

## Overview

This comprehensive guide provides administrators and developers with detailed procedures for upgrading UniERP systems, covering version management, database migrations, and system updates while ensuring data integrity and minimal downtime.

## Table of Contents

1. [Upgrade Planning](#upgrade-planning)
2. [Pre-Upgrade Preparation](#pre-upgrade-preparation)
3. [Database Backup](#database-backup)
4. [Module Updates](#module-updates)
5. [Database Migration](#database-migration)
6. [File System Updates](#file-system-updates)
7. [Configuration Migration](#configuration-migration)
8. [Post-Upgrade Verification](#post-upgrade-verification)
9. [Rollback Procedures](#rollback-procedures)
10. [Troubleshooting](#troubleshooting)

## Upgrade Planning

### Version Management

#### UniERP Versioning

UniERP follows semantic versioning: `MAJOR.MINOR.PATCH`

- **Major**: Significant feature changes or architectural modifications
- **Minor**: New features or substantial improvements
- **Patch**: Bug fixes and minor improvements

#### Upgrade Paths

Supported upgrade paths:

```
From 15.0 → To 16.0: Supported
From 14.0 → To 16.0: Supported
From 13.0 → To 16.0: Manual migration required
From 12.0 → To 16.0: Manual migration required
From 11.0 → To 16.0: Manual migration required
From 10.0 → To 16.0: Manual migration required
```

#### Upgrade Schedule

Plan upgrades during maintenance windows:

1. **Business Hours**: Schedule for weekends or non-peak hours
2. **User Notification**: Inform users 2 weeks in advance
3. **Rollback Window**: Keep rollback option available for 48 hours
4. **Testing Period**: Allow 1-2 weeks for thorough testing

### Compatibility Matrix

| From Version | To Version | Upgrade Type | Downtime Required |
|--------------|------------|--------------|------------------|
| 15.0 | 16.0 | Automated | 15-30 minutes |
| 14.0 | 16.0 | Automated | 30-45 minutes |
| 13.0 | 16.0 | Manual | 2-4 hours |
| 12.0 | 16.0 | Manual | 4-6 hours |
| 11.0 | 16.0 | Manual | 6-8 hours |

## Pre-Upgrade Preparation

### Environment Checklist

#### System Requirements

- [ ] Server meets minimum requirements for target version
- [ ] Sufficient disk space available (2x current database size)
- [ ] Memory requirements met (4GB minimum, 8GB recommended)
- [ ] Python version compatible (3.8+ for v16.0)
- [ ] PostgreSQL version supported (12+ for v16.0)

#### Backup Verification

- [ ] Full database backup completed and verified
- [ ] File system backup completed
- [ ] Configuration files backed up
- [ ] Custom modules backed up
- [ ] Backup restoration tested in staging

#### Access Control

- [ ] Maintenance mode enabled
- [ ] User notifications sent
- [ ] API rate limiting configured
- [ ] SSL certificates valid
- [ ] Load balancer configured (if applicable)

### Dependency Check

```bash
# Check module compatibility
./odoo-bin -d database_name --stop-after-init

# Review module dependencies
grep -r "depends.*=" addons/*/__manifest__.py

# Check for conflicting modules
find addons/ -name "*.py" -exec grep -l "conflict" {} \;
```

## Database Backup

### Full Database Backup

```bash
# Create comprehensive backup
pg_dump -h localhost -U postgres -d database_name \
    --format=custom \
    --compress=9 \
    --verbose \
    --file=backup_before_upgrade_$(date +%Y%m%d_%H%M%S).dump

# Verify backup integrity
pg_restore --list backup_before_upgrade_*.dump
```

### File System Backup

```bash
# Backup custom modules
tar -czf custom_modules_backup_$(date +%Y%m%d).tar.gz \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    addons/

# Backup configuration files
cp -r /etc/odoo/ config_backup_$(date +%Y%m%d)/
cp -r /var/log/odoo/ logs_backup_$(date +%Y%m%d)/
```

### Backup Verification

```bash
# Test backup restoration
mkdir /tmp/restore_test
cd /tmp/restore_test

# Restore database to test environment
createdb test_restore
pg_restore backup_before_upgrade_*.dump test_restore

# Verify data integrity
psql -d test_restore -c "
    SELECT 
        COUNT(*) as total_records,
        COUNT(DISTINCT id) as unique_ids
    FROM res_users;
"
```

## Module Updates

### Module Compatibility Check

```bash
# Check current module versions
./odoo-bin -d database_name --stop-after-init

# List installed modules
./odoo-bin -d database_name -u base --stop-after-init

# Check for updates
for module in addons/*/; do
    if [ -f "$module/__manifest__.py" ]; then
        echo "Checking module: $module"
        # Check version compatibility
    fi
done
```

### Module Update Process

```bash
# Update core modules
./odoo-bin -d database_name -u base --stop-after-init

# Update custom modules
for module_dir in addons/*/; do
    if [ -f "$module_dir/__manifest__.py" ]; then
        echo "Updating module: $module_dir"
        ./odoo-bin -d database_name -u $(basename $module_dir) --stop-after-init
    fi
done

# Verify module updates
./odoo-bin -d database_name -u base --stop-after-init
```

### Module Migration

```python
# Custom module migration script
# migrations/16.0.1.0.0/post-migration.py
from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    """Migration script for custom module"""
    
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Add new field to existing model
        env.cr.execute("""
            ALTER TABLE res_partner 
            ADD COLUMN IF NOT EXISTS custom_field VARCHAR(100);
        """)
        
        # Populate new field with default values
        env.cr.execute("""
            UPDATE res_partner 
            SET custom_field = %s 
            WHERE custom_field IS NULL;
        """, ('Default Value'))
        
        # Create new model if needed
        env.cr.execute("""
            CREATE TABLE IF NOT EXISTS custom_model (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                partner_id INTEGER REFERENCES res_partner(id),
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        print("Migration completed successfully")
```

## Database Migration

### Schema Changes

```sql
-- Example migration script
-- File: migrations/16.0.1.0.0/pre-migration.sql

-- Add new column to existing table
ALTER TABLE res_partner 
ADD COLUMN IF NOT EXISTS custom_field VARCHAR(100);

-- Create index for performance
CREATE INDEX IF NOT EXISTS idx_res_partner_custom_field 
ON res_partner(custom_field);

-- Add new table for custom functionality
CREATE TABLE IF NOT EXISTS custom_workflow (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    res_id INTEGER,
    state VARCHAR(20) DEFAULT 'draft',
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Populate initial data
INSERT INTO custom_workflow (name, model, state)
VALUES 
    ('Initial Approval', 'res.partner', 'draft'),
    ('Final Review', 'sale.order', 'draft');
```

### Data Migration

```python
# Data migration script
# migrations/16.0.1.0.0/data_migration.py
from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    """Migrate data from old structure to new structure"""
    
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Migrate partner categories
        old_categories = env['res.partner.category'].search([])
        for category in old_categories:
            if 'old_' in category.name:
                new_name = category.name.replace('old_', 'new_')
                category.write({'name': new_name})
        
        # Migrate product templates
        old_templates = env['product.template'].search([('type', '=', 'old_type')])
        for template in old_templates:
            template.write({
                'type': 'new_type',
                'description': template.description.replace('Old System', 'UniERP')
            })
        
        print("Data migration completed")
```

### Migration Validation

```python
# Migration validation script
# migrations/16.0.1.0.0/validate_migration.py
from odoo import api, SUPERUSER_ID

def validate_migration(cr, version):
    """Validate migration results"""
    
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Check data integrity
        partner_count = env['res.partner'].search_count([])
        if partner_count == 0:
            raise Exception("Data migration failed: No partners found")
        
        # Check schema consistency
        env.cr.execute("""
            SELECT COUNT(*) 
            FROM information_schema.columns 
            WHERE table_name = 'res_partner'
            AND column_name = 'custom_field'
        """)
        
        if env.cr.fetchone()[0] == 0:
            raise Exception("Schema migration failed: custom_field not created")
        
        print("Migration validation completed successfully")
```

## File System Updates

### Configuration Updates

```bash
# Update configuration files
sudo cp /etc/odoo/odoo.conf /etc/odoo/odoo.conf.backup

# Update configuration for new version
cat >> /etc/odoo/odoo.conf << EOF
[options]
# UniERP 16.0 Configuration
db_host = localhost
db_port = 5432
db_user = unierp
db_password = ${DB_PASSWORD}
db_maxconn = 64
dbfilter = ^unierp.*
addons_path = /opt/unierp/addons
logfile = /var/log/odoo/odoo-server.log
log_level = info
workers = 4
limit_time_cpu = 86400
limit_time_real = 172800
limit_request = 8192
EOF

# Set proper permissions
sudo chown unierp:unierp /etc/odoo/odoo.conf
sudo chmod 640 /etc/odoo/odoo.conf
```

### Service Configuration

```bash
# Update systemd service
sudo systemctl edit odoo.service

# Service file content
[Unit]
Description=UniERP Application Server
After=network.target

[Service]
Type=simple
User=unierp
Group=unierp
ExecStart=/opt/unierp/odoo-bin -c /etc/odoo/odoo.conf
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5
TimeoutSec=300
KillMode=mixed

[Install]
WantedBy=multi-user.target
```

### Log Rotation Setup

```bash
# Configure log rotation
sudo cat > /etc/logrotate.d/odoo << EOF
/var/log/odoo/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644
    su unierp unierp
    postrotate
        systemctl reload odoo
}
EOF

sudo systemctl enable logrotate
```

## Configuration Migration

### System Parameters

```python
# Migration script for system parameters
# migrations/16.0.1.0.0/config_migration.py
from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    """Migrate system configuration"""
    
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Update system parameters
        old_params = {
            'web.base.url': 'http://old-domain.com',
            'report.url': 'http://old-reports.com',
        }
        
        new_params = {
            'web.base.url': 'https://www.uslbd.com',
            'report.url': 'https://reports.uslbd.com',
        }
        
        for key, value in new_params.items():
            env['ir.config_parameter'].set_param(key, value)
        
        # Remove old parameters
        for key in old_params.keys():
            env['ir.config_parameter'].search([('key', '=', key)]).unlink()
        
        print("Configuration migration completed")
```

### Email Configuration

```python
# Email configuration migration
# migrations/16.0.1.0.0/email_migration.py
from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    """Migrate email configuration"""
    
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Update outgoing mail servers
        old_servers = env['ir.mail.server'].search([
            ('name', 'ilike', 'old-domain.com')
        ])
        
        if old_servers:
            old_servers.write({
                'name': old_servers[0].name.replace('old-domain.com', 'uslbd.com'),
                'smtp_host': old_servers[0].smtp_host.replace('old-domain.com', 'uslbd.com'),
            })
        
        print("Email configuration migration completed")
```

## Post-Upgrade Verification

### System Health Check

```bash
# Check system status
systemctl status odoo

# Check resource usage
free -h
df -h
top -n 1

# Check database connections
psql -d unierp -c "SELECT count(*) FROM pg_stat_activity WHERE datname = 'unierp';"

# Check error logs
tail -n 50 /var/log/odoo/odoo-server.log
```

### Functionality Testing

```python
# Post-upgrade test script
# tests/post_upgrade_test.py
import unittest
from odoo import api

class PostUpgradeTest(unittest.TestCase):
    
    def test_user_login(self):
        """Test user authentication after upgrade"""
        # Test login functionality
        pass
    
    def test_module_access(self):
        """Test module accessibility after upgrade"""
        # Test custom modules work
        pass
    
    def test_data_integrity(self):
        """Test data integrity after upgrade"""
        # Verify critical data exists
        pass
    
    def test_performance(self):
        """Test system performance after upgrade"""
        # Check response times
        pass

if __name__ == '__main__':
    unittest.main()
```

### Automated Verification

```bash
# Comprehensive health check
./odoo-bin -d unierp --test-enable --stop-after-init

# Check all modules
./odoo-bin -d unierp -u base --stop-after-init

# Verify database schema
psql -d unierp -c "\dt+"

# Check configuration
./odoo-bin -d unierp --stop-after-init
```

## Rollback Procedures

### Database Rollback

```bash
# Rollback database to previous version
pg_restore --verbose --clean --exit-on-error \
    backup_before_upgrade_20240101_120000.dump

# Verify rollback
psql -d unierp -c "SELECT COUNT(*) FROM res_users;"
```

### File System Rollback

```bash
# Restore configuration files
sudo rm -rf /etc/odoo/
sudo mv config_backup_20240101/ /etc/odoo/

# Restore custom modules
rm -rf addons/
tar -xzf custom_modules_backup_20240101.tar.gz

# Restore service configuration
sudo systemctl daemon-reload
```

### Service Rollback

```bash
# Emergency rollback procedure
sudo systemctl stop odoo
sudo systemctl start odoo

# Check service status
systemctl status odoo

# Monitor startup
journalctl -u odoo -f
```

## Troubleshooting

### Common Upgrade Issues

#### Database Issues

| Problem | Symptoms | Solution |
|---------|-----------|----------|
| Migration script fails | SQL syntax errors in logs | Review migration scripts, check PostgreSQL version compatibility |
| Data corruption | Missing records after upgrade | Restore from backup, re-run migration |
| Performance degradation | Slow queries after upgrade | Update indexes, analyze slow queries |
| Connection failures | Cannot connect to database | Check configuration, firewall settings |

#### Module Issues

| Problem | Symptoms | Solution |
|---------|-----------|----------|
| Module not loading | Import errors in logs | Check Python dependencies, module compatibility |
| View inheritance broken | UI elements missing | Review XPath expressions, view inheritance |
| Access denied | Permission errors after upgrade | Update security rules, user groups |
| Custom module conflicts | Duplicate functionality | Disable conflicting modules, resolve conflicts |

#### System Issues

| Problem | Symptoms | Solution |
|---------|-----------|----------|
| Service won't start | Configuration errors | Check config file syntax, permissions |
| High memory usage | System slow, crashes | Optimize workers, increase memory |
| Disk space full | Upgrade fails | Clean temp files, increase disk space |
| SSL certificate errors | HTTPS warnings | Update certificates, check expiration |

### Debug Mode

Enable comprehensive debugging:

```bash
# Development mode with all debugging options
./odoo-bin -d unierp \
    --dev=reload,qweb,werkzeug,xml \
    --log-level=debug \
    --stop-after-init

# Database query debugging
./odoo-bin -d unierp --log-level=debug_sql
```

### Getting Help

- **Upgrade Documentation**: https://www.uslbd.com/documentation/upgrade
- **Community Support**: https://www.uslbd.com/community/upgrade
- **Professional Services**: https://www.uslbd.com/support/upgrade
- **Emergency Contacts**: support@uslbd.com

---

This comprehensive upgrade procedures guide provides administrators with all the necessary information and procedures to successfully upgrade UniERP systems while minimizing downtime, ensuring data integrity, and maintaining system stability.