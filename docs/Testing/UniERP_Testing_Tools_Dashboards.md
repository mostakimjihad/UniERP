# UniERP Testing Tools & Dashboards Configuration

## Overview

This document provides comprehensive guidelines for configuring and using testing tools and dashboards for the UniERP testing framework. It covers tool setup, dashboard configuration, monitoring, and reporting systems to support effective testing operations.

## Document Information

- **Project:** UniERP Rebranding Project
- **Phase:** Phase 11 - Testing & Quality Assurance
- **Milestone:** 11.1 - Test Planning & Setup
- **Version:** 1.0
- **Created:** November 2024
- **Last Updated:** November 2024
- **Author:** UniERP QA Tools Team
- **Contact:** qa-tools@unierp.com

---

## 1. Testing Tools Overview

### 1.1 Tool Categories

#### 1.1.1 Test Management Tools
- **TestRail:** Test case management and execution tracking
- **GitLab Issues:** Defect tracking and project management
- **Jira (Alternative):** Enterprise test management
- **TestLink (Legacy):** Open source test management

#### 1.1.2 Automation Tools
- **Selenium WebDriver:** Web UI automation
- **pytest:** Python test framework and runner
- **JMeter:** Performance and load testing
- **OWASP ZAP:** Security vulnerability scanning
- **Postman:** API testing and documentation

#### 1.1.3 Monitoring Tools
- **Grafana:** Metrics visualization and dashboards
- **Prometheus:** Metrics collection and storage
- **New Relic:** Application performance monitoring
- **ELK Stack:** Log aggregation and analysis
- **Sentry:** Error tracking and alerting

#### 1.1.4 Reporting Tools
- **Allure:** Test execution reporting
- **ReportLab:** Custom report generation
- **Matplotlib/Seaborn:** Data visualization
- **Jinja2:** Report templating

### 1.2 Tool Integration Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Test Runner  │    │   Test Manager │    │   Defect Tracker│
│   (pytest)     │    │   (TestRail)   │    │   (GitLab)      │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┴──────────────────────┘
                                │
                    ┌─────────┴───────┐
                    │   Monitoring    │
                    │   (Grafana)    │
                    └─────────┬───────┘
                              │
                    ┌─────────┴───────┐
                    │   Reporting     │
                    │   (Allure)     │
                    └──────────────────┘
```

---

## 2. Test Management Tools Configuration

### 2.1 TestRail Setup

#### 2.1.1 TestRail Installation
```bash
# TestRail installation (self-hosted)
cd /opt
wget https://www.gurock.com/testrail/downloads/testrail-latest-en.zip
unzip testrail-latest-en.zip -d testrail

# Configure Apache
sudo apt install -y apache2 libapache2-mod-php
sudo a2enmod rewrite
sudo a2enmod ssl

# Configure VirtualHost
sudo cp /opt/testrail/apache2/vhost.conf /etc/apache2/sites-available/testrail.conf
sudo a2ensite testrail.conf
sudo systemctl reload apache2

# Set permissions
sudo chown -R www-data:www-data /opt/testrail
sudo chmod -R 755 /opt/testrail
```

#### 2.1.2 TestRail Configuration
```php
// config.php
<?php
define('TESTRAIL_LICENSE', 'YOUR_LICENSE_KEY');

// Database Configuration
define('DB_HOST', 'localhost');
define('DB_NAME', 'testrail');
define('DB_USER', 'testrail');
define('DB_PASSWORD', 'secure_password');

// UniERP Branding Configuration
define('APPLICATION_NAME', 'UniERP Test Management');
define('COMPANY_NAME', 'UniERP Solutions');
define('COMPANY_URL', 'https://www.unierp.com');
define('SUPPORT_EMAIL', 'qa@unierp.com');

// Email Configuration
define('SMTP_HOST', 'smtp.unierp.com');
define('SMTP_PORT', 587);
define('SMTP_USER', 'testrail@unierp.com');
define('SMTP_PASSWORD', 'smtp_password');

// Security Configuration
define('ENCRYPTION_KEY', 'your-encryption-key');
define('SESSION_TIMEOUT', 7200); // 2 hours
define('PASSWORD_MIN_LENGTH', 12);

// Integration Configuration
define('GITLAB_URL', 'https://gitlab.unierp.com');
define('GITLAB_TOKEN', 'your-gitlab-token');
define('JIRA_URL', ''); // Optional JIRA integration
?>
```

#### 2.1.3 TestRail Project Setup
```python
# scripts/setup_testrail_project.py
import requests
import json

