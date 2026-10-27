#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建「一周作战计划」资料库页面：复用 p2p-handbook 的样式骨架。"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..", "p2p-handbook", "index.html")
base = open(BASE, encoding="utf-8").read()

NAV = """    <p class="nav-group">总览</p>
    <a class="nav-link is-active" href="#goal"><i class="dot"></i>这周要交出什么</a>
    <a class="nav-link" href="#week"><i class="dot"></i>一周时间表</a>
    <a class="nav-link" href="#daily"><i class="dot"></i>每天固定动作</a>
    <p class="nav-group">Day 1–4 · 出报告</p>
    <a class="nav-link" href="#d1"><i class="dot"></i>Day 1　地基：数据体检</a>
    <a class="nav-link" href="#d2"><i class="dot"></i>Day 2　日报：每日监控</a>
    <a class="nav-link" href="#d3"><i class="dot"></i>Day 3　月报：结构变化</a>
    <a class="nav-link" href="#d4"><i class="dot"></i>Day 4　年报：年度叙事</a>
    <p class="nav-group">Day 5–7 · 出作品</p>
    <a class="nav-link" href="#d5"><i class="dot"></i>Day 5　Power BI 看板</a>
    <a class="nav-link" href="#d6"><i class="dot"></i>Day 6　整合与包装</a>
    <a class="nav-link" href="#d7"><i class="dot"></i>Day 7　复盘与模拟面试</a>
    <p class="nav-group">附录</p>
    <a class="nav-link" href="#accept"><i class="dot"></i>验收标准</a>
    <a class="nav-link" href="#cut"><i class="dot"></i>时间不够怎么砍</a>
    <a class="nav-link" href="#interview"><i class="dot"></i>10 个面试题自测</a>"""


def day_head(no, title, goal, tone="accent"):
    return (
        '<div class="day-h">'
        '<div class="day-badge %s">Day %s</div>'
        "<div><h2 style=\"margin:0;border:0;padding:0\">%s</h2>"
        '<p class="day-goal">%s</p></div></div>' % (tone, no, title, goal)
    )


def time_table(rows):
    tr = "".join(
        "<tr><td class=\"tm\">%s</td><td>%s</td><td class=\"out\">%s</td></tr>" % r
        for r in rows
    )
    return (
        '<div class="table-wrap"><table class="time"><thead><tr>'
        "<th>时段</th><th>任务</th><th>产出</th></tr></thead><tbody>"
        + tr
        + "</tbody></table></div>"
    )


def drill(items):
    li = "".join("<li>%s</li>" % i for i in items)
    return (
        '<div class="drill"><div class="drill-h">SQL 练习 · 不看答案自己写</div>'
        "<ol>%s</ol></div>" % li
    )


def think(q):
    return '<div class="think"><b>业务思考</b><p>%s</p></div>' % q


def deliver(items):
    li = "".join("<li>%s</li>" % i for i in items)
    return (
        '<div class="deliver"><div class="drill-h">今日交付物</div>'
        "<ul>%s</ul></div>" % li
    )


