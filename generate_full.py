# -*- coding: utf-8 -*-
"""Generate standalone_full.html — complete learning platform with syllabus upload."""

import xml.etree.ElementTree as ET
import json

# Parse data.xml
tree = ET.parse('Online_Learning/static/xml/data.xml')
root = tree.getroot()
ce = root.find('courses')
courses = []
for co in ce.findall('course'):
    courses.append({
        'name': (co.find('name').text or '').strip(),
        'id_num': (co.find('id').text or '').strip(),
        'englishName': (co.find('english_name').text or '').strip(),
        'credit': (co.find('credit').text or '').strip(),
        'creditHour': (co.find('credit_hour').text or '').strip(),
        'optional': (co.find('optional').text or 'n').strip(),
        'semester': (co.find('semester').text or '').strip(),
        'details': (co.find('details').text or '').strip(),
        'teacher': (co.find('teacher').text or '').strip()
    })

prereqs = []
ac = root.find('adv-course')
for item in ac.findall('item'):
    ai = int(item.find('adv').text) - 1
    pi = int(item.find('pre').text) - 1
    if ai < len(courses) and pi < len(courses):
        prereqs.append({'course': courses[ai]['name'], 'prereq': courses[pi]['name']})

# Read existing standalone.html template parts
courses_json = json.dumps(courses, ensure_ascii=False, indent=8)
prereqs_json = json.dumps(prereqs, ensure_ascii=False, indent=8)

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>软件工程在线学习平台</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Microsoft YaHei","PingFang SC","Helvetica Neue",Arial,sans-serif;background:#f5f5f5;color:#333;overflow-x:hidden}