class TestRailSetup:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = (username, password)
        self.headers = {'Content-Type': 'application/json'}
    
    def create_project(self):
        """Create UniERP test project"""
        project_data = {
            "name": "UniERP Rebranding Project",
            "announcement": "Test project for UniERP rebranding validation",
            "show_announcement": True,
            "is_completed": False,
            "suite_mode": 3,  # Multiple test suites
            "default_template_id": 1
        }
        
        response = requests.post(
            f"{self.base_url}/index.php?/api/v2/add_project",
            auth=self.auth,
            headers=self.headers,
            json=project_data
        )
        
        if response.status_code == 200:
            project = response.json()
            print(f"Created project: {project['name']} (ID: {project['id']})")
            return project['id']
        else:
            print(f"Failed to create project: {response.text}")
            return None
    
    def create_test_suites(self, project_id):
        """Create test suites for UniERP testing"""
        suites = [
            {
                "name": "Smoke Tests",
                "description": "Critical path smoke tests for UniERP"
            },
            {
                "name": "Functional Tests",
                "description": "Functional testing for UniERP modules"
            },
            {
                "name": "Branding Tests",
                "description": "UniERP branding verification tests"
            },
            {
                "name": "Performance Tests",
                "description": "Performance and load testing"
            },
            {
                "name": "Security Tests",
                "description": "Security vulnerability testing"
            },
            {
                "name": "Integration Tests",
                "description": "Cross-module integration testing"
            }
        ]
        
        suite_ids = []
        for suite in suites:
            suite['project_id'] = project_id
            response = requests.post(
                f"{self.base_url}/index.php?/api/v2/add_suite",
                auth=self.auth,
                headers=self.headers,
                json=suite
            )
            
            if response.status_code == 200:
                suite_result = response.json()
                suite_ids.append(suite_result['id'])
                print(f"Created suite: {suite['name']} (ID: {suite_result['id']})")
        
        return suite_ids
    
    def create_milestones(self, project_id):
        """Create milestones for UniERP project"""
        milestones = [
            {
                "name": "Milestone 11.1 - Test Planning & Setup",
                "description": "Test planning and environment setup completed",
                "due_on": "2024-12-01"
            },
            {
                "name": "Milestone 11.2 - Functional Testing",
                "description": "Functional testing phase completed",
                "due_on": "2024-12-05"
            },
            {
                "name": "Milestone 11.3 - Branding Verification",
                "description": "UniERP branding verification completed",
                "due_on": "2024-12-06"
            },
            {
                "name": "Milestone 11.4 - Performance Testing",
                "description": "Performance testing completed",
                "due_on": "2024-12-08"
            },
            {
                "name": "Milestone 11.5 - Security Testing",
                "description": "Security testing completed",
                "due_on": "2024-12-10"
            },
            {
                "name": "Milestone 11.6 - User Acceptance Testing",
                "description": "UAT phase completed",
                "due_on": "2024-12-11"
            }
        ]
        
        for milestone in milestones:
            milestone['project_id'] = project_id
            response = requests.post(
                f"{self.base_url}/index.php?/api/v2/add_milestone",
                auth=self.auth,
                headers=self.headers,
                json=milestone
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Created milestone: {milestone['name']} (ID: {result['id']})")

# Usage
if __name__ == "__main__":
    setup = TestRailSetup(
        base_url="https://testrail.unierp.com",
        username="admin@unierp.com",
        password="secure_password"
    )
    
    project_id = setup.create_project()
    if project_id:
        setup.create_test_suites(project_id)
        setup.create_milestones(project_id)
```

### 2.2 GitLab Issues Configuration

#### 2.2.1 GitLab Project Setup
```yaml
# .gitlab-ci.yml for testing
stages:
  - test
  - report
  - defect-tracking

variables:
  TESTRAIL_URL: "https://testrail.unierp.com"
  TESTRAIL_PROJECT: "UniERP Rebranding Project"

test_execution:
  stage: test
  script:
    - pytest tests/ --testrail-url=$TESTRAIL_URL --testrail-project=$TESTRAIL_PROJECT
  artifacts:
    reports:
      junit: reports/junit.xml
    paths:
      - reports/
  only:
    - merge_requests
    - main

defect_reporting:
  stage: defect-tracking
  script:
    - python scripts/report_defects.py --testrail-url=$TESTRAIL_URL
  dependencies:
    - test_execution
  only:
    - main
```

#### 2.2.2 Defect Reporting Script
```python
# scripts/report_defects.py
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

class DefectReporter:
    def __init__(self, gitlab_url, gitlab_token, testrail_url, testrail_project):
        self.gitlab_url = gitlab_url
        self.gitlab_token = gitlab_token
        self.testrail_url = testrail_url
        self.testrail_project = testrail_project
        self.gitlab_headers = {
            'PRIVATE-TOKEN': gitlab_token,
            'Content-Type': 'application/json'
        }
    
    def parse_junit_results(self, junit_file):
        """Parse JUnit XML results"""
        tree = ET.parse(junit_file)
        root = tree.getroot()
        
        failed_tests = []
        for testcase in root.findall('.//testcase'):
            failure = testcase.find('failure')
            if failure is not None:
                failed_tests.append({
                    'name': testcase.get('name'),
                    'classname': testcase.get('classname'),
                    'failure_message': failure.get('message'),
                    'failure_details': failure.text
                })
        
        return failed_tests
    
    def create_gitlab_issue(self, test_failure):
        """Create GitLab issue for test failure"""
        title = f"[TEST FAILURE] {test_failure['name']}"
        
        description = f"""
## Test Failure Details

**Test Name:** {test_failure['name']}
**Class:** {test_failure['classname']}
**Failure Message:** {test_failure['failure_message']}

### Failure Details
```
{test_failure['failure_details']}
```

### Environment Information
- **Test Environment:** Integration
- **Test Execution Time:** {datetime.now().isoformat()}
- **UniERP Version:** 16.0
- **Browser:** Chrome (automated)

### Action Required
1. Investigate the test failure
2. Fix the underlying issue
3. Update test if needed
4. Verify fix and close issue

### UniERP Branding Note
This issue affects the UniERP rebranding project quality. Please ensure all fixes maintain UniERP branding consistency.

---
*This issue was automatically generated by UniERP Test Automation Framework*
*Contact: qa@unierp.com*
        """
        
        issue_data = {
            'title': title,
            'description': description,
            'labels': ['bug', 'test-failure', 'unierp-branding'],
            'assignee_ids': [1, 2, 3],  # QA team members
            'milestone': '11.1 - Test Planning & Setup',
            'weight': 5
        }
        
        response = requests.post(
            f"{self.gitlab_url}/api/v4/projects/unierp%2Funierp-testing/issues",
            headers=self.gitlab_headers,
            json=issue_data
        )
        
        if response.status_code == 201:
            issue = response.json()
            print(f"Created issue: {issue['title']} (#{issue['iid']})")
            return issue['iid']
        else:
            print(f"Failed to create issue: {response.text}")
            return None
    
    def update_testrail_result(self, test_failure, issue_id):
        """Update TestRail with GitLab issue reference"""
        # This would integrate with TestRail API to add defect reference
        pass
    
    def report_failures(self, junit_file):
        """Report all test failures to GitLab"""
        failed_tests = self.parse_junit_results(junit_file)
        
        for test_failure in failed_tests:
            issue_id = self.create_gitlab_issue(test_failure)
            if issue_id:
                self.update_testrail_result(test_failure, issue_id)

# Usage
if __name__ == "__main__":
    reporter = DefectReporter(
        gitlab_url="https://gitlab.unierp.com",
        gitlab_token="your-gitlab-token",
        testrail_url="https://testrail.unierp.com",
        testrail_project="UniERP Rebranding Project"
    )
    
    reporter.report_failures("reports/junit.xml")
```

---

## 3. Monitoring and Dashboard Configuration

### 3.1 Grafana Setup

#### 3.1.1 Grafana Installation
```bash
# Install Grafana
sudo apt-get install -y apt-transport-https software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt-get update
sudo apt-get install -y grafana

# Start Grafana
sudo systemctl enable grafana-server
sudo systemctl start grafana-server

# Install Prometheus data source
grafana-cli plugins install grafana-prometheus-datasource

# Install UniERP dashboard plugin
grafana-cli plugins install unierp-testing-dashboard
```

#### 3.1.2 Grafana Configuration
```ini
# /etc/grafana/grafana.ini
[server]
# UniERP Branding
app_name = UniERP Testing Dashboard
root_url = https://grafana.unierp.com

[security]
admin_user = admin
admin_password = secure_password
secret_key = your-secret-key

[database]
type = postgres
host = localhost:5432
name = grafana
user = grafana
password = grafana_password

[users]
allow_sign_up = false
auto_assign_org_role = Viewer

[smtp]
enabled = true
host = smtp.unierp.com:587
user = grafana@unierp.com
password = smtp_password
from_address = grafana@unierp.com
from_name = UniERP Grafana

[log]
mode = file
level = info
```

#### 3.1.3 UniERP Dashboard Configuration
```json
{
  "dashboard": {
    "id": null,
    "title": "UniERP Testing Dashboard",
    "tags": ["unierp", "testing", "qa"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Test Execution Status",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(unierp_test_total)",
            "legendFormat": "Total Tests"
          },
          {
            "expr": "sum(unierp_test_passed)",
            "legendFormat": "Passed Tests"
          },
          {
            "expr": "sum(unierp_test_failed)",
            "legendFormat": "Failed Tests"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {
              "mode": "palette-classic"
            },
            "custom": {
              "displayMode": "list",
              "orientation": "horizontal"
            }
          }
        }
      },
      {
        "id": 2,
        "title": "UniERP Branding Score",
        "type": "gauge",
        "targets": [
          {
            "expr": "unierp_branding_score",
            "legendFormat": "Branding Score"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "min": 0,
            "max": 100,
            "thresholds": {
              "steps": [
                {
                  "color": "red",
                  "value": 70
                },
                {
                  "color": "yellow",
                  "value": 85
                },
                {
                  "color": "green",
                  "value": 95
                }
              ]
            }
          }
        }
      },
      {
        "id": 3,
        "title": "Test Execution Trend",
        "type": "timeseries",
        "targets": [
          {
            "expr": "rate(unierp_test_total[5m])",
            "legendFormat": "Tests per Minute"
          },
          {
            "expr": "rate(unierp_test_passed[5m])",
            "legendFormat": "Passed per Minute"
          },
          {
            "expr": "rate(unierp_test_failed[5m])",
            "legendFormat": "Failed per Minute"
          }
        ]
      },
      {
        "id": 4,
        "title": "Module Test Coverage",
        "type": "piechart",
        "targets": [
          {
            "expr": "sum by (module) (unierp_test_total)",
            "legendFormat": "{{module}}"
          }
        ]
      },
      {
        "id": 5,
        "title": "Performance Metrics",
        "type": "table",
        "targets": [
          {
            "expr": "unierp_performance_response_time",
            "legendFormat": "Response Time",
            "format": "ms"
          },
          {
            "expr": "unierp_performance_throughput",
            "legendFormat": "Throughput",
            "format": "req/s"
          }
        ]
      },
      {
        "id": 6,
        "title": "Security Scan Results",
        "type": "stat",
        "targets": [
          {
            "expr": "unierp_security_vulnerabilities_critical",
            "legendFormat": "Critical"
          },
          {
            "expr": "unierp_security_vulnerabilities_high",
            "legendFormat": "High"
          },
          {
            "expr": "unierp_security_vulnerabilities_medium",
            "legendFormat": "Medium"
          },
          {
            "expr": "unierp_security_vulnerabilities_low",
            "legendFormat": "Low"
          }
        ]
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "30s"
  }
}
```

### 3.2 Prometheus Configuration

#### 3.2.1 Prometheus Installation
```bash
# Install Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.40.0/prometheus-2.40.0.linux-amd64.tar.gz
tar xvfz prometheus-2.40.0.linux-amd64.tar.gz
sudo mv prometheus-2.40.0.linux-amd64 /opt/prometheus
sudo useradd --no-create-home --shell /bin/false prometheus

