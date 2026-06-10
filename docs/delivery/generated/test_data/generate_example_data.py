from __future__ import annotations

import csv
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RNG = random.Random(20260526)


PERFORMANCE_HEADER = [
    "样品编号",
    "数据来源",
    "来源编号",
    "标题",
    "材料体系",
    "材料类别",
    "化学式",
    "掺杂/包覆",
    "制备工艺",
    "前驱体/铁源",
    "锂源",
    "磷源",
    "碳源",
    "烧结温度(℃)",
    "烧结时间(h)",
    "D50(μm)",
    "比表面积(m2/g)",
    "碳含量(wt%)",
    "压实密度(g/cm3)",
    "振实密度(g/cm3)",
    "电解液",
    "电压窗口(V)",
    "测试倍率(C)",
    "首圈放电比容量(mAh/g)",
    "100圈容量(mAh/g)",
    "100圈保持率(%)",
    "库仑效率(%)",
    "5C容量(mAh/g)",
    "低温容量保持率(%)",
    "测试温度(℃)",
    "应用场景",
    "关键结论",
    "风险/限制",
]

PATENT_HEADER = [
    "专利号",
    "标题",
    "材料体系",
    "技术路线",
    "关键权利要求",
    "粒径/级配",
    "压实密度(g/cm3)",
    "1C放电比容量(mAh/g)",
    "倍率性能",
    "循环保持率(%)",
    "安全/热稳定性",
    "适用场景",
    "可用于提问的问题",
]

CYCLE_HEADER = [
    "测试编号",
    "样品编号",
    "材料体系",
    "压实密度(g/cm3)",
    "倍率(C)",
    "循环圈数",
    "温度(℃)",
    "放电比容量(mAh/g)",
    "容量保持率(%)",
    "库仑效率(%)",
    "电压窗口(V)",
    "测试备注",
    "来源编号",
]


SOURCE_IDS = [
    "doi=10.1021/acs.iecr.9b01530",
    "doi=10.1007/s11581-021-04078-x",
    "doi=10.1149/1945-7111_ad2817",
    "doi=10.1039/D2CP05948G",
    "doi=10.1002/adfm.202409230",
    "CN109192948B",
    "CN113562714A",
    "CN115863630B",
    "CN118156497A",
    "CN116986574A",
]

MATERIAL_PROFILES = [
    {
        "system": "LFP/C",
        "category": "正极",
        "formula": "LiFePO4/C",
        "doping": "碳包覆",
        "method": "喷雾干燥+固相烧结",
        "precursor": "FePO4",
        "li": "Li2CO3",
        "p": "NH4H2PO4",
        "carbon": "葡萄糖",
        "voltage": "2.5-3.65",
        "capacity": (150.0, 166.0),
        "retention": (94.0, 99.2),
        "density": (2.35, 2.75),
        "d50": (0.6, 12.0),
        "surface": (6.0, 21.0),
        "carbon_pct": (1.2, 3.8),
        "application": "动力电池/储能电池",
        "finding": "颗粒球形化与均匀碳包覆提升压实密度和倍率性能",
        "risk": "压实过高会降低电解液浸润并损失5C容量",
    },
    {
        "system": "高压实LFP",
        "category": "正极",
        "formula": "LiFePO4",
        "doping": "多粒径级配",
        "method": "二次颗粒级配+辊压",
        "precursor": "球形FePO4",
        "li": "LiOH·H2O",
        "p": "H3PO4",
        "carbon": "蔗糖+导电炭黑",
        "voltage": "2.5-3.65",
        "capacity": (148.0, 160.0),
        "retention": (95.5, 99.0),
        "density": (2.62, 2.95),
        "d50": (4.0, 18.0),
        "surface": (3.5, 12.0),
        "carbon_pct": (0.8, 2.6),
        "application": "高体积能量密度电芯",
        "finding": "大小颗粒填充孔隙后压实密度明显提高",
        "risk": "细粉比例过高会造成倍率性能下降",
    },
    {
        "system": "LMFP/C",
        "category": "正极",
        "formula": "LiMn0.6Fe0.4PO4/C",
        "doping": "Mn/Fe固溶+碳包覆",
        "method": "共沉淀+碳热还原",
        "precursor": "MnFePO4",
        "li": "Li2CO3",
        "p": "NH4H2PO4",
        "carbon": "柠檬酸",
        "voltage": "2.5-4.5",
        "capacity": (135.0, 158.0),
        "retention": (89.0, 97.5),
        "density": (2.45, 3.02),
        "d50": (1.5, 10.0),
        "surface": (8.0, 25.0),
        "carbon_pct": (1.5, 4.2),
        "application": "高电压正极",
        "finding": "LMFP提高电压平台，需通过碳包覆改善电子导电性",
        "risk": "锰溶出和界面阻抗会影响长循环",
    },
    {
        "system": "LFP+导电网络",
        "category": "正极",
        "formula": "LiFePO4/CNT/SP",
        "doping": "CNT+Super P复合导电剂",
        "method": "水系浆料分散+涂布",
        "precursor": "商业LFP粉体",
        "li": "N/A",
        "p": "N/A",
        "carbon": "CNT+Super P",
        "voltage": "2.5-3.65",
        "capacity": (145.0, 162.0),
        "retention": (93.0, 98.8),
        "density": (2.20, 2.58),
        "d50": (0.8, 6.5),
        "surface": (10.0, 28.0),
        "carbon_pct": (2.5, 5.5),
        "application": "高倍率/低温电池",
        "finding": "复合导电网络改善3C和5C容量输出",
        "risk": "导电剂过量会牺牲压实密度和能量密度",
    },
    {
        "system": "Si/C负极匹配LFP",
        "category": "负极",
        "formula": "SiOx/Graphite/C",
        "doping": "碳包覆+弹性粘结剂",
        "method": "机械融合+低温碳化",
        "precursor": "SiOx+石墨",
        "li": "N/A",
        "p": "N/A",
        "carbon": "沥青碳",
        "voltage": "0.01-1.5",
        "capacity": (420.0, 780.0),
        "retention": (80.0, 94.0),
        "density": (1.35, 1.75),
        "d50": (3.0, 15.0),
        "surface": (2.5, 9.0),
        "carbon_pct": (4.0, 12.0),
        "application": "LFP全电池负极匹配",
        "finding": "硅碳提升全电池能量密度，需控制首效损失",
        "risk": "体积膨胀导致循环保持率下降",
    },
]

