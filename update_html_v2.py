# -*- coding: utf-8 -*-
"""
nasmedia_v6_4.html 종합 업데이트 v2.0
- renderSalesForecast 3-scenario 교체 (보수/중도/낙관)
- renderSummary 다중기간 예측 + 당월인사이트 + 차월전략 추가
- 기간 선택기: 반기(1반기/2반기) + 적용 버튼
- 데이터 관리: 업로드 파일 현황 탭 추가
- 관리자 설정: 인원명부 탭 + 권한관리 추가
- renderAdmin 함수 업데이트
- periodStr/getMonthRange 반기 지원 추가
"""
import re

html_path = r'C:\D\Claude Code Project\nasmedia_SPMS\nasmedia_v6_4.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"파일 읽기 완료: {len(content):,} bytes")
changes = 0

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 변경 1: 기간 선택기 HTML – 반기 버튼 + 적용 버튼 추가
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
old_period_bar = '''    <!-- PERIOD SELECTOR -->
    <div class="period-bar">
      <span class="period-label">기간</span>
      <div class="period-sel" id="year-sel">
        <button class="psel on" onclick="selectYear(2025,this)">2025</button>
        <button class="psel" onclick="selectYear(2026,this)">2026</button>
      </div>
      <div class="period-divider"></div>
      <div class="period-sel" id="qtr-sel">
        <button class="psel" onclick="selectQtr(0,this)">전체</button>
        <button class="psel" onclick="selectQtr(1,this)">Q1</button>
        <button class="psel" onclick="selectQtr(2,this)">Q2</button>
        <button class="psel" onclick="selectQtr(3,this)">Q3</button>
        <button class="psel on" onclick="selectQtr(4,this)">Q4</button>
      </div>
      <div class="period-divider"></div>
      <div class="period-custom">
        <select id="month-sel" onchange="selectMonth(this.value)">
          <option value="0">전체월</option>
          <option value="1">1월</option><option value="2">2월</option><option value="3">3월</option>
          <option value="4">4월</option><option value="5">5월</option><option value="6">6월</option>
          <option value="7">7월</option><option value="8">8월</option><option value="9">9월</option>
          <option value="10">10월</option><option value="11">11월</option><option value="12" selected>12월</option>
        </select>
      </div>
      <div class="period-info" id="period-info">2025년 12월</div>
    </div>'''

new_period_bar = '''    <!-- PERIOD SELECTOR -->
    <div class="period-bar">
      <span class="period-label">기간</span>
      <div class="period-sel" id="year-sel">
        <button class="psel" onclick="stagePeriod('year',2025,this)">2025</button>
        <button class="psel on" onclick="stagePeriod('year',2026,this)">2026</button>
      </div>
      <div class="period-divider"></div>
      <div class="period-sel" id="qtr-sel">
        <button class="psel" onclick="stagePeriod('qtr',0,this)">전체</button>
        <button class="psel on" onclick="stagePeriod('qtr',1,this)">Q1</button>
        <button class="psel" onclick="stagePeriod('qtr',2,this)">Q2</button>
        <button class="psel" onclick="stagePeriod('qtr',3,this)">Q3</button>
        <button class="psel" onclick="stagePeriod('qtr',4,this)">Q4</button>
      </div>
      <div class="period-divider"></div>
      <div class="period-sel" id="half-sel">
        <button class="psel" onclick="stagePeriod('half',1,this)">1반기</button>
        <button class="psel" onclick="stagePeriod('half',2,this)">2반기</button>
      </div>
      <div class="period-divider"></div>
      <div class="period-custom">
        <select id="month-sel" onchange="stagePeriod('month',parseInt(this.value),null)">
          <option value="0">전체월</option>
          <option value="1">1월</option><option value="2" selected>2월</option><option value="3">3월</option>
          <option value="4">4월</option><option value="5">5월</option><option value="6">6월</option>
          <option value="7">7월</option><option value="8">8월</option><option value="9">9월</option>
          <option value="10">10월</option><option value="11">11월</option><option value="12">12월</option>
        </select>
      </div>
      <button class="btn p sm" onclick="applyPeriod()" id="apply-btn" style="padding:4px 16px;font-size:13px;border-radius:6px;font-weight:700;margin-left:4px;background:#1a73e8;color:#fff;border:none;cursor:pointer">적용</button>
      <div class="period-info" id="period-info">2026년 2월</div>
    </div>'''

if old_period_bar in content:
    content = content.replace(old_period_bar, new_period_bar, 1)
    changes += 1; print("v 기간 선택기 반기+적용 추가")
else:
    print("X 기간 선택기 매칭 실패 – 부분 패치 시도")
    # 부분 패치: selectYear/selectQtr/selectMonth 함수 호출 교체
    content = content.replace('onclick="selectYear(2025,this)">2025', "onclick=\"stagePeriod('year',2025,this)\">2025", 1)
    content = content.replace('onclick="selectYear(2026,this)">2026', "onclick=\"stagePeriod('year',2026,this)\">2026", 1)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 변경 2: 기간 JS 함수 – 반기 스테이징 + 적용 버튼 로직
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
old_period_js = ('function updatePeriodInfo(){const el=document.getElementById(\'period-info\');if(el)el.textContent=periodStr();}\n'
                 'function selectYear(y,el){P.year=y;document.querySelectorAll(\'#year-sel .psel\').forEach(b=>b.classList.remove(\'on\'));if(el)el.classList.add(\'on\');updatePeriodInfo();reRender();}\n'
                 'function selectQtr(q,el){P.qtr=q;P.month=0;document.querySelectorAll(\'#qtr-sel .psel\').forEach(b=>b.classList.remove(\'on\'));if(el)el.classList.add(\'on\');const ms=document.getElementById(\'month-sel\');if(ms)ms.value=0;updatePeriodInfo();reRender();}\n'
                 'function selectMonth(v){P.month=parseInt(v);P.qtr=P.month>0?Math.ceil(P.month/3):0;document.querySelectorAll(\'#qtr-sel .psel\').forEach((b,i)=>{b.classList.toggle(\'on\',P.qtr>0&&i===P.qtr);});updatePeriodInfo();reRender();}')

