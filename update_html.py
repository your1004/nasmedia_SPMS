# -*- coding: utf-8 -*-
"""
nasmedia_v6_4.html 데이터 업데이트 스크립트
2026년 1~2월 실적 데이터 + 예측 시나리오(보수/중도/낙관) 반영
"""

html_path = r'C:\D\Claude Code Project\nasmedia_SPMS\nasmedia_v6_4.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("원본 파일 읽기 완료:", len(content), "bytes")
changes = 0

# ── 1. D.mt: 2025 실적 → 2026 실적 (1~2월만 확정) ──────────────────────
old = ('"mt":[53774386897,54214784487,65822521613,62524278208,67372935289,'
       '75138902038,76082557866,75324159045,67977752600,79241878275,'
       '81462174577,134037749830]')
new = '"mt":[71766130554,51725015031,0,0,0,0,0,0,0,0,0,0]'
if old in content:
    content = content.replace(old, new, 1); changes += 1; print("v D.mt 2026 업데이트")
else:
    print("X D.mt 매칭 실패")

# ── 2. D.m24: 2024 데이터 → 2025 실적 (구 D.mt 값) ─────────────────────
old = ('"m24":[51975911490,55209458014,55042137866,66847508294,79880522457,'
       '78331690630,83569068545,83882106893,69590939285,66633961049,'
       '71491466178,102953594045]')
new = ('"m24":[53774386897,54214784487,65822521613,62524278208,67372935289,'
       '75138902038,76082557866,75324159045,67977752600,79241878275,'
       '81462174577,134037749830]')
if old in content:
    content = content.replace(old, new, 1); changes += 1; print("v D.m24 2025 업데이트")
else:
    print("X D.m24 매칭 실패")

# ── 3~7. D.bm 본부별 2026 실적 ──────────────────────────────────────────
bm_replacements = [
    (
        '"광고1본부":[24541597512,27797835275,32219639283,31978432672,33467269042,'
        '34537247070,36036205791,34584713009,31613549733,34209887093,'
        '38899171468,80383570552]',
        '"광고1본부":[42024329024,31277436045,0,0,0,0,0,0,0,0,0,0]',
        '광고1본부'
    ),
    (
        '"광고2본부":[17810372984,16545786531,18883157141,21001030167,22413648082,'
        '25134900489,21435469044,19186688021,21389861001,21715391971,'
        '22256788341,29354316192]',
        '"광고2본부":[17316768845,10031721493,0,0,0,0,0,0,0,0,0,0]',
        '광고2본부'
    ),
    (
        '"광고3본부":[8972755262,6533377453,11254287792,6458724866,8280806267,'
        '11927788548,14790930295,16120602489,10868743400,19170033089,'
        '15493767697,19881767087]',
        '"광고3본부":[8503109945,7677528879,0,0,0,0,0,0,0,0,0,0]',
        '광고3본부'
    ),
    (
        '"미디어본부":[397220162,1387954652,1684622516,1182004212,1169748918,'
        '1414238741,1637569312,2685160773,1568885937,1603150885,'
        '2396826144,2129611961]',
        '"미디어본부":[279850568,0,0,0,0,0,0,0,0,0,0,0]',
        '미디어본부'
    ),
    (
        '"플랫폼사업본부":[2052440976,1949830577,1780814881,1904086292,2041462981,'
        '2124727190,2182383423,2746994752,2536712529,2543415238,'
        '2415620928,2288484038]',
        '"플랫폼사업본부":[3642072172,2738328614,0,0,0,0,0,0,0,0,0,0]',
        '플랫폼사업본부'
    ),
]
for old_s, new_s, name in bm_replacements:
    if old_s in content:
        content = content.replace(old_s, new_s, 1); changes += 1
        print(f"v D.bm {name} 업데이트")
    else:
        print(f"X D.bm {name} 매칭 실패")