PATENT_ROWS = [
    [
        "CN109192948B",
        "一种高压实密度磷酸铁锂正极材料及制备方法",
        "LFP",
        "双颗粒级配",
        "球形小颗粒填充大颗粒空隙，提高极片堆积效率",
        "大颗粒+小颗粒二元级配",
        "2.69-2.72",
        "149-150",
        "1C稳定放电",
        "98.0",
        "热稳定性良好",
        "动力电池",
        "哪些专利通过双颗粒级配提高LFP压实密度？",
    ],
    [
        "CN113562714A",
        "多粒度混合磷酸铁锂材料及其制备方法",
        "LFP",
        "多粒度混合",
        "大颗粒磷酸铁与小颗粒按质量比5-50%混合",
        "0.05-0.3μm小颗粒+0.6-3μm大颗粒",
        "2.83-2.87",
        ">150",
        "3C/0.1C保持较高",
        "97.5",
        "压实后结构稳定",
        "储能/动力兼顾",
        "压实密度超过2.8 g/cm3的方案有哪些？",
    ],
    [
        "CN115863630B",
        "基于数学模型的磷酸铁锂级配优化方法",
        "LFP",
        "数学模型优化",
        "通过公式计算不同粒径材料比例，降低级配误差",
        "A/B粒径组分模型匹配",
        "2.84-2.95",
        "151",
        "倍率性能稳定",
        "98.2",
        "批次一致性较好",
        "生产工艺优化",
        "哪些方案用数学模型预测压实密度？",
    ],
    [
        "CN118156497A",
        "精确粒径分布调控的磷酸铁锂材料",
        "LFP",
        "粒径分布调控",
        "限制小于1μm与大于等于3μm颗粒体积占比",
        "<1μm占比50-75%，>=3μm占比5-25%",
        "2.544",
        "150.6",
        "3C/0.1C=0.82",
        "96.8",
        "过宽分布会降低倍率",
        "高倍率正极",
        "粒径分布过宽为什么会影响倍率性能？",
    ],
    [
        "CN101877401A",
        "球形二次颗粒磷酸铁锂的制备方法",
        "LFP/C",
        "共沉淀+喷雾干燥",
        "纳米一次颗粒与碳源混合后喷雾干燥形成球形二次颗粒",
        "纳米一次颗粒/球形二次颗粒",
        "2.40-2.60",
        "145-155",
        "5C容量改善",
        "95.0",
        "碳包覆提高导电性",
        "倍率型电池",
        "球形二次颗粒对LFP性能有什么影响？",
    ],
    [
        "CN113086959B",
        "大粒径二次球形磷酸铁锂材料",
        "LFP",
        "大粒径球形化",
        "控制二次球形颗粒粒径并降低细粉比例",
        "D50约10-18μm",
        "2.62-2.78",
        "148-158",
        "2C容量保持稳定",
        "97.0",
        "极片加工稳定性好",
        "高压实正极",
        "大粒径二次球形颗粒适合什么应用？",
    ],
    [
        "CN116986574A",
        "高压实密度磷酸锰铁锂正极材料",
        "LMFP",
        "锰铁固溶+多粒径级配",
        "通过LMFP颗粒级配提升压实密度和电压平台",
        "D50分段控制",
        "2.80-3.00",
        "142-155",
        "高电压倍率需碳包覆",
        "94.5",
        "需控制Mn溶出",
        "高能量密度电芯",
        "LMFP相对LFP的优势和风险是什么？",
    ],
    [
        "CN118458747A",
        "工业级磷酸铁锂极片压实工艺",
        "LFP",
        "多段辊压",
        "通过多段压力和速度控制减少极片反弹",
        "商业LFP粉体",
        "2.30-2.60",
        "148-160",
        "5C容量受孔隙率影响",
        "96.0",
        "过压会带来浸润不足",
        "规模化涂布辊压",
        "LFP压实密度过高有什么风险？",
    ],
    [
        "CN115692635A",
        "一种磷酸铁锂电池电压窗口控制方法",
        "LFP电芯",
        "电压窗口优化",
        "限定充放电窗口以平衡容量与寿命",
        "正负极匹配",
        "N/A",
        "N/A",
        "2.5-3.65V窗口循环稳定",
        "98.5",
        "减少过充热风险",
        "BMS策略",
        "LFP电芯电压窗口如何影响循环寿命？",
    ],
    [
        "CN116368096A",
        "磷酸铁锂材料电压平台识别方法",
        "LFP",
        "平台电压分析",
        "识别3.4V附近平台并用于电芯一致性评价",
        "N/A",
        "N/A",
        "N/A",
        "平台容量占比评价",
        "N/A",
        "异常曲线可提示失效",
        "检测/分选",
        "如何从电压平台判断LFP材料一致性？",
    ],
]