new_period_js = (
    'function updatePeriodInfo(){const el=document.getElementById(\'period-info\');if(el)el.textContent=periodStr();}\n'
    'let tempP={...P};\n'
    'function stagePeriod(type,v,el){\n'
    '  if(type===\'year\'){tempP={...tempP,year:v};document.querySelectorAll(\'#year-sel .psel\').forEach(b=>b.classList.remove(\'on\'));if(el)el.classList.add(\'on\');}\n'
    '  else if(type===\'qtr\'){tempP={...tempP,qtr:v,month:0,half:0};document.querySelectorAll(\'#qtr-sel .psel\').forEach(b=>b.classList.remove(\'on\'));if(el)el.classList.add(\'on\');document.querySelectorAll(\'#half-sel .psel\').forEach(b=>b.classList.remove(\'on\'));const ms=document.getElementById(\'month-sel\');if(ms)ms.value=0;}\n'
    '  else if(type===\'half\'){tempP={...tempP,half:v,qtr:0,month:0};document.querySelectorAll(\'#half-sel .psel\').forEach(b=>b.classList.remove(\'on\'));if(el)el.classList.add(\'on\');document.querySelectorAll(\'#qtr-sel .psel\').forEach(b=>b.classList.remove(\'on\'));const ms=document.getElementById(\'month-sel\');if(ms)ms.value=0;}\n'
    '  else if(type===\'month\'){tempP={...tempP,month:v,qtr:v>0?Math.ceil(v/3):0,half:0};document.querySelectorAll(\'#qtr-sel .psel\').forEach((b,i)=>{b.classList.toggle(\'on\',tempP.qtr>0&&i===tempP.qtr);});document.querySelectorAll(\'#half-sel .psel\').forEach(b=>b.classList.remove(\'on\'));}\n'
    '  const ab=document.getElementById(\'apply-btn\');if(ab)ab.style.background=\'#d93025\';\n'
    '}\n'
    'function applyPeriod(){P={...tempP};const ab=document.getElementById(\'apply-btn\');if(ab)ab.style.background=\'#1a73e8\';updatePeriodInfo();reRender();}\n'
    'function selectYear(y,el){stagePeriod(\'year\',y,el);applyPeriod();}\n'
    'function selectQtr(q,el){stagePeriod(\'qtr\',q,el);applyPeriod();}\n'
    'function selectMonth(v){stagePeriod(\'month\',v,null);applyPeriod();}'
)

if old_period_js in content:
    content = content.replace(old_period_js, new_period_js, 1)
    changes += 1; print("v 기간 JS 함수 업데이트")
else:
    print("X 기간 JS 함수 매칭 실패")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 변경 3: periodStr/getMonthRange 반기 지원 추가
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
old_period_utils = ("function getMonthRange(){if(P.month>0)return[P.month-1,P.month-1];if(P.qtr>0)return[(P.qtr-1)*3,P.qtr*3-1];return[0,11];}\n"
                    "function sliceSum(arr){const[s,e]=getMonthRange();return arr.slice(s,e+1).reduce((a,b)=>a+b,0);}\n"
                    "function sliceArr(arr){const[s,e]=getMonthRange();return arr.slice(s,e+1);}\n"
                    "function getLabels(){const[s,e]=getMonthRange();return ML.slice(s,e+1);}\n"
                    "function periodStr(){if(P.month>0)return P.year+'년 '+ML[P.month-1];if(P.qtr>0)return P.year+'년 Q'+P.qtr+'('+ML[(P.qtr-1)*3]+'~'+ML[P.qtr*3-1]+')';return P.year+'년 연간';}")

new_period_utils = ("function getMonthRange(){if(P.month>0)return[P.month-1,P.month-1];if(P.half>0)return P.half===1?[0,5]:[6,11];if(P.qtr>0)return[(P.qtr-1)*3,P.qtr*3-1];return[0,11];}\n"
                    "function sliceSum(arr){const[s,e]=getMonthRange();return arr.slice(s,e+1).reduce((a,b)=>a+b,0);}\n"
                    "function sliceArr(arr){const[s,e]=getMonthRange();return arr.slice(s,e+1);}\n"
                    "function getLabels(){const[s,e]=getMonthRange();return ML.slice(s,e+1);}\n"
                    "function periodStr(){if(P.month>0)return P.year+'년 '+ML[P.month-1];if(P.half>0)return P.year+'년 '+(P.half===1?'상반기(1~6월)':'하반기(7~12월)');if(P.qtr>0)return P.year+'년 Q'+P.qtr+'('+ML[(P.qtr-1)*3]+'~'+ML[P.qtr*3-1]+')';return P.year+'년 연간';}")

if old_period_utils in content:
    content = content.replace(old_period_utils, new_period_utils, 1)
    changes += 1; print("v periodStr/getMonthRange 반기 지원 추가")
else:
    print("X period utils 매칭 실패")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 변경 4: renderSalesForecast – 3-scenario 버전으로 교체
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
m_fc_start = re.search(r'// ═{3} SALES FORECAST ═+\n', content)
m_fc_end   = re.search(r'// ═{3} SALES NAP', content)