# ── 8. TARGET_BM: 2025 목표 → 2026 실제 목표 ────────────────────────────
old_tgt = (
    "const TARGET_BM={\n"
    "  '광고1본부':[280,260,320,300,330,350,360,350,320,350,390,500],\n"
    "  '광고2본부':[150,140,170,180,200,220,200,190,200,210,220,280],\n"
    "  '광고3본부':[80,70,100,80,90,110,130,140,110,170,150,220],\n"
    "  '미디어본부':[5,5,6,6,6,8,8,10,8,10,12,20],\n"
    "  '플랫폼사업본부':[18,17,16,17,18,19,19,22,20,21,20,20]\n"
    "};"
)
new_tgt = (
    "const TARGET_BM={\n"
    "  '광고1본부':[292,294,338,340,355,398,376,378,400,416,435,470],\n"
    "  '광고2본부':[185,183,203,204,213,235,227,223,234,244,254,273],\n"
    "  '광고3본부':[90,91,104,109,115,137,140,159,157,157,162,171],\n"
    "  '미디어본부':[2,2,3,3,3,4,4,5,4,4,5,5],\n"
    "  '플랫폼사업본부':[30,27,35,38,40,42,42,45,42,42,43,52]\n"
    "};"
)
if old_tgt in content:
    content = content.replace(old_tgt, new_tgt, 1); changes += 1; print("v TARGET_BM 업데이트")
else:
    print("X TARGET_BM 매칭 실패")

# ── 9. P: 현재 기간 2025 Q4 12월 → 2026 Q1 2월 ─────────────────────────
old_p = 'const P={year:2025,qtr:4,month:12};'
new_p = 'const P={year:2026,qtr:1,month:2};'
if old_p in content:
    content = content.replace(old_p, new_p, 1); changes += 1; print("v P 기간 업데이트")
else:
    print("X P 매칭 실패")

# ── 10. WD + FORECAST + PIPELINE 삽입 ───────────────────────────────────
old_wd = ('const WD={confirmed:[38.5,42.1,48.2,null],proposed:[98.2,112.4,124.6,null],'
          'prev_c:[33.1,37.2,41.9,45.3],prev_p:[85.4,99.1,110.2,118.5]};')

