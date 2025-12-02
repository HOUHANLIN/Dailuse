# EMR-Paper

>  保留所有版权

基于语音输入和大语言模型（LLM）的生成式电子病历系统论文 LaTeX 工程。

本仓库主要用于撰写和维护题为「生成式病历论文结构稿」的学术论文，聚焦在专科（以口腔科为例）场景下，通过专科优化的语音识别（ASR）、受约束的信息提取式 LLM 以及知识库校验，实现安全、可控的语音生成结构化电子病历（EMR）。

## 项目结构

```text
.
├── main.tex              # 主文档入口（ctexart）
├── archive/              # 历史版本与修改记录归档
├── sections/             # 各章节内容
│   ├── abstract.tex      # 摘要与介绍
│   ├── methods.tex       # 材料与方法 / 实验设计
│   ├── results.tex       # 结果
│   ├── discussion.tex    # 讨论
│   ├── methods_refs.tex  # 方法部分参考文献
│   └── discussion_refs.tex # 讨论部分参考文献
├── media/                # 图像资源（示意图等）
│   └── image1.jpeg
├── tmp/                  # 编译生成的中间文件与 PDF
└── README.md
```

> 说明：`tmp/` 目录中已包含一次编译得到的 `main.pdf`，也可以根据下文命令重新生成。

## 编译环境要求

- TeX 发行版：推荐 TeX Live / MacTeX 2020 及以上版本。
- 编译引擎：支持 `xelatex` 或 `lualatex`（本项目默认使用 `xelatex`，UTF-8 编码，`ctexart` 文类）。
- 主要宏包：`ctex`、`graphicx`、`amsmath`、`amssymb`、`hyperref`、`geometry`（通常随完整发行版一并安装）。

## 快速开始

1. 安装 LaTeX 环境  
   - macOS：安装 MacTeX  
   - Windows：安装 TeX Live / MiKTeX  
   - Linux：通过包管理器安装 TeX Live（建议完整安装）

2. 在项目根目录编译论文

   使用 `latexmk`（推荐）：

   ```bash
   latexmk -xelatex -output-directory=tmp main.tex
   ```

   或者使用原生 `xelatex`：

   ```bash
   xelatex -output-directory=tmp main.tex
   xelatex -output-directory=tmp main.tex
   ```

3. 查看 PDF  
   编译成功后，最终论文位于：

   ```text
   tmp/main.pdf
   ```

## 如何编辑论文内容

- 摘要与引言：编辑 `sections/abstract.tex`
- 材料与方法 / 实验设计：编辑 `sections/methods.tex`
- 结果：编辑 `sections/results.tex`
- 讨论：编辑 `sections/discussion.tex`
- 参考文献列表：编辑
  - 方法部分参考文献：`sections/methods_refs.tex`
  - 讨论部分参考文献：`sections/discussion_refs.tex`

如需增加新章节，可以：

1. 在 `sections/` 目录中新增对应的 `xxx.tex` 文件；
2. 在 `main.tex` 中合适的位置添加一行：

   ```tex
   \input{sections/xxx}
   ```

## archive 目录说明

- `archive/` 用于保存论文在不同时间点的历史版本与修改记录，方便回溯与对比。  
- 子目录一般以日期命名（例如 `25-11-30/`）。
- 建议在进行较大结构调整或重要版本提交前，将当前 PDF 与关键修改说明一并归档到新的日期目录中，以形成清晰的演化记录。

## 论文核心思路概览

为了方便快速理解论文内容，本项目主要围绕以下几个关键点展开：

- 通过专科热词库、错词库和术语库，对 ASR 进行定向优化，提高临床语音转写中的医学术语识别准确率。
- 将大语言模型限定为“信息提取与槽位映射器”，从医生口述文本中抽取关键信息，并填入结构化模板槽位，而非让模型自由生成整篇病历，从源头降低幻觉风险。
- 引入医疗知识库，对提取出的关键信息进行召回与校验，修正术语、错词和逻辑错误，进一步提升病历内容的准确性与规范性。
- 基于模板的结构化病历输出，当前以口腔种植等场景为例，可扩展到其他专科，通过新增模板适配不同科室需求。
- 设计包含客观性能、主观质量、效率增益和安全性（幻觉抑制）等维度的评估方案，并通过消融实验验证各模块的贡献。

## 说明与后续计划

- 本仓库仅包含论文的 LaTeX 文稿与示意图资源，不包含模型代码、实际医疗数据或生产系统代码。
- 如后续需要将系统实现代码、数据处理脚本等与论文工程整合，可在本仓库基础上新增 `code/`、`data/` 等目录，并在本文档中补充说明。


