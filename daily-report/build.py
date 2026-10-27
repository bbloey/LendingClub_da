#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建「每日日报」资料库页面：复用 p2p-handbook 的样式/交互骨架，注入 SQL 与实测结果。"""
import csv
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..", "p2p-handbook", "index.html")
SQL = os.path.join(HERE, "..", "..", "..", "..", "..", "Desktop", "项目", "P2P-SQL练习库", "渠道明细日报_9指标.sql")
SQL = r"C:/Users/14362/Desktop/项目/P2P-SQL练习库/渠道明细日报_9指标.sql"
CSV = r"C:/Users/14362/Desktop/项目/P2P-SQL练习库/渠道明细日报_2016-01-26_实测结果.csv"

base = open(BASE, encoding="utf-8").read()
sql = open(SQL, encoding="utf-8").read()

SEP = "-- ############################################################"


def seg(a, b):
    i = sql.index(a)
    j = sql.index(b, i)
    return sql[i:j].strip("\n ")


p_param = seg("-- 0. 参数", SEP + "\n-- 1. 主版本")
p_main = seg("-- 1. 主版本", SEP + "\n-- 2. 保骨架版")
p_skeleton = seg("-- 2. 保骨架版", SEP + "\n-- 3. 总量对账")
p_check = seg("-- 3. 总量对账", SEP + "\n-- 4. 可选替换")
p_ext = seg("-- 4. 可选替换", SEP + "\n-- 5. 口径说明")

CODE_MAIN = p_param + "\n\n" + p_main
CODE_SKEL = p_skeleton
CODE_CHECK = p_check
CODE_EXT = p_ext


def esc(t):
    return html.escape(t, quote=False)


def codeblock(name, code, caption=""):
    cap = '<div class="cap">%s</div>' % caption if caption else ""
    return (
        '<div class="code">'
        '<div class="code-bar"><span class="lights"><i></i><i></i><i></i></span>'
        '<span class="file">%s</span>'
        '<button class="copy" type="button">复制</button></div>'
        "<pre><code>%s</code></pre>%s</div>" % (name, esc(code), cap)
    )


# ---------- 实测结果表 ----------
rows = list(csv.reader(open(CSV, encoding="utf-8-sig")))
head, body = rows[0], rows[1:]
trs = []
for r in body:
    tds = ["<td>%s</td>" % esc(r[0])]
    for c in r[1:]:
        tds.append('<td class="n">%s</td>' % esc(c))
    trs.append("<tr>" + "".join(tds) + "</tr>")
res_table = (
    '<div class="table-wrap"><table class="res-table"><thead><tr>'
    + "".join('<th class="%s">%s</th>' % ("" if i == 0 else "n", esc(h)) for i, h in enumerate(head))
    + "</tr></thead><tbody>"
    + "".join(trs)
    + "</tbody></table></div>"
)
n_rows = len(body)

# ---------- 侧边栏 ----------
NAV = """    <p class="nav-group">开始</p>
    <a class="nav-link is-active" href="#overview"><i class="dot"></i>这条日报是什么</a>
    <a class="nav-link" href="#run"><i class="dot"></i>怎么跑起来</a>
    <p class="nav-group">指标</p>
    <a class="nav-link" href="#metrics"><i class="dot"></i>9 个指标的口径</a>
    <p class="nav-group">SQL</p>
    <a class="nav-link" href="#sql-main"><i class="dot"></i>主版本（CTE）</a>
    <a class="nav-link" href="#sql-skeleton"><i class="dot"></i>保骨架版（9 层 JOIN）</a>
    <a class="nav-link" href="#sql-check"><i class="dot"></i>总量对账</a>
    <a class="nav-link" href="#sql-ext"><i class="dot"></i>可选扩展指标</a>
    <p class="nav-group">排错</p>
    <a class="nav-link" href="#bugs"><i class="dot"></i>原模板 5 个语法坑</a>
    <a class="nav-link" href="#caliber"><i class="dot"></i>3 处口径问题</a>
    <p class="nav-group">结果</p>
    <a class="nav-link" href="#result"><i class="dot"></i>2016-01-26 实测</a>
    <a class="nav-link" href="#notes"><i class="dot"></i>口径说明</a>"""