def fmt(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}".rstrip("0").rstrip(".")


def choose_source(index: int) -> tuple[str, str]:
    if index % 5 == 0:
        return "专利", RNG.choice([item for item in SOURCE_IDS if item.startswith("CN")])
    if index % 7 == 0:
        return "实验", f"EXP-LFP-{20260000 + index}"
    return "文献", RNG.choice([item for item in SOURCE_IDS if item.startswith("doi=")])


def make_performance_row(index: int, *, edge: bool = False) -> list[str]:
    profile = RNG.choice(MATERIAL_PROFILES)
    source_type, source_id = choose_source(index)
    capacity = RNG.uniform(*profile["capacity"])
    retention = RNG.uniform(*profile["retention"])
    capacity_100 = capacity * retention / 100
    density = RNG.uniform(*profile["density"])
    d50 = RNG.uniform(*profile["d50"])
    surface = RNG.uniform(*profile["surface"])
    carbon = RNG.uniform(*profile["carbon_pct"])
    tap_density = density * RNG.uniform(0.52, 0.72)
    rate_5c = capacity * RNG.uniform(0.72, 0.92)
    low_temp = RNG.uniform(58.0, 89.0)
    temp = RNG.choice([25, 25, 25, 45, -20, 0])
    rate = RNG.choice(["0.1C", "0.2C", "0.5C", "1C", "2C", "5C"])
    title = f"{profile['system']}材料性能与工艺参数记录-{index:03d}"

    if edge:
        if index % 6 == 0:
            density_text = f"{fmt(density - 0.03)}-{fmt(density + 0.04)}"
        elif index % 10 == 0:
            density_text = ">2.80"
        else:
            density_text = fmt(density)

        if index % 8 == 0:
            capacity_text = ">150"
        elif index % 9 == 0:
            capacity_text = "未测试"
        else:
            capacity_text = fmt(capacity, 1)

        if index % 7 == 0:
            temp_text = "25±2"
        elif index % 11 == 0:
            temp_text = "室温"
        else:
            temp_text = str(temp)

        retention_text = "~" + fmt(retention, 1) if index % 5 == 0 else fmt(retention, 1)
        d50_text = "<1" if index % 13 == 0 else fmt(d50, 2)
        risk = "" if index % 4 else profile["risk"]
    else:
        density_text = fmt(density)
        capacity_text = fmt(capacity, 1)
        temp_text = str(temp)
        retention_text = fmt(retention, 1)
        d50_text = fmt(d50, 2)
        risk = profile["risk"]

    return [
        f"BAT-{index:04d}",
        source_type,
        source_id,
        title,
        profile["system"],
        profile["category"],
        profile["formula"],
        profile["doping"],
        profile["method"],
        profile["precursor"],
        profile["li"],
        profile["p"],
        profile["carbon"],
        str(RNG.choice([650, 680, 700, 720, 750, 780])),
        str(RNG.choice([6, 8, 10, 12, 16])),
        d50_text,
        fmt(surface, 2),
        fmt(carbon, 2),
        density_text,
        fmt(tap_density, 2),
        RNG.choice(["1M LiPF6 EC/DMC", "1M LiPF6 EC/DEC", "LiFSI+FEC体系", "水系半电池测试"]),
        profile["voltage"],
        rate,
        capacity_text,
        fmt(capacity_100, 1),
        retention_text,
        fmt(RNG.uniform(97.8, 99.9), 2),
        fmt(rate_5c, 1),
        fmt(low_temp, 1),
        temp_text,
        profile["application"],
        profile["finding"],
        risk,
    ]


