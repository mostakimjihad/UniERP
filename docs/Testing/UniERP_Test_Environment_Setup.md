# UniERP Test Environment Setup Guide

## Overview

This document provides comprehensive guidelines for setting up and configuring test environments for UniERP testing activities. It covers environment architecture, configuration procedures, data management, and maintenance procedures to ensure effective testing operations.

## Document Information

- **Project:** UniERP Rebranding Project
- **Phase:** Phase 11 - Testing & Quality Assurance
- **Milestone:** 11.1 - Test Planning & Setup
- **Version:** 1.0
- **Created:** November 2024
- **Last Updated:** November 2024
- **Author:** UniERP DevOps Team
- **Contact:** devops@unierp.com

---

## 1. Environment Architecture

### 1.1 Environment Overview

UniERP testing utilizes a multi-environment approach to ensure comprehensive testing while maintaining separation between development, testing, and production systems.

#### 1.1.1 Environment Types
- **Development Environment:** Individual developer setups for unit testing
- **Integration Testing Environment:** Shared environment for integration testing
- **System Testing Environment:** Production-like environment for comprehensive testing
- **Performance Testing Environment:** Isolated environment for load and stress testing
- **Security Testing Environment:** Isolated environment for security assessments
- **UAT Environment:** Production replica for user acceptance testing

#### 1.1.2 Environment Relationships
```
Development → Integration → System Testing → UAT → Production
     ↓              ↓              ↓          ↓
Unit Tests    Integration Tests  System Tests  UAT Tests
```

### 1.2 Infrastructure Architecture

#### 1.2.1 Hardware Requirements

**Development Environment (Per Developer):**
- CPU: 4 cores minimum (8 cores recommended)
- RAM: 8GB minimum (16GB recommended)
- Storage: 250GB SSD minimum
- Network: 100Mbps connection

**Integration Testing Environment:**
- CPU: 8 cores minimum
- RAM: 16GB minimum
- Storage: 500GB SSD
- Network: 1Gbps connection

**System Testing Environment:**
- CPU: 16 cores minimum
- RAM: 32GB minimum
- Storage: 1TB SSD
- Network: 10Gbps connection

**Performance Testing Environment:**
- CPU: 32 cores minimum
- RAM: 64GB minimum
- Storage: 2TB SSD
- Network: 10Gbps connection

**UAT Environment:**
- CPU: 16 cores minimum
- RAM: 32GB minimum
- Storage: 1TB SSD
- Network: 10Gbps connection

#### 1.2.2 Network Architecture

**Network Segmentation:**
- **Development Network:** Isolated development subnet (10.0.1.0/24)
- **Testing Network:** Dedicated testing subnet (10.0.2.0/24)
- **Performance Network:** Isolated performance testing subnet (10.0.3.0/24)
- **Security Network:** Isolated security testing subnet (10.0.4.0/24)
- **UAT Network:** Dedicated UAT subnet (10.0.5.0/24)

**Firewall Configuration:**
- Inter-environment communication controlled by firewall rules
- Production access restricted to authorized personnel only
- Internet access controlled and monitored
- VPN access for remote team members

---

## 2. Software Installation & Configuration

### 2.1 Operating System Setup

#### 2.1.1 Base OS Installation
```bash
# Ubuntu 20.04 LTS Installation
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git vim htop

# System Configuration
sudo timedatectl set-timezone UTC
sudo locale-gen en_US.UTF-8
```

#### 2.1.2 User and Group Management
```bash
# Create unierp user
sudo useradd -m -s /bin/bash unierp
sudo usermod -aG sudo unierp

# Create directories
sudo mkdir -p /opt/unierp
sudo mkdir -p /var/log/unierp
sudo mkdir -p /var/lib/unierp

# Set permissions
sudo chown -R unierp:unierp /opt/unierp
sudo chown -R unierp:unierp /var/log/unierp
sudo chown -R unierp:unierp /var/lib/unierp
```

### 2.2 Database Setup