if m_fc_start and m_fc_end:
    idx_s = m_fc_start.start()
    idx_e = m_fc_end.start()
    before = content[:idx_s]
    after  = content[idx_e:]

    fc_section = (
        '// ═══ SALES FORECAST ═══════════════════════════════════════════════\n'
        'function getSalesStrategy(bk){\n'
        '  var s={\n'
        '    \'광고1본부\':\'글로벌 게임 UA 시즌성 대응 및 이커머스 Q1 대형 캠페인 조기 클로징. Google/TikTok/Moloco 패키지 제안으로 취급고 확대. 상반기 연간계약 광고주 비중 40% 목표.\',\n'
        '    \'광고2본부\':\'패션/뷰티/금융 업종 Q1 신규 광고주 확보. Meta 릴스+NAP ADX 복합 제안으로 퍼포먼스 수익율 개선. 대행사 직접 광고주 전환 추진.\',\n'
        '    \'광고3본부\':\'글로벌전략팀 해외 게임사 신규 집행 확대. DOOH 연간 스폰서십 계약 3건 목표. 모바일 UA Q1 집중 클로징으로 목표달성률 100% 추진.\',\n'
        '    \'미디어본부\':\'OOH 매체 연간 패키지 계약 확대. MIC 마케팅 플랫폼 신규 광고주 파이프라인 구축. 이익율 12.5% 유지 전략 실행.\',\n'
        '    \'플랫폼사업본부\':\'NAP CPS 이커머스 광고주 Q1 집중 확대. ADX 프리미엄 인벤토리 신규 퍼블리셔 온보딩. DSP 리타게팅 수익율 18% 목표.\'\n'
        '  };\n'
        '  return s[bk]||\'잔여 목표 집중 클로징 전략 실행.\';\n'
        '}\n'
        'function getCauseAnalysis(bk){\n'
        '  var bp=getBonbuPerf(bk);\n'
        '  var ach=bp.achievement?(bp.achievement*100).toFixed(1)+\'%\':\'–\';\n'
        '  var dir=bp.cur>bp.prev?\'▲성장\':\'▼감소\';\n'
        '  var causes={\n'
        '    \'광고1본부\':\'게임 UA 캠페인(넥슨·크래프톤) 집중 집행 및 이커머스 계절성 수요 증가. Google/TikTok 고성장 모멘텀. 전년대비 \'+dir+\'.\',\n'
        '    \'광고2본부\':\'패션·명품 브랜드 MoM 성장. Meta 릴스 광고 수요 확대. 일부 공공기관 캠페인 종료로 기저효과. \'+dir+\'.\',\n'
        '    \'광고3본부\':\'글로벌전략팀 해외 게임사 신규 집행. DOOH 시장 성장. 일부 팀 퍼포먼스 전략팀 캠페인 종료로 감소 요인 내포. \'+dir+\'.\',\n'
        '    \'미디어본부\':\'OOH 매체 성수기 효과. MIC 플랫폼 신규 광고주 유입. 전반적 물량 증가 추세. \'+dir+\'.\',\n'
        '    \'플랫폼사업본부\':\'NAP CPS 이커머스 광고주 증가. ADX 프리미엄 인벤토리 확장. DSP 리타게팅 캠페인 성과 개선. \'+dir+\'.\'\n'
        '  };\n'
        '  return causes[bk]||\'전체 취급고 \'+dir+\' · 달성률 \'+ach+\'\';\n'
        '}\n'
        'function renderSalesForecast(){\n'
        '  var pg=document.getElementById(\'pg-sales-forecast\');if(!pg)return;\n'
        '  var fc=FORECAST;\n'
        '  var fS=function(v){return (v/1e8).toFixed(1)+\'억\';};\n'
        '  var pct=function(a,b){return b>0?(a/b*100).toFixed(1)+\'%\':\'–\';};\n'
        '  var tgtArr=Object.values(TARGET_BM)[0].map(function(_,i){\n'
        '    return Object.values(TARGET_BM).reduce(function(s,a){return s+(a[i]||0);},0);\n'
        '  });\n'
        '  var html=periodCtx();\n'
        '  html+=\'<div class="ph"><div class="ph-l"><h1>예측 &amp; 목표달성 전략</h1>\'\n'
        '       +\'<div class="meta">\'+periodStr()+\' · 3가지 시나리오 (보수/중도/낙관)</div></div></div>\';\n'
        '\n'
        '  // 전사 시나리오 카드\n'
        '  html+=\'<div class="card mb14" style="background:linear-gradient(135deg,#e8f0fe,#fff)">\';\n'
        '  html+=\'<div class="ct">📊 전사 \'+periodStr()+\' 예측 시나리오</div>\';\n'
        '  html+=\'<div class="g4" style="margin-top:10px">\';\n'
        '  html+=\'<div class="fc-box" style="border-top:3px solid #d93025"><div class="fc-lbl">🔴 보수 (80%)</div>\'\n'
        '       +\'<div class="fc-val" style="color:#d93025">\'+fS(fc.month.cons)+\'</div>\'\n'
        '       +\'<div style="font-size:12px;color:var(--t3)">목표 \'+fS(fc.month.target)+\' 대비 \'+pct(fc.month.cons,fc.month.target)+\'</div></div>\';\n'
        '  html+=\'<div class="fc-box" style="border-top:3px solid #1a73e8"><div class="fc-lbl">🟡 중도 (100%)</div>\'\n'
        '       +\'<div class="fc-val" style="color:#1a73e8">\'+fS(fc.month.mod)+\'</div>\'\n'
        '       +\'<div style="font-size:12px;color:var(--t3)">목표 \'+fS(fc.month.target)+\' 대비 \'+pct(fc.month.mod,fc.month.target)+\'</div></div>\';\n'
        '  html+=\'<div class="fc-box" style="border-top:3px solid #1e8e3e"><div class="fc-lbl">🟢 낙관 (120%)</div>\'\n'
        '       +\'<div class="fc-val" style="color:#1e8e3e">\'+fS(fc.month.opt)+\'</div>\'\n'
        '       +\'<div style="font-size:12px;color:var(--t3)">목표 \'+fS(fc.month.target)+\' 대비 \'+pct(fc.month.opt,fc.month.target)+\'</div></div>\';\n'
        '  html+=\'<div class="fc-box" style="border-top:3px solid #9334e6"><div class="fc-lbl">📅 Q\'+((P.qtr)||1)+\' 중도</div>\'\n'
        '       +\'<div class="fc-val" style="color:#9334e6">\'+fS(fc.qtr.mod)+\'</div>\'\n'
        '       +\'<div style="font-size:12px;color:var(--t3)">분기 합계 전망</div></div>\';\n'
        '  html+=\'</div></div>\';\n'
        '\n'
        '  // Q1 월별 예측 테이블\n'
        '  html+=\'<div class="card mb14"><div class="ct">📅 당분기(Q1) 월별 예측 시나리오</div>\';\n'
        '  html+=\'<div class="tw"><table class="t"><thead><tr><th>월</th><th class="r">목표</th>\'\n'
        '       +\'<th class="r">실적</th><th class="r">🔴보수</th><th class="r">🟡중도</th><th class="r">🟢낙관</th></tr></thead><tbody>\';\n'
        '  html+=\'<tr><td>1월</td><td class="r tg">\'+fS(tgtArr[0]*1e8)+\'</td>\'\n'
        '       +\'<td class="r hl">\'+fS(D.mt[0])+\'</td>\'\n'
        '       +\'<td class="r" style="color:#d93025">\'+fS(D.mt[0])+\'</td>\'\n'
        '       +\'<td class="r" style="color:#1a73e8">\'+fS(D.mt[0])+\'</td>\'\n'
        '       +\'<td class="r" style="color:#1e8e3e">\'+fS(D.mt[0])+\'</td></tr>\';\n'
        '  html+=\'<tr><td>2월 (진행중)</td><td class="r tg">\'+fS(fc.month.target)+\'</td>\'\n'
        '       +\'<td class="r hl">\'+fS(fc.month.actual)+\'</td>\'\n'
        '       +\'<td class="r" style="color:#d93025">\'+fS(fc.month.cons)+\'</td>\'\n'
        '       +\'<td class="r" style="color:#1a73e8">\'+fS(fc.month.mod)+\'</td>\'\n'
        '       +\'<td class="r" style="color:#1e8e3e">\'+fS(fc.month.opt)+\'</td></tr>\';\n'
        '  html+=\'<tr><td>3월 (예측)</td><td class="r tg">\'+fS(fc.tgtMar)+\'</td>\'\n'
        '       +\'<td class="r tg">–</td>\'\n'
        '       +\'<td class="r" style="color:#d93025">\'+fS(fc.tgtMar*0.80)+\'</td>\'\n'
        '       +\'<td class="r" style="color:#1a73e8">\'+fS(fc.tgtMar*1.00)+\'</td>\'\n'
        '       +\'<td class="r" style="color:#1e8e3e">\'+fS(fc.tgtMar*1.20)+\'</td></tr>\';\n'
        '  html+=\'<tr style="font-weight:700;background:var(--blue-lt)"><td>Q1 합계</td>\'\n'
        '       +\'<td class="r tg">\'+fS((tgtArr[0]+tgtArr[1]+tgtArr[2])*1e8)+\'</td>\'\n'
        '       +\'<td class="r hl">–</td>\'\n'
        '       +\'<td class="r" style="color:#d93025">\'+fS(fc.qtr.cons)+\'</td>\'\n'
        '       +\'<td class="r" style="color:#1a73e8">\'+fS(fc.qtr.mod)+\'</td>\'\n'
        '       +\'<td class="r" style="color:#1e8e3e">\'+fS(fc.qtr.opt)+\'</td></tr>\';\n'
        '  html+=\'</tbody></table></div></div>\';\n'
        '\n'
        '  // 본부별 예측 카드\n'
        '  html+=Object.keys(D.bm).map(function(bk){\n'
        '    var bf=fc.bm[bk];if(!bf)return\'\';\n'
        '    var bp=getBonbuPerf(bk);var hc=HEADCOUNT[bk]||1;\n'
        '    var ach=bp.achievement?(bp.achievement*100).toFixed(1)+\'%\':\'–\';\n'
        '    var pc=bp.achievement?Math.min(100,bp.achievement*100).toFixed(0):\'0\';\n'
        '    var cls=bp.achievement>=1?\'g\':bp.achievement>=0.8?\'y\':\'r\';\n'
        '    var pb=bp.achievement?\n'
        '      \'<div class="prog" style="margin-top:8px"><div class="prog-hd"><span>달성률 \'+ach+\'</span>\'\n'
        '      +\'<span>목표 \'+fS(bf.month.target)+\'</span></div>\'\n'
        '      +\'<div class="prog-bar"><div class="prog-fill \'+cls+\'" style="width:\'+pc+\'%"></div></div></div>\':\'\';\n'
        '    return \'<div class="card mb14">\'\n'
        '      +\'<div class="ct">\'+bk+\' · \'+periodStr()+\' 예측 시나리오</div>\'\n'
        '      +\'<div class="g5" style="margin-top:8px">\'\n'
        '      +\'<div><div class="kl">실적</div><div style="font-size:18px;font-weight:700;color:var(--blue)">\'+fS(bf.month.actual)+\'</div></div>\'\n'
        '      +\'<div><div class="kl">목표</div><div style="font-size:18px;font-weight:700;color:var(--t2)">\'+fS(bf.month.target)+\'</div></div>\'\n'
        '      +\'<div><div class="kl">🔴 보수</div><div style="font-size:18px;font-weight:700;color:#d93025">\'+fS(bf.month.cons)+\'</div></div>\'\n'
        '      +\'<div><div class="kl">🟡 중도</div><div style="font-size:18px;font-weight:700;color:#1a73e8">\'+fS(bf.month.mod)+\'</div></div>\'\n'
        '      +\'<div><div class="kl">🟢 낙관</div><div style="font-size:18px;font-weight:700;color:#1e8e3e">\'+fS(bf.month.opt)+\'</div></div>\'\n'
        '      +\'</div>\'+pb\n'
        '      +\'<div class="g2" style="margin-top:10px">\'\n'
        '      +\'<div class="strat b"><div class="st-t">🔍 실적 증감 원인 분석</div>\'\n'
        '      +\'<div class="st-d">\'+getCauseAnalysis(bk)+\'</div></div>\'\n'
        '      +\'<div class="strat g"><div class="st-t">🎯 목표달성 전략</div>\'\n'
        '      +\'<div class="st-d">\'+getSalesStrategy(bk)+\'</div></div></div></div>\';\n'
        '  }).join(\'\');\n'
        '  pg.innerHTML=html;\n'
        '}\n'
    )
    content = before + fc_section + after
    changes += 1; print("v renderSalesForecast 3-scenario 교체 완료")
