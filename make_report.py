# -*- coding: utf-8 -*-
import os
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = r"C:\Users\1\DevEcoStudioProjects\FanZhendongMemory"
TEMPLATE = r"C:\Users\1\Downloads\移动应用开发基础_期末大作业个人报告模板.docx"
OUTDIR = os.path.join(ROOT, "report")
os.makedirs(OUTDIR, exist_ok=True)
OUT = os.path.join(OUTDIR, "移动应用开发基础-20240313140-章瑞-期末大作业.docx")

doc = Document(TEMPLATE)
paras = doc.paragraphs


def set_text(p, text, size=None, bold=None, color=None, font=None):
    p.text = ""
    r = p.add_run(text)
    if size:
        r.font.size = Pt(size)
    if bold is not None:
        r.bold = bold
    if color:
        r.font.color.rgb = RGBColor(*color)
    if font:
        r.font.name = font
        r._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), font)


def insert_after(anchor, text, style="学生正文规范"):
    p = doc.add_paragraph(style=style)
    p._p.getparent().remove(p._p)
    anchor._p.addnext(p._p)
    set_text(p, text)
    return p


def insert_paragraphs(anchor, texts, style="学生正文规范"):
    cur = anchor
    for t in texts:
        cur = insert_after(cur, t, style)
    return cur


def remove(p):
    p._p.getparent().remove(p._p)


def add_image_before(caption, path, width_cm):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run()
    run.add_picture(path, width=Cm(width_cm))
    caption._p.addprevious(p._p)
    return p


def add_image_grid_before(caption, items, width_cm=5.0):
    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for i, (label, path) in enumerate(items):
        cell = table.cell(i // 2, i % 2)
        cell.width = Cm(width_cm + 1.0)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        p.add_run().add_picture(path, width=Cm(width_cm))
        lp = cell.add_paragraph(label)
        lp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        lp.paragraph_format.space_before = Pt(1)
        lp.paragraph_format.space_after = Pt(4)
        for r in lp.runs:
            r.font.size = Pt(8)
            r.font.color.rgb = RGBColor(0x66, 0x6F, 0x7A)
    caption._p.addprevious(table._tbl)


def cell_text(cell, text, size=8.5, bold=False, color=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold
    r.font.name = "宋体"
    r._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "宋体")
    if color:
        r.font.color.rgb = RGBColor(*color)


def code_block_after(anchor, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.left_indent = Cm(0.3)
    r = p.add_run(text)
    r.font.size = Pt(8)
    r.font.name = "Consolas"
    r._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "等线")
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), "F3F5F8")
    p._p.get_or_add_pPr().append(shd)
    anchor._p.addnext(p._p)
    return p


# ---------------- 封面 ----------------
# 保留模板的下划线格式，只替换下划线上的内容
def fill_cover(p, value):
    while len(p.runs) > 2:
        r = p.runs[-1]
        r._element.getparent().remove(r._element)
    if len(p.runs) >= 2:
        p.runs[1].text = value
        p.runs[1].underline = True
    else:
        p.add_run(value).underline = True

fill_cover(paras[10], "        24物联2        ")
fill_cover(paras[11], "            章瑞                ")
fill_cover(paras[12], "         20240313140         ")

# ---------------- 表 1.1 基本信息 ----------------
t = doc.tables[4]
info = [
    ("作品名称", "樊振东 · 三线回忆录"),
    ("指定主题", "主题一（交互式回忆探索）"),
    ("姓名（学号）", "章瑞（20240313140）"),
    ("GitHub账号", "【提交前填写：本人 GitHub 用户名】"),
    ("GitHub仓库链接", "【提交前填写：完整仓库 URL，与学习通一致】"),
    ("小组成员", "无（个人独立完成）"),
    ("开发环境", "DevEco Studio 5.0.13 / HarmonyOS SDK 5.0.5(17) / API 17"),
]
for i, (k, v) in enumerate(info, start=1):
    cell_text(t.rows[i].cells[0], k, 9, True, align=WD_ALIGN_PARAGRAPH.CENTER)
    cell_text(t.rows[i].cells[1], v, 9, False,
              color=(0xC0, 0x39, 0x2B) if "提交前填写" in v else None)