CONTENT = """
<div class="hero">
  <div class="hero-grid">
    <div>
      <div class="eyebrow">7-day sprint · 作品集冲刺</div>
      <h1>一周<em>作战计划</em></h1>
      <p class="hero-sub">目标不是"跑完 27 条 SQL"，而是<strong>一周后手里有一份能放进作品集的经营分析报告</strong>：日报、月报、年报各一份，配一套 Power BI 看板，外加一段能写进简历的项目描述。基于 <code>p2p_learning</code> 库，2 万用户 / 20 个月。</p>
      <div class="tags">
        <span class="chip">每天 5.5 小时</span>
        <span class="chip plain">3 份报告</span>
        <span class="chip plain">1 套看板</span>
        <span class="chip plain">7 个交付文件</span>
      </div>
    </div>
    <div class="code-card">
      <div class="code-bar"><span class="lights"><i></i><i></i><i></i></span><span class="file">一周成果物</span></div>
      <pre><code>P2P经营分析报告.pdf   <span class="sql-c">-- 主交付</span>
p2p_dashboard.pbix    <span class="sql-c">-- 看板</span>
data_quality_check.sql<span class="sql-c">-- 体检</span>
daily / monthly / annual.sql
简历-项目段落.md</code></pre>
      <div class="cap">七个文件，缺一个都不算完成</div>
    </div>
  </div>
</div>

<section id="goal">
  <h2><span class="num">01</span>这周要交出什么</h2>
  <p class="lead">先说清优先级。你要的是"找到数据分析师工作"，所以判断标准只有一个：<strong>面试官看到这份东西，会不会认为你干过真实的经营分析</strong>。SQL 写得再花，报告讲不出结论，价值减半。</p>
  <div class="stats">
    <div class="stat"><b>1<span>份</span></b><small>主报告 · 15–20 页 PDF</small></div>
    <div class="stat"><b>3<span>层</span></b><small>日 / 月 / 年三个粒度</small></div>
    <div class="stat"><b>1<span>套</span></b><small>Power BI · 3 页看板</small></div>
    <div class="stat"><b>6<span>类</span></b><small>数据质量校验 SQL</small></div>
  </div>
  <div class="note tip"><div class="body">
    <p><strong>三层报告的分工，别写成三份一样的。</strong>日报回答「昨天发生了什么」，是<em>监控</em>；月报回答「这个月和上个月哪里不一样」，是<em>结构</em>；年报回答「这一年我们做对了什么、错在哪」，是<em>叙事</em>。三份报告的分析方法完全不同，这也正是面试官想看的区分度。</p>
  </div></div>
  <div class="note warn"><div class="body">
    <p><strong>先接受一个前提：这份数据的样本量撑不起"日报"。</strong>2 万用户摊到 609 天，日均注册约 33 人，单渠道日均不到 1 人。所以 Day 2 的日报重点是<strong>报表结构与口径</strong>，不是业务结论；真要看趋势，用周或月做窗口。在报告里主动写清这一点，反而是加分项——说明你知道粒度和样本量的关系。</p>
  </div></div>
</section>

<section id="week">
  <h2><span class="num">02</span>一周时间表</h2>
  <p class="lead">每天三块：上午写 SQL（2 小时）、下午出报告（2.5 小时）、晚上复盘（30 分钟）。周末两天用来整合和打磨，不安排新内容。</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Day</th><th>主题</th><th>核心动作</th><th>当天产出</th></tr></thead>
    <tbody>
      <tr><td><b>1</b></td><td>地基</td><td>数据体检 + 修复时间因果</td><td>体检报告 + 校验 SQL</td></tr>
      <tr><td><b>2</b></td><td>日报</td><td>9 指标宽表 + 口径对齐</td><td>日报 SQL + 模板</td></tr>
      <tr><td><b>3</b></td><td>月报</td><td>同环比 + 结构拆解</td><td>月报 SQL + 8 月页</td></tr>
      <tr><td><b>4</b></td><td>年报</td><td>Cohort 留存 + 帕累托</td><td>年报 SQL + 10 页</td></tr>
      <tr><td><b>5</b></td><td>看板</td><td>星型建模 + 三页布局</td><td>.pbix</td></tr>
      <tr><td><b>6</b></td><td>整合</td><td>合成主报告 + 简历段落</td><td>PDF + 简历</td></tr>
      <tr><td><b>7</b></td><td>复盘</td><td>盲测新数据 + 面试自测</td><td>复盘笔记</td></tr>
    </tbody>
  </table></div>
  <div class="note"><div class="body">
    <p><strong>文件按这个结构放，最后一天不用再整理：</strong><code>01_体检 / 02_日报 / 03_月报 / 04_年报 / 05_看板 / 06_作品集</code>，每个目录里 SQL 和报告放一起。</p>
  </div></div>
</section>

<section id="daily">
  <h2><span class="num">03</span>每天固定动作</h2>
  <p class="lead">比任务本身更重要的是这个节奏，它决定你能不能在一周后还有力气整合。</p>
  <ul>
    <li><strong>开工 10 分钟</strong>：把当天要交的 3 个文件写在纸上，贴屏幕边。写完一条划一条。</li>
    <li><strong>收工 10 分钟</strong>：写三行——今天学会了什么、卡在哪、明天第一件事做什么。这三行是 Day 7 复盘的原料。</li>
    <li><strong>遇到卡壳 20 分钟规则</strong>：一个问题卡超过 20 分钟就记下来跳过，别让它吃掉整块时间。晚上统一查。</li>
    <li><strong>不留未保存的 SQL</strong>：所有写过的查询都存成文件，哪怕是废稿。报告里的每个数字后面都要能追到一条 SQL。</li>
  </ul>
</section>

<section id="d1">
  """ + day_head("1", "地基：先证明数据能不能用", "今天不产出任何业务结论，只做一件事——搞清楚这份数据哪些能信、哪些不能信，并把时间因果修好。") + """
  <p class="lead">昨天我们已经查出来：<strong>84.7% 的投资用户，首投时间早于注册时间</strong>（中位差 −203 天），根因是 <code>gen_data.py</code> 第 178 行把交易时间按全局随机撒了，没绑注册日。不修这个，你后面三份报告里所有"转化"类指标全是错的。</p>
  """ + time_table([
      ("09:00–09:30", "建库导入，跑通 3 条探索查询（月度注册 / 全站漏斗 / 12-31 留存）", "库就绪"),
      ("09:30–11:00", "写 6 类数据质量校验 SQL", "data_quality_check.sql"),
      ("11:00–12:00", "改 gen_data.py 三处，重跑重导", "data_v2.sql"),
      ("14:00–15:30", "复测：6 类检查全部归零", "复测结果截图"),
      ("15:30–17:00", "写《数据质量体检报告》一页", "体检报告.md"),
      ("20:00–20:30", "业务思考题", "笔记三行"),
  ]) + """
  """ + drill([
      "找出「首次成功投资时间早于注册时间」的用户数，以及时间差的中位数。提示：先取每人 <code>MIN(createtime)</code>，再和 <code>registtime</code> 比。",
      "统计绑卡表里 <code>createtime &gt; '2016-08-31'</code> 的记录数。再查 <code>account_partner_trade</code> 的日期范围。这两个越界要出现在你的体检报告里。",
      "同一件事两套口径：<code>account_independent_authentication</code> 里的绑卡人数 vs <code>account.iDdate IS NOT NULL</code> 的人数，差多少？哪个更可信、为什么？",
      "找出交易表里 <code>accountid</code> 不在 <code>account</code> 表的孤儿记录（用 <code>LEFT JOIN ... IS NULL</code> 和 <code>NOT EXISTS</code> 各写一遍，比较执行计划）。",
      "检查金额异常：<code>amount &lt;= 0</code>、四列金额全为 0、以及 <code>amount &gt; 1000000</code> 的记录各有多少条。",
      "勾稽检查：取 <code>2016-08-31</code> 的余额快照总和，和「累计充值 − 累计提现 − 累计投资 + 累计回款」比，差多少？解释为什么对不上。",
  ]) + """
  <div class="note"><div class="body">
    <p><strong>修数据只改三处，别重写整个脚本。</strong>① 交易 <code>createtime</code> = 注册时间 + 随机的 0–45 天（首投），后续笔数按 15–90 天间隔累加；② 回款日期 = 投资日 + <code>selfitem.totalperiods</code> 对应的天数，不再固定 +90；③ 渠道按质量分三档给不同的首投率（应用商店高、信息流低）。改完重跑 <code>python gen_data.py</code>，重新导入。</p>
  </div></div>
  """ + think("老板问：「我们 2 万注册用户里有 26% 投资了，这个转化率可信吗？」你要能在 30 秒内答出三件事：分子分母各是什么、哪张表是权威来源、这个数在行业里算高还是低。想清楚再往下做——这份答案会直接变成你报告里「数据说明」那一节。") + """
  """ + deliver([
      "<code>01_体检/data_quality_check.sql</code>——6 类检查，每类一条 SQL，注释写清预期值和实际值",
      "<code>01_体检/数据质量体检报告.md</code>——一页：发现的 5 个问题、影响哪些指标、怎么处理",
      "修复后的 <code>p2p_learning</code> 库（重跑过的 data.sql）",
      "当晚三行复盘",
  ]) + """
  <div class="note tip"><div class="body">
    <p><strong>今天这份体检报告，是你整周最容易被面试官记住的东西。</strong>大部分候选人的项目是"我写了 SQL 得出 XX 结论"；你能说"我接手后发现首投时间有 85% 早于注册时间，定位到是生成脚本没绑关联键，修复后重算"——这句话证明你懂数据是怎么来的，而不只是会查。</p>
  </div></div>
</section>

<section id="d2">
  """ + day_head("2", "日报：每天必看的 9 个数", "把 9 指标日报从零写一遍（不许看现成答案），然后做成一张能每天填的模板。") + """
  <p class="lead">昨天修完数据，今天第一件事是<strong>合上之前那份 <code>渠道明细日报_9指标.sql</code>，自己重写</strong>。写不出来再看，看的时候重点看它为什么用 CTE 而不是 9 层 JOIN。</p>
  """ + time_table([
      ("09:00–10:30", "不看答案重写 9 指标日报", "daily_report.sql"),
      ("10:30–12:00", "加环比列（对比昨日），两版写法比对", "含 MoM 的版本"),
      ("14:00–15:30", "做日报模板（Excel），含异常标注规则", "日报模板.xlsx"),
      ("15:30–17:00", "跑 3 天（平日 / 双十二 / 月末）并写当日结论", "3 份日报"),
      ("20:00–20:30", "业务思考题", "笔记三行"),
  ]) + """
  """ + drill([
      "9 个指标：当日注册、当日绑卡、当日首投人数、首投金额、当日交易额、当日交易人数，加累计注册、累计交易人数、累计交易额。每人金额统一用 <code>amount + assetamount + bonusamount + couponamount</code>。",
      "给每个指标加「较昨日」列。用 <code>LAG(...) OVER (ORDER BY stat_date)</code>，先把日报跑成一张按日汇总的表，再在外面套一层窗口函数。",
      "算「注册 → 绑卡 → 首投」三级转化率，分母统一用当日注册人数。注意分母不能用「当日绑卡人数」，否则分子分母不同源。",
      "找出当日「注册且当天首投」的用户，他们贡献了多少交易额？占比多少？这才是渠道质量的真实信号。",
      "给日报加一个异常标记列：任一指标环比波动超过 ±30% 就标 1。想想为什么阈值要按指标分开设，而不是都设 30%。",
  ]) + """
  """ + think("9 个指标里如果只能留 3 个，你留哪 3 个？说清楚各自的“看什么、异常了怎么办”。这道题在面试里几乎必问，因为它考的是你有没有真的每天看数——而不是会不会写 SQL。") + """
  """ + deliver([
      "<code>02_日报/daily_report.sql</code>——自己写的版本，和之前那份对比差异",
      "<code>02_日报/日报模板.xlsx</code>——表头 + 3 天样例 + 异常标注规则说明",
      "3 天的日报结果，每份配一句话结论（不超过 40 字）",
  ]) + """
  <div class="note warn"><div class="body">
    <p><strong>写结论时管住手。</strong>日均注册 33 人，单渠道不到 1 人，"某渠道今日注册暴涨 300%"这种结论多半是 1 个人变成 4 个人。日报结论只写方向性判断（如"双十二当日注册为平日 3 倍"），具体数字留给月报。这条自我约束写进报告，是专业度的直接体现。</p>
  </div></div>
</section>

<section id="d3">
  """ + day_head("3", "月报：从「多少」到「为什么」", "月报不是把 30 天的日报加起来。今天练的是拆结构：增长来自哪里、质量有没有变差。") + """
  <p class="lead">月度数据量刚好够做分析：月均注册 1,000 人左右，8 月最高 1,487，2015-12 大促 3,090。今天的核心产出是<strong>一张 12 列的月度宽表</strong>，和一篇能解释「8 月创新高是不是好事」的分析。</p>
  """ + time_table([
      ("09:00–10:30", "月度宽表：注册 / 活跃 / 投资 / 金额 / 复投率", "monthly_report.sql"),
      ("10:30–12:00", "同环比 + 结构占比 + 金额分层", "扩到 15 列"),
      ("14:00–15:30", "写 2016 年 8 月月报（一页 A4）", "2016-08月报.pdf"),
      ("15:30–17:00", "补 2016-01～08 八个月的趋势图", "趋势图 3 张"),
      ("20:00–20:30", "业务思考题", "笔记三行"),
  ]) + """
  """ + drill([
      "月度宽表：月新增注册、月活（App 打开去重人数）、月投资人数、月投资笔数、月交易额、月复投人数、复投率、人均投资额、人均笔数。一次 <code>GROUP BY DATE_FORMAT(dt,'%Y-%m')</code> 出全部。",
      "加环比：交易额、注册量、投资人数三个指标的 <code>LAG</code> 环比，以及 <code>SUM() OVER</code> 累计值。",
      "同期对比：2015 年 1–8 月 vs 2016 年 1–8 月，逐指标并排放。注意 2016 只有 8 个月，不要直接和 2015 全年比。",
      "结构拆解：把月交易额按 <code>biztype</code> 拆成定期（1）和活期（3），算各自占比及环比变化。活期占比上升意味着什么？",
      "金额分层：用 <code>CASE WHEN</code> 把单笔投资额分成 &lt;1k / 1k–5k / 5k–2w / &gt;2w 四档，算各档人数和金额占比。",
      "渠道结构：算 8 月各渠道注册占比，和 7 月比，找出占比变化最大的 3 个渠道。",
  ]) + """
  """ + think("8 月注册 1,487 人，是历史最高。这是好事吗？你要能用数据回答三问：新增的人有没有投资（转化率是升是降）、留下来没有（次月留存）、拉来的人贵不贵（单客首投额）。如果转化率在降而量在涨，说明什么？这条判断会直接进你报告的「核心结论」。") + """
  """ + deliver([
      "<code>03_月报/monthly_report.sql</code>——15 列月度宽表 + 3 个环比指标",
      "<code>03_月报/2016-08月报.pdf</code>——一页 A4，含 3 个结论 + 1 个建议",
      "趋势图 3 张（注册 / 交易额 / 复投率），用 Excel 或 Python 画都行",
  ]) + """
</section>

<section id="d4">
  """ + day_head("4", "年报：讲一个完整的故事", "年报的读者是管理层。今天练的不是取数，是「只讲三页，你讲哪三页」。") + """
  <p class="lead">年报最容易写成流水账。判断标准：<strong>随便翻到一页，能不能用一句话说出这页想证明什么</strong>。今天两个技术重点：Cohort 留存矩阵、帕累托分析，这两个是分析师简历里的高频词，必须自己写出来过。</p>
  """ + time_table([
      ("09:00–10:30", "年度 KPI + 2015 vs 2016 同期对比", "annual_report.sql"),
      ("10:30–12:00", "Cohort 留存矩阵（注册月 × 第 N 月）", "留存矩阵"),
      ("14:00–15:00", "帕累托 + 渠道四象限", "2 张图"),
      ("15:00–17:00", "年报 8–10 页，每页一句话结论", "年报.pptx"),
      ("20:00–20:30", "业务思考题", "笔记三行"),
  ]) + """
  """ + drill([
      "年度 KPI 表：注册、绑卡、首投、投资人数、交易额、复投率、人均投资额，2015 全年 vs 2016 前 8 月两列并排。",
      "Cohort 留存矩阵：行是注册月，列是第 0/1/3/6/12 个月是否活跃（App 打开）。用自连接 + <code>TIMESTAMPDIFF(MONTH, ...)</code>，输出成可以直接贴进 Excel 做热力图的格式。",
      "帕累托：按用户累计投资额降序，算前 1% / 5% / 10% / 20% 用户贡献的金额占比。用 <code>SUM() OVER (ORDER BY ...)</code> 算累计占比。",
      "渠道四象限：横轴注册量、纵轴首投率，找出「量大质优」「量大质差」「量小质优」「量小质差」各有哪些渠道。<em>注意：原始数据里渠道没有质量差异，必须用 Day 1 修复后的数据才算得出差别。</em>",
      "资金结构：按月算充值总额、提现总额、净流入，以及活期 vs 定期的持有结构变化。",
      "增长质量表：每月新增注册 vs 该批人 30 天内的首投率，看量涨的时候质有没有掉。",
  ]) + """
  """ + think("如果只能向 CEO 汇报 3 页，你选哪 3 页？提示：一页讲结果（我们做到了什么）、一页讲问题（哪里在漏）、一页讲下一步（建议做什么、看什么指标）。选完回头检查你的年报，有没有哪一页其实可以删——删不掉说明结构是对的。") + """
  """ + deliver([
      "<code>04_年报/annual_report.sql</code>——KPI + cohort + 帕累托 + 四象限",
      "<code>04_年报/年报.pptx</code>——8–10 页，每页一句话标题（标题即结论）",
      "留存矩阵热力图 + 渠道四象限散点图",
  ]) + """
  <div class="note tip"><div class="body">
    <p><strong>年报标题的写法，决定它像不像专业报告。</strong>不要写「8 月经营情况分析」，要写「8 月注册创新高，但首投转化率环比降 3 个点」。前者是目录，后者是结论。整份报告每一页标题都用这个句式，水平立刻不一样。</p>
  </div></div>
</section>

<section id="d5">
  """ + day_head("5", "Power BI：把 SQL 变成别人能点的东西", "今天不写新指标，只做一件事——把前四天的结论装进三页看板，让别人不问你也能自己看。") + """
  <p class="lead">顺序很重要：<strong>先建模，再画图</strong>。新手最常见的错误是直接拖字段画图，画到第三页发现数字对不上、筛选器联动错了，返工重来。</p>
  """ + time_table([
      ("09:00–10:00", "连 MySQL，Power Query 里加日期列，检查类型", "数据源就绪"),
      ("10:00–11:30", "建日期表 + 星型模型 + 关系", "模型视图截图"),
      ("11:30–12:00", "写 6 个基础度量值", "度量值列表"),
      ("14:00–16:00", "三页看板：总览 / 渠道 / 留存", "3 页截图"),
      ("16:00–17:00", "加切片器、联动、格式统一", ".pbix 成品"),
      ("20:00–20:30", "业务思考题", "笔记三行"),
  ]) + """
  <div class="note"><div class="body">
    <p><strong>连接 MySQL 的两个坑。</strong>① 需要先装 MySQL Connector/NET（或改用 ODBC 数据源），否则「获取数据」里选 MySQL 会报驱动缺失；② <code>createtime</code> 是 datetime，直接和日期表建关系会出问题——先在 Power Query 里加一个 <code>日期 = DateTime.Date([createtime])</code> 列，用它建关系。</p>
  </div></div>
  """ + drill([
      "<strong>日期表</strong>：<code>日期表 = CALENDAR(DATE(2015,1,1), DATE(2016,8,31))</code>，再补年、月、年月、周几四列。标记为日期表。",
      "<strong>六个度量值</strong>：注册用户数（<code>DISTINCTCOUNT</code>）、投资人数（<code>CALCULATE</code> + 三个筛选条件）、首投率（<code>DIVIDE</code>）、投资金额（四列相加）、复投率、环比（<code>CALCULATE</code> + <code>DATEADD</code>）。",
      "<strong>P1 总览页</strong>：4 个 KPI 卡（注册 / 投资人数 / 交易额 / 首投率）+ 月度趋势折线 + 年月切片器。",
      "<strong>P2 渠道页</strong>：漏斗图（注册→绑卡→首投）+ 渠道散点图（横轴注册量、纵轴首投率）+ 渠道明细表。",
      "<strong>P3 留存页</strong>：矩阵视觉对象做 cohort 热力图，行是注册月、列是第 N 月，值用条件格式上色。",
      "<strong>统一格式</strong>：所有金额用千分位、百分比保留 1 位小数、配色不超过 3 种、每页标题写成结论句。",
  ]) + """
  """ + think("这套看板是给谁看的？如果是给运营总监，他每天打开第一眼应该看到什么？如果给 CEO，第一页该砍掉哪些图？把你答案写下来，然后回去调整 P1 的布局——看板的价值不在于图多，而在于「不用解释就能看懂」。") + """
  """ + deliver([
      "<code>05_看板/p2p_dashboard.pbix</code>——三页，可用切片器联动",
      "三页截图各一张（放进最终报告附录）",
      "模型关系图截图（证明你懂星型模型，不是乱拖字段）",
  ]) + """
</section>

<section id="d6">
  """ + day_head("6", "整合：把七天的碎片拼成一份作品", "今天不写新分析，只做减法——把日/月/年三份东西合成一份 15–20 页的《P2P 理财 App 经营分析报告》。") + """
  <p class="lead">合成不是拼贴。主报告要有一条主线：<strong>这家平台在 20 个月里靠买量做到了规模，但增长质量在下降，钱留在了少数人手里</strong>。你的三层报告都是这条主线的证据。</p>
  """ + time_table([
      ("09:00–11:00", "定主报告结构，写第 1–3 章（背景 / 数据 / 结论）", "报告骨架"),
      ("11:00–12:00", "把三份分析填进第 4–6 章", "正文完成"),
      ("14:00–15:00", "写结论页与建议页（3 条结论 + 3 条建议）", "结论页"),
      ("15:00–16:00", "导 PDF，检查排版与图表清晰度", "报告.pdf"),
      ("16:00–17:00", "写简历项目段落 + GitHub README", "简历 + repo"),
      ("20:00–20:30", "通读一遍，删掉所有无结论的段落", "终稿"),
  ]) + """
  <div class="note"><div class="body">
    <p><strong>主报告建议结构（7 章）：</strong>① 业务背景与数据说明　② 数据质量与口径（放 Day 1 的体检结论）　③ 核心结论摘要（3 条，放最前面）　④ 增长分析（渠道 / 漏斗 / 留存）　⑤ 资金分析（投资额 / 结构 / 复投）　⑥ 问题诊断　⑦ 建议与附录（SQL + 看板截图）。</p>
  </div></div>
  """ + drill([
      "<strong>三条结论</strong>：每条必须包含「现象 + 数据 + 影响」。例：<em>2015-12 大促带来 3,090 注册，但该批人 30 天首投率只有 X%，低于全站 26%，说明补贴拉来的是低意向用户。</em>",
      "<strong>三条建议</strong>：每条必须落到「谁、做什么、看什么指标」。例：<em>市场部应把信息流预算向应用商店倾斜，考核指标从注册量改为首投率。</em>",
      "<strong>简历段落</strong>：用 STAR 写 4 行，突出「独立完成」「发现并修复数据问题」「输出三层报告」三个信号。",
  ]) + """
  """ + think("你的报告里，哪一条结论是你自己都没预料到的？如果一条都没有，说明你只是把数据重新排列了一遍。回去找一个反常识的点——比如「注册创新高但首投率在降」这种，它才是报告的价值所在。") + """
  """ + deliver([
      "<code>06_作品集/P2P经营分析报告.pdf</code>——15–20 页，含封面与目录",
      "<code>06_作品集/简历-项目段落.md</code>——STAR 四行，可直接贴简历",
      "GitHub repo 或资料库归档，README 写清数据来源（合成）与分析结论",
  ]) + """
  <div class="note warn"><div class="body">
    <p><strong>一定要写明数据是合成的。</strong>这不减分，反而加分——真实业务数据不可能公开，能自己造一套合理数据并说清局限，本身就是能力。写一句「数据为按业务逻辑生成的合成数据，用于方法演示，结论不代表真实平台」就够了。</p>
  </div></div>
</section>

<section id="d7">
  """ + day_head("7", "复盘：把这一周变成可复用的方法", "今天不产出新东西。做两件事：用陌生数据验证你的「30 分钟定位法」，然后把这一周变成面试能讲的答案。") + """
  <p class="lead">你提过一个很重要的目标：<strong>拿到一份数据，快速判断我想做什么、我能做什么</strong>。这个能力不靠多练几套数据，靠一套固定的提问顺序。今天就用你另一个项目（<code>电商用户行为漏斗分析</code>）来验证。</p>
  """ + time_table([
      ("09:00–10:30", "盲测：拿陌生数据 30 分钟做定位", "定位笔记"),
      ("10:30–12:00", "10 个面试题自测，不会的记下来", "答题稿"),
      ("14:00–15:00", "补做本周最弱的一环", "补丁"),
      ("15:00–16:00", "写复盘 + 下一周计划", "复盘.md"),
  ]) + """
  <div class="note tip"><div class="body">
    <p><strong>30 分钟定位法（五问，固定顺序）：</strong><br>
    ① <b>这张表记录什么动作？</b>（一行 = 一次注册 / 一笔交易 / 一次打开？）<br>
    ② <b>粒度是什么？</b>（人 · 笔 · 天 · 快照）<br>
    ③ <b>时间范围？</b>（决定能做同比还是只能做环比）<br>
    ④ <b>关键状态字段有哪些枚举？</b>（<code>status=20</code> 这种，决定哪些数据要排除）<br>
    ⑤ <b>哪些字段是"因"、哪些是"果"？</b>（时间先后能不能对上，决定能不能做转化分析）<br>
    走完这五问，你就能在纸上写出「这份数据能回答的 5 个问题」和「回答不了的 3 个问题」。</p>
  </div></div>
  """ + drill([
      "用五问法分析 <code>电商用户行为漏斗分析</code> 项目的数据，30 分钟内写出「能回答的 5 个问题」和「不能回答的 3 个问题」。",
      "回头检查你这一周的报告：哪一条结论如果换了数据就站不住？把它标注出来。",
      "把 Day 1 的体检报告重读一遍，问自己：如果只给你 1 小时做体检，你会查哪 3 项？为什么是这 3 项？",
  ]) + """
  """ + think("面试官问「你这一周做了什么」，你要能在 90 秒内讲完。试着计时说一遍：背景一句、做了什么三句、发现什么两句、结论一句。说不完就说明你还没想清楚重点。") + """
  """ + deliver([
      "<code>07_复盘/定位笔记.md</code>——五问法的实战记录",
      "10 道面试题的答题稿（每题 3 行以内）",
      "一周复盘 + 下周计划（学什么、补什么）",
  ]) + """
</section>

<section id="accept">
  <h2><span class="num">04</span>验收标准</h2>
  <p class="lead">别用"做完了"来判断，用这三条。全部满足才算这一周没白过。</p>
  <div class="table-wrap"><table>
    <thead><tr><th>等级</th><th>标准</th></tr></thead>
    <tbody>
      <tr><td><b>合格</b></td><td>7 个文件齐全；三份报告能各自说清一个结论；看板能打开、能联动；SQL 全部可重复执行</td></tr>
      <tr><td><b>良好</b></td><td>报告里每个数字都能指到一条 SQL；口径说明写清分子分母与排除条件；看板标题是结论句而非"图表 1"</td></tr>
      <tr><td><b>优秀</b></td><td>至少 1 条反常识结论（如"量涨质降"）；主动写明数据局限；体检报告能定位到具体生成逻辑</td></tr>
    </tbody>
  </table></div>
  <div class="note"><div class="body">
    <p><strong>一个自检动作：</strong>把报告发给一个不懂业务的朋友，让他读 5 分钟，然后问他"这份报告想说什么"。他答得出来，说明你写清楚了；答不出来，问题在结构不在数据。</p>
  </div></div>
</section>

<section id="cut">
  <h2><span class="num">05</span>时间不够怎么砍</h2>
  <p class="lead">一周很紧，大概率会超时。提前定好砍的顺序，比中途慌乱强。</p>
  <div class="table-wrap"><table>
    <thead><tr><th>优先级</th><th>内容</th><th>处理方式</th></tr></thead>
    <tbody>
      <tr><td><b>不能砍</b></td><td>Day 1 数据体检、Day 3 月报、Day 6 整合</td><td>这三块是报告的骨架，缺了整体不成立</td></tr>
      <tr><td><b>可以缩</b></td><td>Day 4 年报</td><td>从 10 页缩到 3 页，只留 KPI + cohort + 一条结论</td></tr>
      <tr><td><b>可以缩</b></td><td>Day 5 看板</td><td>只做 P1 总览页，但度量值要写全</td></tr>
      <tr><td><b>可以砍</b></td><td>Day 2 日报的 3 天样例</td><td>留 1 天即可，模板比样例重要</td></tr>
      <tr><td><b>可以砍</b></td><td>Day 7 盲测</td><td>挪到下一周，不影响本周交付</td></tr>
    </tbody>
  </table></div>
  <div class="note warn"><div class="body">
    <p><strong>最不该砍的是 Day 1。</strong>如果时间实在紧，宁可不做看板，也要把数据体检和修复做完——因为后面所有结论都建在它上面，数据错了，报告越完整越危险。</p>
  </div></div>
</section>

<section id="interview">
  <h2><span class="num">06</span>10 个面试题自测</h2>
  <p class="lead">这周做完，这些题你应该都能用自己项目里的真实例子回答。答不上来的，就是明天要补的。</p>
  <ol class="traps">
    <li><b>你这份数据里，最不可信的是哪个指标？为什么？</b><br>考数据敏感度。答首投时间与注册时间的因果错位，或渠道间无差异。</li>
    <li><b>留存下降，你怎么归因？</b><br>先拆新老、再拆渠道、再看产品改动，最后才怀疑数据。</li>
    <li><b>渠道 ROI 怎么算？没有成本数据怎么办？</b><br>用首投率 × 人均首投额做质量排序，替代 ROI。</li>
    <li><b>日报和月报的区别是什么？</b><br>监控 vs 结构；异常发现 vs 归因解释。</li>
    <li><b>DAU 掉了 10%，你的排查顺序？</b><br>先验数据（埋点 / 口径 / 时区），再拆维度（渠道 / 版本 / 机型），最后看外部。</li>
    <li><b>怎么定义一个「活跃用户」？</b><br>要能说出为什么选打开、而不是登录或投资。</li>
    <li><b>新客首投率突然降 5 个点，你怎么查？</b><br>分子分母分别拆，注意是不是分母被大促灌水了。</li>
    <li><b>你报告里最有价值的结论是哪条？</b><br>必须有反常识性，且能落到行动。</li>
    <li><b>数据有问题但业务要上线，你怎么办？</b><br>标注置信度、给区间、留回滚方案，别只说"不行"。</li>
    <li><b>你怎么保证不同报表的口径一致？</b><br>指标字典 + 单一数据源 + 定期对账，答到这三层就够。</li>
  </ol>
</section>
"""