# Create directories
sudo mkdir -p /etc/prometheus /var/lib/prometheus
sudo chown prometheus:prometheus /etc/prometheus /var/lib/prometheus

# Configuration
sudo cp /opt/prometheus/prometheus.yml /etc/prometheus/
```

#### 3.2.2 Prometheus Configuration
```yaml
# /etc/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "unierp_rules.yml"

scrape_configs:
  - job_name: 'unierp-test-metrics'
    static_configs:
      - targets: ['localhost:9090']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'unierp-application'
    static_configs:
      - targets: ['test.unierp.com:8069']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'unierp-performance'
    static_configs:
      - targets: ['performance.unierp.com:9091']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'unierp-security'
    static_configs:
      - targets: ['security.unierp.com:9092']
    metrics_path: '/metrics'
    scrape_interval: 60s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

#### 3.2.3 UniERP Alert Rules
```yaml
# /etc/prometheus/unierp_rules.yml
groups:
  - name: unierp_testing_alerts
    rules:
      # Test execution alerts
      - alert: HighTestFailureRate
        expr: (rate(unierp_test_failed[5m]) / rate(unierp_test_total[5m])) > 0.1
        for: 2m
        labels:
          severity: warning
          service: unierp-testing
        annotations:
          summary: "High test failure rate detected"
          description: "Test failure rate is {{ $value | humanizePercentage }} for UniERP testing"

      # UniERP branding alerts
      - alert: LowBrandingScore
        expr: unierp_branding_score < 85
        for: 5m
        labels:
          severity: critical
          service: unierp-branding
        annotations:
          summary: "Low UniERP branding score"
          description: "UniERP branding score is {{ $value }}%, below threshold of 85%"

      # Performance alerts
      - alert: HighResponseTime
        expr: unierp_performance_response_time > 2000
        for: 1m
        labels:
          severity: warning
          service: unierp-performance
        annotations:
          summary: "High response time detected"
          description: "Response time is {{ $value }}ms, above threshold of 2000ms"

      # Security alerts
      - alert: CriticalVulnerabilities
        expr: unierp_security_vulnerabilities_critical > 0
        for: 0m
        labels:
          severity: critical
          service: unierp-security
        annotations:
          summary: "Critical security vulnerabilities detected"
          description: "{{ $value }} critical vulnerabilities found in UniERP"

      # Environment alerts
      - alert: TestEnvironmentDown
        expr: up{job="unierp-test-metrics"} == 0
        for: 1m
        labels:
          severity: critical
          service: unierp-infrastructure
        annotations:
          summary: "UniERP test environment is down"
          description: "Test environment metrics are not available"
```