#### 2.2.1 PostgreSQL Installation
```bash
# Install PostgreSQL 13
sudo apt install -y postgresql-13 postgresql-contrib-13

# Configure PostgreSQL
sudo -u postgres psql << EOF
CREATE USER unierp WITH PASSWORD 'secure_password';
CREATE DATABASE unierp_test OWNER unierp;
CREATE DATABASE unierp_integration OWNER unierp;
CREATE DATABASE unierp_system OWNER unierp;
CREATE DATABASE unierp_performance OWNER unierp;
CREATE DATABASE unierp_uat OWNER unierp;
GRANT ALL PRIVILEGES ON DATABASE unierp_test TO unierp;
GRANT ALL PRIVILEGES ON DATABASE unierp_integration TO unierp;
GRANT ALL PRIVILEGES ON DATABASE unierp_system TO unierp;
GRANT ALL PRIVILEGES ON DATABASE unierp_performance TO unierp;
GRANT ALL PRIVILEGES ON DATABASE unierp_uat TO unierp;
EOF
```

#### 2.2.2 PostgreSQL Configuration
```ini
# /etc/postgresql/13/main/postgresql.conf
listen_addresses = '*'
port = 5432
max_connections = 200
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
```

#### 2.2.3 Database Backup Configuration
```bash
# Create backup script
cat > /opt/unierp/scripts/db_backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/unierp"
DATE=$(date +%Y%m%d_%H%M%S)
DBS="unierp_test unierp_integration unierp_system unierp_performance unierp_uat"

mkdir -p $BACKUP_DIR

for DB in $DBS; do
    pg_dump -h localhost -U unierp -d $DB | gzip > $BACKUP_DIR/${DB}_${DATE}.sql.gz
done

find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
EOF

chmod +x /opt/unierp/scripts/db_backup.sh

# Schedule daily backups
echo "0 2 * * * unierp /opt/unierp/scripts/db_backup.sh" | sudo crontab -
```

### 2.3 UniERP Application Setup

#### 2.3.1 Application Installation
```bash
# Clone UniERP repository
cd /opt/unierp
git clone https://github.com/unierp/unierp.git .

# Install Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt
```

#### 2.3.2 Configuration Files
```python
# /opt/unierp/config/test.py
import os

class TestConfig:
    # Database Configuration
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'unierp_test'
    DB_USER = 'unierp'
    DB_PASSWORD = 'secure_password'
    
    # Application Configuration
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'test-secret-key-change-in-production'
    
    # Server Configuration
    HOST = '0.0.0.0'
    PORT = 8069
    
    # File Storage
    DATA_DIR = '/var/lib/unierp/test'
    LOG_DIR = '/var/log/unierp/test'
    
    # Email Configuration (Test)
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    
    # Security Configuration
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    
    # UniERP Branding
    COMPANY_NAME = 'UniERP Test Environment'
    COMPANY_WEBSITE = 'https://test.unierp.com'
    SUPPORT_EMAIL = 'test-support@unierp.com'
```

```python
# /opt/unierp/config/integration.py
import os

class IntegrationConfig:
    # Database Configuration
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'unierp_integration'
    DB_USER = 'unierp'
    DB_PASSWORD = 'secure_password'
    
    # Application Configuration
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'integration-secret-key'
    
    # Server Configuration
    HOST = '0.0.0.0'
    PORT = 8070
    
    # File Storage
    DATA_DIR = '/var/lib/unierp/integration'
    LOG_DIR = '/var/log/unierp/integration'
    
    # Email Configuration
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.test.unierp.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'test@unierp.com'
    EMAIL_HOST_PASSWORD = 'test-email-password'
    
    # UniERP Branding
    COMPANY_NAME = 'UniERP Integration Environment'
    COMPANY_WEBSITE = 'https://integration.unierp.com'
    SUPPORT_EMAIL = 'integration-support@unierp.com'
```

```python
# /opt/unierp/config/system.py
import os

class SystemConfig:
    # Database Configuration
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'unierp_system'
    DB_USER = 'unierp'
    DB_PASSWORD = 'secure_password'
    
    # Application Configuration
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'system-secret-key-change-in-production'
    
    # Server Configuration
    HOST = '0.0.0.0'
    PORT = 8080
    
    # File Storage
    DATA_DIR = '/var/lib/unierp/system'
    LOG_DIR = '/var/log/unierp/system'
    
    # Email Configuration
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.unierp.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'system@unierp.com'
    EMAIL_HOST_PASSWORD = 'system-email-password'
    
    # Security Configuration
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    
    # UniERP Branding
    COMPANY_NAME = 'UniERP System Testing Environment'
    COMPANY_WEBSITE = 'https://system.unierp.com'
    SUPPORT_EMAIL = 'system-support@unierp.com'
```

