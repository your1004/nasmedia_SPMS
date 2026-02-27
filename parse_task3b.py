# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import re, xml.etree.ElementTree as ET
from collections import defaultdict

xls_path = r'C:\Users\Administrator\Downloads\2026-01~2026-01 취급고_20260128_150943 (2).xls'

with open(xls_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Use namespace-aware parsing
root = ET.fromstring(content)
ns = 'urn:schemas-microsoft-com:office:spreadsheet'

worksheets = root.findall(f'.//{{{ns}}}Worksheet')
print(f"Worksheets: {len(worksheets)}")
ws = worksheets[0]
ws_name = ws.get(f'{{{ns}}}Name', '?')
print(f"Sheet name: {ws_name}")

rows = ws.findall(f'.//{{{ns}}}Row')
print(f"Row count: {len(rows)}")

def get_row_values(row, ns):
    cells = row.findall(f'{{{ns}}}Cell')
    result = []
    prev_idx = 0
    for cell in cells:
        idx_attr = cell.get(f'{{{ns}}}Index')
        if idx_attr:
            idx = int(idx_attr) - 1
            while prev_idx < idx:
                result.append(None)
                prev_idx += 1
        data_el = cell.find(f'{{{ns}}}Data')
        val = data_el.text if data_el is not None else None
        result.append(val)
        prev_idx = len(result)
    return result

# Header
header = get_row_values(rows[0], ns)
print(f"\nHeader ({len(header)} cols):")
for i, h in enumerate(header):
    if h is not None:
        print(f"  [{i}] {h}")

# First 3 data rows
print("\nFirst 3 data rows:")
for r_idx in range(1, 4):
    row_vals = get_row_values(rows[r_idx], ns)
    print(f"  Row{r_idx+1} ({len(row_vals)} vals): {row_vals[:15]}")
    
