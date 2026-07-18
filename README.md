<div align="center">

# 🀄 命理圆桌会 · bazi-roundtable

**让多位不同流派的命理师，对同一张八字命盘圆桌论命**

多视角总评 · 交叉质疑 · 可证伪断语 · 逐轮记分复盘

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-2ea44f.svg?style=flat-square)](LICENSE)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-8A2BE2.svg?style=flat-square&logo=anthropic&logoColor=white)](https://claude.com/claude-code)
[![Python](https://img.shields.io/badge/排盘脚本-Python-3776AB.svg?style=flat-square&logo=python&logoColor=white)](bazi-roundtable/scripts/paipan.py)
[![Stars](https://img.shields.io/github/stars/yanouyuan-bit/bazi-roundtable?style=flat-square&color=e3b341)](https://github.com/yanouyuan-bit/bazi-roundtable/stargazers)

<sub>A Claude skill that stages a multi-school BaZi (Four Pillars) roundtable: fortune-tellers from rival schools analyze the same chart, cross-examine each other's methodology, issue falsifiable predictions with probabilities and time windows, and keep score round by round. Content is in Chinese, matching its use case.</sub>

</div>

---

## 💡 为什么做这个

单一 AI 论命有系统性通病：

- 📈 普遍**高估命主层次**，怎么批都是"中上之命"
- 🪞 **顺着用户说**，用户报出实况后立刻"其实盘里早写了"（事后倒推）
- 🌫️ 喜忌含糊到"喜金水"就完事，**无法准确到字**
- 🎭 断语留两个出口，怎么都对，**不可证伪**

这些毛病靠"提醒模型注意"治不好。本 skill 的思路是**结构性对冲**：

| 机制 | 对冲什么 |
|:--|:--|
| 四个方法论真实分歧的流派互相 counter-review | 单一视角的盲区与趋同 |
| 主持人从严记分：宽泛命中不邀功、含糊断语不入表 | 不可证伪的"怎么都对" |
| 断语强制格式：结论 + 概率 + 应期 + "若……则记我错" | 双头下注与断语漂移 |
| 复盘环节明令禁止倒推，违规点名（六类违规行为清单） | 事后合理化 |
| 场外观众按断语类型重排战绩、检查集体偏差 | 四家共识其实是集体抄社会先验 |

> 定位是"君子玩易"：把命理当作严肃的解释学与推理训练场，不当安慰工具，也不当宿命剧本——**断语当风险清单用，桨在命主自己手里。**

## 👥 阵容

<table>
<tr>
<td width="50%" valign="top">

**🩸 盲派**

做功、宾主，术语密集，敢下凶断

</td>
<td width="50%" valign="top">

**🏛️ 格局派**

子平格局法，引经据典，只答骨架类问题

</td>
</tr>
<tr>
<td width="50%" valign="top">

**🌡️ 调候派**

《穷通宝鉴》一系，寒暖燥湿，爱押体感类赌注

</td>
<td width="50%" valign="top">

**📰 民国派**

韦千里一系，白话直断，敢报具体数字，输得起

</td>
</tr>
<tr>
<td width="50%" valign="top">

**🎙️ 主持人**

出题、控场、记分、点名违规

</td>
<td width="50%" valign="top">

**🧑‍🤝‍🧑 场外观众**（可选）

外行元批评者，检查集体偏差

</td>
</tr>
</table>

> 角色被批评时有两种回应档位：**理想版**（认错干脆、立军令状）与**真实版**（护招牌、抬师承、卸责——符合真实从业者利益结构的话术），可对照呈现。

## 🔄 论命流程

流程**互动式逐环节推进**：每次只走一个环节，主持人开场、收场、报下一步选项，然后停下等你下令。环节可独立触发、自由组合：

```mermaid
flowchart LR
    A["起盘总评"] --> B["交叉 review"] --> C["圆桌问答"] --> D["可证伪硬断轮"]
    D --> E["结账复盘<br/>报实况对账记分"] --> F["前瞻预判"] --> G["观众点评"] --> H["第二次批命"]

    style A fill:#8957e522,stroke:#8957e5,color:#c9d1d9
    style B fill:#8957e522,stroke:#8957e5,color:#c9d1d9
    style C fill:#8957e522,stroke:#8957e5,color:#c9d1d9
    style D fill:#da363322,stroke:#da3633,color:#c9d1d9
    style E fill:#2ea04322,stroke:#2ea043,color:#c9d1d9
    style F fill:#1f6feb22,stroke:#1f6feb,color:#c9d1d9
    style G fill:#1f6feb22,stroke:#1f6feb,color:#c9d1d9
    style H fill:#8957e522,stroke:#8957e5,color:#c9d1d9
```

> 🎯 逐环节停顿不只是阅读节奏——**结账复盘的含金量取决于你在硬断轮之前没有透露实况**。别急着报答案，让他们先把赌注挂满。

也支持轻量模式（"盲派看一眼就行"），或明确说"一次跑完"取消逐轮停顿。中途可随时点名追问某一家、质疑某条断语。

## 📦 安装

<details open>
<summary><b>Claude Code</b></summary>

<br>

```bash
# 个人级：复制到 ~/.claude/skills/
cp -r bazi-roundtable ~/.claude/skills/

# 或项目级：复制到项目的 .claude/skills/
cp -r bazi-roundtable your-project/.claude/skills/
```

</details>

<details>
<summary><b>claude.ai</b></summary>

<br>

下载仓库根目录的 **[bazi-roundtable.zip](https://github.com/yanouyuan-bit/bazi-roundtable/raw/main/bazi-roundtable.zip)**（点击直接下载），在 **Settings → Capabilities → Skills** 上传即可。

这个 zip 已按 skill 上传规范打包：`SKILL.md` 位于压缩包根部、路径用标准正斜杠、含合规 YAML frontmatter，下载即用。

> ⚠️ **注意别用 GitHub 自动生成的 "Source code (zip)"**——那个会多套一层目录、把 SKILL.md 埋进子目录，上传会校验失败。

<sub>维护者注：CI（`.github/workflows/zip.yml`）会在每次 push 时校验此 zip 与 `bazi-roundtable/` 源文件一致，不一致则构建失败；打 `v*` tag 时自动构建 zip 并附到 GitHub Release。本地重打包请用保持正斜杠路径的工具（Windows PowerShell 5.1 的 `Compress-Archive` 会写入反斜杠路径，勿用）。</sub>

</details>

<details>
<summary><b>排盘脚本（推荐）</b></summary>

<br>

盘面准确是一切断语的地基。若只有出生日期时间而无四柱，skill 会调用确定性排盘脚本而非让模型心算节气与日柱：

```bash
pip install lunar-python
python bazi-roundtable/scripts/paipan.py 1990-03-15 10:30 男     # 排盘+大运+换节警告
python bazi-roundtable/scripts/paipan.py --years 2026 2045       # 流年干支
python bazi-roundtable/scripts/paipan.py --selftest              # 自检
```

claude.ai 等无法运行脚本的环境下，skill 会要求你提供可信排盘工具的完整结果。

</details>

## 🚀 使用

贴出八字命盘（四柱干支 + 性别 + 大运），然后：

```text
请用圆桌形式批这个盘
乾造：甲子 丙寅 戊午 壬戌，3 岁起运……
```

## 📁 目录结构

```text
bazi-roundtable/
├── SKILL.md              # 流程骨架、角色简表、纪律清单、输出规范、盘面事实层规则
├── scripts/
│   └── paipan.py         # 确定性排盘：四柱/藏干/十神/大运/换节警告/流年干支
├── references/
│   ├── discipline.md     # 反倒推纪律、记分规则、真实版话术库、观众框架
│   ├── disputes.md       # 争议矩阵：九大争议 × 四派互斥立场（交叉 review 弹药库）
│   ├── ganzhi-years.md   # 流年干支速查表 1940–2060（禁止心算年份干支）
│   ├── archive.md        # 跨会话档案：积分/悬案/概率校准的持久化格式
│   ├── mangpai.md        # 盲派：做功、宾主、作用优先级、取象
│   ├── geju.md           # 格局派：成格破格、用神清浊、十神生克
│   ├── tiaohou.md        # 调候派：十干十二月调候用神表（附版本声明）、寒暖取象
│   └── minguo.md         # 民国派：韦千里式批命体例、报数规则
└── evals/
    └── evals.json        # 验收测试用例（不随 zip 分发，配合 skill-creator 运行）
```

**争议矩阵**（disputes.md）收录九大争议（辰土算不算根、合绊损耗几成、虚透之火如何断……），同一争议四派立场互斥——这是圆桌上真实冲突的燃料。

**跨会话档案**：结账复盘与前瞻预判后，主持人把积分表、悬案清单、概率校准账本写入档案（有文件系统时存 `bazi-archives/`，claude.ai 上输出档案块由你保存）——几个月后拿实况回来对账，赌注还在。

## 🚧 边界

- 未成年人感情/关系类问题不提供命理框架分析
- 健康断语止于"提醒体检方向"，不做诊断
- 财务/法律相关断语不构成投资或法律建议
- 断语的实用价值**不依赖命理为真**——它值钱是因为它敢被证伪

---

<div align="center">

**把命理当作严肃的解释学与推理训练场——断语当风险清单用，桨在命主自己手里。**

用 [MIT](LICENSE) 协议开源 · 如果它对你有用，欢迎点一颗 ⭐

</div>
