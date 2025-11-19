#!/usr/bin/env python3
import sys, glob

errors = 0
for manifest_path in glob.glob('addons/**/__manifest__.py', recursive=True):
    try:
        with open(manifest_path, 'r') as f:
            content = f.read()
            manifest = {}
            exec(content, manifest)
        print(f"✅ {manifest_path}: Valid manifest")
    except Exception as e:
        print(f"❌ {manifest_path}: Invalid manifest - {e}")
        errors += 1

if errors:
    sys.exit(1)
