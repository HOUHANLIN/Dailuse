from graphviz import Digraph

def build():
    g = Digraph("implant_flow", format="pdf")
    # 论文风格：黑白、矢量、统一字体、线条清晰
    g.attr(
        rankdir="TB",
        fontsize="13",
        fontname="SimSun",  # 中文可用宋体/思源宋体等
        bgcolor="#F5F5F5",  # 整体浅灰背景以增强对比
        nodesep="0.5",
        ranksep="0.7",
        pad="0.3",
    )
    g.attr(
        "node",
        shape="box",
        style="rounded,filled",
        color="#333333",
        fillcolor="white",
        fontname="SimSun",
        fontsize="12",
        margin="0.10,0.08",
        penwidth="1.2",
    )
    g.attr(
        "edge",
        color="#333333",
        arrowsize="1.0",  # 箭头略放大
        penwidth="1.4",   # 箭头线条加粗
    )

    # ========== 第一大模块：数据构建与标准化 ==========
    with g.subgraph(name="cluster_data") as c:
        c.attr(label="(1) 口腔种植科语音—病历匹配数据集构建与标准化处理",
               labelloc="t", fontsize="13", fontname="SimSun")
        c.attr(style="rounded,filled", color="#777777", fillcolor="#EDEDED")

        c.node("data_src", "数据来源与构建\n虚拟病例开发 + 真实病例测试")
        c.node("virtual", "虚拟病例（训练/验证）\n专家构建 420 例\n完整病程信息")
        c.node("real", "真实病例（独立测试）\n系统抽取脱敏 2000+ 份\n伦理审批")
        c.node("gen", "语音与文本数据生成\n金标准病历 + 自然口语录音\n回顾性复刻 + 前瞻性采集")
        c.node("prep", "数据预处理与标准化\n语音降噪/切分/PCM统一\n文本术语映射 + 错词纠错")
        c.node("split", "数据集划分\n虚拟→训练/验证\n真实→测试")

        c.edges([("data_src", "virtual"), ("data_src", "real")])
        c.edge("virtual", "gen")
        c.edge("real", "gen")
        c.edge("gen", "prep")
        c.edge("prep", "split")

    # ========== 第二大模块：ASR–LLM 协同 + 模板化生成 ==========
    with g.subgraph(name="cluster_model") as c:
        c.attr(label="(2) 专科适配的 ASR–LLM 协同模型搭建与模板化生成机制开发",
               labelloc="t", fontsize="13", fontname="SimSun")
        c.attr(style="rounded,filled", color="#777777", fillcolor="#EDEDED")

        c.node("asr", "ASR 专科优化\n通用ASR + 专科术语库\n领域自适应微调\n降低 WER/SER")
        c.node("tmpl", "种植科专属模板库设计\n覆盖初诊/复诊/术前/术后等\n7大类 18核心槽位\n数据类型/必填/多值约束")
        c.node("llm", "LLM 槽位信息提取（非自由生成）\n输入：规范化文本 + 槽位定义\n输出：槽位→证据片段（JSON）\n显式禁止虚构/扩写")
        c.node("fill", "模板填充生成结构化病历\n（草稿）")
        c.node("train", "协同训练与优化\n先ASR/LLM单模块→再端到端\n超参搜索 + TensorBoard监控")

        c.edge("asr", "llm")
        c.edge("tmpl", "llm")
        c.edge("llm", "fill")
        c.edge("fill", "train")

    # ========== 第三大模块：系统集成与临床验证 ==========
    with g.subgraph(name="cluster_system") as c:
        c.attr(label="(3) 系统集成与多维度临床验证（双重测试体系）",
               labelloc="t", fontsize="13", fontname="SimSun")
        c.attr(style="rounded,filled", color="#777777", fillcolor="#EDEDED")

        c.node("sys", "系统功能集成\n语音采集→ASR→文本规范→LLM提取→模板生成\n人机协同审核→结构化存储/导出")
        c.node("retro", "回顾性测试\n金标准真实病历对照\nPrecision/Recall/F1\n信息覆盖率\n文本相似度（BERTScore/ROUGE）\n术语规范率/幻觉率")
        c.node("pros", "前瞻性临床队列\n30名医师随机分组\n试验组（系统）vs 对照组（键盘）\n3个月\n效率/质量/安全/满意度\n统计检验（t/Wilcoxon/卡方）")

        c.edge("sys", "retro")
        c.edge("sys", "pros")

    # ========== 第四大模块：评估消融与迭代 ==========
    with g.subgraph(name="cluster_eval") as c:
        c.attr(label="(4) 多维度评估、消融实验与迭代优化",
               labelloc="t", fontsize="13", fontname="SimSun")
        c.attr(style="rounded,filled", color="#777777", fillcolor="#EDEDED")

        c.node("eval", "多维度评估\n客观指标 + 主观Likert\n幻觉发生率 + 总耗时/修改次数")
        c.node("ablate", "消融实验\n模板约束+信息提取\nvs 自由生成LLM")
        c.node("iter", "迭代优化\n更新术语库/错词库/模板槽位\n微调模型参数\n降低审核修改率")

        c.edge("eval", "ablate")
        c.edge("ablate", "iter")

    # ========== 主链路连接（模块之间）==========
    g.edge("split", "asr")
    g.edge("train", "sys")
    g.edge("pros", "eval")

    # ========== 反馈回路（迭代→模型）==========
    g.edge("iter", "asr", style="dashed", label="反馈", fontname="SimSun")

    return g

if __name__ == "__main__":
    dot = build()
    dot.render("implant_flowchart", cleanup=True)   # 输出 implant_flowchart.pdf
    dot.format = "svg"
    dot.render("implant_flowchart", cleanup=True)   # 输出 implant_flowchart.svg
    print("Done: implant_flowchart.pdf / implant_flowchart.svg")