### 3.3 AlertManager Configuration

#### 3.3.1 AlertManager Setup
```bash
# Install AlertManager
wget https://github.com/prometheus/alertmanager/releases/download/v0.25.0/alertmanager-0.25.0.linux-amd64.tar.gz
tar xvfz alertmanager-0.25.0.linux-amd64.tar.gz
sudo mv alertmanager-0.25.0.linux-amd64 /opt/alertmanager
sudo useradd --no-create-home --shell /bin/false alertmanager

# Create directories
sudo mkdir -p /etc/alertmanager /var/lib/alertmanager
sudo chown alertmanager:alertmanager /etc/alertmanager /var/lib/alertmanager
```

#### 3.3.2 AlertManager Configuration
```yaml
# /etc/alertmanager/alertmanager.yml
global:
  smtp_smarthost: 'smtp.unierp.com:587'
  smtp_from: 'alertmanager@unierp.com'
  smtp_auth_username: 'alertmanager@unierp.com'
  smtp_auth_password: 'smtp_password'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'unierp-qa-team'

receivers:
  - name: 'unierp-qa-team'
    email_configs:
      - to: 'qa-team@unierp.com'
        subject: '[UniERP Alert] {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          Labels: {{ range .Labels.SortedPairs }}{{ .Name }}={{ .Value }} {{ end }}
          {{ end }}
        html: |
          <h2>UniERP Testing Alert</h2>
          {{ range .Alerts }}
          <h3>{{ .Annotations.summary }}</h3>
          <p><strong>Description:</strong> {{ .Annotations.description }}</p>
          <p><strong>Severity:</strong> {{ .Labels.severity }}</p>
          <p><strong>Service:</strong> {{ .Labels.service }}</p>
          <hr>
          {{ end }}
          <p><em>This alert was generated by UniERP Testing Infrastructure</em></p>
          <p><em>Contact: qa@unierp.com | +1-555-UNIERP-QA</em></p>

  - name: 'unierp-critical-alerts'
    email_configs:
      - to: 'qa-lead@unierp.com,devops@unierp.com'
        subject: '[CRITICAL] UniERP Alert: {{ .GroupLabels.alertname }}'
        body: |
          CRITICAL ALERT FOR UniERP TESTING
          
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          Severity: {{ .Labels.severity }}
          Service: {{ .Labels.service }}
          Time: {{ .StartsAt }}
          {{ end }}
          
          Immediate action required!

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname']
```

---

## 4. Performance Testing Tools

### 4.1 JMeter Configuration

#### 4.1.1 JMeter Installation
```bash
# Install Java
sudo apt update
sudo apt install -y openjdk-11-jdk

# Install JMeter
wget https://downloads.apache.org//jmeter/binaries/apache-jmeter-5.5.tgz
tar -xzf apache-jmeter-5.5.tgz
sudo mv apache-jmeter-5.5 /opt/jmeter

# Create JMeter user
sudo useradd -m jmeter
sudo chown -R jmeter:jmeter /opt/jmeter

# Set environment variables
echo 'export JMETER_HOME=/opt/jmeter' >> ~/.bashrc
echo 'export PATH=$PATH:$JMETER_HOME/bin' >> ~/.bashrc
```

#### 4.1.2 UniERP Test Plan
```xml
<!-- /opt/jmeter/test_plans/UniERP_Performance_Test.jmx -->
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.5">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="UniERP Performance Test" enabled="true">
      <stringProp name="TestPlan.comments">Performance test for UniERP rebranding project</stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments">
        <collectionProp name="Arguments.arguments">
          <elementProp name="BASE_URL" elementType="Argument">
            <stringProp name="Argument.name">BASE_URL</stringProp>
            <stringProp name="Argument.value">https://test.unierp.com</stringProp>
          </elementProp>
          <elementProp name="UNIERP_LOGIN" elementType="Argument">
            <stringProp name="Argument.name">UNIERP_LOGIN</stringProp>
            <stringProp name="Argument.value">test@unierp.com</stringProp>
          </elementProp>
          <elementProp name="UNIERP_PASSWORD" elementType="Argument">
            <stringProp name="Argument.name">UNIERP_PASSWORD</stringProp>
            <stringProp name="Argument.value">Test123!</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
    </TestPlan>
    
    <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="UniERP Users" enabled="true">
      <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
      <stringProp name="ThreadGroup.num_threads">100</stringProp>
      <stringProp name="ThreadGroup.ramp_time">60</stringProp>
      <boolProp name="ThreadGroup.scheduler">true</boolProp>
      <stringProp name="ThreadGroup.duration">300</stringProp>
      <stringProp name="ThreadGroup.delay"></stringProp>
      <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
    </ThreadGroup>
    
    <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="UniERP Login" enabled="true">
      <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
        <collectionProp name="Arguments.arguments">
          <elementProp name="jsonrpc" elementType="HTTPArgument">
            <boolProp name="HTTPArgument.always_encode">false</boolProp>
            <stringProp name="Argument.value">{"jsonrpc":"2.0","params":{"db":"unierp_test","login":"${UNIERP_LOGIN}","password":"${UNIERP_PASSWORD}"},"method":"call","id":1}</stringProp>
            <stringProp name="Argument.metadata">=</stringProp>
            <boolProp name="HTTPArgument.use_equals">true</boolProp>
            <stringProp name="Argument.name">jsonrpc</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
      <stringProp name="HTTPSampler.domain">${BASE_URL}</stringProp>
      <stringProp name="HTTPSampler.path">/web/session/authenticate</stringProp>
      <stringProp name="HTTPSampler.method">POST</stringProp>
      <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
      <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
      <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
      <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
      <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
      <stringProp name="HTTPSampler.connect_timeout"></stringProp>
      <stringProp name="HTTPSampler.response_timeout"></stringProp>
    </HTTPSamplerProxy>
    
    <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="UniERP Branding Assertion" enabled="true">
      <collectionProp name="Asserion.test_strings">
        <stringProp name="49586">UniERP</stringProp>
        <stringProp name="49587">unierp.com</stringProp>
      </collectionProp>
      <stringProp name="Assertion.custom_message"></stringProp>
      <stringProp name="Assertion.test_field">Assertion.response_data</stringProp>
      <boolProp name="Assertion.assume_success">false</boolProp>
      <intProp name="Assertion.test_type">2</intProp>
    </ResponseAssertion>
    
    <ResultCollector guiclass="ViewResultsFullVisualizer" testclass="ResultCollector" testname="UniERP Test Results" enabled="true">
      <boolProp name="ResultCollector.error_logging">false</boolProp>
      <stringProp name="ResultCollector.filename"></stringProp>
    </ResultCollector>
    
    <Summariser guiclass="SummariserGui" testclass="Summariser" testname="UniERP Summary Report" enabled="true">
      <boolProp name="Summariser.save_config">false</boolProp>
      <boolProp name="Summariser.error_logging">false</boolProp>
      <stringProp name="Summariser.filename"></stringProp>
    </Summariser>
    
  </hashTree>
</jmeterTestPlan>
```