# ---------------- 1.2 项目简介 ----------------
p28 = paras[28]
intro = [
    "本项目以“生涯—球衣—球拍”三条线组织 22 段记忆：生涯线从 2002 年第一次握拍、2008 年进入八一队、2012 年进入国家队，一直写到 2016 世界杯首冠、2021 东京、2024 巴黎、2025 德甲与 2026 当下；球衣线收录 2013—2025 年的 7 件代表性战袍；球拍线收录从启蒙纯木到樊振东 ALC / Super ALC 的 5 个阶段。",
    "主界面用纵向 Swiper 自动轮播回忆卡片，配合 Marquee 流动字幕与胶片带，形成“翻相册”的节奏；底部玻璃 Dock 提供三条线切换；详情页承载长文、引用、收藏与“我的回忆手记”。应用关闭再打开，会恢复上次的线、条目、收藏、手记与动效设置。界面采用深色底、半透明玻璃、细边框与金色强调，借鉴 iOS 26 的 Liquid Glass 质感，但保持简约、克制。",
]
insert_paragraphs(p28, intro)
remove(p28)

# ---------------- 1.3 需求完成情况 ----------------
p30 = paras[30]
done = [
    "对照《软件需求说明书》第 3 章，核心需求均已完成：",
    "（1）主界面：Swiper 自动轮播、Marquee 流动字幕、胶片带、三线 Dock、全部/单线过滤、进度显示。对应需求 3.1。",
    "（2）详情页：大图、长文、引用、标签、配色/面料/配置、时间、收藏、手记、上一段/下一段。对应需求 3.2。",
    "（3）时间线：全部/生涯/球衣/球拍筛选，条目跳转。对应需求 3.3。",
    "（4）设置与成就：减少动态效果、清空数据、探索进度、visited≥10 与 favorites≥5 的条件成就。对应需求 3.4。",
    "（5）数据恢复：Preferences 保存 favorites、visited、lastId、lastLine、reduceMotion 与 note_<id>；启动时恢复，JSON 异常回退。对应需求 3.5。",
    "（6）跨端预览：同源 PWA 支持 iPhone Safari 添加到主屏幕；HarmonyOS HAP 已构建成功。",
]
insert_paragraphs(p30, done)
remove(p30)

# ---------------- 2.1 整体架构 ----------------
p33 = paras[33]
arch_text = [
    "系统采用 HarmonyOS Stage 模型，按“表现层—业务层—数据层—资源层”四层组织。表现层由 Index、DetailPage、TimelinePage、SettingsPage 四个页面与 MemoryPoster、LineDock 两个自定义组件构成；业务层负责三线过滤、条目索引、上下段、状态恢复与条件成就；数据层由 MemoryData、MemoryModels、MemoryStore 组成；资源层存放 22 张 1080×1440 海报、分层图标与 PWA 资源。",
    "本项目为个人独立完成，架构图中“本人负责：全部模块”即实际分工。页面之间通过 router 传参，页面与数据之间通过 MemoryState 与 MemoryStore 交互，避免把持久化逻辑写进 UI。",
]
insert_paragraphs(p33, arch_text)
remove(p33)
add_image_before(paras[34], os.path.join(ROOT, "docs", "architecture.png"), 15.2)
insert_after(paras[34], "数据流可以概括为：用户操作 → @State 页面状态 → MemoryStore → Preferences 文件；应用重启时反向读取，恢复 lastLine / lastId / favorites / notes。表现层不直接操作文件，数据层也不依赖具体页面，二者通过 MemoryState 解耦。")

