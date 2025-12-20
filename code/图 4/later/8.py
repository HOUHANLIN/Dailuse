from graphviz import Digraph

def build():
    g = Digraph("implant_flow", format="pdf")
    # 论文风格：黑白、矢量、统一字体、线条清晰
    g.attr(rankdir="TB", fontsize="12", fontname="SimSun")
    g.attr("graph", splines="ortho")  # 论文里常见的直角连线；不想要可删
    g.attr("node", shape="box", style="rounded", color="black",
           fontname="SimSun", fontsize="11", margin="0.08,0.06")
    g.attr("edge", color="black", arrowsize="0.8", fontname="SimSun", fontsize="10")

    # ===================== (1) 数据构建与标准化 =====================
    with g.subgraph(name="cluster_data") as c:
        c.attr(label="(1) 口腔种植科语音—病历匹配数据集构建与标准化处理",
               labelloc="t", fontsize="12", fontname="SimSun")
        c.attr(style="rounded", color="black")

        # anchor：用于大模块“居中对齐/主链路连接”
        c.node("A_data", "", shape="point", width="0.01", height="0.01", style="invis")

        c.node("data_src", "数据来源与构建\n虚拟病例开发 + 真实病例测试")
        c.node("virtual", "虚拟病例（训练/验证）\n专家构建 420 例\n完整病程信息")
        c.node("real", "真实病例（独立测试）\n系统抽取脱敏 2000+ 份\n伦理审批")
        c.node("gen", "语音与文本数据生成\n金标准病历 + 自然口语录音\n回顾性复刻 + 前瞻性采集")
        c.node("prep", "数据预处理与标准化\n语音降噪/切分/PCM统一\n文本术语映射 + 错词纠错")
        c.node("split", "数据集划分\n虚拟→训练/验证\n真实→测试")

        # 控制左右并排：virtual 与 real 强制同一层
        with c.subgraph() as s:
            s.attr(rank="same")
            s.node("virtual")
            s.node("real")

        # 让 anchor 与模块内部主干对齐（不显示、不干扰结构）
        c.edge("A_data", "data_src", style="invis")

        c.edges([("data_src", "virtual"), ("data_src", "real")])
        c.edge("virtual", "gen")
        c.edge("real", "gen")
        c.edge("gen", "prep")
        c.edge("prep", "split")

    # ===================== (2) ASR–LLM 协同 + 模板化生成 =====================
    with g.subgraph(name="cluster_model") as c:
        c.attr(label="(2) 专科适配的 ASR–LLM 协同模型搭建与模板化生成机制开发",
               labelloc="t", fontsize="12", fontname="SimSun")
        c.attr(style="rounded", color="black")

        c.node("A_model", "", shape="point", width="0.01", height="0.01", style="invis")

        c.node("asr", "ASR 专科优化\n通用ASR + 专科术语库\n领域自适应微调\n降低 WER/SER")
        c.node("tmpl", "种植科专属模板库设计\n覆盖初诊/复诊/术前/术后等\n7大类 18核心槽位\n数据类型/必填/多值约束")
        c.node("llm", "LLM 槽位信息提取（非自由生成）\n输入：规范化文本 + 槽位定义\n输出：槽位→证据片段（JSON）\n显式禁止虚构/扩写")
        c.node("fill", "模板填充生成结构化病历\n（草稿）")
        c.node("train", "协同训练与优化\n先ASR/LLM单模块→再端到端\n超参搜索 + TensorBoard监控")

        # 让 asr 与 tmpl 更“对称”一些：强制同层（可选，但论文观感更稳）
        with c.subgraph() as s:
            s.attr(rank="same")
            s.node("asr")
            s.node("tmpl")

        c.edge("A_model", "llm", style="invis")

        c.edge("asr", "llm")
        c.edge("tmpl", "llm")
        c.edge("llm", "fill")
        c.edge("fill", "train")

    # ===================== (3) 系统集成与临床验证 =====================
    with g.subgraph(name="cluster_system") as c:
        c.attr(label="(3) 系统集成与多维度临床验证（双重测试体系）",
               labelloc="t", fontsize="12", fontname="SimSun")
        c.attr(style="rounded", color="black")

        c.node("A_system", "", shape="point", width="0.01", height="0.01", style="invis")

        c.node("sys", "系统功能集成\n语音采集→ASR→文本规范→LLM提取→模板生成\n人机协同审核→结构化存储/导出")
        c.node("retro", "回顾性测试\n金标准真实病历对照\nPrecision/Recall/F1\n信息覆盖率\n文本相似度（BERTScore/ROUGE）\n术语规范率/幻觉率")
        c.node("pros", "前瞻性临床队列\n30名医师随机分组\n试验组（系统）vs 对照组（键盘）\n3个月\n效率/质量/安全/满意度\n统计检验（t/Wilcoxon/卡方）")

        # 控制左右并排：retro 与 pros 强制同一层
        with c.subgraph() as s:
            s.attr(rank="same")
            s.node("retro")
            s.node("pros")

        c.edge("A_system", "sys", style="invis")

        c.edge("sys", "retro")
        c.edge("sys", "pros")

    # ===================== (4) 评估消融与迭代优化 =====================
    with g.subgraph(name="cluster_eval") as c:
        c.attr(label="(4) 多维度评估、消融实验与迭代优化",
               labelloc="t", fontsize="12", fontname="SimSun")
        c.attr(style="rounded", color="black")

        c.node("A_eval", "", shape="point", width="0.01", height="0.01", style="invis")

        c.node("eval", "多维度评估\n客观指标 + 主观Likert\n幻觉发生率 + 总耗时/修改次数")
        c.node("ablate", "消融实验\n模板约束+信息提取\nvs 自由生成LLM")
        c.node("iter", "迭代优化\n更新术语库/错词库/模板槽位\n微调模型参数\n降低审核修改率")

        c.edge("A_eval", "eval", style="invis")

        c.edge("eval", "ablate")
        c.edge("ablate", "iter")

    # ===================== 主链路连接（用 anchor 保证模块居中对齐） =====================
    # 用 anchor 串模块，减少因为内部节点大小差异导致的“偏左/偏右”
    g.edge("A_data", "A_model")
    g.edge("A_model", "A_system")
    g.edge("A_system", "A_eval")

    # 同时保留语义主链路（可读性更强）；不想重复可删其一
    g.edge("split", "asr")
    g.edge("train", "sys")
    g.edge("pros", "eval")

    # ===================== 反馈回路（防止跨模块拉乱：constraint=false） =====================
    # constraint=false：这条边不参与层级布局，否则可能把 model/data 拉出队形
    g.edge("iter", "asr", style="dashed", label="反馈", constraint="false")

    return g

if __name__ == "__main__":
    dot = build()
    dot.render("implant_flowchart", cleanup=True)   # 输出 implant_flowchart.pdf
    dot.format = "svg"
    dot.render("implant_flowchart", cleanup=True)   # 输出 implant_flowchart.svg
    print("Done: implant_flowchart.pdf / implant_flowchart.svg")