### 2.4 Web Server Configuration

#### 2.4.1 Nginx Installation and Configuration
```bash
# Install Nginx
sudo apt install -y nginx

# Create Nginx configuration for test environment
cat > /etc/nginx/sites-available/unierp-test << 'EOF'
server {
    listen 80;
    server_name test.unierp.com;
    
    client_max_body_size 1G;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Proxy to UniERP
    location / {
        proxy_pass http://127.0.0.1:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
        send_timeout 600s;
    }
    
    # Static files
    location /web/static/ {
        alias /opt/unierp/addons/web/static/;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
    
    # Long polling
    location /longpolling {
        proxy_pass http://127.0.0.1:8072;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/unierp-test /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 2.4.2 SSL Configuration
```bash
# Install Certbot for SSL certificates
sudo apt install -y certbot python3-certbot-nginx

# Generate SSL certificate
sudo certbot --nginx -d test.unierp.com --email admin@unierp.com --agree-tos --non-interactive

# Auto-renewal
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

---

## 3. Test Data Management

### 3.1 Test Data Strategy

#### 3.1.1 Data Categories
- **Master Data:** Companies, users, products, customers, suppliers
- **Transactional Data:** Sales orders, purchase orders, invoices, payments
- **Configuration Data:** System settings, workflows, reports
- **Test Scenarios:** Specific test case data and scenarios

#### 3.1.2 Data Generation Approach
- **Synthetic Data:** Automated generation for consistent testing
- **Anonymized Production Data:** Production data with sensitive information masked
- **Manual Test Data:** Specific scenarios created manually
- **Dynamic Data:** Data generated during test execution

### 3.2 Test Data Generation

#### 3.2.1 Automated Data Generation Script
```python
# /opt/unierp/scripts/generate_test_data.py
import random
import faker
from datetime import datetime, timedelta

class TestDataGenerator:
    def __init__(self):
        self.fake = faker.Faker()
        self.companies = []
        self.users = []
        self.products = []
        self.customers = []
        
    def generate_companies(self, count=10):
        """Generate test companies"""
        for i in range(count):
            company = {
                'name': f'UniERP Test Company {i+1}',
                'email': self.fake.company_email(),
                'phone': self.fake.phone_number(),
                'address': self.fake.address(),
                'website': f'https://test-company{i+1}.unierp.com',
                'tax_id': self.fake.ssn(),
                'created_date': datetime.now() - timedelta(days=random.randint(1, 365))
            }
            self.companies.append(company)
        return self.companies
    
    def generate_users(self, count=50):
        """Generate test users"""
        roles = ['Admin', 'Manager', 'User', 'Viewer']
        for i in range(count):
            user = {
                'name': self.fake.name(),
                'email': self.fake.email(),
                'login': f'user{i+1:03d}',
                'password': 'Test123!',
                'role': random.choice(roles),
                'company': random.choice(self.companies) if self.companies else None,
                'active': True,
                'created_date': datetime.now() - timedelta(days=random.randint(1, 180))
            }
            self.users.append(user)
        return self.users
    
    def generate_products(self, count=100):
        """Generate test products"""
        categories = ['Electronics', 'Furniture', 'Office Supplies', 'Software', 'Services']
        for i in range(count):
            product = {
                'name': f'Test Product {i+1}',
                'description': self.fake.text(max_nb_chars=200),
                'category': random.choice(categories),
                'price': round(random.uniform(10.0, 1000.0), 2),
                'cost': round(random.uniform(5.0, 500.0), 2),
                'sku': f'TP{i+1:04d}',
                'barcode': f'{random.randint(1000000000, 9999999999)}',
                'active': True,
                'created_date': datetime.now() - timedelta(days=random.randint(1, 90))
            }
            self.products.append(product)
        return self.products
    
    def generate_customers(self, count=200):
        """Generate test customers"""
        for i in range(count):
            customer = {
                'name': self.fake.company(),
                'contact_person': self.fake.name(),
                'email': self.fake.email(),
                'phone': self.fake.phone_number(),
                'address': self.fake.address(),
                'city': self.fake.city(),
                'country': self.fake.country(),
                'tax_id': self.fake.ssn(),
                'credit_limit': round(random.uniform(0.0, 10000.0), 2),
                'active': True,
                'created_date': datetime.now() - timedelta(days=random.randint(1, 365))
            }
            self.customers.append(customer)
        return self.customers
    
    def generate_transactional_data(self):
        """Generate transactional data"""
        transactions = []
        for i in range(500):
            transaction = {
                'type': random.choice(['Sale', 'Purchase', 'Payment', 'Refund']),
                'customer': random.choice(self.customers) if self.customers else None,
                'product': random.choice(self.products) if self.products else None,
                'quantity': random.randint(1, 100),
                'unit_price': round(random.uniform(10.0, 1000.0), 2),
                'total_amount': round(random.uniform(10.0, 50000.0), 2),
                'date': datetime.now() - timedelta(days=random.randint(0, 365)),
                'status': random.choice(['Draft', 'Confirmed', 'Paid', 'Cancelled'])
            }
            transactions.append(transaction)
        return transactions

if __name__ == '__main__':
    generator = TestDataGenerator()
    
    # Generate test data
    companies = generator.generate_companies(10)
    users = generator.generate_users(50)
    products = generator.generate_products(100)
    customers = generator.generate_customers(200)
    transactions = generator.generate_transactional_data()
    
    print(f"Generated {len(companies)} companies")
    print(f"Generated {len(users)} users")
    print(f"Generated {len(products)} products")
    print(f"Generated {len(customers)} customers")
    print(f"Generated {len(transactions)} transactions")
```