new_block = (
    'const WD={confirmed:[142.5,168.3,153.7,null],proposed:[285.4,312.8,278.6,null],'
    'prev_c:[125.4,148.7,141.2,155.3],prev_p:[242.1,278.4,265.8,288.5]};\n'
    'const FORECAST=(function(){\n'
    '  var W2=1e8;\n'
    '  var tgtMT=function(i){return Object.values(TARGET_BM).reduce(function(s,a){return s+(a[i]||0);},0)*W2;};\n'
    '  var a0=D.mt[0]||0, a1=D.mt[1]||0;\n'
    '  var tgtFeb=tgtMT(1), tgtMar=tgtMT(2);\n'
    '  var remFeb=Math.max(0,tgtFeb-a1);\n'
    '  var mCons=a1+remFeb*0.80, mMod=a1+remFeb*1.00, mOpt=a1+remFeb*1.20;\n'
    '  var qCons=a0+mCons+tgtMar*0.80;\n'
    '  var qMod=a0+mMod+tgtMar*1.00;\n'
    '  var qOpt=a0+mOpt+tgtMar*1.20;\n'
    '  var bkFc={};\n'
    '  Object.keys(D.bm).forEach(function(bk){\n'
    '    var tgt=TARGET_BM[bk]||[];\n'
    '    var ba0=D.bm[bk][0]||0, ba1=D.bm[bk][1]||0;\n'
    '    var bt1=(tgt[1]||0)*W2, bt2=(tgt[2]||0)*W2;\n'
    '    var brem=Math.max(0,bt1-ba1);\n'
    '    bkFc[bk]={month:{actual:ba1,target:bt1,cons:ba1+brem*0.80,mod:ba1+brem*1.00,opt:ba1+brem*1.20},\n'
    '      qtr:{cons:ba0+(ba1+brem*0.80)+bt2*0.80,mod:ba0+(ba1+brem)+bt2,opt:ba0+(ba1+brem*1.20)+bt2*1.20}};\n'
    '  });\n'
    '  return{month:{actual:a1,target:tgtFeb,cons:mCons,mod:mMod,opt:mOpt},\n'
    '    qtr:{cons:qCons,mod:qMod,opt:qOpt},tgtMar:tgtMar,bm:bkFc};\n'
    '})();\n'
    'const PIPELINE={\n'
    "  'Google':['넥슨','크래프톤','넷마블','문화체육관광부','엘지전자','LG전자(글로벌)','케이티','더블유컨셉코리아','에르메스코리아(유)','국민연금공단'],\n"
    "  'Naver':['넥슨','엘지전자','ELEMENTARYINNOVATIONPTE.LTD.','케이티','크래프톤','월드비전','삼성전자','이엘씨에이','넷마블','국민연금공단'],\n"
    "  'Facebook':['문화체육관광부','넥슨','엘지전자','케이티','더블유컨셉코리아','국민연금공단','넷마블','크래프톤','에르메스코리아(유)','이엘씨에이'],\n"
    "  'kakao':['ELEMENTARYINNOVATIONPTE.LTD.','샤넬 유한회사','넥슨','에르메스코리아(유)','케이티','엘지전자','더블유컨셉코리아','넷마블','이엘씨에이','국민연금공단'],\n"
    "  'NAP':['주식회사 지마켓','쿠팡','REMERGE','넥슨','크래프톤','넷마블','케이티','에스에스지닷컴','카카오','엔씨소프트'],\n"
    "  'Netflix':['넥슨','넥슨게임즈','한샘','크래프톤','케이티','문화체육관광부','이엘씨에이','더블유컨셉코리아','넷마블','에르메스코리아(유)'],\n"
    "  'moloco':['넥슨','크래프톤','넷마블','카카오게임즈','엔씨소프트','컴투스','펄어비스','스마일게이트','위메이드','넥슨게임즈'],\n"
    "  'tiktok':['넥슨','LG전자(글로벌)','더블유컨셉코리아','크래프톤','에르메스코리아(유)','샤넬 유한회사','이엘씨에이','케이티','넷마블','카카오'],\n"
    "  'appier':['넥슨','워시스왓','넷마블','크래프톤','카카오게임즈','쿠팡','에스에스지닷컴','주식회사 지마켓','엔씨소프트','컴투스'],\n"
    "  'apple':['넥슨','넷마블','다이닝브랜즈그룹','크래프톤','카카오게임즈','엔씨소프트','컴투스','펄어비스','스마일게이트','위메이드']\n"
    '};\n'
)
if old_wd in content:
    content = content.replace(old_wd, new_block, 1); changes += 1
    print("v WD+FORECAST+PIPELINE 업데이트")
else:
    print("X WD 매칭 실패")

# ── 11. renderSalesForecast 교체 (섹션 마커 사용) ───────────────────────
FC_START = '// \u2550\u2550\u2550 SALES FORECAST \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550'
FC_END   = '// \u2550\u2550\u2550 SALES NAP'

