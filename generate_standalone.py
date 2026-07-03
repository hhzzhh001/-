# -*- coding: utf-8 -*-
"""Generate standalone.html — a self-contained version of the learning platform."""

import xml.etree.ElementTree as ET
import json

# ── Parse data.xml ──────────────────────────────────────────────────
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

courses_json = json.dumps(courses, ensure_ascii=False, indent=8)
prereqs_json = json.dumps(prereqs, ensure_ascii=False, indent=8)

# ── Build HTML ──────────────────────────────────────────────────────
html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>软件工程在线学习平台</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
/* ===== Reset & Global ===== */
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: "Microsoft YaHei","PingFang SC","Helvetica Neue",Arial,sans-serif; background: #f5f5f5; color: #333; overflow-x: hidden; }

/* ===== Navbar ===== */
.navbar { position: fixed; top: 0; left: 0; right: 0; z-index: 1000; background: #fff; box-shadow: 0 2px 10px rgba(0,0,0,0.1); display: flex; align-items: center; justify-content: space-between; padding: 0 40px; height: 60px; }
.navbar .brand { font-size: 20px; font-weight: bold; color: #6aae7a; text-decoration: none; }
.navbar .nav-links { display: flex; list-style: none; gap: 8px; }
.navbar .nav-links li a { text-decoration: none; color: #555; padding: 8px 16px; border-radius: 4px; font-size: 14px; transition: all 0.3s; cursor: pointer; }
.navbar .nav-links li a:hover, .navbar .nav-links li a.active { color: #6aae7a; background: #f0f9f0; }

/* ===== Page Sections ===== */
.page-section { display: none; padding-top: 60px; min-height: 100vh; }
.page-section.active { display: block; }

/* ===== HOME PAGE ===== */
#page-home .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 100px 20px 80px; text-align: center; }
#page-home .hero h1 { font-size: 42px; font-weight: 900; margin-bottom: 16px; letter-spacing: 2px; }
#page-home .hero p { font-size: 18px; opacity: 0.9; margin-bottom: 30px; }
#page-home .hero .btn { display: inline-block; padding: 12px 28px; margin: 0 10px; border-radius: 30px; font-size: 14px; font-weight: bold; text-decoration: none; cursor: pointer; transition: all 0.3s; border: 2px solid white; color: white; background: transparent; }
#page-home .hero .btn:hover { background: white; color: #667eea; }
#page-home .hero .btn.primary { background: white; color: #667eea; }
#page-home .hero .btn.primary:hover { background: transparent; color: white; }
#page-home .features { display: flex; justify-content: center; gap: 30px; padding: 60px 40px; flex-wrap: wrap; max-width: 1100px; margin: 0 auto; }
#page-home .features .card { background: white; border-radius: 12px; padding: 30px; width: 300px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.08); transition: transform 0.3s; }
#page-home .features .card:hover { transform: translateY(-5px); }
#page-home .features .card .icon { font-size: 48px; margin-bottom: 16px; }
#page-home .features .card h3 { font-size: 18px; margin-bottom: 10px; color: #333; }
#page-home .features .card p { font-size: 13px; color: #888; line-height: 1.6; }
#page-home .features .card a { display: inline-block; margin-top: 14px; color: #6aae7a; font-weight: bold; font-size: 13px; text-decoration: none; cursor: pointer; }
#page-home .about { text-align: center; padding: 40px 20px 60px; color: #888; font-size: 13px; }
#page-home .about a { color: #6aae7a; }

/* ===== GRAPH PAGE ===== */
#page-graph { position: relative; text-align: center; }
#page-graph .graph-container { position: relative; display: inline-block; margin-top: 20px; }

/* SVG Node/Edge styles */
.nodes circle { fill: rgba(108,164,108,1); stroke: rgba(255,255,255,1); stroke-width: 1.5px; }
.links line { stroke: black; }
.nodes circle.inactive { fill: rgba(108,164,108,.3); stroke: rgba(255,255,255,.3); }
.texts text.inactive { display: none; }
.links line.inactive { display: none; }

/* Search box on graph */
#search1 input { padding: 0 15px; border: none; z-index: 2; position: absolute; top: 30px; left: 20px; color: #666; width: 200px; height: 30px; background: #ccc; border-radius: 5px; font-size: 13px; outline: none; }
#search1 input:focus { background: #e0e0e0; }

/* Text labels */
.texts text { font-size: 13px; fill: black; }
.texts text:hover { cursor: pointer; }

/* Info panel */
#info { position: absolute; top: 160px; left: 20px; width: 270px; text-align: left; color: black; }
#info h4 { font-size: 14px; margin-bottom: 6px; }
#info p { font-size: 13px; color: #666; line-height: 1.5; }

/* Breathing animation */
@keyframes breathe-cp {
    0%, 100% { fill: #ff4444; stroke: #ff6666; stroke-width: 2px; filter: url(#glow-breath); opacity: 1; }
    50% { fill: #ff8888; stroke: #ffaaaa; stroke-width: 3px; filter: url(#glow-strong); opacity: 0.85; }
}
.nodes circle.cp-node { fill: #ff4444; stroke: #ff6666; stroke-width: 2px; filter: url(#glow-breath); animation: breathe-cp 1.5s ease-in-out infinite; r: 22px; }
.nodes circle.pre-node { fill: rgba(108,164,108,0.5); stroke: rgba(108,164,108,0.6); stroke-width: 1px; }
.texts text.cp-text { font-size: 14px; font-weight: bold; fill: #cc0000; display: block; }
.texts text.pre-text { font-size: 12px; fill: rgba(80,120,80,0.7); display: block; }
.links line.cp-edge { stroke: #ff4444; stroke-width: 3px; stroke-dasharray: none; opacity: 0.9; filter: url(#glow-breath); }
.links line.pre-edge { stroke: rgba(108,164,108,0.4); stroke-width: 1px; }

/* Path Planning Panel */
#path-panel { position: absolute; top: 100px; left: 20px; z-index: 10; background: rgba(255,255,255,0.95); padding: 16px 18px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); width: 310px; max-height: 80vh; overflow-y: auto; text-align: left; }
#path-panel h5 { color: #2c3e50; margin-bottom: 10px; font-weight: bold; border-bottom: 2px solid #5cb85c; padding-bottom: 6px; font-size: 14px; }
#path-panel .subtitle { font-size: 11px; color: #999; margin-bottom: 10px; display: block; }
#path-panel select { width: 100%; margin-bottom: 8px; font-size: 13px; height: 34px; border: 1px solid #ddd; border-radius: 4px; padding: 4px; }
#path-panel .btn-plan { width: 100%; background: #5cb85c; color: white; font-weight: bold; font-size: 14px; padding: 8px; border: none; border-radius: 5px; cursor: pointer; transition: background 0.3s; }
#path-panel .btn-plan:hover { background: #449d44; }
#path-panel .btn-plan:disabled { background: #ccc; cursor: not-allowed; }
#path-panel .btn-clear { width: 100%; margin-top: 6px; background: none; border: 1px solid #ddd; color: #888; font-size: 12px; padding: 6px; border-radius: 4px; cursor: pointer; }
#path-panel .btn-clear:hover { background: #f5f5f5; color: #555; }
#path-loading { display: none; text-align: center; color: #5cb85c; margin: 8px 0; font-size: 13px; }
#path-error { display: none; color: #d9534f; font-size: 12px; margin-top: 6px; }
#path-result { display: none; margin-top: 12px; animation: fadeInUp 0.4s ease-out; }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
#cp-display { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px 12px; border-radius: 8px; margin-bottom: 10px; font-size: 12px; line-height: 1.7; word-break: break-all; }
#cp-display .cp-arrow { color: #ffd700; font-weight: bold; margin: 0 3px; }
#cp-display .cp-label { font-size: 10px; opacity: 0.85; display: block; margin-bottom: 3px; }
#cp-display .cp-stat { font-size: 11px; margin-top: 4px; opacity: 0.9; }
#sem-plan .sem-item { background: #f8f9fa; border-left: 4px solid #5cb85c; padding: 6px 10px; margin-bottom: 5px; border-radius: 0 5px 5px 0; font-size: 12px; transition: all 0.3s; }
#sem-plan .sem-item:hover { background: #e8f5e9; transform: translateX(3px); }
#sem-plan .sem-num { font-weight: bold; color: #5cb85c; font-size: 13px; }

/* Legend bar */
#path-legend-bar { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.75); color: white; padding: 6px 18px; border-radius: 20px; font-size: 12px; z-index: 5; pointer-events: none; display: none; }
#path-legend-bar .ldot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin: 0 3px; vertical-align: middle; }
#path-legend-bar .ldot.crit { background: #ff4444; box-shadow: 0 0 8px #ff4444; animation: ldBreathe 1.5s ease-in-out infinite; }
#path-legend-bar .ldot.pre { background: rgba(108,164,108,0.5); }
@keyframes ldBreathe { 0%, 100% { box-shadow: 0 0 4px #ff4444; } 50% { box-shadow: 0 0 16px #ff4444, 0 0 24px #ff2222; } }

/* ===== SEARCH PAGE ===== */
#page-search { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; }
#page-search.active { display: flex; }
#page-search .search-box { text-align: center; width: 100%; max-width: 600px; padding: 0 20px; }
#page-search .search-box h2 { color: white; font-size: 32px; margin-bottom: 30px; font-weight: 300; letter-spacing: 2px; }
#page-search .s-bar { display: flex; width: 100%; }
#page-search .s-bar input { flex: 1; padding: 14px 20px; font-size: 16px; border: none; border-radius: 30px 0 0 30px; outline: none; background: rgba(255,255,255,0.9); color: #333; }
#page-search .s-bar button { padding: 14px 28px; font-size: 16px; border: none; border-radius: 0 30px 30px 0; background: #5cb85c; color: white; cursor: pointer; font-weight: bold; transition: background 0.3s; }
#page-search .s-bar button:hover { background: #449d44; }
#page-search .answer { margin-top: 30px; color: white; font-size: 16px; line-height: 1.8; min-height: 30px; text-align: center; max-width: 500px; }
#page-search .copyright { position: absolute; bottom: 20px; color: rgba(255,255,255,0.5); font-size: 12px; }
#page-search .copyright a { color: #5cb85c; text-decoration: none; }

/* ===== Responsive ===== */
@media (max-width: 768px) {
    .navbar { padding: 0 15px; }
    .navbar .brand { font-size: 16px; }
    #page-home .hero h1 { font-size: 28px; }
    #page-home .features { flex-direction: column; align-items: center; }
    #page-home .features .card { width: 100%; max-width: 350px; }
}
</style>
</head>
<body>

<!-- ===== Navigation ===== -->
<nav class="navbar">
    <a class="brand" onclick="showPage('page-home')">📚 软件工程在线学习平台</a>
    <ul class="nav-links">
        <li><a onclick="showPage('page-home')" id="nav-home" class="active">首页</a></li>
        <li><a onclick="showPage('page-graph')" id="nav-graph">知识图谱</a></li>
        <li><a onclick="showPage('page-search')" id="nav-search">智能搜索</a></li>
    </ul>
</nav>

<!-- ===== HOME PAGE ===== -->
<section class="page-section active" id="page-home">
    <div class="hero">
        <h1>软件工程在线学习平台</h1>
        <p>基于知识图谱的智能学习路径规划系统 — 北京邮电大学软件工程专业</p>
        <button class="btn primary" onclick="showPage('page-graph')">📊 浏览知识图谱</button>
        <button class="btn" onclick="showPage('page-search')">🔍 开始搜索课程</button>
    </div>
    <div class="features">
        <div class="card">
            <div class="icon">🗺️</div>
            <h3>知识图谱</h3>
            <p>可视化展示59门软件工程专业课程的先修依赖关系，支持交互式浏览与搜索过滤</p>
            <a onclick="showPage('page-graph')">立即探索 →</a>
        </div>
        <div class="card">
            <div class="icon">📐</div>
            <h3>学习路径规划</h3>
            <p>基于拓扑排序算法，为目标课程自动计算最优学习路径与学期规划</p>
            <a onclick="showPage('page-graph')">开始规划 →</a>
        </div>
        <div class="card">
            <div class="icon">🔍</div>
            <h3>智能搜索</h3>
            <p>输入自然语言问题，智能识别课程名与问题类型，快速查询课程信息</p>
            <a onclick="showPage('page-search')">开始搜索 →</a>
        </div>
    </div>
    <div class="about">
        <p>© 2022 <a href="https://sse.bupt.edu.cn/" target="_blank">新工科U+平台</a> — 数据来源：北京邮电大学软件工程专业培养方案</p>
    </div>
</section>

<!-- ===== GRAPH PAGE ===== -->
<section class="page-section" id="page-graph">
    <div class="graph-container">
        <svg width="1000" height="560" id="svg1">
            <defs>
                <filter id="glow-breath" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="b1"/>
                    <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="b2"/>
                    <feMerge>
                        <feMergeNode in="b2"/>
                        <feMergeNode in="b1"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
                <filter id="glow-strong" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="b1"/>
                    <feGaussianBlur in="SourceGraphic" stdDeviation="12" result="b2"/>
                    <feMerge>
                        <feMergeNode in="b2"/>
                        <feMergeNode in="b1"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
        </svg>

        <div id="search1"><input type="text" placeholder="请输入关键词过滤"></div>
        <div id="info"><h4></h4></div>

        <!-- Path Planning Panel -->
        <div id="path-panel">
            <h5>🗺️ 智能学习路径规划</h5>
            <span class="subtitle">选择目标课程，自动计算最优先修路径</span>
            <select id="target-course-select">
                <option value="">-- 加载课程列表中... --</option>
            </select>
            <button id="btn-plan" class="btn-plan" onclick="planPath()">🚀 规划最优路径</button>
            <button class="btn-clear" onclick="clearPath()">🔄 清除高亮</button>
            <div id="path-loading">⏳ 正在计算最优路径...</div>
            <div id="path-error"></div>
            <div id="path-result">
                <div id="cp-display">
                    <span class="cp-label">⚡ 关键学习路径</span>
                    <span id="cp-text"></span>
                    <div class="cp-stat" id="cp-stat"></div>
                </div>
                <div id="sem-plan"></div>
            </div>
        </div>

        <div id="path-legend-bar">
            <span class="ldot crit"></span> 最优路径节点
            <span style="margin:0 10px;">|</span>
            <span class="ldot pre"></span> 相关先修课
            <span style="margin:0 10px;">|</span>
            其余课程已隐藏
        </div>
    </div>
</section>

<!-- ===== SEARCH PAGE ===== -->
<section class="page-section" id="page-search">
    <div class="search-box">
        <h2>🔍 智能课程搜索</h2>
        <div class="s-bar">
            <input id="question" type="text" placeholder="输入问题，如：算法与数据结构是什么">
            <button onclick="doSearch()">搜索</button>
        </div>
        <div class="answer" id="answer"></div>
    </div>
    <div class="copyright">
        <p>© 2022 <a href="https://sse.bupt.edu.cn/" target="_blank">新工科U+平台</a></p>
    </div>
</section>

<!-- ===== EMBEDDED DATA ===== -->
<script>
// ── Course Data ────────────────────────────────────────────────────
const COURSES = ''' + courses_json + r''';

// ── Prerequisite Relationships ─────────────────────────────────────
const PREREQUISITES = ''' + prereqs_json + r''';
</script>

<!-- ===== APPLICATION LOGIC ===== -->
<script>
// ── Page Navigation ────────────────────────────────────────────────
function showPage(pageId) {
    document.querySelectorAll('.page-section').forEach(function(s) { s.classList.remove('active'); });
    document.getElementById(pageId).classList.add('active');
    document.querySelectorAll('.nav-links a').forEach(function(a) { a.classList.remove('active'); });
    var navId = 'nav-' + pageId.replace('page-', '');
    var navEl = document.getElementById(navId);
    if (navEl) navEl.classList.add('active');
    if (pageId === 'page-graph' && !window._graphInited) { initGraph(); window._graphInited = true; }
}

// ── Path Planning Engine (Kahn's Algorithm) ────────────────────────
var _adj = {};    // courseName -> [prerequisiteNames]
var _revAdj = {}; // courseName -> [dependentNames]

function buildAdjacency() {
    if (Object.keys(_adj).length > 0) return;
    COURSES.forEach(function(c) { _adj[c.name] = []; _revAdj[c.name] = []; });
    PREREQUISITES.forEach(function(p) {
        if (_adj[p.course]) _adj[p.course].push(p.prereq);
        if (_revAdj[p.prereq]) _revAdj[p.prereq].push(p.course);
    });
}

function getAllPrerequisites(target) {
    buildAdjacency();
    if (!_adj[target]) return new Set();
    var visited = new Set();
    var queue = [target];
    visited.add(target);
    while (queue.length > 0) {
        var current = queue.shift();
        (_adj[current] || []).forEach(function(pre) {
            if (!visited.has(pre)) { visited.add(pre); queue.push(pre); }
        });
    }
    visited.delete(target);
    return visited;
}

function topologicalLevels(courseSet) {
    buildAdjacency();
    var subAdj = {};
    var dependents = {};
    var inDegree = {};
    courseSet.forEach(function(course) {
        subAdj[course] = (_adj[course] || []).filter(function(p) { return courseSet.has(p); });
        inDegree[course] = subAdj[course].length;
    });
    courseSet.forEach(function(course) {
        subAdj[course].forEach(function(pre) {
            if (!dependents[pre]) dependents[pre] = [];
            dependents[pre].push(course);
        });
    });
    var levels = [];
    var levelMap = {};
    var queue = [];
    courseSet.forEach(function(course) {
        if (inDegree[course] === 0) queue.push(course);
    });
    while (queue.length > 0) {
        var levelSize = queue.length;
        var currentLevel = [];
        for (var i = 0; i < levelSize; i++) {
            var course = queue.shift();
            currentLevel.push(course);
            levelMap[course] = levels.length;
            (dependents[course] || []).forEach(function(dep) {
                inDegree[dep]--;
                if (inDegree[dep] === 0) queue.push(dep);
            });
        }
        levels.push(currentLevel.sort());
    }
    return { levels: levels, levelMap: levelMap };
}

function findCriticalPath(target) {
    var allPrereqs = getAllPrerequisites(target);
    var allSet = new Set(allPrereqs);
    allSet.add(target);
    var result = topologicalLevels(allSet);
    var levels = result.levels, levelMap = result.levelMap;
    if (levels.length === 0) return { criticalPath: [target], levels: [[target]] };
    buildAdjacency();
    var criticalPath = [];
    var current = target;
    while (current) {
        criticalPath.push(current);
        var prereqsInSet = (_adj[current] || []).filter(function(p) { return allSet.has(p); });
        if (prereqsInSet.length === 0) break;
        var maxLevel = -1, next = null;
        prereqsInSet.forEach(function(p) {
            var lv = levelMap[p];
            if (lv !== undefined && lv > maxLevel) { maxLevel = lv; next = p; }
        });
        if (!next || maxLevel < 0) break;
        current = next;
    }
    criticalPath.reverse();
    return { criticalPath: criticalPath, levels: levels };
}

function plan(target) {
    buildAdjacency();
    if (!_adj[target]) return { exists: false, error: '课程「' + target + '」不存在于知识图谱中' };
    var allPrereqs = getAllPrerequisites(target);
    var cpResult = findCriticalPath(target);
    var semesterPlan = [];
    cpResult.levels.forEach(function(levelCourses, i) {
        semesterPlan.push({ semester: i + 1, courses: levelCourses, count: levelCourses.length });
    });
    var entryCourses = cpResult.levels.length > 0 ? cpResult.levels[0] : [target];
    return {
        target: target, exists: true,
        critical_path: cpResult.criticalPath,
        critical_path_length: cpResult.criticalPath.length,
        semester_plan: semesterPlan,
        total_semesters: cpResult.levels.length,
        total_courses_needed: allPrereqs.size + 1,
        all_prerequisites: Array.from(allPrereqs).sort(),
        entry_courses: entryCourses
    };
}

// ── D3 Knowledge Graph ─────────────────────────────────────────────
var nodes = [];
var edges = [];
var _cpNodes = {};

function initGraph() {
    buildAdjacency();
    // Populate course dropdown
    var sel = document.getElementById('target-course-select');
    sel.innerHTML = '<option value="">-- 请选择目标课程 (' + COURSES.length + '门) --</option>';
    var sortedNames = COURSES.map(function(c) { return c.name; }).sort();
    sortedNames.forEach(function(name) {
        var opt = document.createElement('option');
        opt.value = name;
        opt.textContent = name;
        sel.appendChild(opt);
    });

    // Build nodes & edges
    nodes = COURSES.map(function(c) { return { name: c.name, description: c.details }; });
    var nameToIndex = {};
    nodes.forEach(function(n, i) { nameToIndex[n.name] = i; });
    edges = [];
    PREREQUISITES.forEach(function(p) {
        var si = nameToIndex[p.course];
        var ti = nameToIndex[p.prereq];
        if (si !== undefined && ti !== undefined) {
            edges.push({ source: si, target: ti });
        }
    });

    var svg = d3.select('#svg1');
    var width = +svg.attr('width');
    var height = +svg.attr('height');

    var simulation = d3.forceSimulation()
        .force('link', d3.forceLink().id(function(d) { return d.index; }))
        .force('collide', d3.forceCollide().radius(function() { return 10; }))
        .force('charge', d3.forceManyBody().strength(-150))
        .force('center', d3.forceCenter(width / 2, height / 2 - 60));

    var dragging = false;
    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x; d.fy = d.y; dragging = true;
    }
    function dragged(event, d) { d.fx = event.x; d.fy = event.y; }
    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null; d.fy = null; dragging = false;
    }

    var link = svg.append('g').attr('class', 'links').selectAll('line')
        .data(edges).enter().append('line').attr('stroke-width', '1');

    var node = svg.append('g').attr('class', 'nodes').selectAll('circle')
        .data(nodes).enter().append('circle')
        .attr('r', 20).attr('name', function(d) { return d.name; })
        .attr('description', function(d) { return d.description; })
        .call(d3.drag().on('start', dragstarted).on('drag', dragged).on('end', dragended));

    simulation.nodes(nodes).on('tick', ticked);
    simulation.force('link').links(edges);

    var text = svg.append('g').attr('class', 'texts').selectAll('text')
        .data(nodes).enter().append('text')
        .attr('font-size', '13px').attr('fill', 'rgba(0,0,0,1)')
        .text(function(d) { return d.name; })
        .attr('text-anchor', 'middle')
        .call(d3.drag().on('start', dragstarted).on('drag', dragged).on('end', dragended));

    function ticked() {
        link.attr('x1', function(d) { return d.source.x; })
            .attr('y1', function(d) { return d.source.y; })
            .attr('x2', function(d) { return d.target.x; })
            .attr('y2', function(d) { return d.target.y; });
        node.attr('cx', function(d) { return d.x; }).attr('cy', function(d) { return d.y; });
        text.attr('transform', function(d) { return 'translate(' + d.x + ',' + d.y + ')'; });
    }

    // Search filter
    document.querySelector('#search1 input').addEventListener('input', function() {
        var val = this.value;
        var svgEl = document.getElementById('svg1');
        if (val === '') {
            svgEl.querySelectorAll('.nodes circle,.texts text,.links line').forEach(function(el) { el.classList.remove('inactive'); });
        } else {
            svgEl.querySelectorAll('.nodes circle').forEach(function(circ) {
                var dname = circ.getAttribute('name');
                var match = dname.indexOf(val) >= 0;
                if (!match) {
                    for (var i = 0; i < edges.length; i++) {
                        if ((edges[i].source.name.indexOf(dname) >= 0 && edges[i].target.name.indexOf(val) >= 0) ||
                            (edges[i].target.name.indexOf(dname) >= 0 && edges[i].source.name.indexOf(val) >= 0)) {
                            match = true; break;
                        }
                    }
                }
                circ.classList.toggle('inactive', !match);
            });
            svgEl.querySelectorAll('.texts text').forEach(function(tx) {
                var dname = tx.textContent;
                var match = dname.indexOf(val) >= 0;
                if (!match) {
                    for (var i = 0; i < edges.length; i++) {
                        if ((edges[i].source.name.indexOf(dname) >= 0 && edges[i].target.name.indexOf(val) >= 0) ||
                            (edges[i].target.name.indexOf(dname) >= 0 && edges[i].source.name.indexOf(val) >= 0)) {
                            match = true; break;
                        }
                    }
                }
                tx.classList.toggle('inactive', !match);
            });
            svgEl.querySelectorAll('.links line').forEach(function(ln) {
                var d = ln.__data__;
                var match = d && (d.source.name.indexOf(val) >= 0 || d.target.name.indexOf(val) >= 0);
                ln.classList.toggle('inactive', !match);
            });
        }
    });

    // Hover interaction
    svg.selectAll('.nodes circle').on('mouseenter', function(event, d) {
        if (dragging) return;
        var name = d.name;
        document.querySelector('#info h4').textContent = '课程名称: ' + name;
        var oldP = document.querySelector('#info p');
        if (oldP) oldP.remove();
        var p = document.createElement('p');
        p.style.cssText = 'color:#666;font-size:13px;line-height:1.5;';
        p.innerHTML = '课程描述: <span>' + d.description + '</span>';
        document.getElementById('info').appendChild(p);

        svg.selectAll('.nodes circle').attr('class', function(d2) {
            if (d2.name === name) return '';
            for (var i = 0; i < edges.length; i++) {
                if ((edges[i].source.name === name && edges[i].target.name === d2.name) ||
                    (edges[i].target.name === name && edges[i].source.name === d2.name)) return '';
            }
            return 'inactive';
        });
        svg.selectAll('.texts text').attr('class', function(d2) {
            if (d2.name === name) return '';
            for (var i = 0; i < edges.length; i++) {
                if ((edges[i].source.name === d2.name && edges[i].target.name === name) ||
                    (edges[i].target.name === d2.name && edges[i].source.name === name)) return '';
            }
            return 'inactive';
        });
        svg.selectAll('.links line').attr('class', function(d2) {
            return (d2.source.name === name || d2.target.name === name) ? '' : 'inactive';
        });
    });

    // Store for path planning
    window._svg = svg;
    window._edges = edges;
}

// ── Path Planning UI ────────────────────────────────────────────────
function _showPathErr(msg) {
    var el = document.getElementById('path-error');
    el.textContent = msg;
    el.style.display = 'block';
    setTimeout(function() { el.style.display = 'none'; }, 4000);
}

function planPath() {
    var target = document.getElementById('target-course-select').value;
    if (!target) { _showPathErr('请先选择目标课程'); return; }

    var btn = document.getElementById('btn-plan');
    btn.disabled = true;
    document.getElementById('path-loading').style.display = 'block';
    document.getElementById('path-result').style.display = 'none';
    document.getElementById('path-error').style.display = 'none';
    document.getElementById('path-legend-bar').style.display = 'none';

    setTimeout(function() {
        var result = plan(target);
        btn.disabled = false;
        document.getElementById('path-loading').style.display = 'none';

        if (result.exists) {
            _showResult(result);
            _highlightPath(result);
            document.getElementById('path-legend-bar').style.display = 'block';
        } else {
            _showPathErr(result.error || '路径规划失败');
        }
    }, 100);
}

function _showResult(data) {
    var cp = data.critical_path.join(' <span class="cp-arrow">→</span> ');
    document.getElementById('cp-text').innerHTML = cp;
    document.getElementById('cp-stat').textContent =
        '共 ' + data.total_semesters + ' 学期 · ' + data.critical_path_length + ' 步关键路径 · ' + data.total_courses_needed + ' 门课';

    var html = '';
    data.semester_plan.forEach(function(sem) {
        html += '<div class="sem-item"><span class="sem-num">第' + sem.semester + '学期</span> ';
        html += '<span>(' + sem.count + '门) ' + sem.courses.join('、') + '</span></div>';
    });
    document.getElementById('sem-plan').innerHTML = html;
    document.getElementById('path-result').style.display = 'block';
}

function _highlightPath(data) {
    _cpNodes = {};
    data.critical_path.forEach(function(name) { _cpNodes[name] = true; });

    var relNodes = {};
    if (data.all_prerequisites) {
        data.all_prerequisites.forEach(function(name) { relNodes[name] = 'pre'; });
    }
    relNodes[data.target] = 'target';

    var cpEdges = {};
    for (var i = 0; i < data.critical_path.length - 1; i++) {
        var from = data.critical_path[i];
        var to = data.critical_path[i + 1];
        cpEdges[to + '|||' + from] = true;
        cpEdges[from + '|||' + to] = true;
    }

    var svg = window._svg || d3.select('#svg1');
    svg.selectAll('.nodes circle').attr('class', function(d) {
        if (_cpNodes[d.name]) return 'cp-node';
        if (relNodes[d.name]) return 'pre-node';
        return 'inactive';
    });
    svg.selectAll('.texts text').attr('class', function(d) {
        if (_cpNodes[d.name]) return 'cp-text';
        if (relNodes[d.name]) return 'pre-text';
        return 'inactive';
    });
    svg.selectAll('.links line').attr('class', function(d) {
        var k1 = d.source.name + '|||' + d.target.name;
        var k2 = d.target.name + '|||' + d.source.name;
        if (cpEdges[k1] || cpEdges[k2]) return 'cp-edge';
        if (_cpNodes[d.source.name] && _cpNodes[d.target.name]) return 'pre-edge';
        return 'inactive';
    });
}

function clearPath() {
    _cpNodes = {};
    var svg = window._svg || d3.select('#svg1');
    svg.selectAll('.nodes circle').attr('class', '');
    svg.selectAll('.texts text').attr('class', '');
    svg.selectAll('.links line').attr('class', '');
    document.getElementById('path-result').style.display = 'none';
    document.getElementById('path-legend-bar').style.display = 'none';
}

// ── Search Q&A ─────────────────────────────────────────────────────
function doSearch() {
    var query = document.getElementById('question').value.trim();
    var answerEl = document.getElementById('answer');

    if (!query || query === '搜索') {
        answerEl.textContent = '请输入您的问题';
        answerEl.style.color = '#999';
        return;
    }

    // Find course name in query
    var matchedCourse = null;
    var matchedLen = 0;
    COURSES.forEach(function(c) {
        if (query.indexOf(c.name) >= 0 && c.name.length > matchedLen) {
            matchedCourse = c;
            matchedLen = c.name.length;
        }
    });

    if (!matchedCourse) {
        // Try partial matching
        COURSES.forEach(function(c) {
            if (matchedCourse) return;
            for (var i = 0; i < c.name.length - 1; i++) {
                for (var j = i + 2; j <= c.name.length; j++) {
                    var sub = c.name.substring(i, j);
                    if (sub.length >= 2 && query.indexOf(sub) >= 0 && sub.length > matchedLen) {
                        matchedCourse = c;
                        matchedLen = sub.length;
                    }
                }
            }
        });
    }

    if (!matchedCourse) {
        answerEl.innerHTML = '❌ 未识别出课程名称，请尝试输入完整课程名。<br><small style="color:#aaa;">示例：算法与数据结构是什么 / 操作系统原理的学分</small>';
        answerEl.style.color = '#ff6b6b';
        return;
    }

    var c = matchedCourse;
    var answer = '';
    var q = query.toLowerCase();

    // Intent detection
    if (q.indexOf('介绍') >= 0 || q.indexOf('是什么') >= 0 || q.indexOf('描述') >= 0 || q.indexOf('内容') >= 0 || (q.indexOf('什么是') >= 0)) {
        answer = '<b>' + c.name + '</b><br><br>' + c.details;
    } else if (q.indexOf('先修') >= 0 || q.indexOf('前置') >= 0 || q.indexOf('基础') >= 0 || q.indexOf('需要什么') >= 0) {
        buildAdjacency();
        var prereqs = _adj[c.name] || [];
        if (prereqs.length === 0) {
            answer = '<b>' + c.name + '</b> 没有先修课程（入口课程）';
        } else {
            answer = '<b>' + c.name + '</b> 的先修课程有：<br>' + prereqs.map(function(p) { return '• ' + p; }).join('<br>');
        }
    } else if (q.indexOf('学期') >= 0 || q.indexOf('什么时候') >= 0 || q.indexOf('开课') >= 0) {
        answer = '<b>' + c.name + '</b> 的开课学期是：<b>第 ' + c.semester + ' 学期</b>';
    } else if (q.indexOf('必修') >= 0 || q.indexOf('选修') >= 0 || q.indexOf('必须') >= 0) {
        answer = '<b>' + c.name + '</b> 是 <b>' + (c.optional === 'n' ? '必修课' : '选修课') + '</b>';
    } else if (q.indexOf('学分') >= 0 || q.indexOf('多少分') >= 0) {
        answer = '<b>' + c.name + '</b> 的学分是：<b>' + c.credit + '</b>';
    } else if (q.indexOf('学时') >= 0 || q.indexOf('课时') >= 0) {
        answer = '<b>' + c.name + '</b> 的学时是：<b>' + c.creditHour + '</b>';
    } else if (q.indexOf('编号') >= 0 || q.indexOf('id') >= 0 || q.indexOf('课号') >= 0 || q.indexOf('代码') >= 0) {
        answer = '<b>' + c.name + '</b> 的课程编号是：<b>' + c.id_num + '</b>';
    } else if (q.indexOf('英文') >= 0 || q.indexOf('english') >= 0) {
        answer = '<b>' + c.name + '</b> 的英文名称是：<b>' + c.englishName + '</b>';
    } else if (q.indexOf('老师') >= 0 || q.indexOf('教师') >= 0 || q.indexOf('谁教') >= 0 || q.indexOf('教授') >= 0) {
        answer = '<b>' + c.name + '</b> 的授课老师是：<b>' + c.teacher + '</b>';
    } else {
        // Default: show course overview
        answer = '<b>' + c.name + '</b><br>📖 ' + (c.optional === 'n' ? '必修' : '选修') + ' | ' + c.credit + ' | ' + c.creditHour + ' | 第' + c.semester + '学期<br>👨‍🏫 教师：' + c.teacher + '<br>🔢 编号：' + c.id_num + '<br>🌐 英文：' + c.englishName + '<br><br>' + c.details;
    }

    answerEl.innerHTML = answer;
    answerEl.style.color = '#fff';
    answerEl.style.background = 'rgba(0,0,0,0.4)';
    answerEl.style.padding = '16px 20px';
    answerEl.style.borderRadius = '8px';
    answerEl.style.textAlign = 'left';
}

// Handle Enter key on search
document.getElementById('question').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') doSearch();
});
</script>
</body>
</html>'''

# ── Write output file ───────────────────────────────────────────────
output_path = 'standalone.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Generated {output_path}')
print(f'Courses: {len(courses)}')
print(f'Prerequisites: {len(prereqs)}')

import os
size_kb = os.path.getsize(output_path) / 1024
print(f'File size: {size_kb:.1f} KB')