#### 3.2.2 Data Loading Script
```python
# /opt/unierp/scripts/load_test_data.py
import sys
import os
sys.path.append('/opt/unierp')

from unierp import models
from generate_test_data import TestDataGenerator

class TestDataLoader:
    def __init__(self, database_config):
        self.database_config = database_config
        self.generator = TestDataGenerator()
    
    def load_all_data(self):
        """Load all test data into database"""
        try:
            # Connect to database
            self.connect_database()
            
            # Generate and load data
            print("Generating test data...")
            companies = self.generator.generate_companies(10)
            users = self.generator.generate_users(50)
            products = self.generator.generate_products(100)
            customers = self.generator.generate_customers(200)
            transactions = self.generator.generate_transactional_data()
            
            print("Loading data into database...")
            self.load_companies(companies)
            self.load_users(users)
            self.load_products(products)
            self.load_customers(customers)
            self.load_transactions(transactions)
            
            print("Test data loaded successfully!")
            
        except Exception as e:
            print(f"Error loading test data: {e}")
            sys.exit(1)
        finally:
            self.close_database()
    
    def connect_database(self):
        """Connect to test database"""
        # Database connection logic here
        pass
    
    def load_companies(self, companies):
        """Load companies into database"""
        for company in companies:
            # Insert company into database
            pass
    
    def load_users(self, users):
        """Load users into database"""
        for user in users:
            # Insert user into database
            pass
    
    def load_products(self, products):
        """Load products into database"""
        for product in products:
            # Insert product into database
            pass
    
    def load_customers(self, customers):
        """Load customers into database"""
        for customer in customers:
            # Insert customer into database
            pass
    
    def load_transactions(self, transactions):
        """Load transactions into database"""
        for transaction in transactions:
            # Insert transaction into database
            pass
    
    def close_database(self):
        """Close database connection"""
        # Close database connection
        pass

if __name__ == '__main__':
    # Database configuration for test environment
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'unierp_test',
        'user': 'unierp',
        'password': 'secure_password'
    }
    
    loader = TestDataLoader(db_config)
    loader.load_all_data()
```

### 3.3 Data Privacy and Security

#### 3.3.1 Data Anonymization
```python
# /opt/unierp/scripts/anonymize_data.py
import hashlib
import random
import string

class DataAnonymizer:
    def __init__(self):
        self.salt = 'unierp-test-salt'
    
    def anonymize_email(self, email):
        """Anonymize email addresses"""
        username, domain = email.split('@')
        hash_value = hashlib.sha256((username + self.salt).encode()).hexdigest()[:8]
        return f"user_{hash_value}@{domain}"
    
    def anonymize_phone(self, phone):
        """Anonymize phone numbers"""
        # Keep country code, anonymize rest
        if phone.startswith('+'):
            return phone[:3] + '*' * (len(phone) - 3)
        else:
            return phone[:2] + '*' * (len(phone) - 2)
    
    def anonymize_name(self, name):
        """Anonymize names"""
        return f"Test User {random.randint(1000, 9999)}"
    
    def anonymize_address(self, address):
        """Anonymize addresses"""
        return f"{random.randint(100, 999)} Test Street, Test City, TC 12345"
    
    def anonymize_ssn(self, ssn):
        """Anonymize social security numbers"""
        return f"XXX-XX-{random.randint(1000, 9999)}"
    
    def anonymize_financial_data(self, amount):
        """Anonymize financial amounts"""
        # Keep ranges but change exact values
        if amount < 100:
            return round(random.uniform(10, 99), 2)
        elif amount < 1000:
            return round(random.uniform(100, 999), 2)
        else:
            return round(random.uniform(1000, 9999), 2)
```

