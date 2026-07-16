# -*- coding: utf-8 -*-
"""确定性排盘脚本（bazi-roundtable 盘面事实层）

skill 规则：凡用户只给出生日期时间而未给四柱，必须用本脚本排盘，
禁止模型徒手推算节气分界、日柱、大运起排。

依赖：lunar-python（纯 Python，无需编译）
    pip install lunar-python

用法：
    python paipan.py 1990-03-15 10:30 男          # 排盘 + 大运
    python paipan.py 1990-03-15 10:30 女 --sect 1  # 晚子时日柱算次日（流派选项）
    python paipan.py --year 2031                   # 单年流年干支
    python paipan.py --years 2026 2045             # 流年干支区间
    python paipan.py --selftest                    # 自检（节气分界等已知用例）

说明：
- 年柱、月柱以立春/节（非中气）交接的精确时刻为界
- 出生时间若临近换节（±12 小时内）会打出警告：报错的出生时间会翻转月柱甚至年柱
- 真太阳时校正不在本脚本范围内：如需校正，请用户先按出生地经度换算后再输入
"""
import sys
import argparse

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"


def year_ganzhi(year: int) -> str:
    """公历年份 -> 流年干支（以立春为界；本函数按年份号计算，界内自辨）"""
    return STEMS[(year - 4) % 10] + BRANCHES[(year - 4) % 12]


def print_year_range(start: int, end: int) -> None:
    print("流年干支（以立春为界：立春前出生/事件属上一年干支）")
    for y in range(start, end + 1):
        print(f"  {y}  {year_ganzhi(y)}")


def selftest() -> None:
    from lunar_python import Solar

    cases = [
        # (y, m, d, h, 期望四柱) —— 覆盖立春前后、节气换月、普通用例
        ((2024, 2, 3, 12), ("癸卯", "乙丑", "丁酉", "丙午")),   # 立春(2024-02-04 16:27)前
        ((2024, 2, 5, 12), ("甲辰", "丙寅", "己亥", "庚午")),   # 立春后
        ((1990, 3, 15, 10), ("庚午", "己卯", "己卯", "己巳")),
        ((2026, 7, 16, 12), ("丙午", "乙未", "辛卯", "甲午")),  # 小暑后未月
    ]
    ok = True
    for (y, m, d, h), expect in cases:
        ec = Solar.fromYmdHms(y, m, d, h, 0, 0).getLunar().getEightChar()
        got = (ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime())
        mark = "OK " if got == expect else "FAIL"
        if got != expect:
            ok = False
        print(f"[{mark}] {y}-{m:02d}-{d:02d} {h:02d}:00  期望 {' '.join(expect)}  实得 {' '.join(got)}")
    # 流年公式自检
    for y, gz in [(1984, "甲子"), (2024, "甲辰"), (2026, "丙午")]:
        mark = "OK " if year_ganzhi(y) == gz else "FAIL"
        if year_ganzhi(y) != gz:
            ok = False
        print(f"[{mark}] 流年 {y} = {year_ganzhi(y)}（期望 {gz}）")
    sys.exit(0 if ok else 1)