# ---------- 正文 ----------
CONTENT = """
<div class="hero">
  <div class="hero-grid">
    <div>
      <div class="eyebrow">Daily report · 渠道明细</div>
      <h1>每日<em>日报</em></h1>
      <p class="hero-sub">一条 SQL 出 9 个指标：当日注册、绑卡、新客首投、新客交易、当日交易总额，再加三项累计。基于 <code>p2p_learning</code> 库，按 MySQL 8 默认模式（<code>ONLY_FULL_GROUP_BY</code> 开启）可直接执行。</p>
      <div class="tags">
        <span class="chip">MySQL 8.0.39 实测通过</span>
        <span class="chip plain">9 指标</span>
        <span class="chip plain">34 个渠道</span>
        <span class="chip plain">两版结果逐行一致</span>
      </div>
    </div>
    <div class="code-card">
      <div class="code-bar"><span class="lights"><i></i><i></i><i></i></span><span class="file">投资口径三件套</span></div>
      <pre><code>WHERE biztype IN (1, 3)   <span class="sql-c">-- 理财 + 点点宝</span>
  AND inouttype = 1       <span class="sql-c">-- 流入</span>
  AND `status` = 20       <span class="sql-c">-- 成功</span></code></pre>
      <div class="cap">缺一条，金额与人数至少错一项</div>
    </div>
  </div>
</div>

<section id="overview">
  <h2><span class="num">01</span>这条日报是什么</h2>
  <p class="lead">原始模板用 9 层 <code>LEFT JOIN</code> 把渠道维度摊成一张日报，但只写到第 4 段、且按 MySQL 5.x 的非严格模式写的。本页把 9 个指标补全，并给出两版都能在 MySQL 8 上跑的写法。</p>
  <div class="stats">
    <div class="stat"><b>9<span>个</span></b><small>指标 · 当日 6 + 累计 3</small></div>
    <div class="stat"><b>5<span>处</span></b><small>语法坑 · 其中 3 处直接 1055</small></div>
    <div class="stat"><b>3<span>处</span></b><small>口径坑 · 数字会错但不报错</small></div>
    <div class="stat"><b>34<span>行</span></b><small>2016-01-26 实测渠道数</small></div>
  </div>
  <div class="note tip"><div class="body">
    <p><strong>两种写法，结果一致。</strong>主版本用 CTE，每个指标先聚到 <code>channel</code> 唯一再 JOIN，加指标只需加一段；保骨架版保留 <code>xxx + aaa..iii</code> 的 9 层 LEFT JOIN，用来和原脚本逐段对照。两版 34 行、10 列全部逐值相同。</p>
  </div></div>
</section>

<section id="run">
  <h2><span class="num">02</span>怎么跑起来</h2>
  <p class="lead">只需要改日期。库名、表名、字段名都已按 <code>schema.sql</code> 对齐，不依赖 v2 补全脚本新增的列。</p>
  {param_block}
  <div class="note warn"><div class="body">
    <p><strong>先改一处库名。</strong><code>v2_数据补全.sql</code> 第 7 行写的是 <code>USE tianchi_userbehavior;</code>，那是从原天池脚本带过来的遗留，库实际叫 <code>p2p_learning</code>。不改直接跑会报 <code>Unknown database</code>。</p>
  </div></div>
  <div class="note"><div class="body">
    <p><strong>导数据的字符集。</strong>命令行导入 <code>data.sql</code> 时加 <code>--default-character-set=utf8mb4</code>，否则 Windows 默认 GBK 会在 <code>itemtitle</code> 上报 <code>ERROR 1366</code>。</p>
  </div></div>
</section>

<section id="metrics">
  <h2><span class="num">03</span>9 个指标的口径</h2>
  <p class="lead">列名直接按原模板的占位符顺序：前 4 个模板已给定义，后 5 个（eee / fff / ggg / hhh / iii）在原模板里能看到注释，按注释还原。</p>
  <div class="table-wrap"><table class="dict">
    <thead><tr><th>#</th><th>列名</th><th>口径</th><th>取数</th><th>易错</th></tr></thead>
    <tbody>
      <tr><td>01</td><td>当日注册人数</td><td><code>registtime</code> 落在日报日</td><td><code>account</code></td><td><code>date()</code> 包列索引失效</td></tr>
      <tr><td>02</td><td>当日绑卡人数</td><td>绑卡成功 <code>status=20</code></td><td><code>account_independent_authentication</code></td><td>别用充值代替，实测差 5.8 倍</td></tr>
      <tr><td>03</td><td>当日新客数</td><td>当日有成功投资 且 此前从未成功投资</td><td><code>da_account_trade</code></td><td><code>NOT IN</code> 遇 NULL 整列变空</td></tr>
      <tr><td>04</td><td>新客首投金额</td><td>每人取当日<strong>第一笔</strong></td><td><code>da_account_trade</code></td><td>原模板取的是"任意一笔"</td></tr>
      <tr><td>05</td><td>新客交易额</td><td>新客当日<strong>全部</strong>成功投资</td><td><code>da_account_trade</code></td><td>与 04 的差 = 当日多笔部分</td></tr>
      <tr><td>06</td><td>当日交易总额</td><td>新老客全量</td><td><code>da_account_trade</code></td><td>四列相加，漏 <code>assetamount</code> 会低估</td></tr>
      <tr><td>07</td><td>累计注册人数</td><td><code>registtime &lt; @cum_end</code></td><td><code>account</code></td><td>原模板写死 01-29，与日报日错位</td></tr>
      <tr><td>08</td><td>累计交易人数</td><td>累计去重人数</td><td><code>da_account_trade</code></td><td><code>count(*)</code> 必须先按人去重</td></tr>
      <tr><td>09</td><td>累计交易总额</td><td><code>createtime &lt; @cum_end</code></td><td><code>da_account_trade</code></td><td>同 06 的四列相加</td></tr>
    </tbody>
  </table></div>
  <div class="note"><div class="body">
    <p>「累计」截止日统一取 <code>@cum_end = @dt + 1 天</code>，即累计到日报日结束。想改成"截至昨日"，把它设成 <code>@dt</code> 即可。</p>
  </div></div>
</section>

<section id="sql-main">
  <h2><span class="num">04</span>主版本：CTE</h2>
  <p class="lead">参数 + 6 段 CTE + 一次 LEFT JOIN。每个 CTE 已经聚到 <code>channel</code> 唯一，所以不会放大行数；没有数据的渠道用 <code>COALESCE</code> 显示 0，导 Excel 后直接求和不会报错。</p>
  {main_block}
  <div class="note tip"><div class="body">
    <p><strong>为什么用 CTE 而不是 9 层 JOIN。</strong>同一张 <code>da_account_trade</code> 在骨架版里被扫了 5 遍（新客人数、首投金额、新客金额、当日金额、累计人数、累计金额），CTE 版可以合并到 2 遍。<code>new_user</code> 那段把「当日有没有交易」和「历史上有没有交易」拆成两层，是为了让 <code>ROW_NUMBER</code> 只跑一次。</p>
  </div></div>
</section>

<section id="sql-skeleton">
  <h2><span class="num">05</span>保骨架版：9 层 LEFT JOIN</h2>
  <p class="lead">结构与原模板一模一样：<code>xxx</code> 做渠道全集，<code>aaa..iii</code> 依次挂 9 个指标。只改报错和口径，不改结构，方便和老脚本一行一行对照。</p>
  {skel_block}
  <div class="note warn"><div class="body">
    <p><strong>这段前面为什么要重复两个 CTE。</strong><code>WITH</code> 的作用域只到当前这一条语句结束，主版本定义的 <code>day_tx</code> / <code>new_user</code> 到第 5 段已经失效，直接引用会报 <code>Table 'p2p_learning.day_tx' doesn't exist</code>（1146）。所以骨架版自己带一份定义。</p>
  </div></div>
</section>

<section id="sql-check">
  <h2><span class="num">06</span>总量对账</h2>
  <p class="lead">日报上线前跑一次：这 7 个全表直算值，必须分别等于上面各列的纵向求和。差一个数就说明某列少算或重复算了。</p>
  {check_block}
  <div class="note"><div class="body">
    <p>本库 2016-01-26 的对账结果：注册 <strong>32</strong>、绑卡 <strong>35</strong>、当日交易人数 <strong>31</strong>、当日交易总额 <strong>67,984.24</strong>、累计注册 <strong>10,840</strong>、累计交易人数 <strong>4,749</strong>、累计交易总额 <strong>43,695,791.45</strong>，与分渠道求和全部相等。</p>
  </div></div>
</section>

<section id="sql-ext">
  <h2><span class="num">07</span>可选扩展指标</h2>
  <p class="lead">日报列不够用时按需取用。前三条是直接加计算列，第四条是独立片段。</p>
  {ext_block}
</section>

<section id="bugs">
  <h2><span class="num">08</span>原模板 5 个语法坑</h2>
  <p class="lead">前 3 条在 MySQL 8 默认模式下直接报 1055，第 4 条会让整列变空，第 5 条只是慢。以下报错都是本机 8.0.39 实跑出来的原文。</p>
  <ol class="traps">
    <li class="is-new"><b>ddd 子查询：多列 + <code>GROUP BY 1</code></b><span class="badge">1055</span><br>
      原写法 <code>SELECT accountid, amount, assetamount, ... GROUP BY 1</code>，只有 <code>accountid</code> 在 GROUP BY 里。<br>
      <code>ERROR 1055: Expression #2 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'p2p_learning.da_account_trade.amount'</code><br>
      改法：按人 <code>SUM()</code> 聚合，首笔用 <code>ROW_NUMBER() OVER (PARTITION BY accountid ORDER BY createtime, tradeid) = 1</code>。</li>
    <li><b>hhh 子查询：同一个写法</b><span class="badge">1055</span><br>
      累计交易人数也是 <code>SELECT accountid, amount, ... GROUP BY 1</code>。改法：直接 <code>COUNT(DISTINCT accountid)</code>，语义等价且合法。</li>
    <li><b>最外层 <code>GROUP BY 1</code></b><span class="badge">1055</span><br>
      <code>SELECT xxx.channel, aaa.count, ... GROUP BY 1</code>，其余 9 列都是派生表列、不是聚合函数，MySQL 8 会拒绝：<code>... contains nonaggregated column 'aaa.cnt'</code>。而且每个子查询已经按 channel 唯一，这个 GROUP BY 本来就不需要，删掉即可。</li>
    <li><b><code>NOT IN (子查询)</code></b><span class="badge">逻辑</span><br>
      子查询里只要有一行 <code>accountid IS NULL</code>，<code>NOT IN</code> 恒为 UNKNOWN，整个条件变空、新客数直接归零，而且不报错。改 <code>NOT EXISTS</code> 或 <code>NOT IN (... WHERE accountid IS NOT NULL)</code>。</li>
    <li><b><code>date(createtime) = '2016-01-26'</code></b><span class="badge">性能</span><br>
      函数包住索引列，<code>idx_time</code> 用不上，全表扫。改半开区间 <code>createtime &gt;= @dt AND createtime &lt; @dt + INTERVAL 1 DAY</code>，结果完全一样。</li>
  </ol>
</section>

<section id="caliber">
  <h2><span class="num">09</span>3 处口径问题</h2>
  <p class="lead">这三条不报错，但数字会不对，比语法坑更值得先对齐。</p>
  <div class="table-wrap"><table>
    <thead><tr><th>问题</th><th>原模板</th><th>后果</th><th>本页处理</th></tr></thead>
    <tbody>
      <tr><td>累计截止日错位</td><td>日报日 <code>2016-01-26</code>，累计写 <code>&lt; '2016-01-29'</code></td><td>累计指标多算 3 天，和当日口径对不上</td><td>统一 <code>@cum_end = @dt + 1 天</code>，要改只改一处</td></tr>
      <tr><td>用充值代替绑卡</td><td><code>biztype=4 AND inouttype=1</code></td><td>漏掉"绑卡了但当天没充值"的人。本库同日实测：绑卡表 <strong>35 人</strong>，充值口径只有 <strong>6 人</strong></td><td>改用 <code>account_independent_authentication</code>；想保原口径，替换片段在扩展节</td></tr>
      <tr><td>ddd 与 eee 语义重叠</td><td>ddd 注释"首次交易金额"，实现却是每人取任意一笔</td><td>ddd 可能大于也可能小于 eee，无法解释</td><td>04 明确为首笔、05 明确为当日合计，正常满足 04 ≤ 05</td></tr>
    </tbody>
  </table></div>
</section>

<section id="result">
  <h2><span class="num">10</span>2016-01-26 实测结果</h2>
  <p class="lead">在临时 MySQL 8.0.39 实例上导入 <code>schema.sql</code> + <code>data.sql</code> 后跑出来的原始结果，{n_rows} 个渠道全部返回，没有 NULL。</p>
  {res_table}
  <div class="note warn"><div class="body">
    <p><strong>当天数据偏薄。</strong>合成数据里 2 万用户摊到约 600 天，单渠道当日注册多在 0~6 人，新客常常只有 1~2 人。<strong>看量级建议换成 <code>2015-12-12</code></strong>（双十二，当天带日期的记录约是 01-26 的 1.5 倍），SQL 只改 <code>@dt</code> 一行。</p>
  </div></div>
</section>

<section id="notes">
  <h2><span class="num">11</span>口径说明</h2>
  <p class="lead">对外解释这张表时可以直接抄的部分。</p>
  <ul>
    <li><strong>渠道归因</strong>：全部按注册渠道 <code>account.channel</code>。不要混用 <code>da_account_trade.channel</code>，那是交易发生渠道，两者不同源。</li>
    <li><strong>当日</strong>：<code>[dt, dt+1)</code> 半开区间，不写 <code>DATE(createtime)=dt</code>。</li>
    <li><strong>新客</strong>：当日有成功投资，且该用户历史上没有成功投资。「历史上」用 <code>&lt; @dt</code>，不含当日，所以当日多笔仍算新客。</li>
    <li><strong>首投金额</strong>：该用户当日第一笔（按 <code>createtime, tradeid</code> 排序）的金额；新客交易额是该用户当日全部成功投资金额。</li>
    <li><strong>人数</strong>：全部 <code>COUNT(DISTINCT accountid)</code>，一人多笔只算 1 人。</li>
    <li><strong>金额</strong>：<code>amount + assetamount + bonusamount + couponamount</code> 四列相加。点点宝余额支付走 <code>assetamount</code>，漏掉会低估。</li>
    <li><strong>重叠不算错</strong>：同一用户当日既注册又首投，会同时进「注册人数」和「新客数」，漏斗指标允许重叠。</li>
  </ul>
</section>
"""