# ---------------- 2.2 模块划分 ----------------
t5 = doc.tables[5]
modules = [
    ("数据与模型", "22 条三线记忆、MemoryItem / MemoryLine / MemoryState", "静态数据 → 页面对象", "章瑞"),
    ("持久化", "Preferences 读写、JSON 容错、手记键值", "状态 ↔ 本地文件", "章瑞"),
    ("主界面", "Swiper、Marquee、胶片带、三线 Dock", "手势/点击 → 当前条目/线", "章瑞"),
    ("详情", "长文、收藏、手记、上下段", "条目 → 阅读与记录", "章瑞"),
    ("时间线", "全部/生涯/球衣/球拍筛选与跳转", "线 → 列表", "章瑞"),
    ("设置/成就", "动效开关、清空、进度、条件解锁", "状态 → 设置结果", "章瑞"),
    ("资源与文档", "海报、图标、架构图、README、报告", "设计 → 交付资产", "章瑞"),
]
for i, row in enumerate(modules, start=1):
    if i >= len(t5.rows):
        t5.add_row()
    for j, v in enumerate(row):
        cell_text(t5.rows[i].cells[j], v, 8.2, j == 0)
insert_after(paras[37], "模块之间保持单向依赖：页面依赖组件与 MemoryStore；MemoryStore 依赖 MemoryModels；MemoryData 只提供静态数据。新增一条记忆时，只需在 content.py / MemoryData.ets 中增加一条记录并放入对应图片，不需要改页面逻辑。")

# ---------------- 2.3 本人职责 ----------------
p39 = paras[39]
duty = [
    "本人独立承担全部模块，无小组分工。对应源码路径如下：",
    "• 数据与模型：entry/src/main/ets/model/MemoryModels.ets、entry/src/main/ets/data/MemoryData.ets；",
    "• 持久化：entry/src/main/ets/services/MemoryStore.ets；",
    "• 主界面：entry/src/main/ets/pages/Index.ets、components/MemoryPoster.ets、components/LineDock.ets；",
    "• 详情：entry/src/main/ets/pages/DetailPage.ets；",
    "• 时间线与设置：entry/src/main/ets/pages/TimelinePage.ets、pages/SettingsPage.ets；",
    "• 资源与跨端：entry/src/main/resources/base/media、web/、docs/、report/。",
]
insert_paragraphs(p39, duty)
remove(p39)

# ---------------- 3.1 功能设计 ----------------
p42 = paras[42]
func = [
    "主界面是应用的“入口”，也是情绪的第一层。Index 启动时先读取 Preferences：若有 lastId，则定位到上次条目；否则默认「全部」第 1 条。Swiper 纵向自动轮播 22 条记忆，每张卡片由 MemoryPoster 渲染：大图、线标签、日期、年份、标题、副标题与 Marquee 流动字幕。底部胶片带横向展示全部缩略图，点击可跳转；底部玻璃 Dock 切换生涯、球衣、球拍三条线；顶部「全部」恢复全量。",
    "点击卡片进入 DetailPage。详情页用 Scroll 承载长文，收藏与手记都写入 Preferences。手记使用 note_<id> 键，一条记忆一条记录；保存后即使杀掉应用再打开也能恢复。上一段/下一段在 22 条记忆中循环，适合连续阅读。",
    "TimelinePage 把 22 条记忆按时间排好，支持四条筛选；SettingsPage 提供减少动态效果、清空数据、探索进度与条件成就。成就规则是轻量分支：visited≥10 解锁「巴黎的金色雨」，favorites≥5 解锁「三线收藏家」。",
]
insert_paragraphs(p42, func)
remove(p42)
add_image_before(paras[43], os.path.join(ROOT, "docs", "flow.png"), 15.2)
insert_after(paras[43], "业务流的关键是“状态驱动”：用户每一次切换线、滑动、收藏、写手记，都会改变 MemoryState；MemoryStore 负责把状态落盘；下一次启动时再由 MemoryStore 读回。页面不保存全局单例，避免多个页面之间的状态互相污染。")

