# Phase 5: Core System Rebranding – 1-Day Intensive Plan

**Duration:** 1 Day
**Team:** Senior Backend Developers, Technical Lead
**Prerequisites:** Phases 3 & 4 Complete

---

## Objectives

1. Rebrand core Odoo framework files
2. Update main executable and configuration
3. Modify release information
4. Update system-level branding

---

## 1-Day Milestone Schedule

### **Milestone 5.1 – Main Executable Rebranding (1.5 hours)**

**Objective:** Rename and rebrand the primary system executable.

**Tasks:**

* Rename `odoo-bin` to `unierp-bin` using git mv
* Update file contents with UniERP branding references
* Update shebang lines and internal references
* Set executable permissions
* Test basic functionality of renamed executable

**Deliverables:**

* Renamed `unierp-bin` executable
* Updated executable with UniERP branding
* Verification test results

---

### **Milestone 5.2 – Release Configuration Update (2 hours)**

**Objective:** Modify core release information and system metadata.

**Tasks:**

* Update `odoo/release.py` with UniERP product information
* Set version info to UniERP 1.0.0
* Update author, email, and URL references
* Configure proper LGPL attribution statements
* Update product description and metadata

**Deliverables:**

* Updated `release.py` with UniERP information
* Proper LGPL attribution block
* Version information set to 1.0.0

---

### **Milestone 5.3 – Configuration System Rebranding (1.5 hours)**

**Objective:** Create UniERP-specific configuration templates.

**Tasks:**

* Create UniERP configuration file template (`/etc/unierp/unierp.conf`)
* Update default configuration parameters
* Replace Odoo-specific paths and references
* Update email configuration with UniSoft domains
* Create systemd service file for UniERP

**Deliverables:**

* UniERP configuration template
* Systemd service file (`unierp.service`)
* Updated default parameters

---

### **Milestone 5.4 – Package Metadata Update (1 hour)**

**Objective:** Update all package and distribution metadata.

**Tasks:**

* Update `setup.py` or equivalent packaging files
* Modify package descriptions and metadata
* Update dependency references where needed
* Ensure package names reflect UniERP branding
* Update changelog and version files

**Deliverables:**

* Updated package metadata
* Modified packaging configuration
* Version consistency across files

---

### **Milestone 5.5 – Core Framework Integration Testing (1 hour)**

**Objective:** Verify all core rebranding changes work together.

**Tasks:**

* Test `unierp-bin --version` displays correct information
* Verify configuration files load properly
* Test service start/stop functionality
* Run basic smoke tests on rebranded system
* Validate core functionality remains intact

**Deliverables:**

* Integration test results
* Smoke test report
* Verification checklist completion

---

### **Milestone 5.6 – Documentation & Handover (1 hour)**

**Objective:** Document all changes and prepare for next phase.

**Tasks:**

* Document all modified files and changes
* Create summary of rebranding updates
* Prepare handover documentation for Phase 6
* Update any relevant README files
* Create quick reference guide for changes

**Deliverables:**

* Change documentation
* Phase 5 completion report
* Handover package for next phase

---

## Success Criteria

* ✅ `unierp-bin` executable works correctly
* ✅ Release information shows UniERP branding
* ✅ Configuration system rebranded and functional
* ✅ Package metadata updated consistently
* ✅ Core functionality verified intact
* ✅ All changes documented for next phase

---

## Detailed Implementation Notes

### Critical Files to Modify:

1. **`odoo-bin` → `unierp-bin`**
   - Update all internal references
   - Modify help text and version output
   - Update error messages

2. **`odoo/release.py`**
   - Product name: 'UniERP'
   - Version: '1.0.0'
   - Author: 'UniSoft Systems Ltd.'
   - URLs pointing to uslbd.com

3. **Configuration Files**
   - Default paths updated
   - Email domains changed to unisoft.com.bd
   - Service names updated

4. **System Integration**
   - systemd service file
   - Logrotate configuration
   - Backup script references

### Testing Checklist:

- [ ] `./unierp-bin --version` returns UniERP 1.0.0
- [ ] Configuration file loads without errors
- [ ] Service starts and stops correctly
- [ ] Basic web interface accessible
- [ ] No Odoo references in version output
- [ ] All core modules load properly

### Risk Mitigation:

* Backup all original files before modification
* Test each change individually before proceeding
* Maintain rollback procedures for each milestone
* Document any unexpected issues or dependencies

---

## Hourly Schedule Breakdown

| Time        | Milestone   | Primary Focus                     |
| ----------- | ----------- | --------------------------------- |
| 09:00–10:30 | 5.1         | Main executable rebranding        |
| 10:30–12:30 | 5.2         | Release configuration update       |
| 12:30–13:30 | Lunch/Break | -                                 |
| 13:30–15:00 | 5.3         | Configuration system rebranding    |
| 15:00–16:00 | 5.4         | Package metadata update            |
| 16:00–17:00 | 5.5         | Integration testing                |
| 17:00–18:00 | 5.6         | Documentation & handover          |

---

## Pre-requisites Verification

Before starting Phase 5, ensure:

* [ ] Phase 3 code analysis complete
* [ ] Phase 4 branding assets ready
* [ ] Development environment accessible
* [ ] Git repository properly configured
* [ ] Backup procedures in place
* [ ] Team members available and briefed

---

## Post-Milestone Actions

1. **Immediate (End of Day):**
   * Commit all changes to version control
   * Create Phase 5 completion report
   * Brief team on Phase 6 requirements

2. **Next Day Preparation:**
   * Review any issues encountered
   * Prepare environment for Phase 6
   * Ensure all deliverables accessible to module team

---

## Contact & Support

**Technical Lead:** [Name/Contact]
** escalation:** Project Manager
**Documentation:** All changes tracked in project repository

---

*This intensive one-day plan ensures comprehensive core system rebranding while maintaining system integrity and preparing for successful module-level rebranding in Phase 6.*