CONTENT = CONTENT.format(
    param_block=codeblock("params.sql", p_param, "改日期只动第一行；@cum_end 单独可控"),
    main_block=codeblock("channel_daily_cte.sql", CODE_MAIN, "主版本：参数 + CTE + 一次 LEFT JOIN，可直接整段执行"),
    skel_block=codeblock("channel_daily_join.sql", CODE_SKEL, "保骨架版：与主版本结果逐行一致，只是写法保持原样"),
    check_block=codeblock("reconcile.sql", CODE_CHECK, "7 个全表直算值，与各列纵向求和比对"),
    ext_block=codeblock("extend.sql", CODE_EXT, "转化率 / 复投 / 回款 / 净流入"),
    res_table=res_table,
    n_rows=n_rows,
)

# ---------- 组装 ----------
out = base

out = re.sub(r"<title>.*?</title>", "<title>每日日报</title>", out, count=1)
out = re.sub(
    r'<meta name="description" content=".*?">',
    '<meta name="description" content="P2P 渠道明细日报：9 个指标的完整 SQL（CTE 版 + 9 层 LEFT JOIN 版）、口径说明、原模板 5 个语法坑与 3 处口径问题，MySQL 8 实测通过。">',
    out,
    count=1,
)
out = re.sub(
    r'<script type="application/ld\+json">.*?</script>',
    '<script type="application/ld+json">\n'
    '{"@context":"https://schema.org","@type":"TechArticle","headline":"每日日报",'
    '"about":"P2P 数仓渠道明细日报 SQL","inLanguage":"zh-CN"}\n</script>',
    out,
    count=1,
)

