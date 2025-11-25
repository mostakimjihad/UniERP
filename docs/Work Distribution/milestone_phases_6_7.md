# Phase 6: Module-Level Rebranding – 1-Day Intensive Plan

**Duration:** 1 Day
**Team:** Backend Developers (2-3), Frontend Developer
**Prerequisites:** Phase 5 Complete

---

## Objectives

1. Rebrand all core modules (base, web, mail, etc.)
2. Update module manifest files
3. Modify user-facing strings
4. Replace logos and images

---

## 1-Day Milestone Schedule

### **Milestone 6.1 – Base Module Rebranding (2 hours)**

**Objective:** Rebrand the foundational base module with UniERP identity.

**Tasks:**

* Update `addons/base/__manifest__.py` with UniSoft author information
* Replace default company data with UniERP branding
* Update base module icons and logos
* Modify base module templates and views
* Test base module functionality after changes

**Deliverables:**

* Rebranded base module manifest
* Updated company data XML files
* Replaced logos and icons
* Base module test results

---

### **Milestone 6.2 – Web Module Rebranding (2.5 hours)**

**Objective:** Complete visual rebranding of the web interface module.

**Tasks:**

* Replace all Odoo logos in `addons/web/static/src/img/`
* Update login page templates with UniERP branding
* Modify browser titles and page headers
* Update web module SCSS/CSS variables
* Test web interface functionality

**Deliverables:**

* Replaced logo files (all sizes)
* Updated login templates
* Modified browser title JavaScript
* Updated SCSS color variables
* Web interface verification report

---

### **Milestone 6.3 – Mail Module Rebranding (1.5 hours)**

**Objective:** Rebrand email templates and mail functionality.

**Tasks:**

* Update email templates with UniERP branding
* Modify email headers and footers
* Update notification templates
* Change default email domains to unisoft.com.bd
* Test email functionality

**Deliverables:**

* Rebranded email templates
* Updated notification system
* Modified email configuration
* Email functionality test report

---

### **Milestone 6.4 – Bulk Module Manifest Updates (1 hour)**

**Objective:** Systematically update all remaining module manifests.

**Tasks:**

* Execute bulk update script for all `__manifest__.py` files
* Update author fields to 'UniSoft Systems Ltd.'
* Replace website URLs with uslbd.com
* Update support email addresses
* Verify all modules load without errors

**Deliverables:**

* Updated all module manifests
* Bulk update script execution log
* Module loading verification report

---

### **Milestone 6.5 – Module Integration Testing (1 hour)**

**Objective:** Verify all rebranded modules work together correctly.

**Tasks:**

* Test module installation and loading
* Verify inter-module dependencies
* Check for any remaining Odoo references
* Run smoke tests on rebranded modules
* Validate module functionality

**Deliverables:**

* Integration test results
* Module loading verification
* Smoke test completion report
* Issue log (if any)

---

## Success Criteria

* ✅ All core modules rebranded with UniERP identity
* ✅ No Odoo logos visible in web interface
* ✅ Login page displays UniERP branding
* ✅ Email templates use UniSoft branding
* ✅ All modules load without errors
* ✅ Module functionality preserved

---

## Detailed Implementation Notes

### Critical Files to Modify:

1. **`addons/base/__manifest__.py`**
   - Update author, website, and support fields
   - Replace version information
   - Update license attribution

2. **`addons/web/static/src/img/`**
   - Replace all logo files
   - Update favicon and icons
   - Ensure all sizes are covered

3. **`addons/web/views/login_templates.xml`**
   - Update login page branding
   - Replace Odoo references
   - Add UniSoft attribution

4. **All `__manifest__.py` files**
   - Bulk update author information
   - Replace website URLs
   - Update support email addresses

### Testing Checklist:

- [ ] Base module loads correctly
- [ ] Web interface shows UniERP branding
- [ ] Login page displays correctly
- [ ] Email templates render properly
- [ ] All modules install without errors
- [ ] No Odoo references visible in UI

### Risk Mitigation:

* Backup all original module files before modification
* Test each module individually after updates
* Maintain rollback procedures for critical modules
* Document any module-specific issues

---

## Hourly Schedule Breakdown

| Time        | Milestone   | Primary Focus                     |
| ----------- | ----------- | --------------------------------- |
| 09:00–11:00 | 6.1         | Base module rebranding            |
| 11:00–13:30 | 6.2         | Web module rebranding             |
| 13:30–14:30 | Lunch/Break | -                                 |
| 14:30–16:00 | 6.3         | Mail module rebranding            |
| 16:00–17:00 | 6.4         | Bulk manifest updates            |
| 17:00–18:00 | 6.5         | Module integration testing       |

---

## Pre-requisites Verification

Before starting Phase 6, ensure:

* [ ] Phase 5 core system rebranding complete
* [ ] All branding assets available
* [ ] Development environment accessible
* [ ] Module backup procedures in place
* [ ] Team members briefed on module structure

---

## Post-Milestone Actions

1. **Immediate (End of Day):**
   * Commit all module changes to version control
   * Create Phase 6 completion report
   * Brief database team on Phase 7 requirements

2. **Next Day Preparation:**
   * Review any module-specific issues
   * Prepare database for Phase 7 updates
   * Ensure all module changes are documented

---

## Contact & Support

**Technical Lead:** [Name/Contact]
**Escalation:** Project Manager
**Documentation:** All changes tracked in project repository

---

*This intensive one-day plan ensures comprehensive module-level rebranding while maintaining system integrity and preparing for successful database rebranding in Phase 7.*

---

# Phase 7: Database & Configuration Rebranding – 1-Day Intensive Plan

