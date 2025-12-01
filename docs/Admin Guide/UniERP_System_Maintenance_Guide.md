# UniERP System Maintenance Guide

## Table of Contents

1. [Regular Maintenance Tasks](#regular-maintenance-tasks)
2. [Performance Monitoring](#performance-monitoring)
3. [System Updates](#system-updates)
4. [Log Management](#log-management)
5. [Database Maintenance](#database-maintenance)
6. [Security Maintenance](#security-maintenance)
7. [Backup Management](#backup-management)
8. [Troubleshooting](#maintenance-troubleshooting)

---

## Regular Maintenance Tasks

### Daily Maintenance

#### System Health Checks
1. **Service Status Monitoring**
   ```bash
   #!/bin/bash
   
   # Check all critical services
   for service in unierp postgresql nginx redis; do
       echo "Checking $service service..."
       systemctl is-active --quiet $service
       if [ $? -ne 0 ]; then
           echo "$service is not running"
           # Attempt to restart service
           sudo systemctl restart $service
           sleep 5
           systemctl is-active --quiet $service
           if [ $? -eq 0 ]; then
               echo "$service restarted successfully"
           else
               echo "$service restart failed"
           fi
       else
           echo "$service is running normally"
       fi
   done
   ```

2. **Disk Space Monitoring**
   ```bash
   #!/bin/bash
   
   # Check disk usage
   DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//g')
   
   # Alert if disk usage > 80%
   if [ $DISK_USAGE -gt 80 ]; then
       echo "High disk usage: $DISK_USAGE%"
       # Send alert
       echo "High disk usage on $(hostname)" | mail -s "Disk Alert" admin@uslbd.com
   else
       echo "Disk usage: $DISK_USAGE%"
   fi
   ```

3. **Memory Usage Monitoring**
   ```bash
   #!/bin/bash
   
   # Check memory usage
   MEMORY_USAGE=$(free | awk 'NR==2{printf "%.1f", $3/1024*100}')
   
   # Alert if memory usage > 80%
   if [ $(echo "$MEMORY_USAGE > 80" | bc -l) -eq 1 ]; then
       echo "High memory usage: $MEMORY_USAGE%"
       # Send alert
       echo "High memory usage on $(hostname)" | mail -s "Memory Alert" admin@uslbd.com
   else
       echo "Memory usage: $MEMORY_USAGE%"
   fi
   ```

#### Database Performance Monitoring
1. **Connection Monitoring**
   ```sql
   -- Monitor active connections
   SELECT count(*) FROM pg_stat_activity;
   ```

2. **Slow Query Analysis**
   ```sql
   -- Enable slow query logging
   ALTER SYSTEM SET log_min_duration_statement = 1000;
   ALTER SYSTEM SET log_statement = 'all';
   
   -- Analyze slow queries
   SELECT query, mean_time, calls, total_time
   FROM pg_stat_statements
   WHERE mean_time > 1000
   ORDER BY mean_time DESC
   LIMIT 10;
   ```

### Weekly Maintenance

#### System Updates
1. **Package Updates**
   ```bash
   #!/bin/bash
   
   # Update system packages
   sudo apt-get update
   sudo apt-get upgrade -y
   
   # Update UniERP modules
   cd /opt/unierp
   git pull origin main
   pip3 install -r requirements.txt
   ```

2. **Security Updates**
   ```bash
   #!/bin/bash
   
   # Check for security updates
   sudo apt-get update -y
   
   # Install security patches
   sudo apt-get install -y unattended-upgrades
   
   # Update SSL certificates
   certbot renew --quiet
   ```

#### Log Rotation
1. **Configure Log Rotation**
   ```bash
   #!/bin/bash
   
   # Create logrotate configuration
   sudo nano /etc/logrotate.d/unierp
   ```
   
   ```ini
   /var/log/unierp/*.log {
       daily
       missingok
       rotate 30
       compress
       delaycompress
       notifempty
       create 644 unierp unierp
       postrotate
           systemctl reload unierp
   }
   ```

2. **Test Log Rotation**
   ```bash
   # Test logrotate configuration
   logrotate -f /etc/logrotate.d/unierp
   ```

#### Database Maintenance
1. **Database Vacuum**
   ```sql
   -- Perform vacuum on all tables
   VACUUM ANALYZE;
   VACUUM VERBOSE;
   ```

2. **Index Maintenance**
   ```sql
   -- Rebuild indexes
   REINDEX DATABASE unierp_production;
   
   -- Update table statistics
   ANALYZE unierp_production;
   ```

3. **Database Statistics**
   ```sql
   -- Update table statistics
   ANALYZE unierp_production;
   ```

---

## Performance Monitoring

### System Metrics Collection

#### Resource Monitoring Script
1. **Comprehensive Monitoring**
   ```bash
   #!/bin/bash
   
   # System metrics
   echo "=== System Metrics ===="
   echo "Timestamp: $(date)"
   echo "Hostname: $(hostname)"
   echo "Uptime: $(uptime -p)"
   echo "Load Average: $(uptime | awk '{print $10}')"
   
   # CPU metrics
   echo "CPU Usage:"
   top -b -n 1 | head -20 | awk '{printf "  CPU: %.1f%%", $2}'
   
   # Memory metrics
   echo "Memory Usage:"
   free -h | awk '/^Mem:/ {printf "  Total: %sMB, Used: %sMB, Free: %sMB", $2, $3, $4}'
   
   # Disk metrics
   echo "Disk Usage:"
   df -h | awk '/^\/dev\// {printf "  %s: %s (%s)", $1, $3, $5}'
   
   # Network metrics
   echo "Network Connections:"
   netstat -tuln | grep ESTABLISHED | wc -l
   
   # Save metrics to log
   echo "=== End System Metrics ====" >> /var/log/unierp/system_metrics.log
   ```

2. **Performance Dashboard Setup**
   ```bash
   #!/bin/bash
   
   # Install monitoring tools
   sudo apt-get install htop iotop nethogs
   
   # Configure Grafana for visualization
   # Set up Prometheus for metrics collection
   # Configure alerts and notifications
   ```

#### Application Performance Monitoring
1. **UniERP Application Metrics**
   ```bash
   #!/bin/bash
   
   # Monitor UniERP processes
   ps aux | grep unierp | grep -v grep
   
   # Check response times
   curl -o /dev/null -w "Time: %{time_total}s" -s "Status: %{http_code}" \
       http://localhost:8069/api/web/session/authenticate
   
   # Monitor database queries
   sudo -u postgres psql -d unierp_production -c "
   SELECT query, mean_time, calls
   FROM pg_stat_statements
   WHERE mean_time > 1000
   ORDER BY mean_time DESC
   LIMIT 5;
   "
   ```

2. **Alert Configuration**
   ```ini
   [monitoring]
   cpu_threshold = 80
   memory_threshold = 80
   disk_threshold = 85
   response_time_threshold = 5000
   alert_email = admin@uslbd.com
   alert_sms = True
   ```

---

## System Updates

### Automated Update Management

#### Update Automation
1. **Configure Automatic Updates**
   ```bash
   #!/bin/bash
   
   # Configure unattended upgrades
   sudo dpkg-reconfigure -plow unattended-upgrades
   echo 'unattended-upgrades unattended-upgrades/origin true' \
       > /etc/apt/apt.conf.d/50unattended-upgrades
   
   # Configure security updates
   echo 'Unattended-Upgrade::Automatic-Reboot "false"' \
       > /etc/apt/apt.conf.d/50unattended-upgrades
   
   # Set up automatic security updates
   sudo apt-get install unattended-upgrades
   ```

2. **Update Scheduling**
   ```bash
   #!/bin/bash
   
   # Schedule regular updates
   echo "0 2 * * * /usr/bin/apt-get update" | sudo crontab -
   
   # Schedule security updates
   echo "0 3 * * * /usr/bin/apt-get upgrade -y" | sudo crontab -
   ```

#### Update Testing
1. **Staging Environment Setup**
   ```bash
   #!/bin/bash
   
   # Create staging environment
   cp -r /opt/unierp /opt/unierp_staging
   cd /opt/unierp_staging
   
   # Update staging configuration
   sed -i 's/localhost/staging/g' /etc/unierp/unierp.conf
   
   # Test updates in staging
   git pull origin staging
   sudo apt-get update
   sudo apt-get upgrade -y
   ```

2. **Update Validation**
   ```bash
   #!/bin/bash
   
   # Test UniERP functionality
   cd /opt/unierp_staging
   sudo -u postgres psql -d unierp_staging -c "
   SELECT count(*) FROM res_users;
   "
   
   # Validate all modules
   python3 -c "
   import odoo
   from odoo.tools import config
   config = config.load(['-c', '/opt/unierp_staging/etc/unierp.conf'])
   env = odoo.api.Environment(config)
   
   for module in ['sale', 'purchase', 'stock']:
       try:
           env['ir.module'].search([('state', '=', 'installed')])
           print(f'{module} module validated')
       except Exception as e:
           print(f'Error validating {module}: {e}')
   "
   ```

---

## Log Management

### Log Analysis and Monitoring

#### Log Monitoring Script
1. **Comprehensive Log Analysis**
   ```bash
   #!/bin/bash
   
   # Analyze error logs
   echo "=== Error Log Analysis ===="
   grep "ERROR" /var/log/unierp/unierp-server.log | \
       awk '{print $1, $2, $3, $4, $5}' | \
       tail -20 /var/log/unierp/unierp-server.log | \
       grep "ERROR" | wc -l
   
   # Analyze access logs
   echo "=== Access Log Analysis ===="
   grep "LOGIN" /var/log/unierp/access.log | \
       awk '{print $1, $2, $3, $4, $5}' | \
       tail -20 /var/log/unierp/access.log | \
       grep "LOGIN" | wc -l
   
   # Generate summary report
   echo "=== Log Summary ===="
   echo "Generated on: $(date)"
   echo "Error count: $(grep -c ERROR /var/log/unierp/unierp-server.log)"
   echo "Access count: $(grep -c LOGIN /var/log/unierp/access.log)"
   ```

2. **Log Alerting**
   ```bash
   #!/bin/bash
   
   # Check for critical errors
   CRITICAL_ERRORS=$(grep -c "CRITICAL\|FATAL" /var/log/unierp/unierp-server.log)
   
   if [ $CRITICAL_ERRORS -gt 0 ]; then
       echo "Critical errors detected: $CRITICAL_ERRORS"
       # Send alert
       echo "Critical errors in UniERP" | mail -s "Critical Alert" admin@uslbd.com
   fi
   ```

#### Log Archival
1. **Archive Old Logs**
   ```bash
   #!/bin/bash
   
   # Archive logs older than 30 days
   find /var/log/unierp -name "*.log" -mtime +30 -exec gzip {} \;
   
   # Move archives to backup location
   mv /var/log/unierp/*.log.gz /backup/unierp/logs/
   ```

2. **Log Cleanup**
   ```bash
   #!/bin/bash
   
   # Clean up old log files
   find /var/log/unierp -name "*.log" -mtime +7 -delete
   ```

---

## Database Maintenance

### Database Health Checks

#### Database Monitoring Script
1. **Database Health Monitor**
   ```bash
   #!/bin/bash
   
   # Check database connectivity
   pg_isready -h localhost -p 5432 -U unierp_user
   
   if [ $? -eq 0 ]; then
       echo "Database is ready"
   else
       echo "Database is not ready"
       exit 1
   fi
   
   # Check database size
   sudo -u postgres psql -d unierp_production -c "
   SELECT pg_size_pretty(pg_database_size(current_database()))
   "
   ```

2. **Database Performance Analysis**
   ```sql
   -- Check table sizes
   SELECT 
       schemaname,
       tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
   FROM pg_tables
   ORDER BY pg_total_relation_size DESC
   LIMIT 10;
   ```

#### Database Maintenance Tasks
1. **Regular Maintenance Script**
   ```bash
   #!/bin/bash
   
   echo "Starting database maintenance..."
   
   # Vacuum database
   sudo -u postgres psql -d unierp_production -c "VACUUM ANALYZE VERBOSE;"
   
   # Update statistics
   sudo -u postgres psql -d unierp_production -c "ANALYZE unierp_production;"
   
   # Rebuild indexes
   sudo -u postgres psql -d unierp_production -c "REINDEX DATABASE unierp_production;"
   
   echo "Database maintenance completed"
   ```

---

## Security Maintenance

### Security Audit Procedures

#### Security Monitoring
1. **Security Audit Script**
   ```bash
   #!/bin/bash
   
   echo "=== Security Audit ===="
   
   # Check failed login attempts
   FAILED_LOGINS=$(grep "Failed login" /var/log/auth.log | wc -l)
   echo "Failed login attempts: $FAILED_LOGINS"
   
   # Check for unusual access patterns
   grep "suspicious" /var/log/unierp/access.log | tail -10
   
   # Check file integrity
   find /opt/unierp -name "*.py" -exec md5sum {} \; \
       find /opt/unierp -name "*.py" -exec md5sum {} \; \
       paste - - < /opt/unierp/checksums.md
   diff /opt/unierp/checksums.md
   ```

2. **Vulnerability Scanning**
   ```bash
   #!/bin/bash
   
   # Install security scanner
   sudo apt-get install lynis
   
   # Scan for vulnerabilities
   lynis audit /opt/unierp
   
   # Generate report
   lynis report /opt/unierp > /tmp/security_scan.txt
   ```

#### Security Patch Management
1. **Patch Management Script**
   ```bash
   #!/bin/bash
   
   # Check for available updates
   sudo apt-get update --dry-run
   
   # Install security patches
   sudo apt-get install -y $(apt-get -s upgrade | grep -i 'Inst.*security')
   
   # Reboot if required
   if [ $? -ne 0 ]; then
       echo "System reboot required for security patches"
       sudo reboot
   fi
   ```

---

## Backup Management

### Backup Automation

#### Backup Verification Script
1. **Backup Verification**
   ```bash
   #!/bin/bash
   
   echo "Verifying backup integrity..."
   
   # Check latest backup
   LATEST_BACKUP=$(ls -t /backup/unierp/database/ | head -1)
   
   # Verify backup exists
   if [ -f "/backup/unierp/database/$LATEST_BACKUP/database.sql" ]; then
       echo "Latest backup verified: $LATEST_BACKUP"
   else
       echo "Latest backup not found"
       exit 1
   fi
   ```

#### Backup Restoration Test
1. **Restore Test Script**
   ```bash
   #!/bin/bash
   
   echo "Testing backup restoration..."
   
   # Create test database
   createdb unierp_test_restore
   
   # Restore from backup
   sudo -u postgres psql -d unierp_test_restore \
       -c "restore_command='pg_restore -l /backup/unierp/database/latest/database.sql'"
   
   # Verify restore
   sudo -u postgres psql -d unierp_test_restore -c "SELECT count(*) FROM res_users;"
   
   echo "Backup restoration test completed"
   ```

---

## Troubleshooting

### Common Maintenance Issues

#### Performance Issues
1. **Slow Performance Diagnosis**
   ```bash
   #!/bin/bash
   
   echo "=== Performance Diagnosis ===="
   
   # Check system load
   echo "System Load:"
   uptime
   top -b -n 1 | head -5
   
   # Check memory usage
   echo "Memory Usage:"
   free -h
   vmstat 1 5
   
   # Check disk I/O
   echo "Disk I/O:"
   iostat -x 1 5
   
   # Check database performance
   echo "Database Performance:"
   sudo -u postgres psql -d unierp_production -c "
   SELECT 
           (SELECT count(*) FROM pg_stat_activity) as active_connections,
           (SELECT mean_time FROM pg_stat_statements WHERE mean_time > 1000) as avg_slow_query
       ;
   "
   ```

2. **Resource Optimization**
   ```bash
   #!/bin/bash
   
   # Optimize database connections
   sudo -u postgres psql -d unierp_production -c "
   ALTER SYSTEM SET max_connections = 100;
   "
   
   # Optimize memory usage
   echo "Optimizing memory settings..."
   sudo sysctl -w vm.swappiness=10
   
   # Optimize disk I/O
   echo "Optimizing disk I/O..."
   echo 'deadline' > /proc/sys/vm/dirty_ratio
   ```

#### Service Issues
1. **Service Recovery Script**
   ```bash
   #!/bin/bash
   
   for service in unierp postgresql nginx redis; do
       if ! systemctl is-active --quiet $service; then
           echo "Restarting $service..."
           sudo systemctl restart $service
           sleep 5
           systemctl is-active --quiet $service
           if [ $? -eq 0 ]; then
               echo "$service restarted successfully"
           else
               echo "$service restart failed"
           fi
       fi
   done
   ```

---

## Maintenance Scheduling

#### Maintenance Calendar
1. **Create Maintenance Schedule**
   ```bash
   #!/bin/bash
   
   # Define maintenance windows
   MAINTENANCE_WINDOWS=(
       "Sunday 02:00-04:00: Database Maintenance"
       "Wednesday 22:00-23:00: System Updates"
       "First Saturday of month 09:00-11:00: Security Updates"
   )
   
   # Schedule maintenance tasks
   for window in "${MAINTENANCE_WINDOWS[@]}"; do
       echo "Scheduling: $window"
       # Add to crontab
       (crontab -l 2>/dev/null; echo "$window" | crontab -) || true
   done
   ```

#### Maintenance Notifications
1. **Notification Configuration**
   ```bash
   #!/bin/bash
   
   # Send maintenance notifications
   send_maintenance_notification() {
       local message=$1
       local subject=$2
       
       case $1 in
           "database")
               message="Database maintenance scheduled"
               subject="UniERP Database Maintenance"
               ;;
           "system")
               message="System maintenance scheduled"
               subject="UniERP System Maintenance"
               ;;
           "security")
               message="Security updates scheduled"
               subject="UniERP Security Updates"
               ;;
       esac
       
       echo "$message" | mail -s "$subject" admin@uslbd.com
   }
   
   # Schedule notification for upcoming maintenance
   echo "Scheduling maintenance notifications..."
   ```

---

## Conclusion

This comprehensive system maintenance guide provides:

### Maintenance Framework
- **Regular Tasks**: Daily, weekly, and monthly maintenance procedures
- **Performance Monitoring**: System and application performance tracking
- **System Updates**: Automated update management and testing
- **Log Management**: Log analysis, archiving, and alerting
- **Database Maintenance**: Health checks, optimization, and regular maintenance
- **Security Maintenance**: Auditing, patching, and vulnerability management
- **Backup Management**: Verification, testing, and restoration procedures
- **Troubleshooting**: Common issues and resolution procedures

### Best Practices

1. **Proactive Maintenance**: Prevent issues through regular maintenance
2. **Documentation**: Maintain detailed maintenance logs and procedures
3. **Testing**: Test all changes in staging environments
4. **Monitoring**: Continuous system health and performance monitoring
5. **Automation**: Automate repetitive maintenance tasks
6. **Communication**: Notify stakeholders of maintenance activities
7. **Safety**: Follow safe maintenance procedures and change management

### Support Resources

#### Maintenance Documentation
- **System Guide**: https://docs.uslbd.com/system-maintenance
- **Performance Guide**: https://docs.uslbd.com/performance
- **Security Guide**: https://docs.uslbd.com/security-maintenance
- **Backup Guide**: https://docs.uslbd.com/backup-recovery

#### Support Channels
- **Technical Support**: admin-support@uslbd.com
- **Emergency Support**: +1-555-UNIERP-911
- **Community Forum**: https://community.uslbd.com/system-admin

Remember that regular system maintenance is essential for optimal UniERP performance, security, and reliability.