# ---------------- 3.2 数据设计 ----------------
t6 = doc.tables[6]
data_rows = [
    ("MemoryItem", "id:string；line:MemoryLine；year/date/title/subtitle/caption/description:string；tags:string[]；image:Resource；accent:string；colorway/fabric/spec:string", "一条记忆的完整展示与详情数据", "MemoryData 静态构造；$r 引用图片"),
    ("MemoryState", "favorites:string[]；visited:string[]；lastId:string；lastLine:string；reduceMotion:boolean", "跨页面共享的用户状态", "MemoryStore 序列化到 Preferences"),
    ("Preferences", "favorites/visited:JSON；lastId/lastLine:string；reduceMotion:boolean；note_<id>:string", "应用关闭后的持久化载体", "@kit.ArkData Preferences；put + flush"),
]
for i, row in enumerate(data_rows, start=1):
    if i >= len(t6.rows):
        t6.add_row()
    for j, v in enumerate(row):
        cell_text(t6.rows[i].cells[j], v, 8.0, j == 0)

# ---------------- 3.3 接口设计 ----------------
t7 = doc.tables[7]
api_rows = [
    ("getMemories(line?)", "MemoryLine，可空", "MemoryItem[]", "空线返回全量；未知线由调用方兜底"),
    ("getMemoryById(id)", "string", "MemoryItem | undefined", "找不到返回 undefined，页面回退第一条"),
    ("MemoryStore.load()", "无", "Promise<MemoryState>", "无数据返回默认；JSON 异常回退空数组"),
    ("MemoryStore.saveState(state)", "MemoryState", "Promise<void>", "put + flush；失败不阻塞 UI"),
    ("MemoryStore.getNote(id)", "string", "Promise<string>", "无记录返回空字符串"),
    ("MemoryStore.saveNote(id, note)", "string, string", "Promise<void>", "空字符串视为清除"),
    ("selectFilter(line)", "string", "void", "过滤 items，currentIndex 归零"),
    ("openDetail(item)", "MemoryItem", "void", "router.pushUrl，携带 id"),
]
for i, row in enumerate(api_rows, start=1):
    if i >= len(t7.rows):
        t7.add_row()
    for j, v in enumerate(row):
        cell_text(t7.rows[i].cells[j], v, 8.0, j == 0)
insert_after(paras[48], "异常处理原则：Preferences 读取统一 try/catch，任何 JSON 损坏都回退为空数组；lastId 不属于当前线时回到该线第 1 条；currentIndex 用 clamp + 取模，避免越界；清空数据前二次确认；减少动态效果时关闭 autoPlay 与 Marquee.start，保留手动滑动。")

# ---------------- 4.1 核心代码 ----------------
p51 = paras[51]
a = insert_after(p51, "（1）数据模型：MemoryItem 把展示字段、线枚举、资源与来源信息封装在一个类中，页面只依赖这个类型。")
a = code_block_after(a, """export class MemoryItem {
  id: string; line: MemoryLine; no: string; year: string; date: string;
  title: string; subtitle: string; caption: string; description: string;
  quote: string; tags: string[]; image: Resource; accent: string;
  colorway: string; fabric: string; spec: string; source: string; credit: string;
  constructor(...) { /* 逐字段赋值 */ }
}""")
a = insert_after(a, "路径：entry/src/main/ets/model/MemoryModels.ets。MemoryLine 用字符串枚举区分 CAREER / JERSEY / PADDLE，getMemories 与 getMemoryById 提供最小数据访问接口。")
a = code_block_after(a, """static async load(): Promise<MemoryState> {
  const state = new MemoryState();
  const favorites = await MemoryStore.pref.get('favorites', '[]');
  const lastId = await MemoryStore.pref.get('lastId', '');
  state.favorites = parseArray(String(favorites));
  state.lastId = String(lastId);
  return state;
}
static async saveState(state: MemoryState): Promise<void> {
  await MemoryStore.pref.put('favorites', JSON.stringify(state.favorites));
  await MemoryStore.pref.put('lastId', state.lastId);
  await MemoryStore.pref.flush();
}""")
a = insert_after(a, "路径：entry/src/main/ets/services/MemoryStore.ets。parseArray 捕获 JSON 异常并返回空数组，保证损坏数据不会阻塞启动。")
a = code_block_after(a, """Swiper(this.swiperController) {
  ForEach(this.items, (item: MemoryItem) => {
    MemoryPoster({ item, isFavorite: this.isFavorite(item.id),
      reduceMotion: this.reduceMotion,
      onOpen: () => this.openDetail(item) })
  }, (item: MemoryItem) => item.id)
}
.vertical(true).loop(true).indicator(false)
.autoPlay(!this.reduceMotion).interval(6500).duration(700)
.onChange((index: number) => { this.currentIndex = index; this.persist(); })""")
a = insert_after(a, "路径：entry/src/main/ets/pages/Index.ets。Swiper 负责自动流动，MemoryPoster 内部用 Marquee 呈现流动字幕；onChange 把当前索引写回 MemoryState，实现“看到哪、下次从哪继续”。")
remove(p51)