#### 3.3.2 Data Masking Procedures
```bash
# Data masking script
cat > /opt/unierp/scripts/mask_production_data.sh << 'EOF'
#!/bin/bash

# Backup production data before masking
pg_dump -h production-db -U unierp -d unierp_production | gzip > /var/backups/unierp/production_backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Create masked copy
createdb -h localhost -U unierp unierp_test_masked

# Export and mask data
python3 /opt/unierp/scripts/anonymize_and_load.py

# Verify masking
python3 /opt/unierp/scripts/verify_masking.py

echo "Data masking completed successfully"
EOF

chmod +x /opt/unierp/scripts/mask_production_data.sh
```

---

## 4. Environment Maintenance

### 4.1 Regular Maintenance Tasks

#### 4.1.1 Daily Maintenance
```bash
# /opt/unierp/scripts/daily_maintenance.sh
#!/bin/bash

# Clean up temporary files
find /tmp -name "unierp_*" -mtime +1 -delete

# Rotate logs
logrotate -f /etc/logrotate.d/unierp

# Check disk space
df -h | grep -E "/(var|opt)" | awk '{print $5}' | sed 's/%//' | while read usage; do
    if [ $usage -gt 80 ]; then
        echo "Warning: Disk usage is ${usage}%" | mail -s "Disk Space Alert" admin@unierp.com
    fi
done

# Check service status
systemctl is-active unierp-test || echo "UniERP test service is down" | mail -s "Service Alert" admin@unierp.com

# Update test data (if needed)
if [ $(date +%u) -eq 1 ]; then  # Monday
    python3 /opt/unierp/scripts/refresh_test_data.py
fi
```

#### 4.1.2 Weekly Maintenance
```bash
# /opt/unierp/scripts/weekly_maintenance.sh
#!/bin/bash

# Full database backup
pg_dump -h localhost -U unierp -d unierp_test | gzip > /var/backups/unierp/test_weekly_$(date +%Y%m%d).sql.gz

# Update UniERP code
cd /opt/unierp
git pull origin main
pip install -r requirements.txt

# Restart services
systemctl restart unierp-test
systemctl restart nginx

# Clean up old backups
find /var/backups/unierp -name "*.sql.gz" -mtime +30 -delete

# Performance optimization
python3 /opt/unierp/scripts/optimize_database.py
```

#### 4.1.3 Monthly Maintenance
```bash
# /opt/unierp/scripts/monthly_maintenance.sh
#!/bin/bash

# Security updates
apt update && apt upgrade -y

# Certificate renewal check
certbot certificates

# Performance testing
python3 /opt/unierp/scripts/run_performance_tests.py

# Security scan
python3 /opt/unierp/scripts/security_scan.py

# Generate maintenance report
python3 /opt/unierp/scripts/generate_maintenance_report.py
```

### 4.2 Monitoring and Alerting