# ---------- 组装 ----------
out = base

out = re.sub(r"<title>.*?</title>", "<title>一周作战计划</title>", out, count=1)
out = re.sub(
    r'<meta name="description" content=".*?">',
    '<meta name="description" content="P2P 理财 App 经营分析 7 天作品集冲刺计划：数据体检、日报、月报、年报、Power BI 看板、简历包装与面试自测。">',
    out,
    count=1,
)
out = re.sub(
    r'<script type="application/ld\+json">.*?</script>',
    '<script type="application/ld+json">\n'
    '{"@context":"https://schema.org","@type":"HowTo","name":"一周作战计划",'
    '"description":"P2P 经营分析 7 天作品集冲刺","inLanguage":"zh-CN"}\n</script>',
    out,
    count=1,
)

out = out.replace(
    "<strong>变量查询手册</strong>\n        <span>p2p_learning · MySQL 8</span>",
    "<strong>一周作战计划</strong>\n        <span>7-day sprint · 作品集</span>",
)
out = out.replace('<div class="brand-mark">P2P</div>', '<div class="brand-mark">7D</div>')
out = out.replace(
    "<b>数据 100% 合成</b><br>无真实用户信息 · 仅用于练 SQL",
    "<b>7 天 · 7 个交付</b><br>报告优先 · SQL 与看板为辅",
)