if FC_START in content and FC_END in content:
    idx_start = content.index(FC_START)
    idx_end   = content.index(FC_END)
    before = content[:idx_start]
    after  = content[idx_end:]

    new_fc = (
        '// \u2550\u2550\u2550 SALES FORECAST \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n'
        'function getSalesStrategy(bk){\n'
        "  var s={\n"
        "    '\uad11\uace01\ub3041\ubcf8\ubd80':'\uae00\ub85c\ubc8c \uac8c\uc784 UA \uc2dc\uc98c\uc131 \ub300\uc751 \ubc0f \uc774\ucee4\uba38\uc2a4 Q1 \ub300\ud615 \uce90\ud398\uc778 \uc870\uae30 \ud074\ub85c\uc9d5. Google/TikTok/Moloco \ud328\ud0a4\uc9c0 \uc81c\uc548\uc73c\ub85c \ucde8\uae09\uace0 \ud655\ub300. \uc0c1\ubc18\uae30 \uc5f0\uac04\uacc4\uc57d \uad11\uace0\uc8fc \ube44\uc911 40% \ubaa9\ud45c.',\n"
        "    '\uad11\uace01\ub3042\ubcf8\ubd80':'\ud328\uc158/\ube37\ud2f0/\uae08\uc735 \uc5c5\uc885 Q1 \uc2e0\uaddc \uad11\uace0\uc8fc \ud655\ubcf4. Meta \ub9b4\uc2a4+NAP ADX \ubcf5\ud569 \uc81c\uc548\uc73c\ub85c \ud37c\ud3ec\uba3c\uc2a4 \uc218\uc775\uc728 \uac1c\uc120. \ub300\ud589\uc0ac \uc9c1\uc811\uad11\uace0\uc8fc \uc804\ud658 \ucd94\uc9c4.',\n"
        "    '\uad11\uace01\ub3043\ubcf8\ubd80':'\uae00\ub85c\ubc8c\uc804\ub7b5\ud300 \ud574\uc678 \uac8c\uc784\uc0ac \uc2e0\uaddc \uc9d1\ud589 \ud655\ub300. DOOH \uc5f0\uac04 \uc2a4\ud3f0\uc11c\uc2ed \uacc4\uc57d 3\uac74 \ubaa9\ud45c. \ubaa8\ubc14\uc77c UA Q1 \uc9d1\uc911 \ud074\ub85c\uc9d5\uc73c\ub85c \ubaa9\ud45c \ub2ec\uc131\ub960 100% \ucd94\uc9c4.',\n"
        "    '\ubbf8\ub514\uc5b4\ubcf8\ubd80':'OOH \ub9e4\uccb4 \uc5f0\uac04 \ud328\ud0a4\uc9c0 \uacc4\uc57d \ud655\ub300. MIC \ub9c8\ucf00\ud305 \ud50c\ub7ab\ud3fc \uc2e0\uaddc \uad11\uace0\uc8fc \ud30c\uc774\ud504\ub77c\uc778 \uad6c\ucd95. \uc774\uc775\uc728 12.5% \uc720\uc9c0.',\n"
        "    '\ud50c\ub7ab\ud3fc\uc0ac\uc5c5\ubcf8\ubd80':'NAP CPS \uc774\ucee4\uba38\uc2a4 \uad11\uace0\uc8fc Q1 \uc9d1\uc911 \ud655\ub300. ADX \ud504\ub9ac\ubbf8\uc5c4 \uc778\ubca4\ud1a0\ub9ac \uc2e0\uaddc \ud37c\ube14\ub9ac\uc154 \uc628\ubcf4\ub529. DSP \ub9ac\ud0c0\uac8c\ud305 \uc218\uc775\uc728 18% \ubaa9\ud45c.'\n"
        "  };\n"
        "  return s[bk]||'\uc794\uc5ec \ubaa9\ud45c \uc9d1\uc911 \ud074\ub85c\uc9d5 \uc804\ub7b5 \uc2e4\ud589.';\n"
        '}\n'
        'function renderSalesForecast(){\n'
        "  var pg=document.getElementById('pg-sales-forecast');if(!pg)return;\n"
        '  var fc=FORECAST;\n'
        '  var fS=function(v){return (v/1e8).toFixed(1)+\'\uc5b5\';};\n'
        '  var pct=function(a,b){return b>0?(a/b*100).toFixed(1)+\'%\':\'\u2013\';};\n'
        '  var tgtArr=TARGET_BM[\'\uad11\uace01\ub3041\ubcf8\ubd80\'].map(function(_,i){\n'
        '    return Object.values(TARGET_BM).reduce(function(s,a){return s+(a[i]||0);},0);\n'
        '  });\n'
        '  var html=periodCtx();\n'
        "  html+='<div class=\"ph\"><div class=\"ph-l\"><h1>\uc608\uce21 &amp; \ubaa9\ud45c\ub2ec\uc131 \uc804\ub7b5</h1>'\n"
        "       +'<div class=\"meta\">'+periodStr()+' \xb7 3\uac00\uc9c0 \uc2dc\ub098\ub9ac\uc624 (\ubcf4\uc218/\uc911\ub3c4/\ub099\uad00)</div></div></div>';\n"
        "  html+='<div class=\"card mb14\" style=\"background:linear-gradient(135deg,#e8f0fe,#fff)\">';\n"
        "  html+='<div class=\"ct\">\ud83d\udcca \uc804\uc0ac '+periodStr()+' \uc608\uce21 \uc2dc\ub098\ub9ac\uc624</div>';\n"
        "  html+='<div class=\"g4\" style=\"margin-top:10px\">';\n"
        "  html+='<div class=\"fc-box\" style=\"border-top:3px solid #d93025\"><div class=\"fc-lbl\">\ud83d\udd34 \ubcf4\uc218 (80%)</div>'\n"
        "       +'<div class=\"fc-val\" style=\"color:#d93025\">'+fS(fc.month.cons)+'</div>'\n"
        "       +'<div style=\"font-size:12px;color:var(--t3)\">\ubaa9\ud45c '+fS(fc.month.target)+' \ub300\ube44 '+pct(fc.month.cons,fc.month.target)+'</div></div>';\n"
        "  html+='<div class=\"fc-box\" style=\"border-top:3px solid #1a73e8\"><div class=\"fc-lbl\">\ud83d\udfe1 \uc911\ub3c4 (100%)</div>'\n"
        "       +'<div class=\"fc-val\" style=\"color:#1a73e8\">'+fS(fc.month.mod)+'</div>'\n"
        "       +'<div style=\"font-size:12px;color:var(--t3)\">\ubaa9\ud45c '+fS(fc.month.target)+' \ub300\ube44 '+pct(fc.month.mod,fc.month.target)+'</div></div>';\n"
        "  html+='<div class=\"fc-box\" style=\"border-top:3px solid #1e8e3e\"><div class=\"fc-lbl\">\ud83d\udfe2 \ub099\uad00 (120%)</div>'\n"
        "       +'<div class=\"fc-val\" style=\"color:#1e8e3e\">'+fS(fc.month.opt)+'</div>'\n"
        "       +'<div style=\"font-size:12px;color:var(--t3)\">\ubaa9\ud45c '+fS(fc.month.target)+' \ub300\ube44 '+pct(fc.month.opt,fc.month.target)+'</div></div>';\n"
        "  html+='<div class=\"fc-box\" style=\"border-top:3px solid #9334e6\"><div class=\"fc-lbl\">\ud83d\udcc5 Q1 \uc911\ub3c4</div>'\n"
        "       +'<div class=\"fc-val\" style=\"color:#9334e6\">'+fS(fc.qtr.mod)+'</div>'\n"
        "       +'<div style=\"font-size:12px;color:var(--t3)\">1~3\uc6d4 \ud569\uacc4 \uc804\ub9dd</div></div>';\n"
        "  html+='</div></div>';\n"
        "  html+='<div class=\"card mb14\"><div class=\"ct\">\ud83d\udcc5 \ub2f9\ubd84\uae30(Q1) \uc6d4\ubcc4 \uc608\uce21 \uc2dc\ub098\ub9ac\uc624</div>';\n"
        "  html+='<div class=\"tw\"><table class=\"t\"><thead><tr><th>\uc6d4</th><th class=\"r\">\ubaa9\ud45c</th>'\n"
        "       +'<th class=\"r\">\uc2e4\uc801</th><th class=\"r\">\ud83d\udd34\ubcf4\uc218</th><th class=\"r\">\ud83d\udfe1\uc911\ub3c4</th><th class=\"r\">\ud83d\udfe2\ub099\uad00</th></tr></thead><tbody>';\n"
        "  html+='<tr><td>1\uc6d4</td><td class=\"r tg\">'+fS(tgtArr[0]*1e8)+'</td>'\n"
        "       +'<td class=\"r hl\">'+fS(D.mt[0])+'</td>'\n"
        "       +'<td class=\"r\" style=\"color:#d93025\">'+fS(D.mt[0])+'</td>'\n"
        "       +'<td class=\"r\" style=\"color:#1a73e8\">'+fS(D.mt[0])+'</td>'\n"
        "       +'<td class=\"r\" style=\"color:#1e8e3e\">'+fS(D.mt[0])+'</td></tr>';\n"
        "  html+='<tr><td>2\uc6d4 (\uc9c4\ud589\uc911)</td><td class=\"r tg\">'+fS(fc.month.target)+'</td>'\n"
        "       +'<td class=\"r hl\">'+fS(fc.month.actual)+'</td>'\n"
        "       +'<td class=\"r\" style=\"color:#d93025\">'+fS(fc.month.cons)+'</td>'\n"
        "       +'<td class=\"r\" style=\"color:#1a73e8\">'+fS(fc.month.mod)+'</td>'\n"
        "       +'<td class=\"r\" style=\"color:#1e8e3e\">'+fS(fc.month.opt)+'</td></tr>';\n"
        "  html+='<tr><td>3\uc6d4 (\uc608\uce21)</td><td class=\"r tg\">'+fS(fc.tgtMar)+'</td>'\n"
        "       +'<td class=\"r tg\">\u2013</td>'\n"
        "       +'<td class=\"r\" style=\"color:#d93025\">'+fS(fc.tgtMar*0.80)+'</td>'\n"
        "       +'<td class=\"r\" style=\"color:#1a73e8\">'+fS(fc.tgtMar*1.00)+'</td>'\n"
        "       +'<td class=\"r\" style=\"color:#1e8e3e\">'+fS(fc.tgtMar*1.20)+'</td></tr>';\n"
        "  html+='</tbody></table></div></div>';\n"
        '  html+=Object.keys(D.bm).map(function(bk){\n'
        '    var bf=fc.bm[bk];if(!bf)return\'\';\n'
        '    var bp=getBonbuPerf(bk);var hc=HEADCOUNT[bk]||1;\n'
        '    var ach=bp.achievement?(bp.achievement*100).toFixed(1)+\'%\':\'\u2013\';\n'
        '    var pc=bp.achievement?Math.min(100,bp.achievement*100).toFixed(0):\'0\';\n'
        '    var cls=bp.achievement>=1?\'g\':bp.achievement>=0.8?\'y\':\'r\';\n'
        '    var pb=bp.achievement?\n'
        '      \'<div class="prog" style="margin-top:8px"><div class="prog-hd"><span>\ub2ec\uc131\ub960 \'+ach+\'</span>\'\n'
        '      +\'<span>\ubaa9\ud45c \'+fS(bf.month.target)+\'</span></div>\'\n'
        '      +\'<div class="prog-bar"><div class="prog-fill \'+cls+\'" style="width:\'+pc+\'%"></div></div></div>\':\'\' ;\n'
        "    return '<div class=\"card mb14\"><div class=\"ct\">'+bk+' \xb7 '+periodStr()+' \uc608\uce21 \uc2dc\ub098\ub9ac\uc624</div>'\n"
        "      +'<div class=\"g5\" style=\"margin-top:8px\">'\n"
        "      +'<div><div class=\"kl\">\uc2e4\uc801</div><div style=\"font-size:18px;font-weight:700;color:var(--blue)\">'+fS(bf.month.actual)+'</div></div>'\n"
        "      +'<div><div class=\"kl\">\ubaa9\ud45c</div><div style=\"font-size:18px;font-weight:700;color:var(--t2)\">'+fS(bf.month.target)+'</div></div>'\n"
        "      +'<div><div class=\"kl\">\ud83d\udd34 \ubcf4\uc218</div><div style=\"font-size:18px;font-weight:700;color:#d93025\">'+fS(bf.month.cons)+'</div></div>'\n"
        "      +'<div><div class=\"kl\">\ud83d\udfe1 \uc911\ub3c4</div><div style=\"font-size:18px;font-weight:700;color:#1a73e8\">'+fS(bf.month.mod)+'</div></div>'\n"
        "      +'<div><div class=\"kl\">\ud83d\udfe2 \ub099\uad00</div><div style=\"font-size:18px;font-weight:700;color:#1e8e3e\">'+fS(bf.month.opt)+'</div></div>'\n"
        "      +'</div>'+pb\n"
        "      +'<div class=\"strat b\" style=\"margin-top:10px\"><div class=\"st-t\">\ud83c\udfaf '+bk+' \ubaa9\ud45c\ub2ec\uc131 \uc601\uc5c5\uc804\ub7b5</div>'\n"
        "      +'<div class=\"st-d\">'+getSalesStrategy(bk)+'</div></div></div>';\n"
        '  }).join(\'\');\n'
        '  pg.innerHTML=html;\n'
        '}\n'
    )
    content = before + new_fc + after
    changes += 1; print("v renderSalesForecast 교체 완료")