**Duration:** 1 Day
**Team:** Database Administrator, Backend Developers
**Prerequisites:** Phase 6 Complete

---

## Objectives

1. Update database table data
2. Modify configuration parameters
3. Clean up menu labels
4. Update system settings

---

## 1-Day Milestone Schedule

### **Milestone 7.1 – System Parameters Update (2 hours)**

**Objective:** Update all system parameters and configuration data.

**Tasks:**

* Execute SQL script to update `ir_config_parameter` table
* Replace help URLs with uslbd.com/docs
* Update system name to 'UniERP'
* Modify web.base.url and other critical parameters
* Test parameter updates

**Deliverables:**

* Updated system parameters
* SQL execution log
* Parameter verification report
* Updated configuration values

---

### **Milestone 7.2 – Company Data Rebranding (1.5 hours)**

**Objective:** Update company information and default data.

**Tasks:**

* Update `res_company` table with UniERP information
* Replace default logos and favicons in database
* Update company email addresses
* Modify company website references
* Test company data display

**Deliverables:**

* Updated company records
* New logo and favicon data
* Updated contact information
* Company display verification

---

### **Milestone 7.3 – Menu and Action Labels Update (1.5 hours)**

**Objective:** Clean up any remaining Odoo references in menus and actions.

**Tasks:**

* Execute SQL to update `ir_ui_menu` table
* Replace Odoo references in menu items
* Update action descriptions and labels
* Clean up module names and descriptions
* Verify menu functionality

**Deliverables:**

* Updated menu labels
* Cleaned action descriptions
* Updated module information
* Menu functionality test report

---

### **Milestone 7.4 – Email Configuration Migration (1 hour)**

**Objective:** Update all email-related configurations and templates.

**Tasks:**

* Update email templates in database
* Replace odoo.com domains with unisoft.com.bd
* Update mail configuration parameters
* Test email functionality
* Verify email delivery

**Deliverables:**

* Updated email templates
* Modified email configuration
* Email functionality test results
* Delivery verification report

---

### **Milestone 7.5 – Database Verification & Cleanup (1 hour)**

**Objective:** Verify all database changes and perform final cleanup.

**Tasks:**

* Run comprehensive database verification script
* Check for any remaining Odoo references
* Validate all configuration changes
* Test database functionality
* Create database backup post-rebranding

**Deliverables:**

* Database verification report
* Cleanup completion log
* Final database backup
* Functionality test results

---

## Success Criteria

* ✅ All database parameters updated to UniERP
* ✅ System URLs point to uslbd.com
* ✅ Menu items display UniERP branding
* ✅ Email addresses use unisoft.com.bd domain
* ✅ No Odoo references remain in database
* ✅ All database functionality preserved

---

## Detailed Implementation Notes

### Critical Database Tables:

1. **`ir_config_parameter`**
   - Update help URLs
   - Change system name
   - Replace web URLs

2. **`res_company`**
   - Update company names
   - Replace logos and favicons
   - Modify contact information

3. **`ir_ui_menu`**
   - Clean up menu labels
   - Update action descriptions
   - Remove Odoo references

4. **`mail_template`**
   - Update email domains
   - Replace branding elements
   - Modify templates

### SQL Scripts to Execute:

```sql
-- Update system parameters
UPDATE ir_config_parameter SET value = 'https://uslbd.com/docs' WHERE key = 'help.url';
UPDATE ir_config_parameter SET value = 'UniERP' WHERE key = 'web.base.system_name';

-- Update company data
UPDATE res_company SET name = 'UniERP Demo Company' WHERE id = 1;

-- Update email templates
UPDATE mail_template SET email_from = 'noreply@uslbd.com' WHERE email_from LIKE '%@odoo.com';

-- Update menu items
UPDATE ir_ui_menu SET name = REPLACE(name, 'Odoo', 'UniERP');
```

### Testing Checklist:

- [ ] System parameters updated correctly
- [ ] Company data displays properly
- [ ] Menu items show UniERP branding
- [ ] Email configuration works
- [ ] No Odoo references remain
- [ ] Database functionality intact

### Risk Mitigation:

* Create full database backup before any updates
* Test SQL scripts on staging database first
* Maintain rollback procedures for each update
* Document all database changes

---

## Hourly Schedule Breakdown

| Time        | Milestone   | Primary Focus                     |
| ----------- | ----------- | --------------------------------- |
| 09:00–11:00 | 7.1         | System parameters update          |
| 11:00–12:30 | 7.2         | Company data rebranding           |
| 12:30–14:00 | 7.3         | Menu and action labels update     |
| 14:00–15:00 | 7.4         | Email configuration migration     |
| 15:00–16:00 | 7.5         | Database verification & cleanup  |

---

## Pre-requisites Verification

Before starting Phase 7, ensure:

* [ ] Phase 6 module rebranding complete
* [ ] Database backup procedures verified
* [ ] SQL scripts tested on staging
* [ ] Database access credentials ready
* [ ] Team members briefed on database structure

---

## Post-Milestone Actions

1. **Immediate (End of Day):**
   * Create final database backup
   * Document all database changes
   * Generate Phase 7 completion report
   * Prepare handover for Phase 8

2. **Next Day Preparation:**
   * Review any database issues encountered
   * Verify all changes are consistent
   * Prepare environment for UI rebranding

---

## Contact & Support

**Database Administrator:** Mostakim Jihad
**Escalation:** Software Engineer
**Documentation:** All changes tracked in project repository

---

## Key Assumptions

* All module rebranding from Phase 6 is complete and tested
* Database access permissions are properly configured
* SQL scripts have been validated on staging environment
* Team has necessary database administration skills
* Backup and recovery procedures are in place
* All stakeholders have approved the database changes