#### 4.2.1 System Monitoring
```python
# /opt/unierp/monitoring/system_monitor.py
import psutil
import time
import smtplib
from email.mime.text import MimeText

class SystemMonitor:
    def __init__(self):
        self.cpu_threshold = 80
        self.memory_threshold = 80
        self.disk_threshold = 80
        self.alert_email = 'admin@unierp.com'
    
    def check_cpu_usage(self):
        """Check CPU usage"""
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > self.cpu_threshold:
            self.send_alert(f"High CPU usage: {cpu_percent}%")
        return cpu_percent
    
    def check_memory_usage(self):
        """Check memory usage"""
        memory = psutil.virtual_memory()
        if memory.percent > self.memory_threshold:
            self.send_alert(f"High memory usage: {memory.percent}%")
        return memory.percent
    
    def check_disk_usage(self):
        """Check disk usage"""
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        if disk_percent > self.disk_threshold:
            self.send_alert(f"High disk usage: {disk_percent:.1f}%")
        return disk_percent
    
    def check_service_status(self, service_name):
        """Check if service is running"""
        try:
            import subprocess
            result = subprocess.run(['systemctl', 'is-active', service_name], 
                                capture_output=True, text=True)
            return result.stdout.strip() == 'active'
        except Exception:
            return False
    
    def send_alert(self, message):
        """Send alert email"""
        msg = MimeText(f"UniERP Test Environment Alert: {message}")
        msg['Subject'] = 'UniERP Test Environment Alert'
        msg['From'] = 'monitor@unierp.com'
        msg['To'] = self.alert_email
        
        # Send email (implementation depends on SMTP configuration)
        # smtplib.SMTP('localhost').send_message(msg)
        print(f"ALERT: {message}")
    
    def run_monitoring(self):
        """Run continuous monitoring"""
        while True:
            self.check_cpu_usage()
            self.check_memory_usage()
            self.check_disk_usage()
            
            # Check critical services
            services = ['unierp-test', 'nginx', 'postgresql']
            for service in services:
                if not self.check_service_status(service):
                    self.send_alert(f"Service {service} is down")
            
            time.sleep(60)  # Check every minute

if __name__ == '__main__':
    monitor = SystemMonitor()
    monitor.run_monitoring()
```

#### 4.2.2 Application Monitoring
```python
# /opt/unierp/monitoring/application_monitor.py
import requests
import time
import json
from datetime import datetime

class ApplicationMonitor:
    def __init__(self):
        self.base_url = 'https://test.unierp.com'
        self.health_endpoint = '/web/health'
        self.login_endpoint = '/web/login'
        self.alert_threshold = 5  # consecutive failures
    
    def check_health(self):
        """Check application health"""
        try:
            response = requests.get(f"{self.base_url}{self.health_endpoint}", 
                                 timeout=10)
            return response.status_code == 200
        except Exception:
            return False
    
    def check_login_functionality(self):
        """Check login functionality"""
        try:
            response = requests.post(f"{self.base_url}{self.login_endpoint}",
                                 data={'login': 'admin', 'password': 'admin'},
                                 timeout=10)
            return response.status_code in [200, 302]
        except Exception:
            return False
    
    def check_response_time(self):
        """Check application response time"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}{self.health_endpoint}", 
                                 timeout=10)
            response_time = time.time() - start_time
            return response_time < 2.0  # 2 seconds threshold
        except Exception:
            return False
    
    def log_monitoring_data(self, health_status, login_status, response_time_status):
        """Log monitoring data"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'health_check': health_status,
            'login_check': login_status,
            'response_time_check': response_time_status
        }
        
        with open('/var/log/unierp/monitoring.log', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def run_monitoring(self):
        """Run application monitoring"""
        consecutive_failures = 0
        
        while True:
            health_ok = self.check_health()
            login_ok = self.check_login_functionality()
            response_time_ok = self.check_response_time()
            
            self.log_monitoring_data(health_ok, login_ok, response_time_ok)
            
            if not (health_ok and login_ok and response_time_ok):
                consecutive_failures += 1
                if consecutive_failures >= self.alert_threshold:
                    self.send_alert("Application monitoring detected multiple failures")
                    consecutive_failures = 0
            else:
                consecutive_failures = 0
            
            time.sleep(300)  # Check every 5 minutes
    
    def send_alert(self, message):
        """Send monitoring alert"""
        # Implementation depends on alerting system
        print(f"APPLICATION ALERT: {message}")

if __name__ == '__main__':
    monitor = ApplicationMonitor()
    monitor.run_monitoring()
```

---

## 5. Environment Security

### 5.1 Access Control

#### 5.1.1 User Access Management
```bash
# Create user groups for different access levels
sudo groupadd unierp-dev
sudo groupadd unierp-qa
sudo groupadd unierp-admin

# Add users to appropriate groups
sudo usermod -aG unierp-dev developer1
sudo usermod -aG unierp-qa qa1
sudo usermod -aG unierp-admin admin1

# Set directory permissions
sudo chown -R root:unierp-dev /opt/unierp/src
sudo chown -R root:unierp-qa /opt/unierp/tests
sudo chown -R root:unierp-admin /opt/unierp/config
```