/* Navbar */
.navbar{position:fixed;top:0;left:0;right:0;z-index:1000;background:#fff;box-shadow:0 2px 10px rgba(0,0,0,0.1);display:flex;align-items:center;justify-content:space-between;padding:0 40px;height:60px}
.navbar .brand{font-size:20px;font-weight:bold;color:#6aae7a;text-decoration:none;cursor:pointer}
.navbar .nav-links{display:flex;list-style:none;gap:8px}
.navbar .nav-links li a{text-decoration:none;color:#555;padding:8px 16px;border-radius:4px;font-size:14px;transition:all .3s;cursor:pointer}
.navbar .nav-links li a:hover,.navbar .nav-links li a.active{color:#6aae7a;background:#f0f9f0}

/* Page sections */
.page-section{display:none;padding-top:60px;min-height:100vh}
.page-section.active{display:block}

/* HOME */
#page-home .hero{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;padding:100px 20px 80px;text-align:center}
#page-home .hero h1{font-size:42px;font-weight:900;margin-bottom:16px;letter-spacing:2px}
#page-home .hero p{font-size:18px;opacity:.9;margin-bottom:30px}
#page-home .hero .btn{display:inline-block;padding:12px 28px;margin:0 10px;border-radius:30px;font-size:14px;font-weight:bold;cursor:pointer;transition:all .3s;border:2px solid #fff;color:#fff;background:0 0}
#page-home .hero .btn:hover{background:#fff;color:#667eea}
#page-home .hero .btn.primary{background:#fff;color:#667eea}
#page-home .hero .btn.primary:hover{background:0 0;color:#fff}
#page-home .features{display:flex;justify-content:center;gap:30px;padding:60px 40px;flex-wrap:wrap;max-width:1100px;margin:0 auto}
#page-home .features .card{background:#fff;border-radius:12px;padding:30px;width:300px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,0.08);transition:transform .3s}
#page-home .features .card:hover{transform:translateY(-5px)}
#page-home .features .card .icon{font-size:48px;margin-bottom:16px}
#page-home .features .card h3{font-size:18px;margin-bottom:10px;color:#333}
#page-home .features .card p{font-size:13px;color:#888;line-height:1.6}
#page-home .features .card a{display:inline-block;margin-top:14px;color:#6aae7a;font-weight:bold;font-size:13px;text-decoration:none;cursor:pointer}
#page-home .about{text-align:center;padding:40px 20px 60px;color:#888;font-size:13px}
#page-home .about a{color:#6aae7a}

/* GRAPH PAGE */
#page-graph{text-align:center}
#page-graph .graph-container{position:relative;display:inline-block;margin-top:20px}
.nodes circle{fill:rgba(108,164,108,1);stroke:rgba(255,255,255,1);stroke-width:1.5px}
.links line{stroke:#000}
.nodes circle.inactive{fill:rgba(108,164,108,.3);stroke:rgba(255,255,255,.3)}
.texts text.inactive{display:none}
.links line.inactive{display:none}
#search1 input{padding:0 15px;border:none;z-index:15;position:absolute;top:30px;left:20px;color:#666;width:200px;height:30px;background:#ccc;border-radius:5px;font-size:13px;outline:0}
#search1 input:focus{background:#e0e0e0}
.texts text{font-size:13px;fill:#000}
.texts text:hover{cursor:pointer}
#info{position:absolute;top:160px;left:20px;width:270px;text-align:left;z-index:5}
#info h4{font-size:14px;margin-bottom:6px}
#info p{font-size:13px;color:#666;line-height:1.5}

/* Breathing animation */
@keyframes breathe-cp{0%,100%{fill:#ff4444;stroke:#ff6666;stroke-width:2px;filter:url(#glow-breath);opacity:1}50%{fill:#ff8888;stroke:#ffaaaa;stroke-width:3px;filter:url(#glow-strong);opacity:.85}}
.nodes circle.cp-node{fill:#ff4444;stroke:#ff6666;stroke-width:2px;filter:url(#glow-breath);animation:breathe-cp 1.5s ease-in-out infinite;r:22px}
.nodes circle.pre-node{fill:rgba(108,164,108,.5);stroke:rgba(108,164,108,.6);stroke-width:1px}
.texts text.cp-text{font-size:14px;font-weight:bold;fill:#cc0000;display:block}
.texts text.pre-text{font-size:12px;fill:rgba(80,120,80,.7);display:block}
.links line.cp-edge{stroke:#ff4444;stroke-width:3px;stroke-dasharray:none;opacity:.9;filter:url(#glow-breath)}
.links line.pre-edge{stroke:rgba(108,164,108,.4);stroke-width:1px}

/* Path Planning Panel */
#path-panel{position:absolute;top:100px;left:20px;z-index:10;background:rgba(255,255,255,.95);padding:16px 18px;border-radius:10px;box-shadow:0 4px 20px rgba(0,0,0,.15);width:310px;max-height:75vh;overflow-y:auto;text-align:left}
#path-panel h5{color:#2c3e50;margin-bottom:10px;font-weight:bold;border-bottom:2px solid #5cb85c;padding-bottom:6px;font-size:14px}
#path-panel .subtitle{font-size:11px;color:#999;margin-bottom:10px;display:block}
#path-panel select{width:100%;margin-bottom:8px;font-size:13px;height:34px;border:1px solid #ddd;border-radius:4px;padding:4px}
#path-panel .btn-plan{width:100%;background:#5cb85c;color:#fff;font-weight:bold;font-size:14px;padding:8px;border:none;border-radius:5px;cursor:pointer;transition:background .3s}
#path-panel .btn-plan:hover{background:#449d44}
#path-panel .btn-plan:disabled{background:#ccc;cursor:not-allowed}
#path-panel .btn-clear{width:100%;margin-top:6px;background:0 0;border:1px solid #ddd;color:#888;font-size:12px;padding:6px;border-radius:4px;cursor:pointer}
#path-panel .btn-clear:hover{background:#f5f5f5;color:#555}
#path-loading{display:none;text-align:center;color:#5cb85c;margin:8px 0;font-size:13px}
#path-error{display:none;color:#d9534f;font-size:12px;margin-top:6px}
#path-result{display:none;margin-top:12px;animation:fadeInUp .4s ease-out}
@keyframes fadeInUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
#cp-display{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;padding:10px 12px;border-radius:8px;margin-bottom:10px;font-size:12px;line-height:1.7}
#cp-display .cp-arrow{color:#ffd700;font-weight:bold;margin:0 3px}
#cp-display .cp-label{font-size:10px;opacity:.85;display:block;margin-bottom:3px}
#cp-display .cp-stat{font-size:11px;margin-top:4px;opacity:.9}
#sem-plan .sem-item{background:#f8f9fa;border-left:4px solid #5cb85c;padding:6px 10px;margin-bottom:5px;border-radius:0 5px 5px 0;font-size:12px;transition:all .3s}
#sem-plan .sem-item:hover{background:#e8f5e9;transform:translateX(3px)}
#sem-plan .sem-num{font-weight:bold;color:#5cb85c;font-size:13px}

/* Syllabus Upload Panel */
#syl-panel{position:absolute;top:100px;right:20px;z-index:10;background:rgba(255,255,255,.95);border-radius:10px;box-shadow:0 4px 20px rgba(0,0,0,.15);width:330px;max-height:80vh;overflow-y:auto;text-align:left}
#syl-toggle{padding:14px 16px;cursor:pointer;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;border-radius:10px 10px 0 0;user-select:none}
#syl-toggle h5{margin:0;font-size:14px}
#syl-toggle .chevron{float:right;transition:transform .3s}
#syl-body{padding:14px 16px;display:none}
#syl-body .step{margin-bottom:8px}
#syl-body .step .step-icon{margin-right:4px}
#syl-body .step h6{display:inline;font-size:13px}
#syl-body .step .step-body{margin-top:6px}
#syl-body input[type=file]{width:100%;font-size:12px;margin-bottom:6px}
#syl-body .btn-sm{width:100%;background:#5cb85c;color:#fff;font-weight:bold;font-size:13px;padding:6px;border:none;border-radius:5px;cursor:pointer;transition:background .3s;margin-bottom:4px}
#syl-body .btn-sm:hover{background:#449d44}
#syl-body .btn-sm:disabled{background:#ccc;cursor:not-allowed}
#syl-body .btn-sm.orange{background:#f0ad4e}
#syl-body .btn-sm.orange:hover{background:#ec971f}
#syl-msg{display:none;margin-top:8px;padding:8px;border-radius:4px;font-size:12px}
.syl-table{width:100%;font-size:11px;border-collapse:collapse;margin:6px 0}
.syl-table th{background:#f0f0f0;padding:4px 6px;text-align:left;font-weight:bold;border-bottom:2px solid #ddd}
.syl-table td{padding:3px 6px;border-bottom:1px solid #eee}
.syl-table tr:hover td{background:#f8f8f8}

/* Legend bar */
#path-legend-bar{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,.75);color:#fff;padding:6px 18px;border-radius:20px;font-size:12px;z-index:5;pointer-events:none;display:none}
#path-legend-bar .ldot{display:inline-block;width:10px;height:10px;border-radius:50%;margin:0 3px;vertical-align:middle}
#path-legend-bar .ldot.crit{background:#ff4444;box-shadow:0 0 8px #ff4444;animation:ldBreathe 1.5s ease-in-out infinite}
#path-legend-bar .ldot.pre{background:rgba(108,164,108,.5)}
@keyframes ldBreathe{0%,100%{box-shadow:0 0 4px #ff4444}50%{box-shadow:0 0 16px #ff4444,0 0 24px #ff2222}}

/* LOGIN / REGISTER PAGES */
#page-login,#page-register{display:flex;align-items:center;justify-content:center;min-height:100vh;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%)}
#page-login.active,#page-register.active{display:flex}
.auth-card{background:#fff;border-radius:16px;padding:40px 36px;width:380px;max-width:90%;box-shadow:0 10px 50px rgba(0,0,0,.25)}
.auth-card h2{text-align:center;margin-bottom:24px;color:#333;font-size:24px}
.auth-card .field{margin-bottom:16px}
.auth-card .field label{display:block;font-size:13px;color:#888;margin-bottom:4px}
.auth-card .field input{width:100%;padding:10px 14px;font-size:14px;border:1px solid #ddd;border-radius:8px;outline:0;transition:border .3s}
.auth-card .field input:focus{border-color:#6aae7a}
.auth-card .btn-auth{width:100%;padding:12px;font-size:16px;font-weight:bold;color:#fff;background:#6aae7a;border:none;border-radius:8px;cursor:pointer;transition:background .3s}
.auth-card .btn-auth:hover{background:#5a9e6a}
.auth-card .switch{text-align:center;margin-top:16px;font-size:13px;color:#888}
.auth-card .switch a{color:#6aae7a;cursor:pointer;font-weight:bold}
.auth-card .err-msg{display:none;color:#d9534f;font-size:12px;margin-bottom:12px;text-align:center}

/* SEARCH PAGE */
#page-search{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh}
#page-search.active{display:flex}
#page-search .search-box{text-align:center;width:100%;max-width:600px;padding:0 20px}
#page-search .search-box h2{color:#fff;font-size:32px;margin-bottom:30px;font-weight:300;letter-spacing:2px}
#page-search .s-bar{display:flex;width:100%}
#page-search .s-bar input{flex:1;padding:14px 20px;font-size:16px;border:none;border-radius:30px 0 0 30px;outline:0;background:rgba(255,255,255,.9);color:#333}
#page-search .s-bar button{padding:14px 28px;font-size:16px;border:none;border-radius:0 30px 30px 0;background:#5cb85c;color:#fff;cursor:pointer;font-weight:bold}
#page-search .s-bar button:hover{background:#449d44}
#page-search .answer{margin-top:30px;color:#fff;font-size:16px;line-height:1.8;min-height:30px;text-align:center;max-width:500px}
#page-search .copyright{position:absolute;bottom:20px;color:rgba(255,255,255,.5);font-size:12px}
#page-search .copyright a{color:#5cb85c;text-decoration:none}

/* API Key modal */
.modal-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);z-index:9999;justify-content:center;align-items:center}
.modal-overlay.active{display:flex}
.modal-box{background:#fff;border-radius:12px;padding:24px;max-width:420px;width:90%;box-shadow:0 10px 40px rgba(0,0,0,.3)}
.modal-box h3{margin-bottom:12px}
.modal-box input{width:100%;padding:10px;font-size:14px;border:1px solid #ddd;border-radius:6px;margin-bottom:12px}
.modal-box .modal-btns{display:flex;gap:10px;justify-content:flex-end}
.modal-box .modal-btns button{padding:8px 20px;border-radius:6px;cursor:pointer;font-size:14px}
.modal-box .modal-btns .btn-ok{background:#5cb85c;color:#fff;border:none}
.modal-box .modal-btns .btn-cancel{background:#eee;border:1px solid #ddd}
.modal-box .hint{font-size:11px;color:#999;margin-bottom:12px}

@media(max-width:768px){.navbar{padding:0 15px}.navbar .brand{font-size:16px}#page-home .hero h1{font-size:28px}#page-home .features{flex-direction:column;align-items:center}#page-home .features .card{width:100%;max-width:350px}}
</style>
</head>
<body>

<nav class="navbar">
<a class="brand" onclick="showPage('page-home')">📚 软件工程在线学习平台</a>
<ul class="nav-links">
<li><a onclick="showPage('page-home')" id="nav-home" class="active">首页</a></li>
<li><a onclick="showPage('page-graph')" id="nav-graph">知识图谱</a></li>
<li><a onclick="showPage('page-search')" id="nav-search">智能搜索</a></li>
<li id="nav-login-item"><a onclick="showPage('page-login')" id="nav-login">登录</a></li>
<li id="nav-register-item"><a onclick="showPage('page-register')" id="nav-register">注册</a></li>
<li id="nav-user-item" style="display:none"><a id="nav-user" style="color:#6aae7a;font-weight:bold"></a></li>
<li id="nav-logout-item" style="display:none"><a onclick="logout()" id="nav-logout" style="color:#d9534f">退出</a></li>
</ul>
</nav>

<!-- ===== HOME PAGE ===== -->
<section class="page-section active" id="page-home">
<div class="hero">
<h1>软件工程在线学习平台</h1>
<p>基于知识图谱的智能学习路径规划系统 · 支持多格式大纲动态入库</p>
<button class="btn primary" onclick="showPage('page-graph')">📊 浏览知识图谱</button>
<button class="btn" onclick="showPage('page-search')">🔍 开始搜索课程</button>
</div>
<div class="features">
<div class="card"><div class="icon">🗺️</div><h3>知识图谱</h3><p>可视化展示 ''' + str(len(courses)) + r''' 门软件工程专业课程的先修依赖关系</p><a onclick="showPage('page-graph')">立即探索 -&gt;</a></div>
<div class="card"><div class="icon">📐</div><h3>学习路径规划</h3><p>基于拓扑排序算法，自动计算最优学习路径与学期规划</p><a onclick="showPage('page-graph')">开始规划 →</a></div>
<div class="card"><div class="icon">📤</div><h3>大纲动态入库</h3><p>上传教学大纲(HTML/DOCX/PDF/TXT)，AI自动解析课程依赖并检测逻辑循环</p><a onclick="showPage('page-graph')">上传大纲 →</a></div>
</div>
<div class="about"><p>© 2022 <a href="https://sse.bupt.edu.cn/" target="_blank">新工科U+平台</a></p></div>
</section>

<!-- ===== API Key Modal ===== -->
<div class="modal-overlay" id="api-modal">
<div class="modal-box">
<h3>🔑 设置 DeepSeek API Key</h3>
<p class="hint">用于AI智能解析大纲（可选）。不设置将使用正则解析。<br>获取 Key: <a href="https://platform.deepseek.com/api_keys" target="_blank">platform.deepseek.com</a></p>
<input type="password" id="api-key-input" placeholder="sk-...">
<div style="font-size:12px;margin-bottom:12px">
<input type="checkbox" id="api-save-check"> 记住到本地 (localStorage)
</div>
<div class="modal-btns">
<button class="btn-cancel" onclick="closeApiModal()">跳过</button>
<button class="btn-ok" onclick="saveApiKey()">保存</button>
</div>
</div>
</div>

<!-- ===== GRAPH PAGE ===== -->
<section class="page-section" id="page-graph">
<div class="graph-container">
<svg width="1000" height="560" id="svg1">
<defs>
<filter id="glow-breath" x="-50%" y="-50%" width="200%" height="200%">
<feGaussianBlur in="SourceGraphic" stdDeviation="3" result="b1"/>
<feGaussianBlur in="SourceGraphic" stdDeviation="8" result="b2"/>
<feMerge><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="glow-strong" x="-50%" y="-50%" width="200%" height="200%">
<feGaussianBlur in="SourceGraphic" stdDeviation="4" result="b1"/>
<feGaussianBlur in="SourceGraphic" stdDeviation="12" result="b2"/>
<feMerge><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
</defs>
</svg>

<div id="search1"><input type="text" placeholder="输入关键词过滤节点"></div>
<div id="info"><h4></h4></div>

<!-- Path Planning Panel -->
<div id="path-panel">
<h5>🗺️ 智能学习路径规划</h5>
<span class="subtitle">选择目标课程，自动计算最优先修路径</span>
<select id="target-course-select"><option value="">-- 加载中... --</option></select>
<button id="btn-plan" class="btn-plan" onclick="planPath()">🚀 规划最优路径</button>
<button class="btn-clear" onclick="clearPath()">🔄 清除高亮</button>
<div id="path-loading">⏳ 正在计算最优路径...</div>
<div id="path-error"></div>
<div id="path-result">
<div id="cp-display"><span class="cp-label">⚡ 关键学习路径</span><span id="cp-text"></span><div class="cp-stat" id="cp-stat"></div></div>
<div id="sem-plan"></div>
</div>
</div>

<!-- Syllabus Upload Panel -->
<div id="syl-panel">
<div id="syl-toggle" onclick="toggleSylPanel()">
<h5>📤 大纲动态入库 <span class="chevron">▼</span></h5>
</div>
<div id="syl-body">
<div class="step">
<span class="step-icon">⏳</span><h6>Step 1: 选择大纲文件</h6>
<div class="step-body">
<input type="file" id="syl-file-input" accept=".html,.htm,.docx,.pdf,.txt">
<button class="btn-sm" onclick="sylUpload()">📎 上传并提取文本</button>
<div id="syl-preview" style="display:none;max-height:100px;overflow-y:auto;font-size:11px;background:#f8f8f8;padding:8px;border-radius:4px;margin-top:6px;white-space:pre-wrap"></div>
</div>
</div>
<div class="step" id="syl-step2" style="display:none">
<span class="step-icon" id="syl-s2-icon">⏳</span><h6>Step 2: 智能解析</h6>
<div class="step-body">
<button class="btn-sm orange" onclick="sylAnalyze()">🤖 解析课程信息</button>
<div id="syl-step2-result" style="display:none;margin-top:8px"></div>
</div>
</div>
<div class="step" id="syl-step3" style="display:none">
<span class="step-icon" id="syl-s3-icon">⏳</span><h6>Step 3: 确认入库</h6>
<div class="step-body">
<button class="btn-sm" onclick="sylImport()">💾 导入知识图谱</button>
</div>
</div>
<div id="syl-msg"></div>
</div>
</div>

<!-- Legend bar -->
<div id="path-legend-bar">
<span class="ldot crit"></span> 最优路径节点 <span style="margin:0 10px">|</span>
<span class="ldot pre"></span> 相关先修课 <span style="margin:0 10px">|</span>
其余课程已隐藏
</div>
</div>
</section>

<!-- ===== LOGIN PAGE ===== -->
<section class="page-section" id="page-login">
<div class="auth-card">
<h2>🔐 用户登录</h2>
<div class="err-msg" id="login-err"></div>
<div class="field"><label>用户名</label><input type="text" id="login-username" placeholder="请输入用户名"></div>
<div class="field"><label>密码</label><input type="password" id="login-password" placeholder="请输入密码"></div>
<button class="btn-auth" onclick="doLogin()">登 录</button>
<div class="switch">还没有账号？<a onclick="showPage('page-register')">立即注册</a></div>
<div class="switch"><a onclick="showPage('page-home')">返回首页</a></div>
</div>
</section>

<!-- ===== REGISTER PAGE ===== -->
<section class="page-section" id="page-register">
<div class="auth-card">
<h2>📝 用户注册</h2>
<div class="err-msg" id="register-err"></div>
<div class="field"><label>用户名</label><input type="text" id="register-username" placeholder="请输入用户名（至少3位）"></div>
<div class="field"><label>密码</label><input type="password" id="register-password" placeholder="请输入密码（至少4位）"></div>
<div class="field"><label>确认密码</label><input type="password" id="register-password2" placeholder="请再次输入密码"></div>
<button class="btn-auth" onclick="doRegister()">注 册</button>
<div class="switch">已有账号？<a onclick="showPage('page-login')">立即登录</a></div>
<div class="switch"><a onclick="showPage('page-home')">返回首页</a></div>
</div>
</section>

<!-- ===== SEARCH PAGE ===== -->
<section class="page-section" id="page-search">
<div class="search-box">
<h2>🔍 智能课程搜索</h2>
<div class="s-bar">
<input id="question" type="text" placeholder="输入问题，如：算法与数据结构是什么 / 操作系统原理的学分">
<button onclick="doSearch()">搜索</button>
</div>
<div class="answer" id="answer"></div>
</div>
<div class="copyright"><p>© 2022 <a href="https://sse.bupt.edu.cn/" target="_blank">新工科U+平台</a></p></div>
</section>

<script src="https://d3js.org/d3.v7.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/mammoth@1.8.0/mammoth.browser.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js" defer></script>
<script>
// ═══════════════════════════════════════════════════════════════════
// DATA
// ═══════════════════════════════════════════════════════════════════
const COURSES = ''' + courses_json + r''';
const PREREQUISITES = ''' + prereqs_json + r''';

// Dynamic storage for imported courses (survives imports)
var _dynamicCourses = [];
var _dynamicPrereqs = [];

function getAllCourses() { return COURSES.concat(_dynamicCourses); }
function getAllPrereqs() { return PREREQUISITES.concat(_dynamicPrereqs); }

// ═══════════════════════════════════════════════════════════════════
// API KEY MANAGEMENT
// ═══════════════════════════════════════════════════════════════════
var _apiKey = '';
try { _apiKey = localStorage.getItem('ds_api_key') || ''; } catch(e) {}

function promptApiKey(callback) {
    if (_apiKey) { callback(_apiKey); return; }
    document.getElementById('api-modal').classList.add('active');
    document.getElementById('api-key-input').focus();
    window._apiCallback = callback;
}
function saveApiKey() {
    var key = document.getElementById('api-key-input').value.trim();
    if (key) {
        _apiKey = key;
        if (document.getElementById('api-save-check').checked) {
            try { localStorage.setItem('ds_api_key', key); } catch(e) {}
        }
    }
    document.getElementById('api-modal').classList.remove('active');
    if (window._apiCallback) { window._apiCallback(_apiKey); window._apiCallback = null; }
}
function closeApiModal() {
    document.getElementById('api-modal').classList.remove('active');
    if (window._apiCallback) { window._apiCallback(''); window._apiCallback = null; }
}

// ═══════════════════════════════════════════════════════════════════
// AUTH (localStorage-based)
// ═══════════════════════════════════════════════════════════════════
var _currentUser = null;
try { _currentUser = localStorage.getItem('lp_user'); } catch(e) {}

function refreshNav() {
    var loggedIn = !!_currentUser;
    var loginItem = document.getElementById('nav-login-item');
    var regItem = document.getElementById('nav-register-item');
    var userItem = document.getElementById('nav-user-item');
    var logoutItem = document.getElementById('nav-logout-item');
    if (loginItem) loginItem.style.display = loggedIn ? 'none' : '';
    if (regItem) regItem.style.display = loggedIn ? 'none' : '';
    if (userItem) userItem.style.display = loggedIn ? '' : 'none';
    if (logoutItem) logoutItem.style.display = loggedIn ? '' : 'none';
    if (loggedIn) {
        var userEl = document.getElementById('nav-user');
        if (userEl) userEl.textContent = '\u{1F464} ' + _currentUser;
    }
}

function getUsers() {
    try { return JSON.parse(localStorage.getItem('lp_users') || '{}'); } catch(e) { return {}; }
}

function doRegister() {
    var errEl = document.getElementById('register-err');
    var uEl = document.getElementById('register-username');
    var pEl = document.getElementById('register-password');
    var p2El = document.getElementById('register-password2');
    if (!uEl || !pEl || !p2El || !errEl) { alert('页面加载异常，请刷新重试'); return; }

    var u = uEl.value.trim();
    var p = pEl.value;
    var p2 = p2El.value;

    if (!u || u.length < 3) { errEl.textContent = '用户名至少3位'; errEl.style.display = 'block'; return; }
    if (!p || p.length < 4) { errEl.textContent = '密码至少4位'; errEl.style.display = 'block'; return; }
    if (p !== p2) { errEl.textContent = '两次密码不一致'; errEl.style.display = 'block'; return; }

    var users = getUsers();
    if (users[u]) { errEl.textContent = '用户名已存在'; errEl.style.display = 'block'; return; }

    users[u] = { password: p, createdAt: new Date().toISOString() };
    try { localStorage.setItem('lp_users', JSON.stringify(users)); } catch(e) {}
    _currentUser = u;
    try { localStorage.setItem('lp_user', u); } catch(e) {}
    errEl.style.display = 'none';
    refreshNav();
    showPage('page-home');
}

function doLogin() {
    var errEl = document.getElementById('login-err');
    var uEl = document.getElementById('login-username');
    var pEl = document.getElementById('login-password');
    if (!uEl || !pEl || !errEl) { alert('页面加载异常，请刷新重试'); return; }

    var u = uEl.value.trim();
    var p = pEl.value;

    if (!u || !p) { errEl.textContent = '请输入用户名和密码'; errEl.style.display = 'block'; return; }

    var users = getUsers();
    if (!users[u]) { errEl.textContent = '用户不存在，请先注册'; errEl.style.display = 'block'; return; }
    if (users[u].password !== p) { errEl.textContent = '密码错误'; errEl.style.display = 'block'; return; }

    _currentUser = u;
    try { localStorage.setItem('lp_user', u); } catch(e) {}
    errEl.style.display = 'none';
    uEl.value = '';
    pEl.value = '';
    refreshNav();
    showPage('page-home');
}

function logout() {
    _currentUser = null;
    try { localStorage.removeItem('lp_user'); } catch(e) {}
    refreshNav();
    showPage('page-home');
}

// Initialize auth on load
(function initAuth() {
    refreshNav();
    var lp = document.getElementById('login-password');
    var rp2 = document.getElementById('register-password2');
    var lu = document.getElementById('login-username');
    if (lp) lp.addEventListener('keydown', function(e) { if (e.key === 'Enter') doLogin(); });
    if (lu) lu.addEventListener('keydown', function(e) { if (e.key === 'Enter') doLogin(); });
    if (rp2) rp2.addEventListener('keydown', function(e) { if (e.key === 'Enter') doRegister(); });
})();

// ═══════════════════════════════════════════════════════════════════
// PAGE NAVIGATION
// ═══════════════════════════════════════════════════════════════════
function showPage(pageId) {
    // Auth guard: graph and search require login
    if ((pageId === 'page-graph' || pageId === 'page-search') && !_currentUser) {
        var le = document.getElementById('login-err');
        if (le) { le.textContent = '请先登录后再访问'; le.style.display = 'block'; }
        pageId = 'page-login';
    }

    var sections = document.querySelectorAll('.page-section');
    for (var i = 0; i < sections.length; i++) { sections[i].classList.remove('active'); }
    var target = document.getElementById(pageId);
    if (target) target.classList.add('active');

    var links = document.querySelectorAll('.nav-links a');
    for (var j = 0; j < links.length; j++) { links[j].classList.remove('active'); }
    var navId = 'nav-' + pageId.replace('page-', '');
    var navEl = document.getElementById(navId);
    if (navEl) navEl.classList.add('active');

    if (pageId === 'page-graph' && !window._graphInited) { initGraph(); window._graphInited = true; }

    // Clear login error on page switch
    var loginErr = document.getElementById('login-err');
    if (loginErr && pageId !== 'page-login') loginErr.style.display = 'none';
}

// ═══════════════════════════════════════════════════════════════════
// SYLLABUS UPLOAD ENGINE
// ═══════════════════════════════════════════════════════════════════
var _sylTextFull = '';
var _sylParsed = null;

function toggleSylPanel() {
    var body = document.getElementById('syl-body');
    var chev = document.querySelector('#syl-toggle .chevron');
    if (body.style.display === 'none' || !body.style.display) {
        body.style.display = 'block';
        chev.textContent = '▲';
    } else {
        body.style.display = 'none';
        chev.textContent = '▼';
    }
}

function sylShowMsg(msg, type) {
    var el = document.getElementById('syl-msg');
    var colors = {info:'#31708f',ok:'#3c763d',warn:'#8a6d3b',err:'#a94442'};
    var bgs = {info:'#d9edf7',ok:'#dff0d8',warn:'#fcf8e3',err:'#f2dede'};
    el.textContent = msg;
    el.style.color = colors[type]||'#333';
    el.style.background = bgs[type]||'#f5f5f5';
    el.style.display = 'block';
    setTimeout(function(){el.style.display='none'},6000);
}

function sylSetIcon(step, state) {
    var icons = {wait:'⏳',loading:'⏳',done:'✅',error:'❌'};
    var el = document.getElementById('syl-s'+step+'-icon');
    if (el) el.textContent = icons[state]||icons.wait;
}

// Step 1: Upload & extract text
function sylUpload() {
    var fileInput = document.getElementById('syl-file-input');
    var file = fileInput.files[0];
    if (!file) { sylShowMsg('请先选择文件','warn'); return; }

    var ext = file.name.split('.').pop().toLowerCase();
    if (['html','htm','docx','pdf','txt'].indexOf(ext)===-1) {
        sylShowMsg('不支持 .'+ext+' 格式，请上传 html/docx/pdf/txt','err'); return;
    }

    sylSetIcon(1,'loading');
    sylShowMsg('正在提取文本...','info');

    var reader = new FileReader();
    reader.onload = function(e) {
        var bytes = new Uint8Array(e.target.result);

        if (ext === 'txt') {
            _sylTextFull = new TextDecoder('utf-8').decode(bytes);
            _onTextReady(file.name, _sylTextFull);
        } else if (ext === 'html' || ext === 'htm') {
            _sylTextFull = new TextDecoder('utf-8').decode(bytes);
            // Strip HTML tags using DOMParser
            var doc = new DOMParser().parseFromString(_sylTextFull, 'text/html');
            var scripts = doc.querySelectorAll('script,style,meta,link');
            scripts.forEach(function(s){s.remove()});
            _sylTextFull = (doc.body?doc.body.textContent:doc.documentElement.textContent)||_sylTextFull;
            _sylTextFull = _sylTextFull.replace(/\n{3,}/g,'\n\n').trim();
            _onTextReady(file.name, _sylTextFull);
        } else if (ext === 'docx') {
            if (typeof mammoth === 'undefined') {
                sylShowMsg('mammoth.js 未加载，请检查网络','err'); return;
            }
            mammoth.extractRawText({arrayBuffer: bytes.buffer})
                .then(function(result){ _sylTextFull = result.value; _onTextReady(file.name, _sylTextFull); })
                .catch(function(err){ sylShowMsg('DOCX解析失败: '+err,'err'); sylSetIcon(1,'error'); });
        } else if (ext === 'pdf') {
            if (typeof pdfjsLib === 'undefined') {
                sylShowMsg('pdf.js 未加载，请检查网络','err'); return;
            }
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
            pdfjsLib.getDocument({data: bytes.buffer}).promise
                .then(function(pdf){
                    var pages = [];
                    var promises = [];
                    for (var i=1; i<=pdf.numPages; i++) {
                        promises.push(pdf.getPage(i).then(function(page){
                            return page.getTextContent().then(function(content){
                                var texts = content.items.map(function(it){return it.str});
                                pages.push(texts.join(' '));
                            });
                        }));
                    }
                    return Promise.all(promises).then(function(){return pages.join('\n\n')});
                })
                .then(function(text){ _sylTextFull = text; _onTextReady(file.name, _sylTextFull); })
                .catch(function(err){ sylShowMsg('PDF解析失败: '+err,'err'); sylSetIcon(1,'error'); });
        }
    };

    if (ext === 'docx' || ext === 'pdf') {
        reader.readAsArrayBuffer(file);
    } else {
        reader.readAsArrayBuffer(file);
    }
}

function _onTextReady(filename, text) {
    document.getElementById('syl-preview').textContent = text.substring(0, 2000);
    document.getElementById('syl-preview').style.display = 'block';
    sylSetIcon(1,'done');
    sylShowMsg('文本提取成功！共 '+text.length+' 字符','ok');
    document.getElementById('syl-step2').style.display = 'block';
}

// Step 2: Parse courses (Try LLM first, fallback to regex)
function sylAnalyze() {
    if (!_sylTextFull) { sylShowMsg('请先上传文件','warn'); return; }
    sylSetIcon(2,'loading');
    sylShowMsg('正在解析...','info');
    document.getElementById('syl-step2-result').style.display = 'none';

    if (_apiKey) {
        _sylAnalyzeLLM(_sylTextFull);
    } else {
        // Try prompt for API key, fallback to regex
        promptApiKey(function(key) {
            if (key) {
                _sylAnalyzeLLM(_sylTextFull);
            } else {
                _sylParsed = _regexParse(_sylTextFull);
                _onAnalyzeReady(_sylParsed);
            }
        });
    }
}

function _sylAnalyzeLLM(text) {
    var maxChars = 30000;
    var truncated = text.length > maxChars ? text.substring(0, maxChars) + '\n[截断]' : text;

    fetch('https://api.deepseek.com/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + _apiKey
        },
        body: JSON.stringify({
            model: 'deepseek-chat',
            messages: [
                {role:'system', content: '你是教学大纲解析专家。从文本中提取课程结构化信息。输出纯JSON: {"courses":[{"name":"课程名","english_name":"","id":"","credit":"","credit_hour":"","semester":"","optional":"n","teacher":"","details":""}],"relationships":[{"course":"后修课程名","prerequisite":"先修课程名"}]}。规则: 1.识别所有课程 2.提取字段(名称/编号/英文名/学分/学时/学期/选修必修/教师/描述) 3.识别先修关系(先修课程/预修课程/前置课程后) 4.缺字段留空 5.课程名用中文全称 6.输出合法JSON'},
                {role:'user', content: '请解析以下教学大纲：\n\n'+truncated}
            ],
            temperature: 0.1,
            max_tokens: 4096
        })
    }).then(function(r){return r.json()})
    .then(function(data){
        var content = data.choices[0].message.content;
        // Try to parse JSON
        var result = null;
        try { result = JSON.parse(content); } catch(e) {
            var m = content.match(/```(?:json)?\s*\n?(.*?)\n?```/s) || content.match(/\{.*\}/s);
            if (m) { try { result = JSON.parse(m[1]||m[0]); } catch(e2) {} }
        }
        if (result && result.courses) {
            _sylParsed = _validateResult(result);
            _onAnalyzeReady(_sylParsed);
        } else {
            sylShowMsg('LLM返回格式异常，回退到正则解析','warn');
            _sylParsed = _regexParse(_sylTextFull);
            _onAnalyzeReady(_sylParsed);
        }
    }).catch(function(err){
        sylShowMsg('DeepSeek API调用失败('+err.message+')，回退到正则解析','warn');
        _sylParsed = _regexParse(_sylTextFull);
        _onAnalyzeReady(_sylParsed);
    });
}

function _validateResult(result) {
    var courses = (result.courses||[]).filter(function(c){return c&&c.name});
    var names = {};
    var validCourses = [];
    courses.forEach(function(c){
        if (!c.name||names[c.name]) return;
        names[c.name] = true;
        validCourses.push({
            name: String(c.name||'').trim(),
            english_name: String(c.english_name||'').trim(),
            id: String(c.id||'').trim(),
            credit: String(c.credit||'').trim(),
            credit_hour: String(c.credit_hour||'').trim(),
            semester: String(c.semester||'').trim(),
            optional: (String(c.optional||'n').toLowerCase()==='y'||String(c.optional||'').indexOf('选')>=0)?'y':'n',
            teacher: String(c.teacher||'').trim(),
            details: String(c.details||'').trim()
        });
    });
    var validRels = [];
    (result.relationships||[]).forEach(function(r){
        if (r.course&&r.prerequisite&&names[r.course]&&names[r.prerequisite]&&r.course!==r.prerequisite) {
            validRels.push({course: r.course, prerequisite: r.prerequisite});
        }
    });
    return {courses: validCourses, relationships: validRels};
}

// Client-side regex parser (ported from llm_extractor.py)
function _regexParse(text) {
    text = text.replace(/\r/g,'\n').replace(/\n{3,}/g,'\n\n');
    var courses = [];
    var relationships = [];

    // Find course names from numbered headings
    var headingRe = /[一二三四五六七八九十\d]+[、.]\s*([^\n]{2,40}?)\s*(?:\n|$)/g;
    var courseNames = [];
    var m;
    while ((m = headingRe.exec(text)) !== null) {
        var name = m[1].trim();
        var skipWords = ['适用','制定','学院','前言','目录','说明','总则'];
        if (!skipWords.some(function(w){return name.indexOf(w)>=0}) && name.length>=2 && courseNames.indexOf(name)<0) {
            courseNames.push(name);
        }
    }
    if (!courseNames.length) return {courses:[],relationships:[]};

    // Parse field rows (key | value format)
    var fieldRows = [];
    text.split('\n').forEach(function(line){
        line = line.trim();
        if (line.indexOf('|')>=0 && !line.startsWith('━')) {
            var parts = line.split('|');
            if (parts.length>=2) {
                var k = parts[0].trim(), v = parts[1].trim();
                if (k&&v) fieldRows.push([k,v]);
            }
        }
    });

    var FIELDS_PER = 7;
    var numCourses = Math.min(courseNames.length, Math.floor(fieldRows.length/FIELDS_PER));

    for (var i=0; i<numCourses; i++) {
        var info = {name:courseNames[i],english_name:'',id:'',credit:'',credit_hour:'',semester:'',optional:'n',teacher:'',details:'',_prereqs:[]};
        var start = i*FIELDS_PER;
        for (var j=0; j<FIELDS_PER&&(start+j)<fieldRows.length; j++) {
            var key = fieldRows[start+j][0], val = fieldRows[start+j][1];
            if (key.indexOf('编号')>=0) info.id = val;
            else if (key.indexOf('英文')>=0) info.english_name = val;
            else if (key.indexOf('学分')>=0||key.indexOf('学时')>=0) {
                var cm = val.match(/(\d+)\s*学分/); if(cm)info.credit=cm[1];
                var hm = val.match(/(\d+)\s*学时/); if(hm)info.credit_hour=hm[1];
                var dm = val.match(/^(\d+)\s*[\/\、]\s*(\d+)/); if(dm){if(!info.credit)info.credit=dm[1];if(!info.credit_hour)info.credit_hour=dm[2]}
            } else if (key.indexOf('性质')>=0||key.indexOf('选修')>=0||key.indexOf('必修')>=0) {
                info.optional = val.indexOf('选')>=0?'y':'n';
            } else if (key.indexOf('学期')>=0) {
                var sm = val.match(/(\d+)/); if(sm)info.semester=sm[1];
            } else if (key.indexOf('教师')>=0) {
                info.teacher = val;
            } else if (key.indexOf('先修')>=0||key.indexOf('预修')>=0||key.indexOf('前置')>=0) {
                if (val&&['无','—','-','/'].indexOf(val)<0) {
                    val.split(/[、,，\s]+/).forEach(function(n){n=n.trim().replace(/课程$/,'');if(n.length>=2)info._prereqs.push(n)});
                }
            }
        }
        courses.push(info);
    }

    // Extract descriptions
    courses.forEach(function(c){
        var nameEsc = c.name.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
        var dm = text.match(new RegExp(nameEsc+'\\s*\\n(?:课程简介\\s*\\n)?(.+?)(?=\\n[一二三四五六七八九十\\d]+[、.]|\\n课程编号|\\Z)','s'));
        if (dm) { var d=dm[1].trim(); c.details = d.length>300?d.substring(0,300)+'...':d; }
    });

    // Build relationships
    var nameSet = {};
    courses.forEach(function(c){nameSet[c.name]=true});
    courses.forEach(function(c){
        (c._prereqs||[]).forEach(function(pre){
            if (nameSet[pre]) relationships.push({course: c.name, prerequisite: pre});
        });
        delete c._prereqs;
    });

    return {courses:courses,relationships:relationships,_parser:'regex'};
}

function _onAnalyzeReady(data) {
    document.getElementById('syl-step2-result').innerHTML = _renderParseResult(data);
    document.getElementById('syl-step2-result').style.display = 'block';
    sylSetIcon(2,'done');
    sylShowMsg('解析完成！识别 '+data.courses.length+' 门课程、'+(data.relationships||[]).length+' 条关系','ok');
    document.getElementById('syl-step3').style.display = 'block';
}

function _renderParseResult(data) {
    var h='';
    h+='<h6 style="color:#5cb85c">📚 识别课程 ('+data.courses.length+'门)</h6>';
    h+='<table class="syl-table"><tr><th>课程名</th><th>学分</th><th>学期</th><th>教师</th></tr>';
    data.courses.forEach(function(c){
        h+='<tr><td><strong>'+c.name+'</strong></td><td>'+(c.credit||'-')+'</td><td>'+(c.semester||'-')+'</td><td>'+(c.teacher||'-')+'</td></tr>';
    });
    h+='</table>';
    if (data.relationships&&data.relationships.length>0) {
        h+='<h6 style="color:#5cb85c;margin-top:10px">🔗 先修关系 ('+data.relationships.length+'条)</h6>';
        h+='<table class="syl-table"><tr><th>后修课程</th><th style="text-align:center">←</th><th>先修课程</th></tr>';
        data.relationships.forEach(function(r){
            h+='<tr><td>'+r.course+'</td><td style="text-align:center;color:#d9534f">←</td><td>'+r.prerequisite+'</td></tr>';
        });
        h+='</table>';
    }
    return h;
}

// Step 3: Import with cycle detection
function sylImport() {
    if (!_sylParsed) { sylShowMsg('请先完成解析','warn'); return; }
    var courses = _sylParsed.courses;
    var rels = _sylParsed.relationships||[];

    if (!confirm('确认导入 '+courses.length+' 门课程及 '+rels.length+' 条关系？')) return;

    sylSetIcon(3,'loading');
    sylShowMsg('正在环检测并导入...','info');

    // Get existing edges (prerequisite -> course direction)
    var existingEdges = [];
    getAllPrereqs().forEach(function(p){
        existingEdges.push([p.prereq, p.course]);
    });

    // New edges: prerequisite -> course
    var newEdges = rels.map(function(r){return [r.prerequisite, r.course]});

    // Get existing course names
    var existingNames = {};
    getAllCourses().forEach(function(c){existingNames[c.name]=true});
    courses.forEach(function(c){existingNames[c.name]=true});
    var allNames = Object.keys(existingNames);

    var cycleResult = _detectCycles(allNames, existingEdges, newEdges);

    if (cycleResult.has_cycle) {
        var warnMsg = '⚠️ 检测到逻辑循环！\n\n';
        cycleResult.cycles.forEach(function(c){warnMsg+='🔴 环: '+c.join(' → ')+'\n'});
        warnMsg+='\n✅ 安全: '+cycleResult.safe_edges.length+' 条\n❌ 阻止: '+cycleResult.blocked_edges.length+' 条\n\n只导入安全的？';
        if (confirm(warnMsg)) {
            // Convert safe edges back to relationships
            var safeRels = cycleResult.safe_edges.map(function(e){return {course:e[1],prerequisite:e[0]}});
            _doImport(courses, safeRels);
        }
        sylSetIcon(3,'error');
        sylShowMsg('部分关系因逻辑循环被阻止','warn');
    } else {
        _doImport(courses, rels);
        sylSetIcon(3,'done');
        sylShowMsg('✅ 导入成功！课程:'+courses.length+' 关系:'+rels.length,'ok');
    }
}

function _doImport(newCourses, newRels) {
    // Append courses (skip duplicates)
    var existingNames = {};
    getAllCourses().forEach(function(c){existingNames[c.name]=true});
    newCourses.forEach(function(c){
        if (!existingNames[c.name]) {
            _dynamicCourses.push({
                name: c.name,
                id_num: c.id||'',
                englishName: c.english_name||'',
                credit: c.credit||'',
                creditHour: c.credit_hour||'',
                optional: c.optional||'n',
                semester: c.semester||'',
                details: c.details||'',
                teacher: c.teacher||''
            });
            existingNames[c.name] = true;
        }
    });

    // Append relationships (skip duplicates)
    var existingRels = {};
    getAllPrereqs().forEach(function(p){existingRels[p.course+'|||'+p.prereq]=true});
    newRels.forEach(function(r){
        var key = r.course+'|||'+r.prerequisite;
        if (!existingRels[key]) {
            _dynamicPrereqs.push({course: r.course, prereq: r.prerequisite});
            existingRels[key] = true;
        }
    });

    // Rebuild and re-render graph
    _rebuildGraph();

    // Reset syllabus state
    _sylTextFull = '';
    _sylParsed = null;
    document.getElementById('syl-file-input').value = '';
    document.getElementById('syl-preview').style.display = 'none';
    document.getElementById('syl-step2').style.display = 'none';
    document.getElementById('syl-step3').style.display = 'none';
    document.getElementById('syl-step2-result').style.display = 'none';
    ['1','2','3'].forEach(function(s){sylSetIcon(s,'wait')});

    setTimeout(function(){
        if (confirm('导入完成！节点已增加。是否刷新？')) {
            // Just reset highlight
            clearPath();
        }
    },500);
}

// ═══════════════════════════════════════════════════════════════════
// CYCLE DETECTION (ported from py)
// ═══════════════════════════════════════════════════════════════════
function _detectCycles(courseNames, existingEdges, newEdges) {
    var allEdges = existingEdges.concat(newEdges);
    var adj = {};
    var allNodes = {};
    courseNames.forEach(function(n){allNodes[n]=true});
    allEdges.forEach(function(e){allNodes[e[0]]=true;allNodes[e[1]]=true});

    Object.keys(allNodes).forEach(function(n){adj[n]=[]});
    allEdges.forEach(function(e){
        if (!adj[e[0]]) adj[e[0]]=[];
        adj[e[0]].push(e[1]);
    });

    var WHITE=0,GRAY=1,BLACK=2;
    var color={}, parent={}, allCycles=[];
    Object.keys(allNodes).forEach(function(n){color[n]=WHITE});

    function dfs(node) {
        color[node]=GRAY;
        (adj[node]||[]).forEach(function(neighbor){
            if (color[neighbor]===GRAY) {
                var cycle = [neighbor, node];
                var cur = node;
                while (cur!==neighbor && parent[cur]) { cur=parent[cur]; cycle.push(cur); }
                cycle.reverse();
                allCycles.push(cycle);
            } else if (color[neighbor]===WHITE) {
                parent[neighbor]=node;
                dfs(neighbor);
            }
        });
        color[node]=BLACK;
    }
    Object.keys(allNodes).forEach(function(n){if(color[n]===WHITE)dfs(n)});

    var safeEdges=[], blockedEdges=[];
    if (allCycles.length>0) {
        newEdges.forEach(function(edge){
            var testEdges = existingEdges.slice();
            testEdges.push(edge);
            if (_hasCycle(Object.keys(allNodes), testEdges)) blockedEdges.push(edge);
            else safeEdges.push(edge);
        });
    } else {
        safeEdges = newEdges.slice();
    }
    return {has_cycle:allCycles.length>0,cycles:allCycles,safe_edges:safeEdges,blocked_edges:blockedEdges};
}

function _hasCycle(nodes, edges) {
    var adj = {};
    nodes.forEach(function(n){adj[n]=[]});
    edges.forEach(function(e){adj[e[0]].push(e[1])});
    var WHITE=0,GRAY=1,BLACK=2;
    var color = {};
    nodes.forEach(function(n){color[n]=WHITE});

    function dfs(n) {
        color[n]=GRAY;
        for (var i=0;i<(adj[n]||[]).length;i++) {
            var nb=adj[n][i];
            if (color[nb]===GRAY) return true;
            if (color[nb]===WHITE&&dfs(nb)) return true;
        }
        color[n]=BLACK;
        return false;
    }
    for (var i=0;i<nodes.length;i++) {
        if (color[nodes[i]]===WHITE&&dfs(nodes[i])) return true;
    }
    return false;
}

// ═══════════════════════════════════════════════════════════════════
// PATH PLANNING (Kahn's Algorithm)
// ═══════════════════════════════════════════════════════════════════
var _adj={},_revAdj={};
function buildAdjacency() {
    if (Object.keys(_adj).length>0) return;
    getAllCourses().forEach(function(c){_adj[c.name]=[];_revAdj[c.name]=[]});
    getAllPrereqs().forEach(function(p){
        if (_adj[p.course])_adj[p.course].push(p.prereq);
        if (_revAdj[p.prereq])_revAdj[p.prereq].push(p.course);
    });
}
function resetAdjacency() { _adj={}; _revAdj={}; buildAdjacency(); }

function getAllPrerequisites(target) {
    buildAdjacency();
    if (!_adj[target]) return new Set();
    var visited=new Set(),queue=[target];
    visited.add(target);
    while(queue.length>0){
        var cur=queue.shift();
        (_adj[cur]||[]).forEach(function(pre){if(!visited.has(pre)){visited.add(pre);queue.push(pre)}});
    }
    visited.delete(target);
    return visited;
}
function topologicalLevels(courseSet) {
    buildAdjacency();
    var subAdj={},deps={},inDeg={};
    courseSet.forEach(function(c){
        subAdj[c]=(_adj[c]||[]).filter(function(p){return courseSet.has(p)});
        inDeg[c]=subAdj[c].length;
    });
    courseSet.forEach(function(c){subAdj[c].forEach(function(pre){if(!deps[pre])deps[pre]=[];deps[pre].push(c)})});
    var levels=[],levelMap={},queue=[];
    courseSet.forEach(function(c){if(inDeg[c]===0)queue.push(c)});
    while(queue.length>0){
        var sz=queue.length,curLvl=[];
        for(var i=0;i<sz;i++){var c=queue.shift();curLvl.push(c);levelMap[c]=levels.length;(deps[c]||[]).forEach(function(d){inDeg[d]--;if(inDeg[d]===0)queue.push(d)})}
        levels.push(curLvl.sort());
    }
    return {levels:levels,levelMap:levelMap};
}
function findCriticalPath(target) {
    var allPrereqs=getAllPrerequisites(target);
    var allSet=new Set(allPrereqs);allSet.add(target);
    var r=topologicalLevels(allSet);
    if(r.levels.length===0)return{criticalPath:[target],levels:[[target]]};
    buildAdjacency();
    var path=[],cur=target;
    while(cur){path.push(cur);var pres=(_adj[cur]||[]).filter(function(p){return allSet.has(p)});if(!pres.length)break;var maxLv=-1,nxt=null;pres.forEach(function(p){var lv=r.levelMap[p];if(lv!==undefined&&lv>maxLv){maxLv=lv;nxt=p}});if(!nxt||maxLv<0)break;cur=nxt}
    path.reverse();
    return{criticalPath:path,levels:r.levels};
}
function plan(target) {
    buildAdjacency();
    if(!_adj[target])return{exists:false,error:'课程不存在'};
    var allPrereqs=getAllPrerequisites(target);
    var cpResult=findCriticalPath(target);
    var semPlan=[];
    cpResult.levels.forEach(function(lc,i){semPlan.push({semester:i+1,courses:lc,count:lc.length})});
    var entries=cpResult.levels.length>0?cpResult.levels[0]:[target];
    return{target:target,exists:true,critical_path:cpResult.criticalPath,critical_path_length:cpResult.criticalPath.length,semester_plan:semPlan,total_semesters:cpResult.levels.length,total_courses_needed:allPrereqs.size+1,all_prerequisites:Array.from(allPrereqs).sort(),entry_courses:entries};
}

// ═══════════════════════════════════════════════════════════════════
// D3 GRAPH
// ═══════════════════════════════════════════════════════════════════
var nodes=[],edges=[],_cpNodes={};

function initGraph() { _rebuildGraph(); }

function _rebuildGraph() {
    resetAdjacency();
    // Clear existing SVG elements
    var svg = d3.select('#svg1');
    svg.selectAll('g').remove();

    var sel = document.getElementById('target-course-select');
    sel.innerHTML = '<option value="">-- 选择目标课程 ('+getAllCourses().length+'门) --</option>';
    getAllCourses().map(function(c){return c.name}).sort().forEach(function(name){
        var opt=document.createElement('option');opt.value=name;opt.textContent=name;sel.appendChild(opt);
    });

    nodes = getAllCourses().map(function(c){return{name:c.name,description:c.details}});
    var nameToIdx = {};
    nodes.forEach(function(n,i){nameToIdx[n.name]=i});
    edges = [];
    getAllPrereqs().forEach(function(p){
        var si=nameToIdx[p.course],ti=nameToIdx[p.prereq];
        if(si!==undefined&&ti!==undefined) edges.push({source:si,target:ti});
    });

    var width=+svg.attr('width'),height=+svg.attr('height');
    var sim = d3.forceSimulation()
        .force('link',d3.forceLink().id(function(d){return d.index}))
        .force('collide',d3.forceCollide().radius(function(){return 10}))
        .force('charge',d3.forceManyBody().strength(-150))
        .force('center',d3.forceCenter(width/2,height/2-60));

    var dragging=false;
    function ds(event,d){if(!event.active)sim.alphaTarget(0.3).restart();d.fx=d.x;d.fy=d.y;dragging=true}
    function dd(event,d){d.fx=event.x;d.fy=event.y}
    function de(event,d){if(!event.active)sim.alphaTarget(0);d.fx=null;d.fy=null;dragging=false}

    var link=svg.append('g').attr('class','links').selectAll('line').data(edges).enter().append('line').attr('stroke-width','1');
    var node=svg.append('g').attr('class','nodes').selectAll('circle').data(nodes).enter().append('circle')
        .attr('r',20).attr('name',function(d){return d.name}).attr('description',function(d){return d.description})
        .call(d3.drag().on('start',ds).on('drag',dd).on('end',de));
    sim.nodes(nodes).on('tick',ticked);
    sim.force('link').links(edges);

    var text=svg.append('g').attr('class','texts').selectAll('text').data(nodes).enter().append('text')
        .attr('font-size','13px').attr('fill','black').text(function(d){return d.name}).attr('text-anchor','middle')
        .call(d3.drag().on('start',ds).on('drag',dd).on('end',de));

    function ticked(){
        link.attr('x1',function(d){return d.source.x}).attr('y1',function(d){return d.source.y}).attr('x2',function(d){return d.target.x}).attr('y2',function(d){return d.target.y});
        node.attr('cx',function(d){return d.x}).attr('cy',function(d){return d.y});
        text.attr('transform',function(d){return'translate('+d.x+','+d.y+')'});
    }

    // Search filter
    document.querySelector('#search1 input').addEventListener('input',function(){
        var val=this.value,sv=document.getElementById('svg1');
        if(!val){sv.querySelectorAll('.nodes circle,.texts text,.links line').forEach(function(el){el.classList.remove('inactive')});return}
        sv.querySelectorAll('.nodes circle').forEach(function(circ){
            var dn=circ.getAttribute('name'),match=dn.indexOf(val)>=0;
            if(!match){for(var i=0;i<edges.length;i++){if((edges[i].source.name.indexOf(dn)>=0&&edges[i].target.name.indexOf(val)>=0)||(edges[i].target.name.indexOf(dn)>=0&&edges[i].source.name.indexOf(val)>=0)){match=true;break}}}
            circ.classList.toggle('inactive',!match);
        });
        sv.querySelectorAll('.texts text').forEach(function(tx){
            var dn=tx.textContent,match=dn.indexOf(val)>=0;
            if(!match){for(var i=0;i<edges.length;i++){if((edges[i].source.name.indexOf(dn)>=0&&edges[i].target.name.indexOf(val)>=0)||(edges[i].target.name.indexOf(dn)>=0&&edges[i].source.name.indexOf(val)>=0)){match=true;break}}}
            tx.classList.toggle('inactive',!match);
        });
        sv.querySelectorAll('.links line').forEach(function(ln){var d=ln.__data__;var match=d&&(d.source.name.indexOf(val)>=0||d.target.name.indexOf(val)>=0);ln.classList.toggle('inactive',!match)});
    });

    // Hover
    node.on('mouseenter',function(event,d){
        if(dragging)return;
        var name=d.name;
        document.querySelector('#info h4').textContent='课程名称: '+name;
        var oldP=document.querySelector('#info p');if(oldP)oldP.remove();
        var p=document.createElement('p');p.style.cssText='color:#666;font-size:13px;line-height:1.5';
        p.innerHTML='描述: <span>'+d.description+'</span>';
        document.getElementById('info').appendChild(p);
        svg.selectAll('.nodes circle').attr('class',function(d2){
            if(d2.name===name)return'';
            for(var i=0;i<edges.length;i++){if((edges[i].source.name===name&&edges[i].target.name===d2.name)||(edges[i].target.name===name&&edges[i].source.name===d2.name))return''}
            return'inactive';
        });
        svg.selectAll('.texts text').attr('class',function(d2){
            if(d2.name===name)return'';
            for(var i=0;i<edges.length;i++){if((edges[i].source.name===d2.name&&edges[i].target.name===name)||(edges[i].target.name===d2.name&&edges[i].source.name===name))return''}
            return'inactive';
        });
        svg.selectAll('.links line').attr('class',function(d2){return(d2.source.name===name||d2.target.name===name)?'':'inactive'});
    });

    window._svg=svg;window._edges=edges;window._sim=sim;
}

// ═══════════════════════════════════════════════════════════════════
// PATH PLANNING UI
// ═══════════════════════════════════════════════════════════════════
function _showPathErr(msg){var el=document.getElementById('path-error');el.textContent=msg;el.style.display='block';setTimeout(function(){el.style.display='none'},4000)}

function planPath(){
    var target=document.getElementById('target-course-select').value;
    if(!target){_showPathErr('请先选择目标课程');return}
    var btn=document.getElementById('btn-plan');btn.disabled=true;
    document.getElementById('path-loading').style.display='block';
    document.getElementById('path-result').style.display='none';
    document.getElementById('path-error').style.display='none';
    document.getElementById('path-legend-bar').style.display='none';
    setTimeout(function(){
        var result=plan(target);btn.disabled=false;
        document.getElementById('path-loading').style.display='none';
        if(result.exists){_showResult(result);_highlightPath(result);document.getElementById('path-legend-bar').style.display='block'}
        else _showPathErr(result.error||'规划失败');
    },100);
}
function _showResult(data){
    document.getElementById('cp-text').innerHTML=data.critical_path.join(' <span class="cp-arrow">→</span> ');
    document.getElementById('cp-stat').textContent='共 '+data.total_semesters+' 学期 · '+data.critical_path_length+' 步关键路径 · '+data.total_courses_needed+' 门课';
    var h='';
    data.semester_plan.forEach(function(sem){h+='<div class="sem-item"><span class="sem-num">第'+sem.semester+'学期</span> <span>('+sem.count+'门) '+sem.courses.join('、')+'</span></div>'});
    document.getElementById('sem-plan').innerHTML=h;
    document.getElementById('path-result').style.display='block';
}
function _highlightPath(data){
    _cpNodes={};data.critical_path.forEach(function(n){_cpNodes[n]=true});
    var relNodes={};(data.all_prerequisites||[]).forEach(function(n){relNodes[n]='pre'});
    relNodes[data.target]='target';
    var cpEdges={};
    for(var i=0;i<data.critical_path.length-1;i++){var f=data.critical_path[i],t=data.critical_path[i+1];cpEdges[t+'|||'+f]=true;cpEdges[f+'|||'+t]=true}
    var svg=window._svg||d3.select('#svg1');
    svg.selectAll('.nodes circle').attr('class',function(d){if(_cpNodes[d.name])return'cp-node';if(relNodes[d.name])return'pre-node';return'inactive'});
    svg.selectAll('.texts text').attr('class',function(d){if(_cpNodes[d.name])return'cp-text';if(relNodes[d.name])return'pre-text';return'inactive'});
    svg.selectAll('.links line').attr('class',function(d){var k1=d.source.name+'|||'+d.target.name,k2=d.target.name+'|||'+d.source.name;if(cpEdges[k1]||cpEdges[k2])return'cp-edge';if(_cpNodes[d.source.name]&&_cpNodes[d.target.name])return'pre-edge';return'inactive'});
}
function clearPath(){
    _cpNodes={};
    var svg=window._svg||d3.select('#svg1');
    svg.selectAll('.nodes circle').attr('class','');svg.selectAll('.texts text').attr('class','');svg.selectAll('.links line').attr('class','');
    document.getElementById('path-result').style.display='none';document.getElementById('path-legend-bar').style.display='none';
}

// ═══════════════════════════════════════════════════════════════════
// SEARCH Q&A
// ═══════════════════════════════════════════════════════════════════
function doSearch(){
    var query=document.getElementById('question').value.trim();
    var ans=document.getElementById('answer');
    if(!query||query==='搜索'){ans.textContent='请输入您的问题';ans.style.color='#999';return}
    var matched=null,mlen=0;
    getAllCourses().forEach(function(c){if(query.indexOf(c.name)>=0&&c.name.length>mlen){matched=c;mlen=c.name.length}});
    if(!matched){getAllCourses().forEach(function(c){for(var i=0;i<c.name.length-1;i++){for(var j=i+2;j<=c.name.length;j++){var sub=c.name.substring(i,j);if(sub.length>=2&&query.indexOf(sub)>=0&&sub.length>mlen){matched=c;mlen=sub.length}}}})}
    if(!matched){ans.innerHTML='❌ 未识别出课程名称<br><small style="color:#aaa">示例：算法与数据结构是什么 / 操作系统原理的学分</small>';ans.style.color='#ff6b6b';return}
    var c=matched,q=query.toLowerCase(),a='';
    if(q.indexOf('介绍')>=0||q.indexOf('是什么')>=0||q.indexOf('内容')>=0||q.indexOf('什么是')>=0)a='<b>'+c.name+'</b><br><br>'+c.details;
    else if(q.indexOf('先修')>=0||q.indexOf('前置')>=0||q.indexOf('基础')>=0||q.indexOf('需要什么')>=0){buildAdjacency();var prs=_adj[c.name]||[];a=prs.length?'<b>'+c.name+'</b> 的先修课程：<br>'+prs.map(function(p){return'• '+p}).join('<br>'):'<b>'+c.name+'</b> 无先修课程（入口课程）'}
    else if(q.indexOf('学期')>=0||q.indexOf('什么时候')>=0||q.indexOf('开课')>=0)a='<b>'+c.name+'</b> 开课学期：<b>第 '+c.semester+' 学期</b>';
    else if(q.indexOf('必修')>=0||q.indexOf('选修')>=0)a='<b>'+c.name+'</b> 是 <b>'+(c.optional==='n'?'必修课':'选修课')+'</b>';
    else if(q.indexOf('学分')>=0)a='<b>'+c.name+'</b> 学分：<b>'+c.credit+'</b>';
    else if(q.indexOf('学时')>=0||q.indexOf('课时')>=0)a='<b>'+c.name+'</b> 学时：<b>'+c.creditHour+'</b>';
    else if(q.indexOf('编号')>=0||q.indexOf('代码')>=0)a='<b>'+c.name+'</b> 编号：<b>'+c.id_num+'</b>';
    else if(q.indexOf('英文')>=0)a='<b>'+c.name+'</b> 英文名：<b>'+c.englishName+'</b>';
    else if(q.indexOf('老师')>=0||q.indexOf('教师')>=0||q.indexOf('谁教')>=0)a='<b>'+c.name+'</b> 教师：<b>'+c.teacher+'</b>';
    else a='<b>'+c.name+'</b><br>📖 '+(c.optional==='n'?'必修':'选修')+' | '+c.credit+' | '+c.creditHour+' | 第'+c.semester+'学期<br>👨‍🏫 '+c.teacher+'<br>🔢 '+c.id_num+'<br><br>'+c.details;
    ans.innerHTML=a;ans.style.color='#fff';ans.style.background='rgba(0,0,0,0.4)';ans.style.padding='16px 20px';ans.style.borderRadius='8px';ans.style.textAlign='left';
}
document.getElementById('question').addEventListener('keydown',function(e){if(e.key==='Enter')doSearch()});
</script>
</body>
</html>'''

# Write the file
output_path = 'standalone_full.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

import os
size_kb = os.path.getsize(output_path) / 1024
print(f'Generated: {output_path}')
print(f'Size: {size_kb:.1f} KB')
print(f'Courses: {len(courses)}')
