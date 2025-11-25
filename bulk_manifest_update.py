#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive script to update ALL module manifests with UniERP branding
Scans entire project structure for any __manifest__.py files
"""

import os
import re
import ast
import subprocess
import sys
from pathlib import Path

def update_manifest_file(file_path):
    """Update a single manifest file with UniERP branding"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the Python dictionary
        manifest_dict = ast.literal_eval(content)
        
        # Update author field
        if 'author' in manifest_dict:
            if manifest_dict['author'] in ['Odoo S.A.', 'Odoo SA', 'Odoo']:
                manifest_dict['author'] = 'UniSoft Systems Ltd.'
        
        # Update website field
        if 'website' in manifest_dict:
            if 'odoo.com' in manifest_dict['website'] or 'www.odoo.com' in manifest_dict['website']:
                manifest_dict['website'] = 'https://uslbd.com'
        
        # Write back the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(repr(manifest_dict))
        
        print(f"Updated: {file_path}")
        return True
        
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def test_manifest_file(file_path):
    """Test if a manifest file compiles without errors"""
    try:
        result = subprocess.run(['python', '-m', 'py_compile', file_path], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error testing {file_path}: {e}")
        return False

def find_all_manifests(project_root):
    """Find all __manifest__.py files in the entire project"""
    manifest_files = []
    
    # Convert to Path object for easier path handling
    project_root = Path(project_root)
    
    # Search for all __manifest__.py files recursively
    for manifest_path in project_root.rglob('**/__manifest__.py'):
        if manifest_path.is_file():
            manifest_files.append(str(manifest_path))
            print(f"Found: {manifest_path}")
    
    return manifest_files

def main():
    """Main function to update all manifest files in the project"""
    project_root = '.'  # Current directory
    updated_files = []
    failed_files = []
    test_passed = []
    
    print("🔍 SCANNING FOR ALL MODULE MANIFESTS...")
    print("=" * 60)
    
    # Find all manifest files in the project
    manifest_files = find_all_manifests(project_root)
    
    print(f"\n📊 FOUND {len(manifest_files)} MANIFEST FILES")
    
    if not manifest_files:
        print("❌ No manifest files found in the project!")
        return 1
    
    print("\n🔄 PROCESSING FILES...")
    print("-" * 60)
    
    # Process each manifest file
    for file_path in manifest_files:
        # Update the file
        if update_manifest_file(file_path):
            updated_files.append(file_path)
        else:
            failed_files.append(file_path)
        
        # Test the file
        if test_manifest_file(file_path):
            test_passed.append(file_path)
        else:
            failed_files.append(file_path)
    
    print(f"\n{'='*60}")
    print(f"📋 MANIFEST UPDATE SUMMARY")
    print(f"{'='*60}")
    
    print(f"✅ Files Updated: {len(updated_files)}")
    for file in updated_files:
        print(f"  ✓ {file}")
    
    if failed_files:
        print(f"\n❌ Files Failed to Update: {len(failed_files)}")
        for file in failed_files:
            print(f"  ✗ {file}")
    
    print(f"\n🧪 Files Tested: {len(test_passed)}")
    for file in test_passed:
        print(f"  ✓ {file}")
    
    if failed_files:
        print(f"\n❌ Files Failed to Test: {len([f for f in failed_files if f not in updated_files])}")
        for file in [f for f in failed_files if f not in updated_files]:
            print(f"  ✗ {file}")
    
    print(f"\n{'='*60}")
    
    # Final summary
    total_files = len(manifest_files)
    success_count = len(updated_files)
    success_rate = (success_count / total_files) * 100 if total_files > 0 else 0
    
    print(f"\n📈 FINAL RESULTS:")
    print(f"  Total manifest files found: {total_files}")
    print(f"  Successfully updated: {success_count} ({success_rate:.1f}%)")
    print(f"  Failed to update: {len(failed_files)}")
    print(f"  All files tested: {len(test_passed)}")
    
    # Return appropriate exit code
    return 0 if not failed_files else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)