#### 4.1.3 JMeter Distributed Testing
```bash
# /opt/jmeter/scripts/start_distributed_test.sh
#!/bin/bash

# Configuration
JMETER_MASTER="jmeter-master.unierp.com"
JMETER_SLAVES=("jmeter-slave1.unierp.com" "jmeter-slave2.unierp.com" "jmeter-slave3.unierp.com")
TEST_PLAN="/opt/jmeter/test_plans/UniERP_Performance_Test.jmx"
RESULTS_DIR="/opt/jmeter/results/$(date +%Y%m%d_%H%M%S)"

# Create results directory
mkdir -p $RESULTS_DIR

# Start distributed test
echo "Starting UniERP distributed performance test..."
/opt/jmeter/bin/jmeter \
  -n \
  -t $TEST_PLAN \
  -R ${JMETER_SLAVES[@]} \
  -l $RESULTS_DIR/unierp_performance.jtl \
  -e \
  -o $RESULTS_DIR/unierp_performance_report \
  -JBASE_URL=https://test.unierp.com \
  -JUNIERP_LOGIN=test@unierp.com \
  -JUNIERP_PASSWORD=Test123!

echo "Test completed. Results saved to: $RESULTS_DIR"

# Generate summary report
python3 /opt/jmeter/scripts/generate_summary.py $RESULTS_DIR/unierp_performance.jtl $RESULTS_DIR/unierp_summary.html

# Send notification
echo "UniERP performance test completed. Results available at: $RESULTS_DIR" | mail -s "UniERP Performance Test Results" qa-team@unierp.com
```

---

## 5. Security Testing Tools

### 5.1 OWASP ZAP Configuration

#### 5.1.1 ZAP Installation
```bash
# Install ZAP
wget https://github.com/zaproxy/zaproxy/releases/download/v2.12.0/ZAP_2.12.0_Linux.tar.gz
tar -xzf ZAP_2.12.0_Linux.tar.gz
sudo mv ZAP_2.12.0 /opt/zap
sudo useradd -m zap

# Create ZAP directories
sudo mkdir -p /opt/zap/workspace /opt/zap/policies
sudo chown -R zap:zap /opt/zap
```

#### 5.1.2 ZAP Configuration
```xml
<!-- /opt/zap/config.xml -->
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<configuration>
    <scanner>
        <strength>HIGH</strength>
        <alertThreshold>LOW</alertThreshold>
        <hostPerScan>1</hostPerScan>
        <threadPerHost>5</threadPerHost>
        <delayInMs>0</delayInMs>
    </scanner>
    
    <spider>
        <maxDepth>10</maxDepth>
        <maxDuration>60</maxDuration>
        <maxParseSizeBytes>1048576</maxParseSizeBytes>
        <acceptCookies>true</acceptCookies>
        <handleODataParametersVisited>true</handleODataParametersVisited>
    </spider>
    
    <authentication>
        <loginUrl>https://test.unierp.com/web/login</loginUrl>
        <username>test@unierp.com</username>
        <password>Test123!</password>
        <usernameParameter>login</usernameParameter>
        <passwordParameter>password</passwordParameter>
    </authentication>
    
    <context>
        <name>UniERP Test Environment</name>
        <includeInContext>https://test\.unierp\.com.*</includeInContext>
        <excludeFromContext></excludeFromContext>
    </context>
    
    <unierp-branding>
        <checkLogo>true</checkLogo>
        <checkTitle>true</checkTitle>
        <checkContent>true</checkContent>
        <checkLinks>true</checkLinks>
        <checkColors>true</checkColors>
        <brandingScoreThreshold>90</brandingScoreThreshold>
    </unierp-branding>
</configuration>
```

