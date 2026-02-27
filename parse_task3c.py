# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import xml.etree.ElementTree as ET
from collections import defaultdict

xls_path = r'C:\Users\Administrator\Downloads\2026-01~2026-01 취급고_20260128_150943 (2).xls'
ns = 'urn:schemas-microsoft-com:office:spreadsheet'

with open(xls_path, 'r', encoding='utf-8') as f:
    content = f.read()

root = ET.fromstring(content)
ws = root.findall(f'.//{{{ns}}}Worksheet')[0]
rows = ws.findall(f'.//{{{ns}}}Row')

def get_row_values(row):
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

# Row 2 = actual header (row index 1)
header = get_row_values(rows[1])
print(f"Header ({len(header)} cols):")
for i, h in enumerate(header):
    if h is not None:
        print(f"  [{i}] {h}")

# Sample rows 3-5 full width
print("\nSample rows:")
for r_idx in range(2, 6):
    row_vals = get_row_values(rows[r_idx])
    print(f"  Row{r_idx+1} ({len(row_vals)} vals):")
    for i, v in enumerate(row_vals):
        if v is not None:
            print(f"    [{i}]={v[:40] if v else ''}")
            