else:
    print("X renderSalesForecast 섹션 마커 미발견")
    if FC_START not in content:
        print("  -> FC_START 없음")
    if FC_END not in content:
        print("  -> FC_END 없음")

# ── 12. renderSummary에 예측 카드 삽입 ──────────────────────────────────
SUM_MARKER = ('<div class="abox2"><div class="ax-title">\ud83d\udccb ${periodStr()} '
              '\uc804\uc0ac \uc885\ud569 \uc778\uc0ac\uc774\ud2b8</div>')
if SUM_MARKER in content:
    fc_card = (
        '<div class="card mb14" style="background:linear-gradient(135deg,#e8f0fe,#fff)">'
        '<div class="ct">\ud83d\udd2e \ub2f9\uc6d4 \uc608\uce21 \xb7 \ub2f9\ubd84\uae30(Q1) \uc6d4\ubcc4 \uc608\uce21 (\ubcf4\uc218/\uc911\ub3c4/\ub099\uad00)</div>'
        '<div class="g4" style="margin-top:8px">'
        '<div class="fc-box" style="border-top:3px solid #d93025">'
        '<div class="fc-lbl">\ud83d\udd34 \ubcf4\uc218 (80%)</div>'
        '<div class="fc-val" style="color:#d93025">${fmtB1(FORECAST.month.cons)}</div>'
        '<div style="font-size:11px;color:var(--t3)">\uc794\uc5ec\ubaa9\ud45c 80% \ub2ec\uc131 \uc2dc</div></div>'
        '<div class="fc-box" style="border-top:3px solid #1a73e8">'
        '<div class="fc-lbl">\ud83d\udfe1 \uc911\ub3c4 (100%)</div>'
        '<div class="fc-val" style="color:#1a73e8">${fmtB1(FORECAST.month.mod)}</div>'
        '<div style="font-size:11px;color:var(--t3)">\uc794\uc5ec\ubaa9\ud45c 100% \ub2ec\uc131 \uc2dc</div></div>'
        '<div class="fc-box" style="border-top:3px solid #1e8e3e">'
        '<div class="fc-lbl">\ud83d\udfe2 \ub099\uad00 (120%)</div>'
        '<div class="fc-val" style="color:#1e8e3e">${fmtB1(FORECAST.month.opt)}</div>'
        '<div style="font-size:11px;color:var(--t3)">\uc794\uc5ec\ubaa9\ud45c 120% \ub2ec\uc131 \uc2dc</div></div>'
        '<div class="fc-box" style="border-top:3px solid #9334e6">'
        '<div class="fc-lbl">\ud83d\udcc5 Q1 \uc911\ub3c4</div>'
        '<div class="fc-val" style="color:#9334e6">${fmtB1(FORECAST.qtr.mod)}</div>'
        '<div style="font-size:11px;color:var(--t3)">1~3\uc6d4 \ud569\uacc4 \uc804\ub9dd</div></div>'
        '</div></div>'
        + SUM_MARKER
    )
    content = content.replace(SUM_MARKER, fc_card, 1)
    changes += 1; print("v renderSummary 예측 카드 추가")