#### 5.1.3 ZAP Automation Script
```python
# /opt/zap/scripts/unierp_security_scan.py
import time
import json
from zapv2 import ZAPv2

class UniERPSecurityScanner:
    def __init__(self, zap_proxy='http://127.0.0.1:8080', api_key='your-zap-api-key'):
        self.zap = ZAPv2(proxies={'http': zap_proxy}, apikey=api_key)
        self.target_url = 'https://test.unierp.com'
        
    def setup_authentication(self):
        """Setup authentication for UniERP"""
        context_id = self.zap.context.new_context('UniERP Test Environment')
        
        # Setup authentication
        auth_method = 'formBasedAuthentication'
        login_url = f'{self.target_url}/web/login'
        login_data = 'login=test@unierp.com&password=Test123!'
        
        self.zap.authentication.set_authentication_method(
            contextid=context_id,
            authmethodname=auth_method,
            authmethodconfigparams=f'loginUrl={login_url}&loginRequestData={login_data}'
        )
        
        print(f"Authentication setup completed for context: {context_id}")
        return context_id
    
    def spider_scan(self, context_id):
        """Run spider scan"""
        print("Starting spider scan...")
        scan_id = self.zap.spider.scan(self.target_url, contextid=context_id)
        
        while int(self.zap.spider.status(scan_id)) < 100:
            print(f"Spider progress: {self.zap.spider.status(scan_id)}%")
            time.sleep(5)
        
        print("Spider scan completed")
        return self.zap.spider.results(scan_id)
    
    def active_scan(self, context_id):
        """Run active scan"""
        print("Starting active scan...")
        scan_id = self.zap.ascan.scan(self.target_url, contextid=context_id)
        
        while int(self.zap.ascan.status(scan_id)) < 100:
            print(f"Active scan progress: {self.zap.ascan.status(scan_id)}%")
            time.sleep(10)
        
        print("Active scan completed")
        return self.zap.ascan.results(scan_id)
    
    def check_unierp_branding(self):
        """Check UniERP branding compliance"""
        print("Checking UniERP branding...")
        
        # Get page content
        response = self.zap.core.messages(baseurl=self.target_url)
        branding_issues = []
        
        for message in response:
            if 'response' in message:
                content = message['response']['body']
                
                # Check for UniERP branding elements
                if 'UniERP' not in content:
                    branding_issues.append("Missing UniERP text")
                
                if 'unierp.com' not in content:
                    branding_issues.append("Missing unierp.com references")
                
                if 'odoo.com' in content.lower():
                    branding_issues.append("Found odoo.com references")
        
        return branding_issues
    
    def generate_security_report(self, spider_results, active_results, branding_issues):
        """Generate comprehensive security report"""
        report = {
            'scan_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'target_url': self.target_url,
            'spider_results': spider_results,
            'active_scan_results': active_results,
            'branding_issues': branding_issues,
            'unierp_compliance': {
                'branding_score': max(0, 100 - len(branding_issues) * 10),
                'issues_found': len(branding_issues),
                'compliance_status': 'PASS' if len(branding_issues) == 0 else 'FAIL'
            }
        }
        
        # Save report
        report_file = f'/opt/zap/reports/unierp_security_report_{int(time.time())}.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Security report saved to: {report_file}")
        return report_file
    
    def run_full_scan(self):
        """Run complete security scan"""
        print("Starting UniERP security scan...")
        
        # Setup authentication
        context_id = self.setup_authentication()
        
        # Run spider scan
        spider_results = self.spider_scan(context_id)
        
        # Run active scan
        active_results = self.active_scan(context_id)
        
        # Check branding
        branding_issues = self.check_unierp_branding()
        
        # Generate report
        report_file = self.generate_security_report(spider_results, active_results, branding_issues)
        
        print("UniERP security scan completed!")
        return report_file

# Usage
if __name__ == "__main__":
    scanner = UniERPSecurityScanner()
    scanner.run_full_scan()
```

---

## 6. Reporting and Analytics

### 6.1 Allure Reporting

#### 6.1.1 Allure Installation
```bash
# Install Allure Commandline
wget https://github.com/allure-framework/allure2/releases/download/2.19.0/allure-2.19.0.tgz
tar -xzf allure-2.19.0.tgz
sudo mv allure-2.19.0 /opt/allure
sudo ln -s /opt/allure/bin/allure /usr/local/bin/allure

# Install Allure Pytest Plugin
pip install allure-pytest
```

#### 6.1.2 Allure Configuration
```yaml
# /opt/allure/config/allure.yml
allure:
  report:
    directory: reports/allure
    clean: true
    
  plugins:
    - name: custom-logo-plugin
      enabled: true
      config:
        logo-path: /opt/allure/config/unierp-logo.png
        company-name: UniERP
        company-url: https://www.unierp.com
    
    - name: branding-plugin
      enabled: true
      config:
        check-unierp-branding: true
        branding-threshold: 90
    
    - name: performance-plugin
      enabled: true
      config:
        response-time-threshold: 2000
        throughput-threshold: 100
```

#### 6.1.3 Custom Allure Plugin for UniERP Branding
```python
# /opt/allure/plugins/unierp_branding_plugin.py
import allure_commons
from allure_commons.utils import uuid4
from allure_commons.model2 import TestResult, TestStepResult
import re

class UniERPBrandingPlugin(allure_commons.plugin_manager.Plugin):
    def __init__(self):
        self.branding_checks = {
            'logo_present': False,
            'title_contains_unierp': False,
            'links_point_to_unierp': False,
            'no_odoo_references': True,
            'colors_match_brand': False
        }
    
    @allure_commons.hookimpl
    def report_result(self, result: TestResult):
        """Check UniERP branding in test results"""
        if result.status == 'passed':
            self._check_branding_compliance(result)
    
    def _check_branding_compliance(self, result):
        """Check UniERP branding compliance"""
        # Check test name for branding tests
        if 'branding' in result.name.lower():
            self._analyze_branding_test(result)
        
        # Check test attachments for branding evidence
        for attachment in result.attachments:
            if attachment.type == 'text/plain':
                content = attachment.source.read().decode('utf-8')
                self._analyze_content_for_branding(content)
    
    def _analyze_branding_test(self, result):
        """Analyze specific branding test results"""
        if 'logo' in result.name.lower():
            self.branding_checks['logo_present'] = result.status == 'passed'
        
        if 'title' in result.name.lower():
            self.branding_checks['title_contains_unierp'] = result.status == 'passed'
        
        if 'links' in result.name.lower():
            self.branding_checks['links_point_to_unierp'] = result.status == 'passed'
    
    def _analyze_content_for_branding(self, content):
        """Analyze content for UniERP branding"""
        # Check for UniERP references
        if 'UniERP' in content:
            self.branding_checks['logo_present'] = True
        
        # Check for odoo.com references (should not exist)
        if 'odoo.com' in content.lower():
            self.branding_checks['no_odoo_references'] = False
        
        # Check for unierp.com links
        if 'unierp.com' in content:
            self.branding_checks['links_point_to_unierp'] = True
    
    def get_branding_score(self):
        """Calculate overall branding score"""
        passed_checks = sum(self.branding_checks.values())
        total_checks = len(self.branding_checks)
        return (passed_checks / total_checks) * 100
    
    @allure_commons.hookimpl
    def report_container(self, container):
        """Add UniERP branding information to report"""
        if container.name == 'UniERP Test Suite':
            # Add branding score as custom data
            branding_data = {
                'unierp_branding_score': self.get_branding_score(),
                'branding_checks': self.branding_checks,
                'compliance_status': 'PASS' if self.get_branding_score() >= 90 else 'FAIL'
            }
            
            # Add custom data to container
            container.extra.append(branding_data)
```