# ---------------- 4.2 技术应用 ----------------
p53 = paras[53]
tech = [
    "ArkTS / 面向对象：MemoryItem、MemoryState 用 class 建模，MemoryLine 用 enum，接口用 interface；页面只处理 MemoryItem[]，数据与 UI 解耦。",
    "ArkUI 布局：Column / Row / Stack / Flex / Scroll 组合出沉浸式页面；Swiper 做纵向自动轮播；Marquee 做流动字幕；Image 的 objectFit 与 linearGradient 做海报与暗角。",
    "状态管理：@State 管理当前索引、当前线、收藏、动效；@Prop 把 item / activeLine / reduceMotion 传给自定义组件；onPageShow 在从详情返回时刷新收藏状态。",
    "自定义组件：MemoryPoster 封装海报与字幕，LineDock 封装底部三线玻璃 Dock；组件只通过 props 与回调与页面通信。",
    "页面导航：router.pushUrl 进入详情/时间线/设置，router.replaceUrl 在详情内切换上一条/下一条，router.back 返回。",
    "Ability Kit / 数据：EntryAbility 加载 Index；@kit.ArkData Preferences 做持久化；getContext(this) 提供 UIAbilityContext。",
    "视觉：深色底 + 半透明玻璃 + 细边框 + 金色强调；22 张原创海报统一 1080×1440，保证主界面与详情页的构图一致。",
]
insert_paragraphs(p53, tech)
remove(p53)

# ---------------- 4.3 Git 提交记录 ----------------
t8 = doc.tables[8]
commits = [
    ("77ea3ee", "chore: 初始化 HarmonyOS Stage 工程与基础配置", "AppScope、entry/module.json5、EntryAbility、构建配置"),
    ("e0c4501", "feat: 添加 22 条三线记忆数据与原创视觉资产", "MemoryModels、MemoryData、22 张海报与图标"),
    ("3488be1", "feat: 实现回忆流主界面与三线玻璃 Dock", "Index、MemoryPoster、LineDock"),
    ("b366581", "feat: 完成详情页、收藏与 Preferences 持久化", "DetailPage、MemoryStore"),
    ("127b421", "feat: 增加时间线、设置与条件成就", "TimelinePage、SettingsPage"),
    ("dfa5de0", "feat: 增加 iPhone PWA 跨端预览、文档与部署工作流", "web/、docs/、README、GitHub Pages"),
]
for i, row in enumerate(commits, start=1):
    if i >= len(t8.rows):
        t8.add_row()
    for j, v in enumerate(row):
        cell_text(t8.rows[i].cells[j], v, 8.0, j == 0)
insert_after(paras[56], "以上 Commit 均来自本人本地仓库，提交顺序与模块开发顺序一致；报告中的代码路径与 Commit 涉及文件一一对应。GitHub 远端仓库链接与账号见封面后的表 1.1（提交前替换为实际信息）。")

