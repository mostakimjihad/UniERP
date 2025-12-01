# UniERP Backup & Recovery Guide

## Table of Contents

1. [Backup Strategy](#backup-strategy)
2. [Database Backup Procedures](#database-backup-procedures)
3. [File System Backup](#file-system-backup)
4. [Application Backup](#application-backup)
5. [Disaster Recovery](#disaster-recovery)
6. [High Availability](#high-availability)
7. [Backup Verification](#backup-verification)
8. [Recovery Testing](#recovery-testing)

---

## Backup Strategy

### Backup Policy Overview

#### Backup Objectives
- **Data Protection**: Ensure data integrity and availability
- **Business Continuity**: Minimize downtime and data loss
- **Compliance**: Meet regulatory and business requirements
- **Recovery Capability**: Enable quick system restoration

#### Backup Classification

#### Full Backups
- **Frequency**: Weekly
- **Scope**: Complete system backup
- **Retention**: 4 weeks (daily backups retained for 4 weeks)
- **Storage**: Off-site and on-site storage

#### Incremental Backups
- **Frequency**: Daily
- **Scope**: Changes since last full backup
- **Retention**: 30 days
- **Storage**: Primary backup storage

#### Transaction Log Backups
- **Frequency**: Every 15 minutes
- **Scope**: Database transaction logs
- **Retention**: 7 days
- **Storage**: High-performance storage

---

## Database Backup Procedures

### Automated Database Backup

#### PostgreSQL Backup Script
1. **Create Backup Script**:
   ```bash
   #!/bin/bash
   
   # Configuration
   BACKUP_DIR="/backup/unierp/database"
   DB_NAME="unierp_production"
   DB_USER="unierp_user"
   RETENTION_DAYS=30
   S3_BUCKET="s3://unierp-backups"
   
   # Create backup directory
   mkdir -p $BACKUP_DIR/$(date +%Y%m%d_%H%M%S)
   
   # Database backup
   pg_dump -h localhost -U $DB_USER -d $DB_NAME \
       -f $BACKUP_DIR/$(date +%Y%m%d_%H%M%S)/database.sql \
       --verbose --no-password --clean
   
   # Compress backup
   gzip $BACKUP_DIR/$(date +%Y%m%d_%H%M%S)/database.sql
   
   # Upload to S3 (if configured)
   if [ ! -z "$S3_BUCKET" ]; then
       aws s3 cp $BACKUP_DIR/$(date +%Y%m%d_%H%M%S)/database.sql.gz \
           $S3_BUCKET/database/$(date +%Y%m%d)/database.sql.gz
   fi
   
   # Clean old backups
   find $BACKUP_DIR -type f -mtime +$RETENTION_DAYS -exec rm -f {} \;
   ```

2. **Schedule Automated Backups**:
   ```bash
   # Add to crontab
   crontab -e
   0 2 * * /opt/unierp/scripts/backup_database.sh >> /var/log/backup.log 2>&1
   ```

#### Backup Verification
1. **Backup Integrity Check**:
   ```bash
   #!/bin/bash
   
   BACKUP_FILE=$1
   EXPECTED_CHECKSUM=$2
   
   # Calculate checksum of current backup
   CURRENT_CHECKSUM=$(sha256sum $BACKUP_FILE | awk '{print $1}')
   
   # Compare with expected checksum
   if [ "$CURRENT_CHECKSUM" = "$EXPECTED_CHECKSUM" ]; then
       echo "Backup integrity verified"
   else
       echo "Backup integrity check failed"
       exit 1
   fi
   ```

### Point-in-Time Recovery (PITR)

#### PITR Configuration
1. **Enable PITR**:
   ```sql
   -- Enable PITR in PostgreSQL
   ALTER SYSTEM SET wal_level = minimal;
   ALTER SYSTEM SET archive_mode = on;
   ALTER SYSTEM SET archive_command = 'cp %p /backup/pitr_archive/%f';
   ```

2. **PITR Recovery Script**:
   ```bash
   #!/bin/bash
   
   # Configuration
   RECOVERY_TIME="2024-01-15 10:30:00"
   RECOVERY_DIR="/recovery/unierp"
   
   # Create recovery point
   pg_createunierp_recoverypoint $RECOVERY_TIME
   
   # Restore database
   pg_ctl start -D /var/lib/postgresql/data \
       -c "restore_command='pg_restore -l $RECOVERY_DIR/unierp_backup'"
   ```

---

## File System Backup

### System Backup Script
1. **Complete System Backup**:
   ```bash
   #!/bin/bash
   
   # Configuration
   BACKUP_DIR="/backup/unierp/system"
   UNIERP_DIR="/opt/unierp"
   CONFIG_DIR="/etc/unierp"
   RETENTION_DAYS=30
   
   # Create backup directory
   mkdir -p $BACKUP_DIR/$(date +%Y%m%d_%H%M%S)
   
   # Backup configuration files
   cp -r $CONFIG_DIR $BACKUP_DIR/$(date +%Y%m%d_%H%M%S)/config/
   
   # Backup UniERP application
   tar -czf $BACKUP_DIR/$(date +%Y%m%d_%H%M%S)/unierp_system.tar.gz \
       -C $UNIERP_DIR --exclude='*.log'
   
   # Backup custom modules
   tar -czf $BACKUP_DIR/$(date +%Y%m%d_%H%M%S)/custom_modules.tar.gz \
       -C $UNIERP_DIR/addons --exclude='*.pyc'
   
   # Clean old backups
   find $BACKUP_DIR -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \;
   ```

2. **Incremental File Backup**:
   ```bash
   #!/bin/bash
   
   # Configuration
   SOURCE_DIR="/opt/unierp"
   BACKUP_DIR="/backup/unierp/incremental"
   REFERENCE_DIR="/backup/unierp/last_full"
   
   # Create incremental backup
   rsync -av --compare-dest=$REFERENCE_DIR $SOURCE_DIR $BACKUP_DIR/$(date +%Y%m%d)
   
   # Update reference
   cp -al $BACKUP_DIR/$(date +%Y%m%d) $REFERENCE_DIR
   ```

---

## Application Backup

### Configuration Backup
1. **Export UniERP Configuration**:
   ```bash
   #!/bin/bash
   
   # Export database configuration
   sudo -u postgres psql -d unierp_production -c "
   \copy (SELECT 'db_host', 'db_port', 'db_user', 'db_password', 'db_maxconn') 
   TO '/tmp/unierp_config.csv' WITH CSV HEADER;
   "
   
   # Export system configuration
   sudo -u unierp python3 -c "
   import odoo.tools.config
   config = odoo.tools.config.load(['-c', '/etc/unierp/unierp.conf'])
   
   with open('/tmp/unierp_system_config.json', 'w') as f:
       json.dump({
           'xmlrpc_port': config.get('xmlrpc_port'),
           'db_maxconn': config.get('db_maxconn'),
           'workers': config.get('workers')
       }, f, indent=2)
   "
   ```

2. **Module Data Backup**:
   ```bash
   #!/bin/bash
   
   # Export module data
   sudo -u unierp python3 -c "
   import json
   import psycopg2
   
   conn = psycopg2.connect(
       host='localhost',
       database='unierp_production',
       user='unierp_user',
       password='secure_password'
   )
   
   cursor = conn.cursor()
   
   # Export installed modules
   cursor.execute(\"\"\"
       SELECT name, state, latest_version 
       FROM ir_module 
       WHERE state IN ('installed', 'to upgrade', 'to remove')
       \"\"\")
   
   with open('/tmp/modules_backup.json', 'w') as f:
       json.dump(cursor.fetchall(), f, indent=2)
   
   conn.close()
   "
   ```

### Custom Data Backup
1. **User Data Export**:
   ```bash
   #!/bin/bash
   
   # Export user data with attachments
   sudo -u unierp python3 -c "
   import json
   import psycopg2
   import base64
   
   conn = psycopg2.connect(
       host='localhost',
       database='unierp_production',
       user='unierp_user',
       password='secure_password'
   )
   
   cursor = conn.cursor()
   
   # Export users with attachments
   cursor.execute(\"\"\"
       SELECT 
           u.id, u.login, u.name, u.email, u.company_id,
           u.signature, u.image,
           c.name as company_name, c.logo as company_logo
       FROM res_users u
       JOIN res_company c ON u.company_id = c.id
       WHERE u.active = true
       \"\"\")
   
   users = []
   for row in cursor.fetchall():
       user_data = {
           'id': row[0],
           'login': row[1],
           'name': row[2],
           'email': row[3],
           'company': {
               'name': row[4],
               'logo': base64.b64encode(row[5]).decode() if row[5] else None
           }
       }
       users.append(user_data)
   
   with open('/tmp/users_backup.json', 'w') as f:
       json.dump(users, f, indent=2)
   
   conn.close()
   "
   ```

---

## Disaster Recovery

### Recovery Procedures

#### System Recovery Plan
1. **Recovery Team**:
   - **Team Lead**: System Administrator
   - **Technical Lead**: Database Administrator
   - **Communications Lead**: IT Manager
   - **Business Lead**: Operations Manager

2. **Recovery Priorities**:
   - **Critical**: Database restoration
   - **High**: Application functionality
   - **Medium**: Configuration restoration
   - **Low**: Non-essential services

3. **Recovery Steps**:
   - **Assessment**: Evaluate damage and recovery requirements
   - **Planning**: Develop detailed recovery plan
   - **Execution**: Execute recovery procedures
   - **Verification**: Validate system functionality
   - **Documentation**: Document recovery process and outcomes

#### Recovery Scenarios

#### Complete System Failure
1. **Hardware Failure**:
   - **Assessment**: Identify failed components
   - **Replacement**: Procure and install replacement hardware
   - **Data Recovery**: Restore from backup to new hardware
   - **Configuration**: Reconfigure system settings
   - **Testing**: Verify all functionality

2. **Data Corruption**:
   - **Assessment**: Identify corrupted data extent
   - **Isolation**: Take corrupted system offline
   - **Recovery**: Restore from last known good backup
   - **Validation**: Verify data integrity
   - **Prevention**: Implement additional safeguards

#### Partial System Failure
1. **Application Failure**:
   - **Isolation**: Identify and isolate failed components
   - **Workaround**: Implement temporary solutions
   - **Repair**: Attempt to fix failed components
   - **Monitoring**: Enhanced monitoring during recovery

#### Cybersecurity Incident
1. **Containment**:
   - **Isolation**: Disconnect affected systems
   - **Preservation**: Preserve evidence for investigation
   - **Communication**: Notify stakeholders of incident
   - **Documentation**: Document all actions and decisions

2. **Eradication**:
   - **Removal**: Eliminate malware and threats
   - **System Rebuild**: Rebuild affected systems from scratch
   - **Security Hardening**: Implement enhanced security measures
   - **Recovery**: Restore from clean backups

---

## High Availability

### Load Balancer Configuration

#### Nginx Load Balancer
1. **Configuration**:
   ```nginx
   upstream unierp_cluster {
       server 192.168.1.10:8069 weight=1 max_fails=3;
       server 192.168.1.11:8069 weight=1 max_fails=3;
       server 192.168.1.12:8069 weight=1 max_fails=3;
       
       # Health checks
       server 192.168.1.10:8069;
       server 192.168.1.11:8069;
       server 192.168.1.12:8069;
   }
   
   server {
       listen 443 ssl;
       server_name unierp.your-domain.com;
       
       # SSL configuration
       ssl_certificate /etc/ssl/certs/unierp.crt;
       ssl_certificate_key /etc/ssl/private/unierp.key;
       
       # Proxy configuration
       location / {
           proxy_pass http://unierp_backend;
           proxy_set_header Host $host;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_connect_timeout 60s;
           proxy_send_timeout 60s;
           client_max_body_size 200m;
       }
       
       # Health check endpoint
       location /health {
           access_log off;
           return 200 "healthy";
           add_header Content-Type text/plain;
       }
   }
   ```

#### Database Replication
1. **Master-Slave Configuration**:
   ```ini
   # Master configuration
   [options]
   db_host = localhost
   db_port = 5432
   db_name = unierp_production_master
   db_user = unierp_user
   db_password = secure_password
   
   # Slave configuration
   [options]
   db_host = 192.168.1.20
   db_port = 5432
   db_name = unierp_production_slave
   db_user = unierp_user_readonly
   db_password = secure_password
   master_host = 192.168.1.10
   master_port = 5432
   master_user = unierp_user
   master_password = secure_password
   ```

### Failover Configuration

#### Automatic Failover
1. **Health Monitoring**:
   ```bash
   #!/bin/bash
   
   # Check master database
   MASTER_HEALTH=$(pg_isready -h 192.168.1.10 -p 5432 -U unierp_user)
   
   # Check slave database
   SLAVE_HEALTH=$(pg_isready -h 192.168.1.20 -p 5432 -U unierp_user_readonly)
   
   # Determine active database
   if [ "$MASTER_HEALTH" = "ready" ]; then
       ACTIVE_DB="master"
       ACTIVE_HOST="192.168.1.10"
   elif [ "$SLAVE_HEALTH" = "ready" ]; then
       ACTIVE_DB="slave"
       ACTIVE_HOST="192.168.1.20"
   else
       echo "Both databases unavailable"
       exit 1
   fi
   
   # Update load balancer configuration
   sed -i "s/server 192.168.1.10:8069 weight=1;/server 192.168.1.10:8069 weight=3;/" \
       /etc/nginx/conf.d/unierp.conf
   
   # Reload Nginx
   sudo nginx -s reload
   ```

---

## Backup Verification

### Backup Testing Procedures

#### Restore Testing
1. **Database Restore Test**:
   ```bash
   #!/bin/bash
   
   # Create test database
   createdb unierp_test_restore
   
   # Restore backup to test database
   pg_restore -h localhost -d unierp_test_restore \
       -U unierp_user -d unierp_production \
       /backup/unierp/database/latest/database.sql
   
   # Verify restore
   psql -h localhost -d unierp_test_restore -c "
   SELECT count(*) FROM res_users;
   SELECT count(*) FROM ir_module;
   "
   
   # Clean up test database
   dropdb unierp_test_restore
   ```

2. **File Restore Test**:
   ```bash
   #!/bin/bash
   
   # Test file system restore
   mkdir -p /tmp/restore_test
   tar -xzf /backup/unierp/system/latest/unierp_system.tar.gz -C /tmp/restore_test
   
   # Verify restored files
   ls -la /tmp/restore_test/opt/unierp/
   ls -la /tmp/restore_test/etc/unierp/
   ```

#### Backup Integrity Verification
1. **Checksum Verification**:
   ```bash
   #!/bin/bash
   
   BACKUP_FILE=$1
   EXPECTED_CHECKSUM=$2
   
   # Calculate current checksum
   CURRENT_CHECKSUM=$(sha256sum $BACKUP_FILE | awk '{print $1}')
   
   # Compare with stored checksum
   if [ "$CURRENT_CHECKSUM" = "$EXPECTED_CHECKSUM" ]; then
       echo "Backup integrity verified"
   else
       echo "Backup integrity check failed"
       exit 1
   fi
   ```

2. **Restore Testing**:
   ```bash
   #!/bin/bash
   
   # Test restore process
   RESTORE_DATE=$1
   RESTORE_LOG="/tmp/restore_test_$RESTORE_DATE.log"
   
   # Execute restore with logging
   /opt/unierp/scripts/restore_system.sh $RESTORE_DATE 2>&1 | tee $RESTORE_LOG
   
   # Verify restore success
   if [ $? -eq 0 ]; then
       echo "Restore test successful"
   else
       echo "Restore test failed"
   fi
   ```

---

## Recovery Testing

### Disaster Recovery Drills

#### Recovery Drill Scenarios
1. **Database Corruption Recovery**:
   - **Scenario**: Database corruption detected
   - **Objective**: Restore database from backup
   - **Steps**:
     1. Stop UniERP service
     2. Identify last good backup
     3. Restore database from backup
     4. Verify data integrity
     5. Start UniERP service
     6. Test application functionality
   - **Success Criteria**: Database accessible, data verified, application functional

2. **System Failure Recovery**:
   - **Scenario**: Complete system failure
   - **Objective**: Restore system operations from backup
   - **Steps**:
     1. Assess hardware damage
     2. Procure replacement hardware
     3. Install operating system
     4. Restore UniERP application
     5. Restore configuration from backup
     6. Restore data from backup
     7. Test all functionality
     8. Update documentation
   - **Success Criteria**: System fully operational, data verified

3. **Cybersecurity Incident Recovery**:
   - **Scenario**: Security breach detected
   - **Objective**: Eradicate threat and restore secure operations
   - **Steps**:
     1. Isolate affected systems
     2. Preserve forensic evidence
     3. Eradicate malware
     4. Rebuild affected systems
     5. Restore from clean backups
     6. Implement enhanced security
     7. Monitor for recurrence
   - **Success Criteria**: Systems secure, threat eliminated, monitoring active

---

## Conclusion

This comprehensive backup and recovery guide provides essential procedures for:

### Backup Success Factors

1. **Comprehensive Coverage**: All system components backed up
2. **Automation**: Automated backup procedures minimize human error
3. **Verification**: Regular backup integrity checks
4. **Off-Site Storage**: Secure backup storage at separate location
5. **Documentation**: Clear procedures and responsibilities

### Recovery Success Factors

1. **Quick Recovery**: Minimized downtime through efficient procedures
2. **Data Integrity**: Verified data restoration and validation
3. **System Restoration**: Complete system recovery capabilities
4. **High Availability**: Load balancing and failover mechanisms
5. **Testing**: Regular recovery testing and validation

### Ongoing Management

1. **Regular Testing**: Monthly recovery procedure testing
2. **Backup Validation**: Weekly backup integrity verification
3. **Procedure Updates**: Quarterly review and update of procedures
4. **Training**: Regular recovery training for IT staff
5. **Documentation**: Maintain current recovery documentation

For additional backup and recovery assistance:
- **Technical Support**: admin-support@uslbd.com
- **Emergency**: +1-555-UNIERP-911
- **Documentation**: https://docs.uslbd.com/backup-recovery
- **Community Forum**: https://community.uslbd.com/disaster-recovery

Remember that regular testing and validation of backup and recovery procedures is essential for ensuring business continuity and data protection.