### 6.2 Custom Report Generation

#### 6.2.1 Report Template
```html
<!-- /opt/allure/templates/unierp_report_template.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UniERP Test Report</title>
    <link rel="stylesheet" href="https://unierp.com/assets/test-report-styles.css">
    <script src="https://unierp.com/assets/test-report-charts.js"></script>
</head>
<body>
    <header class="unierp-header">
        <img src="https://unierp.com/assets/logo.png" alt="UniERP Logo" class="unierp-logo">
        <h1>UniERP Test Execution Report</h1>
        <div class="unierp-branding-score">
            <span class="score-label">Branding Score:</span>
            <span class="score-value" id="branding-score">{{ branding_score }}%</span>
        </div>
    </header>
    
    <main class="unierp-main">
        <section class="summary-section">
            <h2>Test Execution Summary</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <h3>Total Tests</h3>
                    <p class="metric-value">{{ total_tests }}</p>
                </div>
                <div class="metric-card">
                    <h3>Passed</h3>
                    <p class="metric-value passed">{{ passed_tests }}</p>
                </div>
                <div class="metric-card">
                    <h3>Failed</h3>
                    <p class="metric-value failed">{{ failed_tests }}</p>
                </div>
                <div class="metric-card">
                    <h3>Pass Rate</h3>
                    <p class="metric-value">{{ pass_rate }}%</p>
                </div>
            </div>
        </section>
        
        <section class="branding-section">
            <h2>UniERP Branding Verification</h2>
            <div class="branding-checks">
                {% for check in branding_checks %}
                <div class="check-item {{ 'passed' if check.passed else 'failed' }}">
                    <span class="check-name">{{ check.name }}</span>
                    <span class="check-status">{{ '✓' if check.passed else '✗' }}</span>
                </div>
                {% endfor %}
            </div>
        </section>
        
        <section class="charts-section">
            <h2>Test Analytics</h2>
            <div class="charts-container">
                <div class="chart-item">
                    <canvas id="execution-trend-chart"></canvas>
                    <h3>Test Execution Trend</h3>
                </div>
                <div class="chart-item">
                    <canvas id="module-coverage-chart"></canvas>
                    <h3>Module Test Coverage</h3>
                </div>
                <div class="chart-item">
                    <canvas id="branding-trend-chart"></canvas>
                    <h3>Branding Score Trend</h3>
                </div>
            </div>
        </section>
        
        <section class="details-section">
            <h2>Test Results Details</h2>
            <table class="results-table">
                <thead>
                    <tr>
                        <th>Test Suite</th>
                        <th>Test Case</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Branding Score</th>
                        <th>Issues</th>
                    </tr>
                </thead>
                <tbody>
                    {% for test in test_results %}
                    <tr class="test-row {{ test.status }}">
                        <td>{{ test.suite }}</td>
                        <td>{{ test.name }}</td>
                        <td class="status-{{ test.status }}">{{ test.status.upper() }}</td>
                        <td>{{ test.duration }}s</td>
                        <td>{{ test.branding_score }}%</td>
                        <td>{{ test.issues | length }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </section>
    </main>
    
    <footer class="unierp-footer">
        <p>Generated by UniERP Test Automation Framework</p>
        <p>© 2024 UniERP Solutions. All rights reserved.</p>
        <p>Contact: <a href="mailto:qa@unierp.com">qa@unierp.com</a></p>
    </footer>
    
    <script>
        // Initialize charts with UniERP branding
        initializeCharts({
            brandingColors: ['#007bff', '#28a745', '#ffc107', '#dc3545'],
            unierpLogo: 'https://unierp.com/assets/logo.png',
            companyName: 'UniERP'
        });
    </script>
</body>
</html>
```

---

## 7. Integration and Automation

### 7.1 CI/CD Integration

#### 7.1.1 GitLab CI Pipeline
```yaml
# .gitlab-ci.yml (Extended with testing tools)
stages:
  - setup
  - test
  - security
  - performance
  - report
  - notify

variables:
  TESTRAIL_URL: "https://testrail.unierp.com"
  GRAFANA_URL: "https://grafana.unierp.com"
  ZAP_PROXY: "http://zap.unierp.com:8080"

setup_test_environment:
  stage: setup
  script:
    - ./scripts/setup_test_environment.sh
    - ./scripts/generate_test_data.sh
  artifacts:
    paths:
      - test_data/
  only:
    - merge_requests
    - main

run_tests:
  stage: test
  script:
    - pytest tests/ --alluredir=reports/allure --testrail-url=$TESTRAIL_URL
  artifacts:
    reports:
      junit: reports/junit.xml
    paths:
      - reports/allure/
  dependencies:
    - setup_test_environment
  coverage: '/TOTAL.*\s+(\d+%)$/'
  only:
    - merge_requests
    - main

security_scan:
  stage: security
  script:
    - python /opt/zap/scripts/unierp_security_scan.py --target=$CI_ENVIRONMENT_URL --proxy=$ZAP_PROXY
    - python scripts/analyze_security_results.py
  artifacts:
    reports:
      junit: reports/security-junit.xml
    paths:
      - reports/security/
  dependencies:
    - setup_test_environment
  only:
    - schedules
    - main

performance_test:
  stage: performance
  script:
    - /opt/jmeter/scripts/start_distributed_test.sh --environment=$CI_ENVIRONMENT_URL
    - python scripts/analyze_performance_results.py
  artifacts:
    reports:
      junit: reports/performance-junit.xml
    paths:
      - reports/performance/
  dependencies:
    - setup_test_environment
  only:
    - schedules
    - main

generate_reports:
  stage: report
  script:
    - allure generate reports/allure -o reports/allure-report
    - python scripts/generate_unierp_report.py --template=unierp_report_template.html
    - python scripts/upload_metrics_to_grafana.py --grafana-url=$GRAFANA_URL
  artifacts:
    paths:
      - reports/allure-report/
      - reports/unierp_report.html
  dependencies:
    - run_tests
    - security_scan
    - performance_test
  only:
    - merge_requests
    - main

notify_results:
  stage: notify
  script:
    - ./scripts/send_email_notification.sh
    - ./scripts/post_to_slack.sh
    - ./scripts/update_testrail_milestones.sh
  dependencies:
    - generate_reports
  only:
    - main
```