# ---------------- 5.1 Mock 测试设计 ----------------
p59 = paras[59]
mock = [
    "Mock 对象：MemoryState（favorites / visited / lastId / lastLine / reduceMotion）、MemoryItem 数组、Preferences 中的 JSON 字符串。被测接口：getMemories、getMemoryById、MemoryStore.load / saveState / saveNote、selectFilter、selectItem。",
    "测试方式：在 DevEco Studio 中构建 HAP，使用同源 PWA 做页面级走查；对服务层用临时 Mock 数据替换 Preferences 的返回值，验证正常、边界、异常三类输入。页面测试覆盖三线切换、胶片带跳转、详情上下段、手记保存、动效开关、成就条件。",
    "证据：docs/screenshots 下的主界面、详情、时间线、设置截图；docs/demo.gif 为页面操作演示；HAP 构建日志显示 BUILD SUCCESSFUL。",
]
insert_paragraphs(p59, mock)
remove(p59)

# ---------------- 5.2 测试结果 ----------------
t9 = doc.tables[9]
tests = [
    ("正常", "favorites=[]，收藏 career_2024", "isFavorite 返回 true，Preferences 写入该 ID", "通过；重启后仍为已收藏"),
    ("正常", "在详情写“第一次看巴黎决赛”并保存", "note_career_2024 写入，重新进入恢复", "通过；TextArea 回显"),
    ("边界", "22 条全部访问；收藏 5 条", "进度 22/22；解锁两个成就", "通过；设置页显示“巴黎的金色雨”“三线收藏家”"),
    ("边界", "lastId 不在当前 lastLine", "回到该线第 1 条", "通过；currentIndex 归零"),
    ("异常", "favorites 写入 not-json", "parseArray 捕获异常，回退 []", "通过；应用正常启动"),
    ("异常", "清空 Preferences 后启动", "默认 all / 第 1 条，不崩溃", "通过；显示第一条 2002"),
]
for i, row in enumerate(tests, start=1):
    if i >= len(t9.rows):
        t9.add_row()
    for j, v in enumerate(row):
        cell_text(t9.rows[i].cells[j], v, 7.8, j == 0)

# ---------------- 5.3 问题与修复 ----------------
p64 = paras[64]
issues = [
    "问题 1：工程放在含中文的 OneDrive 路径下时，hvigor 报“Invalid project path”。修复：把工程迁移到纯 ASCII 路径 C:\\Users\\1\\DevEcoStudioProjects\\FanZhendongMemory，并在构建脚本中显式设置 DEVECO_SDK_HOME 与 NODE_HOME。",
    "问题 2：DetailPage 初次编译报 “Property 'Justify' does not exist on type 'typeof TextAlign'”。修复：改为 TextAlign.JUSTIFY，重新构建通过。",
    "问题 3：海报中烘焙了年份/标题，与页面 overlay 重复。修复：把图片中的文字层移除，只保留画面与纹理，所有标题/字幕交给 ArkUI / PWA 渲染。",
    "问题 4：HarmonyOS .hap 无法安装到 iPhone。修复：保留 HarmonyOS 原生 HAP，同时提供同源 PWA，iPhone Safari 可“添加到主屏幕”；在 README 与报告中明确两者边界。",
    "问题 5：本机没有可用的 HarmonyOS 模拟器，无法做真机截图。处理：以 DevEco 构建成功 + 同源 PWA 页面走查作为验证；真机安装需在 DevEco 中配置签名后执行。",
]
insert_paragraphs(p64, issues)
remove(p64)