else:
    print("X renderSummary 마커 미발견")

# ── 13. 주간 차트 레이블 & 연도 업데이트 ────────────────────────────────
if "const wks=['1\uc8fc','2\uc8fc','3\uc8fc','4\uc8fc'];" in content:
    content = content.replace(
        "const wks=['1\uc8fc','2\uc8fc','3\uc8fc','4\uc8fc'];",
        "const wks=['2\uc6d41\uc8fc','2\uc6d42\uc8fc','2\uc6d43\uc8fc','2\uc6d44\uc8fc'];", 1)
    changes += 1; print("v 주차 레이블 업데이트")

if "label:'2025\ud655\uc815',data:WD.confirmed" in content:
    content = content.replace(
        "label:'2025\ud655\uc815',data:WD.confirmed",
        "label:'2026\ud655\uc815',data:WD.confirmed", 1)
    changes += 1; print("v 차트 2026 레이블")

if "label:'2024\ud655\uc815',data:WD.prev_c" in content:
    content = content.replace(
        "label:'2024\ud655\uc815',data:WD.prev_c",
        "label:'2025\ud655\uc815',data:WD.prev_c", 1)
    changes += 1; print("v 차트 전년도 레이블")

print(f"\n총 {changes}개 변경 완료")

# ── 저장 ────────────────────────────────────────────────────────────────
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"파일 저장 완료: {len(content):,} bytes")

