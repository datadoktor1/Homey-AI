#!/usr/bin/env python3
"""Sync scripts FROM Homey to local ./scripts/ folder"""
from homey_control import HomeyController
from config import HOMEY_IP, HOMEY_API_KEY
import os

h = HomeyController(HOMEY_IP, HOMEY_API_KEY)

print("Syncing scripts from Homey...\n")

# Get all script IDs first
scripts_meta = h.get_scripts()

os.makedirs("scripts", exist_ok=True)

count = 0
for script_id, meta in scripts_meta.items():
    name = meta.get("name", "unknown")
    
    # Skip example scripts
    if name.startswith("example-"):
        continue
    
    # Fetch FULL script with code
    script = h.get_script(script_id)
    code = script.get("code", "")
    
    if not code.strip():
        print(f"  ⚠️  {name}: empty")
        continue
    
    # Save locally
    filename = f"scripts/{name}.js"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"// Script ID: {script_id}\n")
        f.write(f"// Name: {name}\n\n")
        f.write(code)
    
    lines = len(code.split("\n"))
    print(f"  ✅ {name}: {lines} lines")
    count += 1

print(f"\n✅ Synced {count} scripts to ./scripts/")