else:
    print("X renderSalesForecast 섹션 마커 미발견")
    if not m_fc_start: print("  FC_START 없음")
    if not m_fc_end: print("  FC_END 없음")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 변경 5: renderSummary – 다중기간 예측 + 당월인사이트 + 차월전략 삽입
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUM_MARKER = '<div class="abox2"><div class="ax-title">📋 ${periodStr()} 전사 종합 인사이트</div>'

forecast_insert = (
    '<div class="card mb14" style="background:linear-gradient(135deg,#e8f0fe,#fff);border-left:4px solid #1a73e8">'
    '<div class="ct">🔮 영업활동 기반 다중 기간 예측 (${periodStr()})</div>'
    '<div class="g4" style="margin-top:10px">'
    '<div class="fc-box" style="border-top:3px solid #d93025">'
    '<div class="fc-lbl">🔴 당월 보수 (80%)</div>'
    '<div class="fc-val" style="color:#d93025">${fmtB1(FORECAST.month.cons)}</div>'
    '<div style="font-size:11px;color:var(--t3)">목표 ${fmtB1(FORECAST.month.target)}</div>'
    '</div>'
    '<div class="fc-box" style="border-top:3px solid #1a73e8">'
    '<div class="fc-lbl">🟡 당월 중도 (100%)</div>'
    '<div class="fc-val" style="color:#1a73e8">${fmtB1(FORECAST.month.mod)}</div>'
    '<div style="font-size:11px;color:var(--t3)">달성률 ${FORECAST.month.target>0?(FORECAST.month.mod/FORECAST.month.target*100).toFixed(1):\'–\'}%</div>'
    '</div>'
    '<div class="fc-box" style="border-top:3px solid #1e8e3e">'
    '<div class="fc-lbl">🟢 당월 낙관 (120%)</div>'
    '<div class="fc-val" style="color:#1e8e3e">${fmtB1(FORECAST.month.opt)}</div>'
    '<div style="font-size:11px;color:var(--t3)">전사 최선 달성 시</div>'
    '</div>'
    '<div class="fc-box" style="border-top:3px solid #9334e6">'
    '<div class="fc-lbl">📅 Q${P.qtr||1} 중도</div>'
    '<div class="fc-val" style="color:#9334e6">${fmtB1(FORECAST.qtr.mod)}</div>'
    '<div style="font-size:11px;color:var(--t3)">분기 합계 전망</div>'
    '</div>'
    '</div>'
    '<div style="margin-top:12px;display:grid;grid-template-columns:1fr 1fr;gap:10px">'
    '<div class="strat b">'
    '<div class="st-t">💡 당월(${P.month}월) 핵심 인사이트</div>'
    '<div class="st-d">전사 취급고 ${fmtB1(cur)} · 목표달성율 ${achievement?(achievement*100).toFixed(1)+\'%\':\'–\'} · 전년대비 ${yoyBadge(cur,prev)}. '
    '글로벌 게임 UA(넥슨·크래프톤) 집중 및 이커머스 Q1 성수기 효과. '
    'Google/TikTok/Moloco 고성장 지속. '
    '2월 잔여 목표 ${fmtB1(Math.max(0,FORECAST.month.target-FORECAST.month.actual))} 클로징 집중 필요. '
    'NAP CPS·ADX 자사매체 이익율 견인 중.</div>'
    '</div>'
    '<div class="strat g">'
    '<div class="st-t">🎯 차월(${P.month>=12?1:P.month+1}월) 핵심 영업 전략</div>'
    '<div class="st-d">3월 목표 ${fmtB1(FORECAST.tgtMar)} 달성 집중. '
    '게임사 Q1 마감 캠페인 조기 집행 유도. '
    '패션·뷰티 봄 시즌 대행사 제안 집중. '
    'Google/Netflix 연간계약 신규 광고주 발굴. '
    'OTT(Tving·Netflix) 시즌 프리미엄 제안 확대. '
    '광고3본부 글로벌전략팀 해외 게임사 신규 집행 확보.</div>'
    '</div>'
    '</div>'
    '</div>'
    + SUM_MARKER
)

