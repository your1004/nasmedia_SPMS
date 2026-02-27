# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import xml.etree.ElementTree as ET
from collections import defaultdict
import json

xls_path = r'C:\Users\Administrator\Downloads\2026-01~2026-01 취급고_20260128_150943 (2).xls'
ns = 'urn:schemas-microsoft-com:office:spreadsheet'

print("Reading XML file...")
with open(xls_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Parsing XML tree...")
root = ET.fromstring(content)
ws = root.findall(f'.//{{{ns}}}Worksheet')[0]
rows = ws.findall(f'.//{{{ns}}}Row')
print(f"Total rows: {len(rows)}")

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

# Col indices (confirmed from header row 2, data starts row 3)
COL_TEAM = 4      # 담당팀
COL_CATEGORY = 6  # 카테고리
COL_ADVERTISER = 7  # 광고주
COL_AGENCY = 10   # 대행사
COL_MEDIA = 11    # 매체
COL_GROSS = 23    # Gross

# Aggregation
total_gross = 0.0
by_team = defaultdict(float)
by_media = defaultdict(float)
by_advertiser = defaultdict(float)
by_category = defaultdict(float)
by_dept = defaultdict(float)

skip_count = 0
data_count = 0

def get_dept(team_name):
    """Derive 본부 from 팀 name"""
    if not team_name:
        return '기타'
    t = str(team_name)
    if '광고1본부' in t or t.startswith('광고1'):
        return '광고1본부'
    if '광고2본부' in t or t.startswith('광고2'):
        return '광고2본부'
    if '광고3본부' in t or t.startswith('광고3'):
        return '광고3본부'
    if '미디어본부' in t or 'MIC' in t or 'OOH매체' in t or '미디어기획' in t:
        return '미디어본부'
    if '플랫폼' in t or '플랫폼사업' in t:
        return '플랫폼사업본부'
    if 'O&P' in t:  # O&P is under 미디어본부
        return '미디어본부'
    return '기타'

# Process data rows (skip row 0=blank, row 1=header)
print("Processing data rows...")
for r_idx in range(2, len(rows)):
    row_vals = get_row_values(rows[r_idx])
    
    # Get Gross value
    gross_raw = row_vals[COL_GROSS] if len(row_vals) > COL_GROSS else None
    if gross_raw is None:
        skip_count += 1
        continue
    
    try:
        gross = float(gross_raw)
    except (ValueError, TypeError):
        skip_count += 1
        continue
    
    if gross == 0:
        skip_count += 1
        continue
    
    team = row_vals[COL_TEAM] if len(row_vals) > COL_TEAM else None
    category = row_vals[COL_CATEGORY] if len(row_vals) > COL_CATEGORY else None
    advertiser = row_vals[COL_ADVERTISER] if len(row_vals) > COL_ADVERTISER else None
    media = row_vals[COL_MEDIA] if len(row_vals) > COL_MEDIA else None
    
    team = str(team) if team else '미분류'
    category = str(category) if category else '미분류'
    advertiser = str(advertiser) if advertiser else '미분류'
    media = str(media) if media else '미분류'
    
    dept = get_dept(team)
    
    total_gross += gross
    by_team[team] += gross
    by_media[media] += gross
    by_advertiser[advertiser] += gross
    by_category[category] += gross
    by_dept[dept] += gross
    data_count += 1

print(f"\nProcessed: {data_count} rows, skipped: {skip_count}")
print(f"\n=== 2026년 1월 취급고 집계 결과 ===")
print(f"Total Gross: {total_gross:,.0f} 원")
print(f"Total Gross (억): {total_gross/1e8:,.2f}억")

print(f"\n[본부별 Gross]")
for k, v in sorted(by_dept.items(), key=lambda x: -x[1]):
    pct = v/total_gross*100
    print(f"  {k}: {v:,.0f} ({pct:.1f}%)")

print(f"\n[담당팀별 Gross (상위 30)]")
for k, v in sorted(by_team.items(), key=lambda x: -x[1])[:30]:
    pct = v/total_gross*100
    print(f"  {k}: {v:,.0f} ({pct:.1f}%)")

print(f"\n[매체별 Gross (상위 30)]")
for k, v in sorted(by_media.items(), key=lambda x: -x[1])[:30]:
    pct = v/total_gross*100
    print(f"  {k}: {v:,.0f} ({pct:.1f}%)")

print(f"\n[카테고리별 Gross]")
for k, v in sorted(by_category.items(), key=lambda x: -x[1]):
    pct = v/total_gross*100
    print(f"  {k}: {v:,.0f} ({pct:.1f}%)")

print(f"\n[광고주별 Gross (상위 20)]")
top20_adv = sorted(by_advertiser.items(), key=lambda x: -x[1])[:20]
for i, (k, v) in enumerate(top20_adv, 1):
    pct = v/total_gross*100
    print(f"  {i}. {k}: {v:,.0f} ({pct:.1f}%)")

# Check all unique team names to verify dept mapping
print(f"\n[전체 팀명 목록 (부서 매핑 확인)]")
for team in sorted(by_team.keys()):
    dept = get_dept(team)
    print(f"  '{team}' -> {dept}")