# ---------------- 6.1 运行效果 ----------------
p67 = paras[67]
run_text = [
    "主界面以深色底和金色强调建立统一风格：顶部是品牌与进度，中央是自动流动的海报卡片，底部是胶片带与三线玻璃 Dock。卡片上的线标签、日期、年份、标题与流动字幕形成清晰的信息层级；胶片带让 22 条记忆始终“在手边”。",
    "详情页把海报放大，长文、引用、标签、配置与手记依次展开；收藏与手记按钮使用金色/半透明两种状态，操作反馈明确。时间线把三条线收束成一条纵向列表，设置页把动效、数据与成就集中管理。",
]
insert_paragraphs(p67, [run_text[0]])
remove(p67)
add_image_grid_before(paras[68], [
    ("主界面 · 生涯（2024 巴黎）", os.path.join(ROOT, "docs", "screenshots", "main_career.png")),
    ("主界面 · 球衣（2024 巴黎）", os.path.join(ROOT, "docs", "screenshots", "main_jersey.png")),
    ("详情页 · 巴黎登顶", os.path.join(ROOT, "docs", "screenshots", "detail.png")),
    ("时间线 · 全部", os.path.join(ROOT, "docs", "screenshots", "timeline.png")),
], width_cm=4.8)
b = insert_after(paras[68], run_text[1])
insert_after(b, "以上截图来自项目同源 PWA 预览版，与 HarmonyOS 页面共用同一套数据、组件结构与视觉资产。PWA 与 HAP 的差异主要在容器与签名方式，不在业务逻辑。")

# ---------------- 6.2 数据恢复与集成 ----------------
p70 = paras[70]
recovery = [
    "持久化验证：在详情页收藏 career_2024、写入手记，然后完全退出应用并重新启动。Index 读取 Preferences 后恢复到生涯线第 8 条，收藏心形为实心，详情页 TextArea 恢复手记；在设置页可以看到探索进度与成就状态随访问/收藏数量变化。",
    "集成结果：DevEco Studio 5.0.13 构建 HAP 成功，产物为 entry/build/default/outputs/default/entry-default-unsigned.hap；应用包含 22 张海报与 4 个页面，资源打包正常。PWA 通过 GitHub Pages 部署后可在 iPhone Safari 添加到主屏幕，作为跨端预览与演示入口。",
]
insert_paragraphs(p70, recovery)
remove(p70)
add_image_before(paras[71], os.path.join(ROOT, "docs", "screenshots", "settings.png"), 6.0)
insert_after(paras[71], "设置页同时承担“数据恢复”的可视化验证：探索进度、收藏数量与条件成就会随着使用变化；清空数据后回到默认状态，下一次启动不再恢复旧记录。")

# ---------------- 6.3 个人总结 ----------------
p73 = paras[73]
summary = [
    "这次大作业我把“内容策划—视觉资产—ArkTS 数据模型—ArkUI 页面—Preferences 持久化—文档与交付”完整走了一遍。最大的收获不是某个组件，而是学会把“记忆”拆成可维护的数据结构：一条 MemoryItem 同时服务主界面、详情、时间线与 PWA，改一处数据就能让四个界面同步。",
    "技术难点主要有三处：一是让 22 条记忆的 Swiper、胶片带、Dock 与详情页保持索引一致；二是 Preferences 的异步读写与 JSON 容错；三是把“玻璃感”做得克制，不让半透明和动效压过内容。解决方式分别是：统一 currentIndex / lastId、在 MemoryStore 内集中处理异常、用深色底 + 细边框 + 低饱和金色控制视觉层级。",
    "不足也很明确：本机没有 HarmonyOS 模拟器，真机截图与录屏需要签名后补；iPhone 只能使用 PWA，不是原生 iOS 应用；成就系统目前是轻量条件分支，还可以扩展成多结局、隐藏线索与更完整的探索路径。后续如果继续迭代，我会补充真机录屏、增加“回忆地图/随机漫游”，并把 22 条记忆扩展成可配置的内容后台。",
]
insert_paragraphs(p73, summary)
remove(p73)

for p in list(doc.paragraphs):
    if "【填写提示】" in p.text:
        remove(p)
    elif p.text.strip().startswith("•"):
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    elif p.text.strip().startswith("Mock 对象"):
        p.paragraph_format.keep_together = True

try:
    settings = doc.settings.element
    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    settings.append(update)
except Exception:
    pass

doc.save(OUT)
print("saved", OUT)