#### 5.1.2 SSH Configuration
```bash
# /etc/ssh/sshd_config security hardening
Port 2222  # Non-standard port
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
AllowGroups unierp-dev unierp-qa unierp-admin

# Restart SSH service
sudo systemctl restart sshd
```

#### 5.1.3 Firewall Configuration
```bash
# UFW firewall configuration
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH on custom port
sudo ufw allow 2222/tcp

# Allow web traffic
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow database access from specific IPs
sudo ufw allow from 10.0.2.0/24 to any port 5432
sudo ufw allow from 10.0.3.0/24 to any port 5432

# Enable firewall
sudo ufw enable
```

### 5.2 Security Hardening

#### 5.2.1 SSL/TLS Configuration
```nginx
# Enhanced SSL configuration in Nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
ssl_stapling on;
ssl_stapling_verify on;

# HSTS
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

# Other security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

#### 5.2.2 Application Security
```python
# Security configuration for UniERP
class SecurityConfig:
    # Session security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_AGE = 3600  # 1 hour
    SESSION_SAVE_EVERY_REQUEST = True
    
    # CSRF protection
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_TRUSTED_ORIGINS = ['https://test.unierp.com']
    
    # Content security
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    
    # Password policy
    PASSWORD_MIN_LENGTH = 12
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_LOWERCASE = True
    PASSWORD_REQUIRE_DIGITS = True
    PASSWORD_REQUIRE_SPECIAL = True
    PASSWORD_HISTORY_COUNT = 5
    
    # Rate limiting
    LOGIN_ATTEMPT_LIMIT = 5
    LOGIN_ATTEMPT_TIMEOUT = 300  # 5 minutes
    API_RATE_LIMIT = 100  # requests per minute
```

---

## 6. Troubleshooting Guide

### 6.1 Common Issues and Solutions

#### 6.1.1 Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check database connectivity
psql -h localhost -U unierp -d unierp_test -c "SELECT 1;"

# Check database logs
sudo tail -f /var/log/postgresql/postgresql-13-main.log

# Common solutions
# 1. Restart PostgreSQL
sudo systemctl restart postgresql

# 2. Check database configuration
sudo -u postgres psql -c "SHOW config_file;"

# 3. Verify user permissions
sudo -u postgres psql -c "\du"
```

#### 6.1.2 Application Startup Issues
```bash
# Check UniERP service status
sudo systemctl status unierp-test

# Check application logs
sudo tail -f /var/log/unierp/test/unierp.log

# Check configuration
python3 -c "from config.test import TestConfig; print('Config OK')"

# Common solutions
# 1. Check dependencies
pip install -r requirements.txt

# 2. Verify file permissions
sudo chown -R unierp:unierp /opt/unierp
sudo chown -R unierp:unierp /var/lib/unierp
sudo chown -R unierp:unierp /var/log/unierp

# 3. Restart service
sudo systemctl restart unierp-test
```

#### 6.1.3 Performance Issues
```bash
# Check system resources
top
htop
iostat
free -h
df -h

# Check database performance
sudo -u postgres psql -d unierp_test -c "SELECT * FROM pg_stat_activity;"

# Check slow queries
sudo -u postgres psql -d unierp_test -c "SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"

# Common solutions
# 1. Optimize database
sudo -u postgres psql -d unierp_test -c "VACUUM ANALYZE;"

# 2. Restart services
sudo systemctl restart postgresql
sudo systemctl restart unierp-test
sudo systemctl restart nginx

# 3. Clear caches
python3 -c "from unierp import cache; cache.clear()"
```

### 6.2 Emergency Procedures

#### 6.2.1 Service Recovery
```bash
# Emergency service recovery script
cat > /opt/unierp/scripts/emergency_recovery.sh << 'EOF'
#!/bin/bash

echo "Starting emergency recovery procedures..."

# Stop all services
sudo systemctl stop unierp-test
sudo systemctl stop nginx
sudo systemctl stop postgresql

# Wait for services to stop
sleep 10

# Start services in correct order
sudo systemctl start postgresql
sleep 5
sudo systemctl start unierp-test
sleep 5
sudo systemctl start nginx

# Verify services are running
sudo systemctl status postgresql
sudo systemctl status unierp-test
sudo systemctl status nginx

# Send notification
echo "Emergency recovery completed at $(date)" | mail -s "UniERP Emergency Recovery" admin@unierp.com
EOF

chmod +x /opt/unierp/scripts/emergency_recovery.sh
```