out = out.replace(
    '<strong>变量查询手册</strong>\n        <span>p2p_learning · MySQL 8</span>',
    '<strong>每日日报</strong>\n        <span>channel_daily · MySQL 8</span>',
)
out = out.replace('<div class="brand-mark">P2P</div>', '<div class="brand-mark">日报</div>')
out = out.replace(
    '<b>数据 100% 合成</b><br>无真实用户信息 · 仅用于练 SQL',
    "<b>9 指标 · 已实测</b><br>MySQL 8.0.39 · p2p_learning",
)

# nav
out = re.sub(r'<nav class="sb-nav" id="nav">.*?</nav>', '<nav class="sb-nav" id="nav">\n' + NAV + "\n  </nav>", out, flags=re.S)

# topbar
out = out.replace(
    '<span>资料库</span><span class="sep">/</span><span>P2P 练习库</span><span class="sep">/</span><b>变量查询手册</b>',
    '<span>资料库</span><span class="sep">/</span><span>P2P 练习库</span><span class="sep">/</span><b>每日日报</b>',
)
out = out.replace(
    '<span class="chip">v3.1</span>\n      <span class="chip plain">32 张表</span>',
    '<span class="chip">9 指标</span>\n      <span class="chip plain">MySQL 8.0</span>',
)