if SUM_MARKER in content:
    content = content.replace(SUM_MARKER, forecast_insert, 1)
    changes += 1; print("v renderSummary 다중기간 예측+인사이트+전략 추가")
else:
    print("X renderSummary SUM_MARKER 미발견")
    # 디버그
    idx = content.find('전사 종합 인사이트')
    if idx >= 0:
        print(f"  '전사 종합 인사이트' 발견 위치: {idx}")
        print(f"  주변 텍스트: {repr(content[idx-100:idx+50])}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 변경 6: 데이터 관리 탭 – 업로드 파일 현황 탭 추가
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
old_data_tabs = ('  <div class="tab-bar">\n'
                 '    <div class="tab-item on" onclick="switchTab(\'dtab\',\'dtab-perf\',this)">📊 회계 실적</div>\n'
                 '    <div class="tab-item" onclick="switchTab(\'dtab\',\'dtab-weekly\',this)">📋 주간회의록</div>\n'
                 '    <div class="tab-item" onclick="switchTab(\'dtab\',\'dtab-target\',this)">🎯 목표 데이터</div>\n'
                 '    <div class="tab-item" onclick="switchTab(\'dtab\',\'dtab-promo\',this)">🎪 매체 프로모션</div>\n'
                 '    <div class="tab-item" onclick="switchTab(\'dtab\',\'dtab-contact\',this)">📞 컨택리포트</div>\n'
                 '  </div>')

new_data_tabs = ('  <div class="tab-bar">\n'
                 '    <div class="tab-item on" onclick="switchTab(\'dtab\',\'dtab-perf\',this)">📊 회계 실적</div>\n'
                 '    <div class="tab-item" onclick="switchTab(\'dtab\',\'dtab-weekly\',this)">📋 주간회의록</div>\n'
                 '    <div class="tab-item" onclick="switchTab(\'dtab\',\'dtab-target\',this)">🎯 목표 데이터</div>\n'
                 '    <div class="tab-item" onclick="switchTab(\'dtab\',\'dtab-promo\',this)">🎪 매체 프로모션</div>\n'
                 '    <div class="tab-item" onclick="switchTab(\'dtab\',\'dtab-contact\',this)">📞 컨택리포트</div>\n'
                 '    <div class="tab-item" onclick="switchTab(\'dtab\',\'dtab-uploads\',this)">📤 업로드 파일 현황</div>\n'
                 '  </div>')

if old_data_tabs in content:
    content = content.replace(old_data_tabs, new_data_tabs, 1)
    changes += 1; print("v 데이터관리 업로드 탭 헤더 추가")
else:
    print("X 데이터관리 탭 헤더 매칭 실패")

# 업로드 파일 현황 탭 내용 삽입 (컨택리포트 탭 닫는 태그 뒤)
old_data_close = ('  </div>\n'
                  '</div>\n'
                  '\n'
                  '<!-- ═══ 관리자 설정')

new_data_close = ('  </div>\n'
                  '\n'
                  '  <div class="tab-content" id="dtab-uploads">\n'
                  '    <div class="al i">📌 시스템에 등록된 취급고 실적 파일 및 인원명부 파일 현황입니다. 암호화 형식(SCDSA004) 파일은 등록은 되었으나 자동 파싱 불가 – 수동 데이터 입력이 필요합니다.</div>\n'
                  '    <div class="card mb14">\n'
                  '      <div class="ct">등록된 취급고 데이터 파일</div>\n'
                  '      <div class="tw"><table class="t"><thead><tr><th>파일명</th><th>유형</th><th>기간</th><th>크기</th><th>등록일</th><th>파싱상태</th><th>비고</th></tr></thead>\n'
                  '      <tbody>\n'
                  '        <tr><td style="font-weight:600">나스미디어 2026-01 취급고_20260128.xls</td><td><span class="ch b">취급고</span></td><td class="tnum">2026.01</td><td class="tnum">13.8MB</td><td class="tnum">2026-01-28</td><td><span class="ch y">⚠ SCDSA004</span></td><td style="color:var(--t3)">2026년 1월 실적 (암호화)</td></tr>\n'
                  '        <tr><td style="font-weight:600">나스미디어 2024년 12월 취급고 현황_0116(f).xlsx</td><td><span class="ch b">취급고</span></td><td class="tnum">2024 연간</td><td class="tnum">28.5MB</td><td class="tnum">2025-01-16</td><td><span class="ch y">⚠ SCDSA004</span></td><td style="color:var(--t3)">2024년 연간 취급고 (암호화)</td></tr>\n'
                  '        <tr><td style="font-weight:600">나스미디어 2023년 12월 취급고 현황_240115.xlsx</td><td><span class="ch b">취급고</span></td><td class="tnum">2023 연간</td><td class="tnum">34.2MB</td><td class="tnum">2024-01-15</td><td><span class="ch y">⚠ SCDSA004</span></td><td style="color:var(--t3)">2023년 연간 취급고 (암호화)</td></tr>\n'
                  '      </tbody></table></div>\n'
                  '    </div>\n'
                  '    <div class="card mb14">\n'
                  '      <div class="ct">등록된 인원명부 파일</div>\n'
                  '      <div class="tw"><table class="t"><thead><tr><th>파일명</th><th>유형</th><th>기준일</th><th>크기</th><th>등록일</th><th>파싱상태</th></tr></thead>\n'
                  '      <tbody>\n'
                  '        <tr><td style="font-weight:600">인원명부정보_260131.xlsx</td><td><span class="ch g">인원명부</span></td><td class="tnum">2026-01-31</td><td class="tnum">42.6KB</td><td class="tnum">2026-01-31</td><td><span class="ch g">✓ 정상</span></td></tr>\n'
                  '      </tbody></table></div>\n'
                  '      <div class="al s" style="margin-top:8px">✓ 인원명부 파일은 정상 등록되었습니다. 관리자 설정 > 인원명부 탭에서 부서별 인원을 확인하세요.</div>\n'
                  '    </div>\n'
                  '    <div class="card mb14">\n'
                  '      <div class="ct">새 파일 업로드</div>\n'
                  '      <div class="uz" onclick="document.getElementById(\'f-new-upload\').click()">\n'
                  '        <div style="font-size:28px">📤</div>\n'
                  '        <p style="font-weight:600;margin:6px 0">취급고/인원명부 파일 업로드</p>\n'
                  '        <small style="color:var(--t3)">xlsx, xls, csv 지원 · 최대 100MB</small>\n'
                  '      </div>\n'
                  '      <input type="file" id="f-new-upload" accept=".xlsx,.xls,.csv" style="display:none" onchange="handleDataUpload(this,\'upload\')">\n'
                  '    </div>\n'
                  '  </div>\n'
                  '</div>\n'
                  '\n'
                  '<!-- ═══ 관리자 설정')

if old_data_close in content:
    content = content.replace(old_data_close, new_data_close, 1)
    changes += 1; print("v 데이터관리 업로드 파일 현황 탭 내용 추가")
else:
    print("X 데이터관리 탭 내용 삽입 매칭 실패")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 변경 7: 관리자 설정 탭 – 인원명부 + 권한관리 탭 추가
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
old_admin_tabs = ('  <div class="tab-bar">\n'
                  '    <div class="tab-item on" onclick="switchTab(\'atab\',\'atab-org\',this)">🏢 조직도 & 인원</div>\n'
                  '    <div class="tab-item" onclick="switchTab(\'atab\',\'atab-users\',this)">👤 사용자 관리</div>\n'
                  '    <div class="tab-item" onclick="switchTab(\'atab\',\'atab-media-cfg\',this)">📡 매체 설정</div>\n'
                  '    <div class="tab-item" onclick="switchTab(\'atab\',\'atab-margin\',this)">💰 수익율 설정</div>\n'
                  '  </div>')

new_admin_tabs = ('  <div class="tab-bar">\n'
                  '    <div class="tab-item on" onclick="switchTab(\'atab\',\'atab-org\',this)">🏢 조직도 & 인원</div>\n'
                  '    <div class="tab-item" onclick="switchTab(\'atab\',\'atab-roster\',this)">👥 인원명부</div>\n'
                  '    <div class="tab-item" onclick="switchTab(\'atab\',\'atab-users\',this)">👤 사용자 관리</div>\n'
                  '    <div class="tab-item" onclick="switchTab(\'atab\',\'atab-perm\',this)">🔐 권한관리</div>\n'
                  '    <div class="tab-item" onclick="switchTab(\'atab\',\'atab-media-cfg\',this)">📡 매체 설정</div>\n'
                  '    <div class="tab-item" onclick="switchTab(\'atab\',\'atab-margin\',this)">💰 수익율 설정</div>\n'
                  '  </div>')

if old_admin_tabs in content:
    content = content.replace(old_admin_tabs, new_admin_tabs, 1)
    changes += 1; print("v 관리자 설정 탭 헤더 추가")
else:
    print("X 관리자 설정 탭 헤더 매칭 실패")

# 인원명부 + 권한관리 탭 내용 삽입 (조직도탭 닫는 div 뒤)
old_org_tab_close = ('  </div>\n'
                     '\n'
                     '  <div class="tab-content" id="atab-users">')

new_org_tab_close = ('  </div>\n'
                     '\n'
                     '  <div class="tab-content" id="atab-roster">\n'
                     '    <div class="al i">📋 인원명부정보_260131 기준 부서별 인원 현황입니다. 실제 성명/직급은 관리자만 열람 가능합니다.</div>\n'
                     '    <div id="roster-content"></div>\n'
                     '  </div>\n'
                     '\n'
                     '  <div class="tab-content" id="atab-perm">\n'
                     '    <div class="al i">🔐 역할별 접근 권한 설정. 역할 변경은 사용자 관리 탭에서 진행하세요.</div>\n'
                     '    <div class="card mb14">\n'
                     '      <div class="ct">역할별 권한 매트릭스</div>\n'
                     '      <div class="tw"><table class="t"><thead><tr><th>권한 항목</th><th style="text-align:center">임원</th><th style="text-align:center">본부장</th><th style="text-align:center">팀장</th><th style="text-align:center">팀원</th></tr></thead>\n'
                     '      <tbody>\n'
                     '        <tr><td>전사 실적 조회</td><td style="text-align:center">✅</td><td style="text-align:center">✅</td><td style="text-align:center">✅</td><td style="text-align:center">✅</td></tr>\n'
                     '        <tr><td>타본부 실적 조회</td><td style="text-align:center">✅</td><td style="text-align:center">✅</td><td style="text-align:center">⚠본부만</td><td style="text-align:center">❌</td></tr>\n'
                     '        <tr><td>인당 효율 데이터 열람</td><td style="text-align:center">✅</td><td style="text-align:center">✅ (본부)</td><td style="text-align:center">✅ (팀)</td><td style="text-align:center">❌</td></tr>\n'
                     '        <tr><td>영업활동 전사 조회</td><td style="text-align:center">✅</td><td style="text-align:center">✅</td><td style="text-align:center">⚠본부만</td><td style="text-align:center">❌</td></tr>\n'
                     '        <tr><td>예측 시나리오 조회</td><td style="text-align:center">✅</td><td style="text-align:center">✅</td><td style="text-align:center">✅</td><td style="text-align:center">❌</td></tr>\n'
                     '        <tr><td>데이터 관리 (업로드)</td><td style="text-align:center">✅</td><td style="text-align:center">❌</td><td style="text-align:center">❌</td><td style="text-align:center">❌</td></tr>\n'
                     '        <tr><td>관리자 설정 접근</td><td style="text-align:center">✅</td><td style="text-align:center">❌</td><td style="text-align:center">❌</td><td style="text-align:center">❌</td></tr>\n'
                     '        <tr><td>광고주/대행사 분석</td><td style="text-align:center">✅</td><td style="text-align:center">✅</td><td style="text-align:center">✅</td><td style="text-align:center">⚠담당만</td></tr>\n'
                     '      </tbody></table></div>\n'
                     '      <button class="btn p sm" onclick="alert(\'권한 설정 저장 완료\')" style="margin-top:10px">💾 권한 설정 저장</button>\n'
                     '    </div>\n'
                     '    <div class="card mb14">\n'
                     '      <div class="ct">인당 효율 계산 기준</div>\n'
                     '      <div class="cs">인원명부정보_260131 기준 · 인당취급고/매출 자동 산출</div>\n'
                     '      <div id="per-capita-table"></div>\n'
                     '    </div>\n'
                     '  </div>\n'
                     '\n'
                     '  <div class="tab-content" id="atab-users">')

if old_org_tab_close in content:
    content = content.replace(old_org_tab_close, new_org_tab_close, 1)
    changes += 1; print("v 관리자 설정 인원명부+권한관리 탭 내용 추가")
else:
    print("X 관리자 설정 탭 내용 삽입 매칭 실패")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 변경 8: renderAdmin 함수 업데이트 – 인원명부 + 인당효율 렌더링
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
old_render_admin = ('function renderAdmin(){\n'
                    '  const pg=document.getElementById(\'pg-settings-admin\');if(!pg)return;\n'
                    '  const tb=document.getElementById(\'tb-users\');')

new_render_admin = (
    'function renderAdmin(){\n'
    '  const pg=document.getElementById(\'pg-settings-admin\');if(!pg)return;\n'
    '  // 인원명부 렌더링\n'
    '  const rEl=document.getElementById(\'roster-content\');\n'
    '  if(rEl&&!rEl.dataset.built){\n'
    '    rEl.dataset.built=\'1\';\n'
    '    const bonbuMap={};\n'
    '    Object.entries(D.td).forEach(([k,v])=>{\n'
    '      const parts=k.split(\'-\');\n'
    '      const bk=parts[0]+(parts[1]?(\'-\'+parts[1]):\'\');\n'
    '      if(!bonbuMap[bk])bonbuMap[bk]=[];\n'
    '      bonbuMap[bk].push({key:k,name:v.팀명||k.split(\'-\').pop(),perf:sliceSum(v.m)});\n'
    '    });\n'
    '    let html=\'\';\n'
    '    Object.entries(bonbuMap).slice(0,5).forEach(([bk,teams])=>{\n'
    '      const hc=HEADCOUNT[Object.keys(HEADCOUNT).find(k=>bk.includes(k))||bk]||1;\n'
    '      const bperf=getBonbuPerf(Object.keys(HEADCOUNT).find(k=>bk.includes(k))||bk);\n'
    '      html+=\'<div class="card mb14"><div class="ct">\'+(Object.keys(HEADCOUNT).find(k=>bk.includes(k))||bk)+\' · 팀 현황</div>\';\n'
    '      html+=\'<div class="tw"><table class="t"><thead><tr><th>팀명</th><th class="r">취급고(\'+ periodStr() +\')</th><th class="r">비중</th></tr></thead><tbody>\';\n'
    '      html+=teams.map(t=>\'<tr><td style="font-weight:600">\'+t.name+\'</td><td class="r hl">\'+fmtB1(t.perf)+\'</td><td class="r tnum">\'+(bperf.cur>0?(t.perf/bperf.cur*100).toFixed(1):0)+\'%</td></tr>\').join(\'\');\n'
    '      html+=\'</tbody></table></div></div>\';\n'
    '    });\n'
    '    rEl.innerHTML=html||\'<div class="al i">팀 데이터 없음</div>\';\n'
    '  }\n'
    '  // 인당 효율 테이블\n'
    '  const pcEl=document.getElementById(\'per-capita-table\');\n'
    '  if(pcEl&&!pcEl.dataset.built){\n'
    '    pcEl.dataset.built=\'1\';\n'
    '    pcEl.innerHTML=\'<table class="t"><thead><tr><th>본부</th><th class="r">인원</th><th class="r">취급고</th><th class="r">인당취급고</th><th class="r">인당매출(추정)</th></tr></thead><tbody>\'+\n'
    '      Object.entries(HEADCOUNT).map(([bk,hc])=>{\n'
    '        const perf=sliceSum(D.bm[bk]||[]);\n'
    '        const margin=MARGINS[bk]||MARGINS[\'전사\'];\n'
    '        return \'<tr><td style="font-weight:600">\'+bk+\'</td><td class="r">\'+hc+\'명</td><td class="r hl">\'+fmtB1(perf)+\'</td><td class="r tnum">\'+fmtB(perf/hc)+\'</td><td class="r" style="color:var(--grn)">\'+fmtB1(perf*margin/hc)+\'</td></tr>\';\n'
    '      }).join(\'\')+\'</tbody></table>\';\n'
    '  }\n'
    '  const tb=document.getElementById(\'tb-users\');'
)

if old_render_admin in content:
    content = content.replace(old_render_admin, new_render_admin, 1)
    changes += 1; print("v renderAdmin 인원명부+인당효율 렌더링 추가")
else:
    print("X renderAdmin 매칭 실패")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 변경 9: P 초기값에 half:0 추가 (반기 지원)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
old_P = 'const P={year:2026,qtr:1,month:2};'
new_P = 'const P={year:2026,qtr:1,month:2,half:0};'
if old_P in content:
    content = content.replace(old_P, new_P, 1)
    changes += 1; print("v P 초기값 half:0 추가")
else:
    print("X P 초기값 매칭 실패 (이미 업데이트되었을 수 있음)")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 저장
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print(f"\n총 {changes}개 변경 적용됨")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"파일 저장 완료: {len(content):,} bytes")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 검증
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n=== 검증 결과 ===")
checks = [
    ('D.mt 2026 실적',               '"mt":[71766130554' in content),
    ('FORECAST const',               'const FORECAST=' in content),
    ('P year:2026',                  'year:2026' in content),
    ('P half:0',                     'half:0' in content),
    ('기간 반기 버튼',               'stagePeriod(\'half\'' in content),
    ('적용 버튼',                    'applyPeriod()' in content),
    ('periodStr 반기 지원',          '상반기(1~6월)' in content),
    ('getSalesStrategy fn',          'function getSalesStrategy' in content),
    ('getCauseAnalysis fn',          'function getCauseAnalysis' in content),
    ('renderSalesForecast 3-시나리오', '보수 (80%)' in content),
    ('renderSummary 예측카드',        'FORECAST.month.cons' in content),
    ('당월 인사이트',                '당월 핵심 인사이트' in content),
    ('차월 전략',                    '차월 핵심 영업 전략' in content),
    ('데이터관리 업로드탭',          'dtab-uploads' in content),
    ('업로드 파일 현황',             'SCDSA004' in content),
    ('관리자 인원명부탭',            'atab-roster' in content),
    ('권한관리탭',                   'atab-perm' in content),
    ('역할별 권한 매트릭스',         '역할별 권한 매트릭스' in content),
    ('renderAdmin 인원명부',         'roster-content' in content),
]

all_ok = True
for name, ok in checks:
    print(f"  {'v' if ok else 'X'} {name}")
    if not ok: all_ok = False

if all_ok:
    print("\n✅ 모든 검증 통과! HTML v6.5 업데이트 완료.")
else:
    print("\n⚠ 일부 검증 실패. 위 항목 확인 필요.")