#### 6.2.2 Data Recovery
```bash
# Data recovery script
cat > /opt/unierp/scripts/data_recovery.sh << 'EOF'
#!/bin/bash

BACKUP_FILE=$1
DATABASE=$2

if [ -z "$BACKUP_FILE" ] || [ -z "$DATABASE" ]; then
    echo "Usage: $0 <backup_file> <database_name>"
    exit 1
fi

echo "Recovering data to database: $DATABASE"

# Drop existing database
sudo -u postgres dropdb $DATABASE

# Create new database
sudo -u postgres createdb $DATABASE

# Restore from backup
gunzip -c $BACKUP_FILE | sudo -u postgres psql $DATABASE

echo "Data recovery completed"
EOF

chmod +x /opt/unierp/scripts/data_recovery.sh
```

---

## 7. Documentation and Procedures

### 7.1 Environment Documentation

#### 7.1.1 Environment Inventory
| Environment | Purpose | Server IP | Database | Status | Contact |
|-------------|---------|-----------|----------|---------|---------|
| Development | Unit testing | 10.0.1.10 | unierp_dev | Active | dev-team@unierp.com |
| Integration | Integration testing | 10.0.2.10 | unierp_integration | Active | qa-team@unierp.com |
| System | System testing | 10.0.2.20 | unierp_system | Active | qa-team@unierp.com |
| Performance | Load testing | 10.0.3.10 | unierp_performance | Active | qa-team@unierp.com |
| Security | Security testing | 10.0.4.10 | unierp_security | Active | security@unierp.com |
| UAT | User acceptance | 10.0.5.10 | unierp_uat | Active | qa-team@unierp.com |

#### 7.1.2 Access Matrix
| Role | Development | Integration | System | Performance | Security | UAT |
|-------|-------------|-------------|---------|-------------|----------|-----|
| Developer | Read/Write | Read | Read | Read | No Access | Read |
| QA Engineer | Read | Read/Write | Read/Write | Read/Write | Read/Write | Read/Write |
| DevOps Engineer | Admin | Admin | Admin | Admin | Admin | Admin |
| Project Manager | Read | Read | Read | Read | Read | Read |
| Business User | No Access | No Access | No Access | No Access | No Access | Read/Write |

### 7.2 Standard Operating Procedures

#### 7.2.1 Environment Setup Procedure
1. **Planning**
   - Define environment requirements
   - Allocate resources
   - Schedule setup timeline

2. **Infrastructure Setup**
   - Provision servers
   - Install operating system
   - Configure network settings

3. **Software Installation**
   - Install required software
   - Configure applications
   - Set up services

4. **Data Preparation**
   - Create databases
   - Load test data
   - Configure data privacy

5. **Testing and Validation**
   - Test functionality
   - Validate performance
   - Verify security

6. **Documentation**
   - Document configuration
   - Create procedures
   - Train team members

#### 7.2.2 Environment Refresh Procedure
1. **Preparation**
   - Schedule refresh window
   - Notify stakeholders
   - Backup current data

2. **Data Refresh**
   - Clear existing data
   - Load fresh test data
   - Validate data integrity

3. **Configuration Update**
   - Update configurations
   - Restart services
   - Verify functionality

4. **Testing**
   - Run smoke tests
   - Validate key functionality
   - Document results

5. **Communication**
   - Notify completion
   - Update documentation
   - Record lessons learned

---

## 8. Conclusion

This comprehensive test environment setup guide provides the foundation for effective testing operations in the UniERP rebranding project. Proper environment configuration, data management, security measures, and maintenance procedures ensure reliable and efficient testing activities.

Regular reviews and updates to this guide will ensure its continued relevance and effectiveness throughout the project lifecycle. All team members should familiarize themselves with these procedures and follow them consistently to maintain testing environment quality and reliability.

For questions or support regarding test environment setup, please contact the UniERP DevOps Team at devops@unierp.com.

---

**Document Status:** Approved
**Next Review Date:** December 2024
**Document Owner:** UniERP DevOps Team
**Contact Information:** devops@unierp.com | +1-555-UNIERP-DEVOPS