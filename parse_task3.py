# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import re, xml.etree.ElementTree as ET
from collections import defaultdict

xls_path = r'C:\Users\Administrator\Downloads\2026-01~2026-01 취급고_20260128_150943 (2).xls'

print("Reading file...")
with open(xls_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File size: {len(content):,} chars")
print("First 300 chars:", content[:300])

# Strip namespaces
content = re.sub(r' xmlns[^=]*="[^"]*"', '', content)
content = re.sub(r'<(\w+):(\w+)', r'<\2', content)
content = re.sub(r'</(\w+):(\w+)', r'</\2', content)

print("\nParsing XML...")
root = ET.fromstring(content)
print(f"Root tag: {root.tag}")

# Find worksheets
worksheets = root.findall('.//Worksheet')
print(f"Worksheets found: {len(worksheets)}")
for ws in worksheets:
    name = ws.get('Name', '?')
    rows = ws.findall('.//Row')
    print(f"  Sheet '{name}': {len(rows)} rows")

# Process first (main) worksheet
ws = worksheets[0]
rows = ws.findall('.//Row')
print(f"\nProcessing sheet with {len(rows)} rows")

# Parse header row
def get_row_values(row):
    cells = row.findall('.//Cell')
    result = []
    prev_idx = 0
    for cell in cells:
        idx_attr = cell.get('Index')
        if idx_attr:
            idx = int(idx_attr) - 1  # 1-based to 0-based
            while prev_idx < idx:
                result.append(None)
                prev_idx += 1
        data = cell.find('.//Data')
        val = data.text if data is not None else None
        result.append(val)
        prev_idx = len(result)
    return result

header = get_row_values(rows[0])
print(f"\nHeader ({len(header)} cols):")
for i, h in enumerate(header):
    if h:
        print(f"  [{i}] {h}")

