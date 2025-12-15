import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from matplotlib import rcParams

# =================配置区域=================
# 尝试设置中文字体，按优先级尝试（Windows/Mac/Linux）
fonts = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'WenQuanYi Micro Hei', 'sans-serif']
rcParams['font.sans-serif'] = fonts
rcParams['axes.unicode_minus'] = False # 解决负号显示问题

# 配色方案 (学术医疗风格)
COLOR_ARROW = '#D1E5F0'       # 浅蓝（箭头填充）
COLOR_ARROW_EDGE = '#6FA8DC'  # 深蓝（箭头边框）
COLOR_NODE_BG = '#F9F9F9'     # 极浅灰（节点背景，模拟图片底色）
COLOR_NODE_BORDER = '#DDDDDD' # 节点边框
COLOR_TEXT_TITLE = '#204E7F'  # 深蓝（上方动作文字）
COLOR_TEXT_DESC = '#000000'   # 纯黑（下方对象文字）
COLOR_ACCENT = '#FF6B6B'      # 强调色（用于第5步迭代）

# 导出图片文件名
OUTPUT_FILE = "flowchart.png"

# 画布设置
FIG_WIDTH = 16
FIG_HEIGHT = 5

# ==================数据定义=================
# 格式：(上方动作文本, 中间节点模拟图文字, 下方对象描述文本)
steps = [
    ("语音采集", "AUDIO\nINPUT", "医生口述语音\n规范化文本序列"),
    ("语义分析", "LLM\nCORE", "LLM意图识别\n结构化槽位提取"),
    ("质量控制", "VERIFY\nSYSTEM", "知识库一致性校验\n术语自动纠错"),
    ("生成输出", "EMR\nDOC", "结构化电子病历\n人机协同终审"),
    ("闭环优化", "UPDATE\nLOOP", "系统持续迭代\n参数微调优化")
]

# ==================绘图函数=================

def draw_chevron_arrow(ax, start_x, y, width, height, label):
    """绘制宽体燕尾箭头 (Chevron Arrow)"""
    # 定义箭头的顶点坐标
    tail_depth = width * 0.2
    head_depth = width * 0.2
    
    # 形状路径: (x,y) -> ...
    verts = [
        (start_x, y - height/2),                  # 左下
        (start_x + width - head_depth, y - height/2), # 右下(箭头根部)
        (start_x + width, y),                     # 箭头尖端
        (start_x + width - head_depth, y + height/2), # 右上(箭头根部)
        (start_x, y + height/2),                  # 左上
        (start_x + tail_depth, y)                 # 左侧内凹点
    ]
    
    path = patches.Polygon(verts, closed=True, 
                           facecolor=COLOR_ARROW, edgecolor=COLOR_ARROW_EDGE, 
                           linewidth=1, zorder=1)
    ax.add_patch(path)
    
    # 添加上方文字 (动作)
    ax.text(start_x + width/2, y + height/1.8, label, 
            ha='center', va='bottom', fontsize=11, 
            fontweight='bold', color=COLOR_TEXT_TITLE)

def draw_node_box(ax, x, y, width, height, icon_text, desc_text, is_last=False, image_path=None):
    """绘制代表'图片/电脑'的节点框，支持按框大小填充真实图片"""
    # 绘制矩形框 (模拟参考图中的截图/电脑屏幕)
    box = patches.FancyBboxPatch((x, y - height/2), width, height,
                                 boxstyle="round,pad=0.1,rounding_size=0.05",
                                 facecolor=COLOR_NODE_BG, edgecolor=COLOR_NODE_BORDER,
                                 linewidth=1.5, zorder=2)
    ax.add_patch(box)
    
    # 如果提供了图片路径，则优先显示真实图片，并根据节点框自动缩放填充
    if image_path is not None:
        img = mpimg.imread(image_path)
        # 让图片尽量填满整个节点框
        x0 = x
        x1 = x + width
        y0 = y - height/2
        y1 = y + height/2
        # aspect='auto' 按矩形比例拉伸填充
        ax.imshow(img, extent=(x0, x1, y0, y1), zorder=3, aspect='auto')
    else:
        # 否则使用文字图标占位
        ax.text(x + width/2, y, icon_text, 
                ha='center', va='center', fontsize=10, 
                color='#888888', fontweight='bold', alpha=0.6)
            
    # 下方文字 (对象描述)
    ax.text(x + width/2, y - height/1.5, desc_text, 
            ha='center', va='top', fontsize=12, 
            fontweight='bold', color=COLOR_TEXT_DESC, linespacing=1.4)

    # 最后一步不再使用特殊颜色样式，保持和前面节点一致

# ==================主程序=================

def main():
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    ax.set_xlim(0, FIG_WIDTH)
    ax.set_ylim(0, FIG_HEIGHT)
    ax.axis('off') # 隐藏坐标轴

    # 布局参数
    start_x = 0.5
    center_y = FIG_HEIGHT / 2
    
    node_w = 1.8  # 节点宽度
    node_h = 1.2  # 节点高度
    arrow_w = 1.2 # 箭头宽度 (连接距离)
    arrow_h = 0.6 # 箭头高度 (粗细)
    
    current_x = start_x

    # 如果图片在根目录（和 1.py 同一层），这里直接写文件名
    image_paths = [
        "1.png",  # 对应步骤 1
        "2.png",  # 对应步骤 2
        "3.png",  # 对应步骤 3
        "4.png",  # 对应步骤 4
        "5.png"   # 对应步骤 5
    ]

    for i, (action_text, icon_text, desc_text) in enumerate(steps):
        is_last = (i == len(steps) - 1)
        image_path = image_paths[i] if i < len(image_paths) else None
        
        # 1. 绘制节点 (Node)
        draw_node_box(ax, current_x, center_y, node_w, node_h, 
                      icon_text, desc_text, is_last, image_path=image_path)
        current_x += node_w + 0.1 # 节点后留一点小空隙
        
        # 2. 绘制连接箭头 (Arrow) - 如果不是最后一个节点
        if not is_last:
            # 箭头的动作文字取自下一个节点的逻辑（或者当前转换逻辑）
            # 根据您的描述，Step 1 "ASR预处理" 是连接 1和2 的过程
            # 这里我们将 steps[i][0] (action_text) 放在该节点之后的箭头上
            # 注意：列表中的 action_text 是 "该步骤的动作"。
            # 逻辑调整：节点1 -> 箭头(动作1) -> 节点2
            
            # 获取下一个动作名称 (Hack: 为了对齐您的文本逻辑)
            # 如果是最后一个，就没有箭头了
            
            # 在这里，我们将当前步骤的 "Action" 放在连接到下一个节点的箭头上
            # 比如 "数据输入" 是第一个状态，箭头应该是 "ASR处理"
            # 为了适配您的文案，我稍微调整了显示逻辑：
            # 箭头上的文字直接使用 steps[i] 中的 action 稍微有些错位
            # 让我们手动指定箭头文字以完美匹配您的 5 步流程：
            
            arrow_labels = [
                "ASR 预处理",       # 1 -> 2
                "结构化映射",       # 2 -> 3
                "知识库纠错",       # 3 -> 4
                "人机协同审核"      # 4 -> 5
            ]
            
            current_arrow_label = arrow_labels[i] if i < len(arrow_labels) else ""
            
            draw_chevron_arrow(ax, current_x, center_y, arrow_w, arrow_h, current_arrow_label)
            current_x += arrow_w + 0.1

    # 保存并显示（尽量去掉边缘和标题）
    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight', pad_inches=0.02)
    plt.show()

if __name__ == "__main__":
    main()
