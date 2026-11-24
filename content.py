# -*- coding: utf-8 -*-
"""Single source of truth for the 22 memory items. Generates web/data.js and ArkTS seed data."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

ITEMS = [
    # ---------------- CAREER ----------------
    dict(id="career_2002", line="career", no="01", year="2002", date="2002.01", title="第一块球拍",
         subtitle="5岁 · 广州海珠区少年宫", caption="5岁 · 第一块球拍 · 广州海珠区少年宫",
         description="2002年，5岁的樊振东被妈妈带到广州海珠区少年宫学乒乓球。他个子矮，够不到球台，教练就在地上垫了一块木板，让他踮着脚练。第一次握拍，球拍几乎和手掌一样大。",
         quote="有些起点，只是一块垫脚的木板。",
         tags=["起点", "广州", "少年宫"], image="career_2002.jpg", accent="#E7B768",
         source="原创插画", credit="FZD Memory Archive"),
    dict(id="career_2008", line="career", no="02", year="2008", date="2008.09", title="八一队",
         subtitle="11岁 · 离开广州", caption="11岁 · 离开广州 · 入选八一队",
         description="2008年，11岁的樊振东凭借广州市团体和双打第一名的成绩入选八一队。他离开广州，开始集体生活与更严格的专业训练，也第一次真正看见国家队的样子。",
         quote="把想家的夜晚，练成第二天的球。",
         tags=["八一队", "少年", "专业训练"], image="career_2008.jpg", accent="#5D91EF",
         source="原创插画", credit="FZD Memory Archive"),
    dict(id="career_2012", line="career", no="03", year="2012", date="2012.02", title="国家队",
         subtitle="15岁 · 国家二队", caption="15岁 · 进入国家二队 · 世青赛三金一银",
         description="2012年2月，15岁的樊振东进入国家二队；同年12月世青赛，他拿下三金一银，一战成名。少年成名只是开始，真正的长路还在后面。",
         quote="少年成名，只是更长路的开始。",
         tags=["国家队", "世青赛", "15岁"], image="career_2012.jpg", accent="#E7B768",
         source="原创插画", credit="FZD Memory Archive"),
    dict(id="career_2016", line="career", no="04", year="2016", date="2016.10", title="世界杯首冠",
         subtitle="19岁 · 萨尔布吕肯", caption="19岁 · 萨尔布吕肯 · 首个单打世界冠军",
         description="2016年10月，德国萨尔布吕肯男子世界杯，19岁的樊振东夺得职业生涯首个单打世界冠军。从里约周期的替补席，到世界之巅，他用了四年。",
         quote="从替补席到领奖台，他用了四年。",
         tags=["世界杯", "首冠", "萨尔布吕肯"], image="career_2016.jpg", accent="#D24A4E",
         source="公开报道资料图", credit="新浪体育 / 仅课程学习使用"),
    dict(id="career_2021", line="career", no="05", year="2021", date="2021.07—08", title="东京周期",
         subtitle="男团金牌 · 男单银牌", caption="东京 · 男团金牌 · 男单银牌",
         description="2021年东京奥运会，樊振东随中国队获得男团金牌，男单收获银牌；同年休斯敦世乒赛，他拿下男单冠军。银牌不是终点，而是下一次出发的坐标。",
         quote="银牌不是终点，是下一次出发的坐标。",
         tags=["东京", "奥运", "男团"], image="career_2021.jpg", accent="#E7B768",
         source="公开报道资料图", credit="新华社 / 仅课程学习使用"),
    dict(id="career_2022", line="career", no="06", year="2022", date="2022.10", title="成都世乒赛",
         subtitle="男团冠军 · 主场作战", caption="成都 · 男团冠军 · 主场作战",
         description="2022年成都世乒赛，樊振东与队友一起拿下男团冠军。主场的声音、熟悉的红色球台，他把压力打成了每一板的质量。",
         quote="主场的声音，会落在每一板球上。",
         tags=["成都", "世乒赛", "男团"], image="career_2022.jpg", accent="#E7B768",
         source="公开报道资料图", credit="新浪体育 / 仅课程学习使用"),
    dict(id="career_2023", line="career", no="07", year="2023", date="2023.05", title="德班封王",
         subtitle="世乒赛男单冠军", caption="德班 · 世乒赛男单冠军",
         description="2023年德班世乒赛，樊振东第二次捧起圣·勃莱德杯。从2017年的亚军到2023年的冠军，他把遗憾留在昨天，把名字写进奖杯。",
         quote="把遗憾留在昨天，把名字写进奖杯。",
         tags=["德班", "世乒赛", "男单"], image="career_2023.jpg", accent="#5D91EF",
         source="公开报道资料图", credit="新浪体育 / 仅课程学习使用"),
    dict(id="career_2024", line="career", no="08", year="2024", date="2024.08.04", title="巴黎登顶",
         subtitle="男单金牌 · 大满贯", caption="巴黎 · 男单金牌 · 大满贯",
         description="2024年8月4日，巴黎奥运会男单决赛，樊振东4:1战胜瑞典选手莫雷加德，拿下男单金牌；随后又随中国队获得男团金牌，完成职业生涯大满贯。",
         quote="所有等待，在最后一分落地时有了答案。",
         tags=["巴黎", "奥运", "大满贯"], image="career_2024.jpg", accent="#E7B768",
         source="公开报道资料图", credit="新浪体育 / 仅课程学习使用"),
    dict(id="career_2025", line="career", no="09", year="2025", date="2025.06", title="远行",
         subtitle="德甲 · 萨尔布吕肯", caption="2025 · 德甲 · 萨尔布吕肯",
         description="2025年，樊振东加盟德国乒乓球甲级联赛萨尔布吕肯俱乐部，开启留洋赛季。换一片球台，还是同一颗白球；在另一种联赛节奏里，他继续打球。",
         quote="换一片球台，还是同一颗白球。",
         tags=["德甲", "萨尔布吕肯", "留洋"], image="career_2025.jpg", accent="#8FC3FF",
         source="公开报道资料图", credit="萨尔布吕肯俱乐部 / 仅课程学习使用"),
    dict(id="career_2026", line="career", no="10", year="2026", date="2026", title="当下",
         subtitle="杜塞尔多夫 · 未完待续", caption="2026 · 杜塞尔多夫 · 未完待续",
         description="2026年，樊振东转会杜塞尔多夫，继续在球台前。故事没有结束，只是进入下一页。对回忆录来说，当下不是终点，而是正在发生的回忆。",
         quote="当下不是终点，是正在发生的回忆。",
         tags=["当下", "杜塞尔多夫", "未完待续"], image="career_2026.jpg", accent="#E7B768",
         source="原创插画", credit="FZD Memory Archive"),

    # ---------------- JERSEYS ----------------
    dict(id="jersey_2013", line="jersey", no="01", year="2013", date="2013", title="初登世界赛场",
         subtitle="中国红 / 黑", caption="2013 · 初登世界赛场 · 中国红",
         description="2013年，16岁的樊振东第一次站上世乒赛单打舞台。红色主场球衣、黑色短裤，青涩却敢打。那是他留给世界的第一帧。",
         quote="第一次被世界看见，衣服也是红的。",
         tags=["2013", "世乒赛", "中国红"], image="jersey_2013.jpg", accent="#E7B768",
         source="原创球衣插画", credit="FZD Memory Archive", colorway="中国红 / 黑", fabric="轻量速干"),
    dict(id="jersey_2016", line="jersey", no="02", year="2016", date="2016", title="萨尔布吕肯",
         subtitle="蓝紫几何 / 荧光黄", caption="2016 · 萨尔布吕肯 · 蓝紫几何",
         description="2016年世界杯，樊振东穿着彩色几何纹样球衣在萨尔布吕肯夺冠。那一年的颜色很跳，像他横空出世的球风。",
         quote="颜色越跳，心越定。",
         tags=["2016", "世界杯", "蓝紫"], image="jersey_2016.jpg", accent="#F4C542",
         source="公开报道资料图", credit="新浪体育 / 仅课程学习使用", colorway="蓝紫 / 荧光黄", fabric="轻量速干"),
    dict(id="jersey_2021", line="jersey", no="03", year="2021", date="2021", title="东京",
         subtitle="白 / 红", caption="2021 · 东京 · 白红战袍",
         description="东京奥运会，樊振东的白色领奖服与红白战袍一起被记住。男团金牌、男单银牌，那一届的白色很安静，也很重。",
         quote="白色很安静，故事很响。",
         tags=["2021", "东京", "白红"], image="jersey_2021.jpg", accent="#D24A4E",
         source="原创球衣插画", credit="FZD Memory Archive", colorway="白 / 红", fabric="透气网眼"),
    dict(id="jersey_2022", line="jersey", no="04", year="2022", date="2022", title="黑色龙纹",
         subtitle="黑 / 粉紫", caption="2022 · 成都 · 黑色龙纹",
         description="2022年成都世乒赛，黑色底、粉紫龙纹的球衣成为主场记忆。龙纹盘在胸前，像把主场的声音穿在身上。",
         quote="龙纹在胸前，主场在身后。",
         tags=["2022", "成都", "黑紫"], image="jersey_2022.jpg", accent="#E7B768",
         source="公开报道资料图", credit="新浪体育 / 仅课程学习使用", colorway="黑 / 粉紫", fabric="弹力速干"),
    dict(id="jersey_2023", line="jersey", no="05", year="2023", date="2023", title="蓝色客场",
         subtitle="深蓝 / 浅蓝", caption="2023 · 德班 · 蓝色客场",
         description="2023年德班世乒赛，蓝色渐变球衣陪着樊振东拿下男单冠军。蓝色是客场，也是他把比赛打成主场的一年。",
         quote="客场也可以打成主场。",
         tags=["2023", "德班", "蓝色"], image="jersey_2023.jpg", accent="#5D91EF",
         source="公开报道资料图", credit="新浪体育 / 仅课程学习使用", colorway="深蓝 / 浅蓝", fabric="轻量速干"),
    dict(id="jersey_2024", line="jersey", no="06", year="2024", date="2024", title="巴黎",
         subtitle="中国红 / 金", caption="2024 · 巴黎 · 中国红 / 金",
         description="巴黎奥运会，红色龙纹球衣配黑金细节。男单决赛最后一分落地，红色成为那一届奥运会最醒目的记忆之一。",
         quote="最后一分落地，红色成为答案。",
         tags=["2024", "巴黎", "中国红"], image="jersey_2024.jpg", accent="#E7B768",
         source="公开报道资料图", credit="人民日报 / 仅课程学习使用", colorway="中国红 / 金", fabric="轻量速干"),
    dict(id="jersey_2025", line="jersey", no="07", year="2025", date="2025", title="萨尔布吕肯",
         subtitle="深蓝 / 白", caption="2025 · 萨尔布吕肯 · 深蓝俱乐部",
         description="2025年留洋赛季，萨尔布吕肯的深蓝俱乐部球衣。胸前的队徽和赞助商字样，是另一种职业生涯的注脚。",
         quote="换一件球衣，还是那个握拍的人。",
         tags=["2025", "德甲", "深蓝"], image="jersey_2025.jpg", accent="#8FC3FF",
         source="原创球衣插画", credit="FZD Memory Archive", colorway="深蓝 / 白", fabric="俱乐部比赛服"),

    # ---------------- PADDLES ----------------
    dict(id="paddle_2008", line="paddle", no="01", year="2008", date="2008", title="启蒙纯木",
         subtitle="五夹纯木 / 控制优先", caption="2008 · 启蒙纯木 · 五夹",
         description="少年时期的五夹纯木底板，控制优先、手感清晰。它不追求一击致命，却把基本功、摩擦和手感一点点打进身体里。",
         quote="先把球打上台，再谈速度和力量。",
         tags=["纯木", "启蒙", "手感"], image="paddle_2008.jpg", accent="#E7B768",
         source="原创球拍插画", credit="FZD Memory Archive", spec="5-ply wood · control first"),
    dict(id="paddle_2015", line="paddle", no="02", year="2015", date="2015", title="外置芳碳",
         subtitle="芳碳 / 速度与旋转", caption="2015 · 外置芳碳 · 速度与旋转",
         description="进入主力层后，外置芳碳底板成为更具攻击性的选择。出球更快、弧线更低，正手连续进攻的压迫感开始成形。",
         quote="速度上来之后，旋转才有牙齿。",
         tags=["芳碳", "速度", "主力层"], image="paddle_2015.jpg", accent="#D9A066",
         source="原创球拍插画", credit="FZD Memory Archive", spec="outer ALC · spin + speed"),
    dict(id="paddle_2021", line="paddle", no="03", year="2021", date="2021", title="樊振东 ALC",
         subtitle="狂飙3 蓝海绵 / Dignics 09C", caption="2021 · 樊振东 ALC · 东京周期",
         description="东京周期，樊振东使用蝴蝶樊振东 ALC 底板，正手红双喜狂飙3国套蓝海绵，反手蝴蝶 Dignics 09C。稳定、扎实，适合他高质量的两面弧圈。",
         quote="器材是手的延伸，手感才是答案。",
         tags=["ALC", "狂飙3", "Dignics"], image="paddle_2021.jpg", accent="#E7B768",
         source="原创球拍插画", credit="公开资料整理 / 仅课程学习使用", spec="FH Hurricane 3 Blue · BH Dignics 09C"),
    dict(id="paddle_2024", line="paddle", no="04", year="2024", date="2024", title="巴黎之刃",
         subtitle="Super ALC / 巴黎", caption="2024 · Super ALC · 巴黎",
         description="巴黎周期，樊振东的球拍延续芳碳结构，正手狂飙3蓝海绵、反手 Dignics 09C。器材细节以官方为准，但“稳定 + 质量”始终是关键词。",
         quote="最后一板的质量，来自前面每一板的积累。",
         tags=["Super ALC", "巴黎", "大满贯"], image="paddle_2024.jpg", accent="#E7B768",
         source="原创球拍插画", credit="公开资料整理 / 仅课程学习使用", spec="FH Hurricane 3 Blue · BH Dignics 09C"),
    dict(id="paddle_2026", line="paddle", no="05", year="2026", date="2026", title="杜塞尔多夫",
         subtitle="现在 / 继续", caption="2026 · 杜塞尔多夫 · 现在",
         description="2026年，球拍配置仍在延续：樊振东 ALC 系列底板，正手狂飙3蓝海绵，反手 Dignics 09C。装备会更新，握拍的手没有变。",
         quote="拍子会旧，手感会新。",
         tags=["现在", "杜塞尔多夫", "继续"], image="paddle_2026.jpg", accent="#8FC3FF",
         source="原创球拍插画", credit="公开资料整理 / 仅课程学习使用", spec="FH Hurricane 3 Blue · BH Dignics 09C"),
]

LINES = {
    "career": dict(label="生涯", en="CAREER", accent="#E7B768", desc="从第一块球拍到巴黎，再到当下。"),
    "jersey": dict(label="球衣", en="JERSEY", accent="#D24A4E", desc="颜色会变，红色底色不变。"),
    "paddle": dict(label="球拍", en="PADDLE", accent="#59B89A", desc="从纯木到芳碳，手感一直在。"),
}

OUT_WEB = os.path.join(BASE, "web")
OUT_ETS = os.path.join(BASE, "entry", "src", "main", "ets", "data")
os.makedirs(OUT_WEB, exist_ok=True)
os.makedirs(OUT_ETS, exist_ok=True)

with open(os.path.join(OUT_WEB, "data.js"), "w", encoding="utf-8") as f:
    f.write("window.MEMORIES = " + json.dumps(ITEMS, ensure_ascii=False, indent=2) + ";\n")
    f.write("window.LINES = " + json.dumps(LINES, ensure_ascii=False, indent=2) + ";\n")

# ArkTS seed file
def esc(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")

lines = []
lines.append("import { MemoryItem, MemoryLine } from '../model/MemoryModels';")
lines.append("")
lines.append("export const MEMORIES: MemoryItem[] = [")
for it in ITEMS:
    tags = "[" + ", ".join("'" + esc(t) + "'" for t in it["tags"]) + "]"
    line = "MemoryLine.CAREER" if it["line"] == "career" else ("MemoryLine.JERSEY" if it["line"] == "jersey" else "MemoryLine.PADDLE")
    lines.append("  new MemoryItem(")
    lines.append(f"    '{esc(it['id'])}', {line}, '{esc(it['no'])}', '{esc(it['year'])}', '{esc(it['date'])}',")
    lines.append(f"    '{esc(it['title'])}', '{esc(it['subtitle'])}', '{esc(it['caption'])}',")
    lines.append(f"    '{esc(it['description'])}', '{esc(it['quote'])}', {tags},")
    lines.append(f"    $r('app.media.{it['image'][:-4]}'), '{it['accent']}',")
    lines.append(f"    '{esc(it.get('colorway', ''))}', '{esc(it.get('fabric', ''))}', '{esc(it.get('spec', ''))}',")
    lines.append(f"    '{esc(it['source'])}', '{esc(it['credit'])}'")
    lines.append("  ),")
lines.append("];")
lines.append("")
lines.append("export function getMemories(line?: MemoryLine): MemoryItem[] {")
lines.append("  if (line === undefined) { return MEMORIES; }")
lines.append("  return MEMORIES.filter((item: MemoryItem) => item.line === line);")
lines.append("}")
lines.append("")
lines.append("export function getMemoryById(id: string): MemoryItem | undefined {")
lines.append("  return MEMORIES.find((item: MemoryItem) => item.id === id);")
lines.append("}")
with open(os.path.join(OUT_ETS, "MemoryData.ets"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("items:", len(ITEMS))
