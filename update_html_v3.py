# -*- coding: utf-8 -*-
"""
update_html_v3.py - 실제 데이터(암호해제된 엑셀)로 HTML 업데이트
1. HEADCOUNT 실제값으로 업데이트 (인원명부_260131 기준: 327명)
2. D.m24 실제 2024년 연간 월별 데이터로 업데이트
3. D.m23 추가 (2023년 연간 월별 데이터)
"""
import sys
import io
import re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

html_path = r'C:\D\Claude Code Project\nasmedia_SPMS\nasmedia_v6_4.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"원본 파일 크기: {len(content):,} bytes")
changes = []

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. HEADCOUNT 업데이트 (인원명부_260131 실제값)
#    광고1본부:94, 광고2본부:62, 광고3본부:48,
#    미디어본부:52, 플랫폼사업본부:71 (총 327명)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
old_hc = "const HEADCOUNT={'광고1본부':42,'광고2본부':28,'광고3본부':22,'미디어본부':8,'플랫폼사업본부':12};"
new_hc = "const HEADCOUNT={'광고1본부':94,'광고2본부':62,'광고3본부':48,'미디어본부':52,'플랫폼사업본부':71};"

if old_hc in content:
    content = content.replace(old_hc, new_hc)
    changes.append("✓ HEADCOUNT 업데이트: 112명→327명 (광1:94, 광2:62, 광3:48, 미디어:52, 플랫폼:71)")
else:
    # 변형된 형태도 시도
    m = re.search(r"const HEADCOUNT=\{[^}]+\};", content)
    if m:
        changes.append(f"! HEADCOUNT 현재값: {m.group()[:80]}")
    changes.append("X HEADCOUNT 기존값 미발견 - 수동 확인 필요")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. D.m24 실제 2024년 데이터로 업데이트
#    출처: 나스미디어 2024년 12월 취급고 현황 - 2024년 연간 결산 시트
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
m24_real = [
    51975911489,  # 1월
    55209458013,  # 2월
    55042137865,  # 3월
    66847508293,  # 4월
    79880522457,  # 5월
    78331690630,  # 6월
    83569068544,  # 7월
    83882106893,  # 8월
    69590939285,  # 9월
    66633961049,  # 10월
    71491466177,  # 11월
    102953594044, # 12월
]
# 연간합: 865,408,364,739원 (8,654억)
m24_str = '[' + ','.join(str(v) for v in m24_real) + ']'

m24_pattern = r'"m24":\[[0-9,]+\]'
m24_replacement = f'"m24":{m24_str}'
m24_match = re.search(m24_pattern, content)
if m24_match:
    old_m24_snippet = m24_match.group()[:60]
    content = re.sub(m24_pattern, m24_replacement, content)
    changes.append(f"✓ D.m24 업데이트: 2024년 실제 연간 데이터 (연간합 865,408억)")
    changes.append(f"  이전값: {old_m24_snippet}...")
else:
    changes.append("X D.m24 패턴 미발견")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. D.m23 추가 (2023년 연간 월별 데이터)
#    출처: 나스미디어 2023년 12월 취급고 현황 - 2023년 연간 결산 시트
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
m23_data = [
    55319770652,  # 1월
    54809395621,  # 2월
    62923032345,  # 3월
    60154398212,  # 4월
    70991645444,  # 5월
    67163930100,  # 6월
    71756593170,  # 7월
    71480769313,  # 8월
    68538784099,  # 9월
    70944630365,  # 10월
    78059371084,  # 11월
    94833094557,  # 12월
]
# 연간합: 826,975,414,962원 (8,270억)
m23_str = '[' + ','.join(str(v) for v in m23_data) + ']'

if '"m23":' in content:
    changes.append("○ D.m23 이미 존재 (스킵)")
else:
    # "m24": 앞에 "m23":[...], 삽입
    m23_insert = f'"m23":{m23_str},'
    if '"m24":' in content:
        content = content.replace('"m24":', m23_insert + '"m24":', 1)
        changes.append("✓ D.m23 추가: 2023년 실제 연간 데이터 (연간합 826,975억)")
    else:
        changes.append("X D.m24 기준점 미발견 → m23 삽입 실패")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 결과 출력
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n변경 내역:")
for c in changes:
    print(f"  {c}")

# 저장
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"\n파일 저장 완료: {len(content):,} bytes")

# 검증
print("\n검증:")
hc94 = "'광고1본부':94" in content
hc71 = "'플랫폼사업본부':71" in content
m23_exists = '"m23":' in content
m24_first = str(m24_real[0]) in content  # 51975911489
m24_last  = str(m24_real[11]) in content # 102953594044
m23_first = str(m23_data[0]) in content  # 55319770652
m23_last  = str(m23_data[11]) in content # 94833094557

print(f"  광고1본부:94        → {'O' if hc94 else 'X'}")
print(f"  플랫폼사업본부:71   → {'O' if hc71 else 'X'}")
print(f"  D.m23 존재          → {'O' if m23_exists else 'X'}")
print(f"  D.m24[0]=51975...   → {'O' if m24_first else 'X'}")
print(f"  D.m24[11]=10295...  → {'O' if m24_last else 'X'}")
print(f"  D.m23[0]=55319...   → {'O' if m23_first else 'X'}")
print(f"  D.m23[11]=94833...  → {'O' if m23_last else 'X'}")

all_ok = all([hc94, hc71, m23_exists, m24_first, m24_last, m23_first, m23_last])
print(f"\n{'모든 변경 완료!' if all_ok else '일부 변경 실패 - 위 X 항목 확인'}")