def paipan(date_str: str, time_str: str, gender: str, sect: int) -> None:
    from lunar_python import Solar

    y, m, d = (int(x) for x in date_str.replace("/", "-").split("-"))
    hh, mm = (int(x) for x in time_str.replace("：", ":").split(":"))
    solar = Solar.fromYmdHms(y, m, d, hh, mm, 0)
    lunar = solar.getLunar()
    ec = lunar.getEightChar()
    ec.setSect(sect)

    print(f"# 盘面事实表（{date_str} {time_str} {gender}，晚子时日柱={'当日' if sect == 2 else '次日'}）")
    print()
    print("## 四柱")
    print()
    print("| | 年柱 | 月柱 | 日柱 | 时柱 |")
    print("|---|---|---|---|---|")
    print(f"| 干支 | {ec.getYear()} | {ec.getMonth()} | {ec.getDay()} | {ec.getTime()} |")
    print(f"| 天干十神 | {ec.getYearShiShenGan()} | {ec.getMonthShiShenGan()} | 日主 | {ec.getTimeShiShenGan()} |")
    zhi_ss = [
        "/".join(ec.getYearShiShenZhi()),
        "/".join(ec.getMonthShiShenZhi()),
        "/".join(ec.getDayShiShenZhi()),
        "/".join(ec.getTimeShiShenZhi()),
    ]
    print(f"| 支藏十神 | {zhi_ss[0]} | {zhi_ss[1]} | {zhi_ss[2]} | {zhi_ss[3]} |")
    hide = [
        "/".join(ec.getYearHideGan()),
        "/".join(ec.getMonthHideGan()),
        "/".join(ec.getDayHideGan()),
        "/".join(ec.getTimeHideGan()),
    ]
    print(f"| 支藏干 | {hide[0]} | {hide[1]} | {hide[2]} | {hide[3]} |")
    print()
    print(f"- 日主：{ec.getDay()[0]}　旬空：年柱空亡 {ec.getYearXunKong()}，日柱空亡 {ec.getDayXunKong()}")

    # 换节临近警告
    prev_jie, next_jie = lunar.getPrevJie(), lunar.getNextJie()
    for jie, rel in ((prev_jie, "上一节"), (next_jie, "下一节")):
        js = jie.getSolar()
        delta_h = abs(js.subtractMinute(solar)) / 60.0
        line = f"- {rel}：{jie.getName()}　{js.toYmdHms()}（距出生 {delta_h:.1f} 小时）"
        if delta_h <= 12:
            line += "　⚠️ 临近换节：出生时间若有误差，月柱（立春则连年柱）会翻转，务必与命主核实钟点"
        print(line)
    if hh == 23 or hh == 0:
        print("- ⚠️ 子时出生：早晚子时的日柱归属存在流派分歧，可用 --sect 1/2 对照两种排法")

    # 大运
    yun = ec.getYun(1 if gender in ("男", "m", "M", "male") else 0)
    print()
    print("## 大运")
    print()
    print(f"- 起运：出生后 {yun.getStartYear()} 年 {yun.getStartMonth()} 个月 {yun.getStartDay()} 天"
          f"（{'顺' if yun.isForward() else '逆'}排）")
    print()
    print("| 大运 | 起于（公历年） | 虚岁 | 流年 |")
    print("|---|---|---|---|")
    for dy in yun.getDaYun()[1:9]:
        start = dy.getStartYear()
        liunian = "、".join(f"{yy} {year_ganzhi(yy)}" for yy in range(start, start + 10, 3))
        print(f"| {dy.getGanZhi()} | {start} | {dy.getStartAge()} | {liunian} … |")
    print()
    print("> 流年干支列仅为速查抽样（每 3 年一列），完整逐年干支用 `--years 起 止` 生成。")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="bazi-roundtable 排盘脚本")
    ap.add_argument("date", nargs="?", help="公历出生日期，如 1990-03-15")
    ap.add_argument("time", nargs="?", help="出生时间（24 小时制），如 10:30")
    ap.add_argument("gender", nargs="?", help="男 / 女（决定大运顺逆）")
    ap.add_argument("--sect", type=int, default=2, choices=(1, 2),
                    help="晚子时(23-24点)日柱归属：2=算当日(默认)，1=算次日")
    ap.add_argument("--year", type=int, help="查询单年流年干支")
    ap.add_argument("--years", type=int, nargs=2, metavar=("START", "END"), help="查询流年干支区间")
    ap.add_argument("--selftest", action="store_true", help="运行自检用例")
    args = ap.parse_args()

    if args.selftest:
        selftest()
    elif args.year:
        print(f"{args.year}  {year_ganzhi(args.year)}（以立春为界）")
    elif args.years:
        print_year_range(args.years[0], args.years[1])
    elif args.date and args.time and args.gender:
        try:
            paipan(args.date, args.time, args.gender, args.sect)
        except ImportError:
            print("缺少依赖：请先运行  pip install lunar-python", file=sys.stderr)
            sys.exit(1)
    else:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