out = re.sub(r'<nav class="sb-nav" id="nav">.*?</nav>', '<nav class="sb-nav" id="nav">\n' + NAV + "\n  </nav>", out, flags=re.S)

out = out.replace(
    '<span>资料库</span><span class="sep">/</span><span>P2P 练习库</span><span class="sep">/</span><b>变量查询手册</b>',
    '<span>资料库</span><span class="sep">/</span><span>P2P 练习库</span><span class="sep">/</span><b>一周作战计划</b>',
)
out = out.replace(
    '<span class="chip">v3.1</span>\n      <span class="chip plain">32 张表</span>',
    '<span class="chip">7 天</span>\n      <span class="chip plain">作品集冲刺</span>',
)

extra_css = """
/* ---------- study plan ---------- */
.day-h{display:flex;gap:14px;align-items:flex-start;margin:0 0 18px}
.day-badge{
  flex:0 0 auto;padding:7px 11px;border-radius:8px;background:var(--accent-soft);
  color:var(--accent-ink);font-family:var(--font-mono);font-size:12px;letter-spacing:.02em;
  border:1px solid rgba(37,87,214,.18);white-space:nowrap;margin-top:4px
}
.day-badge.tone-teal{background:var(--teal-soft);color:var(--teal);border-color:rgba(14,116,144,.2)}
.day-goal{margin:6px 0 0;color:var(--ink-2);font-size:14px;line-height:1.65}
table.time td{font-size:13.6px;vertical-align:top}
table.time td.tm{font-family:var(--font-mono);font-size:12.4px;color:var(--ink-3);white-space:nowrap;width:112px}
table.time td.out{color:var(--accent-ink);font-size:12.8px;white-space:nowrap}
.drill{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius);padding:16px 20px;margin:18px 0}
.drill-h{font-family:var(--font-mono);font-size:11.5px;color:var(--ink-3);letter-spacing:.06em;text-transform:uppercase;margin:0 0 10px}
.drill ol{margin:0;padding-left:20px;color:var(--ink-2);font-size:14px;line-height:1.72}
.drill ol li{margin:0 0 9px}
.drill ol li:last-child{margin-bottom:0}
.think{border-left:3px solid var(--warn);background:var(--warn-soft);border-radius:0 var(--radius) var(--radius) 0;padding:14px 18px;margin:18px 0}
.think b{display:block;font-family:var(--font-mono);font-size:11.5px;color:var(--warn);letter-spacing:.06em;margin-bottom:6px}
.think p{margin:0;color:var(--ink-2);font-size:14px;line-height:1.7}
.deliver{border:1px dashed var(--line-2);border-radius:var(--radius);padding:14px 18px;margin:18px 0}
.deliver ul{list-style:none;margin:0;padding:0}
.deliver li{position:relative;padding-left:22px;margin:0 0 7px;color:var(--ink-2);font-size:13.8px}
.deliver li:last-child{margin-bottom:0}
.deliver li::before{
  content:"";position:absolute;left:0;top:6px;width:12px;height:12px;
  border:1px solid var(--ink-3);border-radius:3px
}
@media (max-width:640px){
  .day-h{flex-direction:column;gap:8px}
  table.time td.out{white-space:normal}
  table.time td.tm{width:auto}
}
</style>"""
out = out.replace("</style>", extra_css, 1)

i = out.index('<div class="wrap">') + len('<div class="wrap">')
j = out.index("  <footer>")
out = out[:i] + "\n" + CONTENT + "\n  </div>\n\n" + out[j:]

out = out.replace('<p class="fb">P2P 数仓变量查询手册 v3.1</p>', '<p class="fb">一周作战计划 · 作品集冲刺</p>')
out = out.replace(
    "<p>配套 p2p_learning 练习库 · MySQL 8.0 · 数据 100% 合成，无任何真实用户信息</p>",
    "<p>配套 p2p_learning 练习库 · 7 天 · 3 份报告 + 1 套看板</p>",
)
out = out.replace(
    "snapshot 2016-01-11<br>\n        data range 2015-01 ~ 2016-08<br>\n        updated 2026-10-23",
    "duration 7 days<br>\n        scope 日 / 月 / 年<br>\n        updated 2026-10-23",
)

open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
print("written", len(out), "chars")
print("sections:", len(re.findall(r'<section id="', out)), "nav:", len(re.findall(r'class="nav-link', out)))