#### 7.1.2 Metrics Collection Script
```python
# scripts/upload_metrics_to_grafana.py
import requests
import json
import time
from datetime import datetime

class GrafanaMetricsUploader:
    def __init__(self, grafana_url, api_key):
        self.grafana_url = grafana_url
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def upload_test_metrics(self, test_results):
        """Upload test execution metrics to Grafana"""
        metrics = {
            "job": "unierp-testing",
            "instance": "test-runner",
            "metrics": [
                {
                    "name": "unierp_test_total",
                    "type": "counter",
                    "value": test_results.get('total', 0),
                    "timestamp": int(time.time())
                },
                {
                    "name": "unierp_test_passed",
                    "type": "counter", 
                    "value": test_results.get('passed', 0),
                    "timestamp": int(time.time())
                },
                {
                    "name": "unierp_test_failed",
                    "type": "counter",
                    "value": test_results.get('failed', 0),
                    "timestamp": int(time.time())
                },
                {
                    "name": "unierp_branding_score",
                    "type": "gauge",
                    "value": test_results.get('branding_score', 0),
                    "timestamp": int(time.time())
                }
            ]
        }
        
        response = requests.post(
            f"{self.grafana_url}/api/metrics",
            headers=self.headers,
            json=metrics
        )
        
        if response.status_code == 204:
            print("Metrics uploaded successfully to Grafana")
        else:
            print(f"Failed to upload metrics: {response.text}")
    
    def upload_performance_metrics(self, performance_results):
        """Upload performance metrics to Grafana"""
        metrics = {
            "job": "unierp-performance",
            "instance": "performance-test",
            "metrics": [
                {
                    "name": "unierp_performance_response_time",
                    "type": "histogram",
                    "value": performance_results.get('avg_response_time', 0),
                    "timestamp": int(time.time())
                },
                {
                    "name": "unierp_performance_throughput",
                    "type": "gauge",
                    "value": performance_results.get('throughput', 0),
                    "timestamp": int(time.time())
                },
                {
                    "name": "unierp_performance_error_rate",
                    "type": "gauge",
                    "value": performance_results.get('error_rate', 0),
                    "timestamp": int(time.time())
                }
            ]
        }
        
        response = requests.post(
            f"{self.grafana_url}/api/metrics",
            headers=self.headers,
            json=metrics
        )
        
        if response.status_code == 204:
            print("Performance metrics uploaded successfully to Grafana")
        else:
            print(f"Failed to upload performance metrics: {response.text}")
    
    def upload_security_metrics(self, security_results):
        """Upload security metrics to Grafana"""
        vulnerability_counts = security_results.get('vulnerability_counts', {})
        
        metrics = {
            "job": "unierp-security",
            "instance": "security-scan",
            "metrics": [
                {
                    "name": "unierp_security_vulnerabilities_critical",
                    "type": "gauge",
                    "value": vulnerability_counts.get('critical', 0),
                    "timestamp": int(time.time())
                },
                {
                    "name": "unierp_security_vulnerabilities_high",
                    "type": "gauge",
                    "value": vulnerability_counts.get('high', 0),
                    "timestamp": int(time.time())
                },
                {
                    "name": "unierp_security_vulnerabilities_medium",
                    "type": "gauge",
                    "value": vulnerability_counts.get('medium', 0),
                    "timestamp": int(time.time())
                },
                {
                    "name": "unierp_security_vulnerabilities_low",
                    "type": "gauge",
                    "value": vulnerability_counts.get('low', 0),
                    "timestamp": int(time.time())
                }
            ]
        }
        
        response = requests.post(
            f"{self.grafana_url}/api/metrics",
            headers=self.headers,
            json=metrics
        )
        
        if response.status_code == 204:
            print("Security metrics uploaded successfully to Grafana")
        else:
            print(f"Failed to upload security metrics: {response.text}")

# Usage
if __name__ == "__main__":
    uploader = GrafanaMetricsUploader(
        grafana_url="https://grafana.unierp.com",
        api_key="your-grafana-api-key"
    )
    
    # Load test results
    with open('reports/test_results.json', 'r') as f:
        test_results = json.load(f)
    
    with open('reports/performance_results.json', 'r') as f:
        performance_results = json.load(f)
    
    with open('reports/security_results.json', 'r') as f:
        security_results = json.load(f)
    
    # Upload metrics
    uploader.upload_test_metrics(test_results)
    uploader.upload_performance_metrics(performance_results)
    uploader.upload_security_metrics(security_results)
```

---

## 8. Conclusion

The UniERP Testing Tools & Dashboards Configuration provides a comprehensive infrastructure for effective testing operations. With integrated test management, monitoring, reporting, and automation tools, it ensures thorough validation of UniERP system quality and branding consistency.

Key components include:
- **Test Management:** TestRail integration for comprehensive test case management
- **Monitoring:** Grafana dashboards for real-time test metrics and UniERP branding scores
- **Security Testing:** OWASP ZAP integration for automated security scanning
- **Performance Testing:** JMeter distributed testing for load and stress testing
- **Reporting:** Allure and custom reporting with UniERP branding
- **CI/CD Integration:** GitLab CI pipeline for automated testing workflows

Regular maintenance and updates to these tools and configurations will ensure their continued effectiveness in supporting UniERP testing activities and maintaining high quality standards.

For questions or support regarding testing tools and dashboards, please contact UniERP QA Tools Team at qa-tools@unierp.com.

---

**Document Status:** Approved
**Next Review Date:** December 2024
**Document Owner:** UniERP QA Tools Team
**Contact Information:** qa-tools@unierp.com | +1-555-UNIERP-TOOLS