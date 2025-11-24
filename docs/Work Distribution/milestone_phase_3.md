# Phase 3: Comprehensive Code Analysis – 1-Day Plan

**Duration:** 1 Day
**Team:** Technical Lead, Senior Backend Developers, Business Analyst
**Prerequisites:** Phase 2 Complete

---

## Objectives

1. Map all Odoo branding occurrences across codebase
2. Identify critical vs. non-critical branding elements
3. Document code structure and dependencies
4. Create rebranding checklist
5. Analyze licensing requirements

---

## 1-Day Milestone Schedule

### **Milestone 3.1 – Brand Occurrences Mapping (2 hours)**

**Objective:** Quickly scan the codebase for Odoo branding.

**Tasks:**

* Run the automated branding scan script over the full codebase
* Focus on high-priority file types: `.py`, `.js`, `.xml`, `.html`, `.css`
* Capture file path, line number, term, and context snippet

**Deliverables:**

* Raw branding scan report (CSV/JSON)
* Initial summary: total occurrences per file and term

---

### **Milestone 3.2 – Prioritize Branding Elements (1 hour)**

**Objective:** Classify scan results by importance for rebranding.

**Tasks:**

* Review raw scan report
* Categorize findings into Priority 1–4:

  * **Critical:** `odoo-bin`, logos, login page templates, browser titles, email templates
  * **High:** `__manifest__.py`, user strings, tooltips, error messages
  * **Medium:** comments, dev docs, safe variable names
  * **Low:** logs, debug messages
* Create **actionable checklist** for the team

**Deliverables:**

* Prioritized rebranding checklist

---

### **Milestone 3.3 – Architecture & Dependency Mapping (1.5 hours)**

**Objective:** Identify key modules, dependencies, and code structure.

**Tasks:**

* Document main module hierarchy
* Map internal and external dependencies
* Highlight critical templates and configuration files
* Optional: create a simple dependency diagram

**Deliverables:**

* Architecture & dependency documentation
* Visual module dependency map (optional)

---

### **Milestone 3.4 – Licensing Review (1 hour)**

**Objective:** Ensure all modifications comply with LGPL v3.

**Tasks:**

* Review licensing requirements for rebranding and modifications
* Ensure attribution and copyright statements are ready
* Highlight any files requiring special attention

**Deliverables:**

* License compliance checklist
* Standardized UniERP attribution block

---

### **Milestone 3.5 – Consolidated Reporting & Handover (1.5 hours)**

**Objective:** Merge all findings into a single actionable report.

**Tasks:**

* Combine results from branding scan, prioritization, architecture, and licensing
* Identify high-risk areas for rebranding
* Present summary to the team with next-phase recommendations

**Deliverables:**

* Final Phase 3 report (Markdown/PDF)
* Rebranding task list ready for execution
* Risk assessment summary

---

## Success Criteria

* ✅ All critical Odoo branding occurrences identified
* ✅ Rebranding checklist prioritized and actionable
* ✅ Architecture & dependencies documented
* ✅ Licensing compliance verified
* ✅ Team aligned on next steps and risks