# 追加少量页面专用样式
extra_css = """
/* ---------- daily report ---------- */
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;font-family:var(--font-mono);font-size:12.4px;white-space:nowrap}
.res-table td:first-child{font-family:var(--font-mono);font-size:12.4px;white-space:nowrap;color:#22314d}
.traps code{white-space:normal;word-break:break-word}
table.dict td:nth-child(3){color:var(--ink-2)}
table.dict td:nth-child(5){color:var(--ink-3);font-size:12.6px}
@media (max-width:640px){ td.n,th.n{font-size:11.8px} }
</style>"""
out = out.replace("</style>", extra_css, 1)

# 主体内容（footer 在 main 内部，切点放在 footer 之前，保留页脚）
i = out.index('<div class="wrap">') + len('<div class="wrap">')
j = out.index("  <footer>")
out = out[:i] + "\n" + CONTENT + "\n  </div>\n\n" + out[j:]

# footer 文案
out = out.replace(
    '<p class="fb">P2P 数仓变量查询手册 v3.1</p>',
    '<p class="fb">每日日报 · 渠道明细</p>',
)
out = out.replace(
    "<p>配套 p2p_learning 练习库 · MySQL 8.0 · 数据 100% 合成，无任何真实用户信息</p>",
    "<p>SQL 与 <code>渠道明细日报_9指标.sql</code> 同步 · p2p_learning · 数据 100% 合成</p>",
)
out = out.replace(
    "snapshot 2016-01-11<br>\n        data range 2015-01 ~ 2016-08<br>\n        updated 2026-10-23",
    "report date 2016-01-26<br>\n        verified MySQL 8.0.39<br>\n        updated 2026-10-23",
)

open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
print("written", os.path.join(HERE, "index.html"), len(out), "chars")
print("sections:", len(re.findall(r'<section id="', out)), "nav links:", len(re.findall(r'class="nav-link', out)))
