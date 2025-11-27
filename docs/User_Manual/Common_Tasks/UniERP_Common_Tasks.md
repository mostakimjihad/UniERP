# UniERP Common Tasks Guide

## Table of Contents

1. [User Account Management](#user-account-management)
2. [Data Entry and Management](#data-entry-and-management)
3. [Sales Operations](#sales-operations)
4. [Purchase Operations](#purchase-operations)
5. [Inventory Management](#inventory-management)
6. [Financial Operations](#financial-operations)
7. [Reporting and Analytics](#reporting-and-analytics)
8. [System Administration](#system-administration)

---

## User Account Management

### Creating a New User Account

#### Prerequisites
- Administrator access rights
- User's personal information
- Department and role information

#### Steps
1. **Log in as Administrator**
   - Navigate to Settings → Users & Companies → Users
   - Click "New" to create a new user

2. **Enter User Information**
   - **Name**: Full name of the user
   - **Email**: Professional email address
   - **Login**: Unique username for system access
   - **Password**: Initial password (user will change on first login)

3. **Configure Access Rights**
   - **Application Access**: Select modules user can access
   - **Groups**: Assign appropriate permission groups
   - **Companies**: Set company access if multi-company setup
   - **Sales Teams**: Assign to relevant sales teams

4. **Set Preferences**
   - **Language**: User's preferred interface language
   - **Timezone**: User's local timezone
   - **Email Signature**: Default email signature template

5. **Save and Activate**
   - Review all entered information
   - Click "Save" to create the account
   - Send login credentials to the user
   - Verify user can log in successfully

### Modifying User Account

#### Updating Personal Information
1. **Log in to UniERP**
2. **Go to User Profile** (top-right corner)
3. **Edit Personal Details**:
   - Name and contact information
   - Email signature
   - Notification preferences
4. **Save Changes**

#### Changing Password
1. **Navigate to User Profile → Security**
2. **Click "Change Password"**
3. **Enter Current Password**
4. **Set New Password** (must meet security requirements)
5. **Confirm New Password**
6. **Click "Update Password"

### Managing User Permissions

#### Assigning Additional Access
1. **Go to Settings → Users & Companies → Users**
2. **Search and Select User**
3. **Edit Access Rights**:
   - Add module access as needed
   - Assign additional permission groups
   - Update company access if required
4. **Save Changes**

#### Removing Access
1. **Select User Account**
2. **Edit Access Rights**
3. **Remove Unnecessary Permissions**
4. **Document Reason for Access Change**
5. **Save and Notify User**

---

## Data Entry and Management

### Creating and Managing Records

#### General Data Entry Best Practices
- **Accuracy**: Double-check all entered information
- **Completeness**: Fill in all required fields (marked with *)
- **Consistency**: Use standardized formats and naming conventions
- **Validation**: Verify data before saving records
- **Documentation**: Add relevant notes and attachments

#### Creating a New Record
1. **Navigate to Appropriate Module**
2. **Click "New" Button**
3. **Fill in Required Fields**:
   - Required fields are marked with red asterisk (*)
   - Use dropdown menus for standardized values
   - Enter dates in correct format (DD/MM/YYYY)
4. **Add Optional Information**:
   - Additional details for context
   - Attach relevant documents
   - Add notes for future reference
5. **Save the Record**:
   - Click "Save" to store the record
   - Wait for confirmation message
   - Verify the record appears in listings

#### Editing Existing Records
1. **Locate the Record**:
   - Use search functionality
   - Apply filters to narrow results
   - Sort by relevant columns
2. **Open Record for Editing**:
   - Click on the record to open details
   - Click "Edit" button or double-click record
3. **Make Changes**:
   - Update outdated information
   - Add missing details
   - Correct any errors
4. **Save Changes**:
   - Click "Save" to update the record
   - Verify changes are reflected

### Data Import and Export

#### Importing Data from External Files
1. **Prepare Data File**:
   - Use CSV or Excel format
   - Include column headers
   - Follow UniERP field naming conventions
   - Validate data format and values

2. **Navigate to Import Function**:
   - Go to Settings → Data Import
   - Select the data type to import
   - Choose file from your computer

3. **Configure Import Settings**:
   - **File Type**: CSV, Excel, or other format
   - **Delimiter**: Comma, semicolon, or tab
   - **Encoding**: UTF-8 recommended
   - **Header Row**: Indicate if first row contains headers

4. **Map Fields**:
   - Match file columns to UniERP fields
   - Set default values for unmapped fields
   - Configure validation rules
   - Preview import data

5. **Execute Import**:
   - Click "Import" to start process
   - Monitor import progress
   - Review import results and errors
   - Handle any rejected records

#### Exporting Data
1. **Navigate to Desired Module**
2. **Apply Filters**:
   - Set date ranges
   - Select specific categories
   - Apply status filters
   - Customize view columns

3. **Export Data**:
   - Click "Export" or "Download" button
   - **Choose Export Format**:
     - Excel (.xlsx)
     - CSV (.csv)
     - PDF (.pdf)
     - Other formats as available
4. **Save File**:
   - Choose save location
   - Enter filename
   - Confirm export

### Data Validation and Quality Control

#### Data Quality Checks
1. **Completeness Check**:
   - Verify all required fields are filled
   - Check for missing information
   - Ensure consistent data entry

2. **Accuracy Verification**:
   - Cross-reference with source documents
   - Validate calculations and totals
   - Check for duplicate entries

3. **Consistency Review**:
   - Standardize naming conventions
   - Verify formatting consistency
   - Check for data type mismatches

#### Handling Data Issues
1. **Identify Problem Records**:
   - Use data validation reports
   - Run duplicate detection
   - Check for outliers and anomalies

2. **Correct Issues**:
   - Edit problematic records
   - Merge duplicate entries
   - Delete invalid records with proper documentation

3. **Prevent Future Issues**:
   - Set up validation rules
   - Create data entry templates
   - Train users on best practices

---

## Sales Operations

### Creating a Sales Order

#### Prerequisites
- Customer information in system
- Product catalog configured
- Pricing rules established
- User has sales module access

#### Step-by-Step Process

1. **Navigate to Sales Module**
   - Go to Sales → Orders → Orders
   - Click "New" to create sales order

2. **Enter Customer Information**
   - **Customer Selection**:
     - Search existing customer
     - Create new customer if needed
     - Verify customer credit limit
   - **Delivery Address**:
     - Select from customer addresses
     - Add new delivery address
     - Verify shipping information

3. **Add Order Lines**
   - **Product Selection**:
     - Search and select products
     - Verify product availability
     - Check pricing and discounts
   - **Quantity and Details**:
     - Enter order quantities
     - Set delivery dates
     - Add product descriptions if needed
   - **Pricing Configuration**:
     - Apply customer-specific pricing
     - Add discounts and promotions
     - Calculate taxes automatically

4. **Review Order Details**
   - **Order Summary**:
     - Verify subtotal calculations
     - Check tax calculations
     - Review shipping costs
     - Confirm total amount
   - **Terms and Conditions**:
     - Set payment terms
     - Define delivery terms
     - Add special instructions
     - Attach relevant documents

5. **Confirm and Process**
   - **Order Confirmation**:
     - Click "Confirm" to validate order
     - Check for any validation errors
     - Generate order confirmation
   - **Order Processing**:
     - Create delivery orders
     - Generate invoice if required
     - Send confirmation to customer

### Managing Sales Quotations

#### Creating a Quotation
1. **Navigate to Sales → Quotations**
2. **Click "New" to create quotation**
3. **Follow same process as sales order**
4. **Set Quotation Validity Period**
5. **Send Quotation to Customer**
6. **Track Quotation Status**

#### Converting Quotation to Sales Order
1. **Open Quotation**
2. **Click "Convert to Order"**
3. **Review and Confirm Conversion**
4. **Process as Sales Order**

### Managing Customer Returns

#### Creating a Return Order
1. **Navigate to Sales → Returns**
2. **Click "New Return Order"**
3. **Select Original Sales Order**
4. **Enter Return Details**:
   - Products to be returned
   - Return quantities
   - Reason for return
   - Return authorization number
5. **Process Return**:
   - Receive returned items
   - Inspect returned products
   - Process refund or credit
   - Update inventory

---

## Purchase Operations

### Creating a Purchase Order

#### Prerequisites
- Supplier information in system
- Product catalog configured
- Approval workflows set up
- User has purchase module access

#### Step-by-Step Process

1. **Navigate to Purchase Module**
   - Go to Purchase → Orders → Orders
   - Click "New" to create purchase order

2. **Enter Supplier Information**
   - **Supplier Selection**:
     - Search existing supplier
     - Create new supplier if needed
     - Verify supplier status and terms
   - **Supplier Details**:
     - Select supplier contact person
     - Verify payment terms
     - Check delivery terms

3. **Add Order Lines**
   - **Product Selection**:
     - Search and select products
     - Compare supplier prices
     - Check lead times and availability
   - **Quantity and Details**:
     - Enter order quantities
     - Set delivery dates
     - Specify product requirements
   - **Pricing Configuration**:
     - Negotiate prices and discounts
     - Include shipping costs
     - Calculate taxes automatically

4. **Review Order Details**
   - **Order Summary**:
     - Verify subtotal calculations
     - Check tax calculations
     - Review additional costs
     - Confirm total amount
   - **Terms and Conditions**:
     - Confirm payment terms
     - Verify delivery terms
     - Add special instructions
     - Attach relevant documents

5. **Submit for Approval**
   - **Order Validation**:
     - Check budget availability
     - Verify approval requirements
     - Complete all required fields
   - **Submit for Approval**:
     - Click "Send for Approval"
     - Route to appropriate approver
     - Track approval status
   - **Order Confirmation**:
     - Once approved, confirm order
     - Send to supplier
     - Track order acknowledgment

### Managing Purchase Receipts

#### Receiving Goods
1. **Navigate to Purchase → Receipts**
2. **Select Purchase Order to Receive**
3. **Verify Delivery**:
   - Check against purchase order
   - Verify quantities and quality
   - Document any discrepancies
4. **Process Receipt**:
   - Confirm receipt quantities
   - Update inventory
   - Generate receipt documents
   - Notify relevant departments

### Processing Supplier Invoices

#### Invoice Validation
1. **Navigate to Purchase → Bills**
2. **Create New Bill**
3. **Link to Purchase Order**
4. **Three-Way Matching**:
   - Compare invoice to purchase order
   - Verify against receipt quantities
   - Check pricing and calculations
5. **Approve for Payment**:
   - Resolve any discrepancies
   - Submit for payment approval
   - Schedule payment processing

---

## Inventory Management

### Stock Movement Operations

#### Receiving Stock
1. **Navigate to Inventory → Operations → Receipts**
2. **Create New Receipt**
3. **Select Source**:
   - Purchase order receipt
   - Production receipt
   - Transfer receipt
   - Return receipt
4. **Enter Receipt Details**:
   - Products and quantities
   - Batch/lot numbers if applicable
   - Expiration dates
   - Storage location assignment
5. **Validate and Process**:
   - Verify all information
   - Process receipt
   - Update inventory levels
   - Generate receipt documents

#### Issuing Stock
1. **Navigate to Inventory → Operations → Deliveries**
2. **Create New Delivery**
3. **Select Destination**:
   - Sales order fulfillment
   - Internal consumption
   - Production usage
   - Transfer to other location
4. **Enter Issue Details**:
   - Products and quantities
   - Batch/lot selection
   - FIFO/LIFO selection if applicable
   - Destination specification
5. **Process Issue**:
   - Validate availability
   - Process stock issue
   - Update inventory levels
   - Generate issue documents

### Stock Adjustment Procedures

#### Physical Inventory Count
1. **Prepare for Count**:
   - Define count areas
   - Prepare count sheets
   - Freeze inventory movements
   - Assign counting teams

2. **Execute Count**:
   - Count all items in assigned areas
   - Record counts on count sheets
   - Note any discrepancies
   - Verify unusual items

3. **Process Count Results**:
   - Enter count data into system
   - Calculate variances
   - Generate adjustment proposals
   - Review and approve adjustments

#### Stock Adjustment
1. **Navigate to Inventory → Operations → Adjustments**
2. **Create New Adjustment**
3. **Select Products**:
   - Choose products to adjust
   - Enter current quantities
   - Enter system quantities
   - Specify adjustment reason

4. **Process Adjustment**:
   - Review adjustment details
   - Submit for approval if required
   - Process approved adjustments
   - Update inventory records

---

## Financial Operations

### Creating Customer Invoices

#### Prerequisites
- Sales orders completed
- Customer billing information current
- Tax configuration complete
- User has accounting access

#### Invoice Creation Process
1. **Navigate to Accounting → Customers → Invoices**
2. **Click "New" to create invoice**
3. **Select Customer**:
   - Search customer database
   - Verify billing address
   - Check payment terms
   - Review credit status

4. **Create Invoice Lines**:
   - **From Sales Orders**:
     - Select completed sales orders
     - Verify delivered quantities
     - Apply agreed pricing
   - **Manual Invoice Lines**:
     - Add service charges
     - Include recurring fees
     - Apply late payment penalties
     - Add miscellaneous charges

5. **Calculate Invoice Totals**:
   - Verify line item totals
   - Apply tax calculations
   - Add shipping and handling
   - Calculate final amount due

6. **Review and Validate**:
   - Check all calculations
   - Verify terms and conditions
   - Attach supporting documents
   - Review payment schedule

7. **Post Invoice**:
   - Submit for approval if required
   - Post to general ledger
   - Generate invoice PDF
   - Send to customer

### Processing Supplier Payments

#### Payment Processing
1. **Navigate to Accounting → Vendors → Payments**
2. **Create New Payment**
3. **Select Supplier**:
   - Search supplier database
   - Review outstanding bills
   - Check payment terms
   - Verify bank details

4. **Select Bills to Pay**:
   - Choose invoices for payment
   - Verify amounts and due dates
   - Apply early payment discounts
   - Handle partial payments

5. **Configure Payment Details**:
   - **Payment Method**:
     - Bank transfer
     - Check payment
     - Credit card payment
     - Electronic payment
   - **Payment Information**:
     - Bank account selection
     - Payment reference
     - Payment date
     - Memo/notes

6. **Process Payment**:
   - Validate payment information
   - Submit for approval if required
   - Execute payment
   - Update supplier accounts

### Bank Reconciliation

#### Reconciliation Process
1. **Navigate to Accounting → Configuration → Bank Reconciliation**
2. **Select Bank Account**:
   - Choose bank statement
   - Upload statement file
   - Import transaction data
   - Verify statement period

3. **Match Transactions**:
   - **Automatic Matching**:
     - System suggests matches
     - Review proposed matches
     - Accept valid matches
   - **Manual Matching**:
     - Find corresponding transactions
     - Match payments to invoices
     - Handle unmatched items
     - Create journal entries if needed

4. **Complete Reconciliation**:
   - Verify all transactions matched
   - Handle remaining differences
   - Generate reconciliation report
   - Confirm reconciliation completion

---

## Reporting and Analytics

### Generating Standard Reports

#### Sales Reports
1. **Navigate to Sales → Reporting**
2. **Select Report Type**:
   - Sales by Product
   - Sales by Customer
   - Sales by Salesperson
   - Sales by Period
3. **Configure Report Parameters**:
   - Date range selection
   - Filter by customer/product
   - Group by categories
   - Choose output format
4. **Generate and Export**:
   - Click "Generate Report"
   - Review report results
   - Export to desired format
   - Save or share report

#### Financial Reports
1. **Navigate to Accounting → Reporting**
2. **Select Financial Statement**:
   - Balance Sheet
   - Income Statement
   - Cash Flow Statement
   - Trial Balance
3. **Set Report Parameters**:
   - Reporting period
   - Comparison periods
   - Currency selection
   - Level of detail
4. **Generate Report**:
   - Run report generation
   - Review calculations
   - Add notes and comments
   - Export or print report

### Creating Custom Reports

#### Using Report Builder
1. **Navigate to Reporting → Report Builder**
2. **Create New Report**:
   - Select data source
   - Choose report type
   - Define report layout
   - Set up calculations

3. **Configure Data Fields**:
   - Select required fields
   - Set up filters
   - Define groupings
   - Create calculated fields

4. **Design Report Layout**:
   - Arrange field positions
   - Set up headers and footers
   - Configure formatting
   - Add charts and graphs

5. **Save and Test**:
   - Save report template
   - Test with sample data
   - Refine as needed
   - Share with other users

### Dashboard Configuration

#### Creating Personal Dashboard
1. **Navigate to Dashboard → My Dashboard**
2. **Add Widgets**:
   - Drag widgets from palette
   - Configure widget parameters
   - Set data filters
   - Arrange layout

3. **Configure KPIs**:
   - Select key performance indicators
   - Set target values
   - Configure alerts
   - Choose display format

4. **Save Dashboard**:
   - Save layout configuration
   - Set as default view
   - Share with team if needed
   - Test functionality

---

## System Administration

### System Configuration

#### General Settings
1. **Navigate to Settings → General Settings**
2. **Configure Company Information**:
   - Company name and address
   - Contact information
   - Tax identification numbers
   - Banking information

3. **System Preferences**:
   - Default language and timezone
   - Date and number formats
   - Email server configuration
   - Security settings

4. **Module Configuration**:
   - Enable/disable modules
   - Configure module-specific settings
   - Set up integrations
   - Configure user access

#### User Management
1. **Navigate to Settings → Users & Companies**
2. **Manage User Accounts**:
   - Create new users
   - Modify existing users
   - Deactivate inactive users
   - Manage access rights

3. **Configure Access Controls**:
   - Set up permission groups
   - Configure record rules
   - Manage company access
   - Set up security policies

### Data Backup and Maintenance

#### System Backup
1. **Navigate to Settings → Technical → Backup**
2. **Configure Backup Settings**:
   - Backup frequency
   - Backup location
   - Retention period
   - Compression options

3. **Execute Backup**:
   - Start backup process
   - Monitor progress
   - Verify completion
   - Test backup integrity

#### System Maintenance
1. **Regular Maintenance Tasks**:
   - Database optimization
   - Log file cleanup
   - Cache clearing
   - Performance monitoring

2. **System Updates**:
   - Check for available updates
   - Review update notes
   - Schedule update installation
   - Test system after update

### Troubleshooting Common Issues

#### Performance Issues
1. **Identify Symptoms**:
   - Slow page loading
   - Long report generation times
   - System freezes
   - Error messages

2. **Diagnostic Steps**:
   - Check internet connection
   - Verify browser compatibility
   - Clear browser cache
   - Check system resources

3. **Resolution Actions**:
   - Restart application
   - Contact IT support
   - Report issue to system administrator
   - Document problem details

#### Data Access Issues
1. **Check User Permissions**:
   - Verify module access
   - Check record-level permissions
   - Confirm company access
   - Review security rules

2. **Resolve Access Problems**:
   - Contact system administrator
   - Request additional permissions
   - Verify user account status
   - Check for system locks

---

## Best Practices Summary

### General Best Practices

1. **Data Quality**
   - Always validate data before entry
   - Use standardized formats and conventions
   - Regularly review and clean data
   - Implement data validation rules

2. **Security**
   - Use strong passwords and change regularly
   - Log out when finished working
   - Report suspicious activities
   - Protect confidential information

3. **Efficiency**
   - Learn keyboard shortcuts
   - Use favorites and quick links
   - Customize workspace for your needs
   - Automate repetitive tasks

4. **Communication**
   - Document processes and procedures
   - Share knowledge with team members
   - Provide feedback for system improvements
   - Participate in training programs

### Module-Specific Tips

#### Sales Module
- Keep customer information up to date
- Follow up on leads promptly
- Use quotation templates for consistency
- Monitor sales metrics regularly

#### Purchase Module
- Maintain good supplier relationships
- Compare prices from multiple suppliers
- Process invoices promptly
- Track supplier performance

#### Inventory Module
- Perform regular cycle counts
- Use FIFO/LIFO consistently
- Monitor stock levels and reorder points
- Implement quality control procedures

#### Accounting Module
- Reconcile accounts regularly
- Review financial reports monthly
- Maintain proper documentation
- Follow accounting standards and regulations

---

## Conclusion

This guide covers the most common tasks performed in UniERP. For additional assistance:

- **Online Help**: Click the "?" icon in any module
- **User Community**: https://community.uslbd.com
- **Video Tutorials**: https://training.uslbd.com
- **Technical Support**: support@uslbd.com

Remember that regular training and continuous learning are key to maximizing the benefits of UniERP for your organization.