# ── 검증 ────────────────────────────────────────────────────────────────
print("\n=== 검증 결과 ===")
checks = [
    ('D.mt 2026 실적',        '"mt":[71766130554' in content),
    ('D.m24 2025 실적',       '"m24":[53774386897' in content),
    ('D.bm 광고1 2026',       '"광고1본부":[42024329024' in content),
    ('D.bm 광고2 2026',       '"광고2본부":[17316768845' in content),
    ('D.bm 미디어 2026',      '"미디어본부":[279850568' in content),
    ('D.bm 플랫폼 2026',      '"플랫폼사업본부":[3642072172' in content),
    ('TARGET_BM 광고1 292억', "'광고1본부':[292,294" in content),
    ('P year:2026',           'const P={year:2026,qtr:1,month:2}' in content),
    ('WD 2026 weekly',        'confirmed:[142.5,168.3' in content),
    ('FORECAST const',        'const FORECAST=' in content),
    ('PIPELINE const',        'const PIPELINE=' in content),
    ('getSalesStrategy fn',   'function getSalesStrategy' in content),
    ('renderSalesForecast 3-scenario', '보수 (80%)' in content),
    ('renderSummary forecast', 'FORECAST.month.cons' in content),
]
all_ok = True
for name, ok in checks:
    print(f"  {'v' if ok else 'X'} {name}")
    if not ok:
        all_ok = False

if all_ok:
    print("\n모든 검증 통과! HTML 업데이트 완료.")
else:
    print("\n일부 검증 실패. 위 항목 확인 필요.")
