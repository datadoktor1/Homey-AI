#!/usr/bin/env python3
"""Push a local script to Homey"""
import sys
import re
from homey_control import HomeyController
from config import HOMEY_IP, HOMEY_API_KEY

if len(sys.argv) < 2:
    print("Usage: python push_script.py <script_name>")
    print("Example: python push_script.py global-timer")
    sys.exit(1)

script_name = sys.argv[1]
filename = f"scripts/{script_name}.js"

try:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print(f"❌ File not found: {filename}")
    sys.exit(1)

# Extract script ID from header
match = re.search(r"// Script ID: ([a-f0-9-]+)", content)
if not match:
    print("❌ No Script ID found in file header")
    sys.exit(1)

script_id = match.group(1)

# Remove header comments to get clean code
lines = content.split("\n")
code_lines = []
in_header = True
for line in lines:
    if in_header and (line.startswith("// Script ID:") or line.startswith("// Name:") or line.strip() == ""):
        continue
    in_header = False
    code_lines.append(line)

code = "\n".join(code_lines)

h = HomeyController(HOMEY_IP, HOMEY_API_KEY)
print(f"Pushing {script_name} to Homey...")
h.update_script(script_id, code)
print(f"✅ Updated {script_name} (ID: {script_id})")