def make_cycle_rows(count: int) -> list[list[str]]:
    rows: list[list[str]] = []
    for index in range(1, count + 1):
        profile = RNG.choice(MATERIAL_PROFILES[:4])
        base_capacity = RNG.uniform(*profile["capacity"])
        density = RNG.uniform(*profile["density"])
        rate = RNG.choice(["0.2C", "0.5C", "1C", "2C", "3C", "5C"])
        cycles = RNG.choice([50, 100, 200, 500, 1000])
        temp = RNG.choice([25, 25, 45, -20, 0])
        rate_factor = {"0.2C": 1.0, "0.5C": 0.97, "1C": 0.94, "2C": 0.88, "3C": 0.82, "5C": 0.74}[rate]
        cycle_factor = max(0.72, 1 - cycles / 10000)
        temp_factor = 0.72 if temp == -20 else 0.86 if temp == 0 else 0.96 if temp == 45 else 1.0
        capacity = base_capacity * rate_factor * temp_factor
        retention = RNG.uniform(88.0, 99.0) * cycle_factor
        note = "高压实样品，关注浸润" if density > 2.7 else "常规循环测试"
        if rate in {"3C", "5C"}:
            note = "高倍率测试，比较容量衰减"
        rows.append(
            [
                f"CYCLE-{index:04d}",
                f"BAT-{RNG.randint(1, 180):04d}",
                profile["system"],
                fmt(density),
                rate,
                str(cycles),
                str(temp),
                fmt(capacity, 1),
                fmt(retention, 1),
                fmt(RNG.uniform(98.0, 99.95), 2),
                profile["voltage"],
                note,
                RNG.choice(SOURCE_IDS),
            ]
        )
    return rows


def write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        writer.writerows(rows)


def main() -> None:
    small = [make_performance_row(i) for i in range(1, 25)]
    medium = [make_performance_row(i) for i in range(1, 121)]
    edge = [make_performance_row(i, edge=True) for i in range(1, 37)]

    all_rows = []
    for index, row in enumerate([*medium, *edge], start=1):
        next_row = list(row)
        next_row[0] = f"BAT-{index:04d}"
        all_rows.append(next_row)

    cycle_rows = make_cycle_rows(80)

    write_csv(ROOT / "example-data-test-small.csv", PERFORMANCE_HEADER, small)
    write_csv(ROOT / "example-data-test-medium.csv", PERFORMANCE_HEADER, medium)
    write_csv(ROOT / "example-data-test-edge-cases.csv", PERFORMANCE_HEADER, edge)
    write_csv(ROOT / "example-data-test-all.csv", PERFORMANCE_HEADER, all_rows)

    write_csv(ROOT / "battery-material-performance-small.csv", PERFORMANCE_HEADER, small)
    write_csv(ROOT / "battery-material-performance-medium.csv", PERFORMANCE_HEADER, medium)
    write_csv(ROOT / "battery-cycle-rate-edge-cases.csv", PERFORMANCE_HEADER, edge)
    write_csv(ROOT / "battery-table-qa-all.csv", PERFORMANCE_HEADER, all_rows)
    write_csv(ROOT / "battery-patent-comparison.csv", PATENT_HEADER, PATENT_ROWS)
    write_csv(ROOT / "battery-cycle-rate-tests.csv", CYCLE_HEADER, cycle_rows)

    print(f"generated test CSV files under {ROOT}")


if __name__ == "__main__":
    main()
