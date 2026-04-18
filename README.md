# OrcaNote PyPlus

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

本项目是对 [OrcaNote CLI](https://github.com/sethyuan/orca-note-cli) 的 Python 封装，主要解决Windows 系统下中文编码问题，简化参数传递。使用前需先安装 [OrcaNote CLI](https://github.com/sethyuan/orca-note-cli) ，感谢原作者 [@sethyuan](https://github.com/sethyuan) 提供优秀的命令行工具。

## ✨ 功能特点

| 功能 | 说明 |
|------|------|
| 🔧 **完整 CLI 封装** | 支持所有 OrcaNote CLI 工具 |
| 📝 **Markdown 支持** | 直接插入文本或从 `.md` 文件导入 |
| 📊 **表格支持** | 从 CSV/Excel 文件导入，支持指定 sheet |
| 🏷️ **标签管理** | 创建标签、添加/移除标签（支持属性） |
| 🔄 **仓库别名** | 配置多个仓库别名，快速切换 |
| 🖥️ **Windows 优化** | 自动处理 UTF-8 编码，解决中文乱码 |
| 📦 **双模式** | 类 API 和命令行两种使用方式 |

## 📁 目录结构

**本仓库文件：**

```
orca-pylus/
├── orcanote_pylus.py      # 主脚本
├── README.md              # 本说明文件
└── requirements.txt       # Python 依赖
```

**需要放置到官方技能目录：**

```plaintext
<opencode>/skills/orcanote_skill/
├── orcanote.exe                    # 官方 CLI（已有）
├── references/                     # 官方参考文档（已有）
│   ├── tools.md
│   └── query-blocks.md
├── scripts/                        # ← 将本仓库文件放这里
│   ├── orcanote_pylus.py           # ← 主脚本
│   ├── README.md                   # ← 脚本说明
│   └── requirements.txt            # ← 依赖
└── SKILL.md                        # ← 需要修改（见下文）
```

## 📦 安装

### 1. 下载本仓库

```bash
git clone https://github.com/yourname/orca-pylus.git
```

### 2. 放置文件

将以下文件复制到 `<opencode>/skills/orcanote_skill/scripts/` 目录：

| 文件 | 目标位置 |
|------|---------|
| `orcanote_pylus.py` | `scripts/orcanote_pylus.py` |
| `README.md` | `scripts/README.md` |
| `requirements.txt` | `scripts/requirements.txt` |

### 3. 安装依赖

```bash
pip install -r scripts/requirements.txt
```

依赖说明：
- `pandas` - 读取 CSV/Excel
- `openpyxl` - xlsx 支持
- `xlrd` - xls 支持

### 4. 配置 SKILL.md

**重要**：需要将本仓库的 `SKILL.md` 内容复制追加到官方 `SKILL.md` ：

### 安装依赖

```bash
pip install -r scripts/requirements.txt
```

### 配置

在脚本顶部修改仓库别名：

```python
REPO_CONFIG = {
    "default": "your_repo_id",    # 默认仓库
    "work": "work_repo_id",       # 工作仓库
    # 用户可添加其他仓库别名
}
```

### 使用示例

```python
from orcanote_pylus import OrcaNoteCLI

# 使用默认仓库（default 别名）
cli = OrcaNoteCLI()

# 使用仓库别名
cli = OrcaNoteCLI(repo_alias="work")

# 直接指定仓库 ID
cli = OrcaNoteCLI(repo_id="other_repo_id")

# 插入 Markdown 文件
cli.insert_markdown(ref_block_id=123, markdown_file="content.md")

# 插入表格（CSV/Excel）
cli.insert_table(ref_block_id=123, table_file="data.csv")

# 插入 Excel 指定 sheet
cli.insert_table(ref_block_id=123, table_file="data.xlsx", sheet_name="Sheet2")

# 搜索文本
cli.search_text("keyword")
```

### 命令行使用

```bash
# 使用默认仓库
python scripts/orcanote_pylus.py insert-md --ref 123 --file content.md

# 使用仓库别名
python scripts/orcanote_pylus.py --repo work insert-md --ref 123 --file content.md

# 直接指定仓库 ID
python scripts/orcanote_pylus.py --repoid other_repo_id insert-md --ref 123 --file content.md

# 插入 Excel 指定 sheet
python scripts/orcanote_pylus.py insert-table --ref 123 --file data.xlsx --sheet "Sheet2"

# 搜索
python scripts/orcanote_pylus.py search --text "keyword"

# 更多命令见 scripts/README.md
```
```

## ⚙️ 配置

修改脚本顶部的仓库别名：

```python
REPO_CONFIG = {
    "default": "your_repo_id",    # 默认仓库
    "work": "work_repo_id",       # 工作仓库
    "personal": "personal_repo_id", # 个人仓库
}
```

## 🚀 快速开始

### 命令行模式

```bash
# 使用默认仓库
python orcanote_pylus.py insert-md --ref 123 --file note.md

# 使用仓库别名
python orcanote_pylus.py --repo work insert-md --ref 123 --file note.md

# 直接指定仓库 ID
python orcanote_pylus.py --repoid xxx insert-md --ref 123 --file note.md

# 插入 Excel 表格（指定 sheet）
python orcanote_pylus.py insert-table --ref 123 --file data.xlsx --sheet "Sheet2"

# 搜索文本
python orcanote_pylus.py search --text "关键词"

# 创建页面
python orcanote_pylus.py create-page --name "新页面"

# 获取今日日记
python orcanote_pylus.py journal
```

### Python API 模式

```python
from orcanote_pylus import OrcaNoteCLI

# 初始化
cli = OrcaNoteCLI(repo_alias="default")  # 或 cli = OrcaNoteCLI(repo_id="xxx")

# 插入 Markdown
cli.insert_markdown(ref_block_id=123, text="# 标题\n内容")
cli.insert_markdown(ref_block_id=123, markdown_file="note.md")

# 插入表格
cli.insert_table(ref_block_id=123, table_file="data.csv")
cli.insert_table(ref_block_id=123, table_file="data.xlsx", sheet_name="Sheet2")

# 创建标签（带属性）
cli.create_tags([
    {
        "name": "任务",
        "properties": [
            {"name": "优先级", "type": "select", "options": ["低", "中", "高"]},
            {"name": "截止日期", "type": "date"}
        ]
    }
])

# 搜索
result = cli.search_text("关键词")

# 获取今日日记
journal = cli.get_today_journal()
```

## 📖 支持的操作

| 命令 | 说明 |
|------|------|
| `insert-md` | 插入 Markdown（文本或文件） |
| `insert-table` | 插入表格（CSV/Excel） |
| `get` | 获取块内容 |
| `search` | 搜索文本 |
| `create-page` | 创建页面 |
| `delete` | 删除块 |
| `move` | 移动块 |
| `tags` | 添加标签 |
| `journal` | 获取今日日记 |

## 🔧 全局参数

| 参数 | 说明 |
|------|------|
| `--repo` | 仓库别名（默认 `default`） |
| `--repoid` | 直接指定仓库 ID（优先级更高） |
| `--cli-path` | orcanote.exe 路径 |

## 📝 文件格式支持

| 格式 | 说明 |
|------|------|
| `.md` | Markdown 文件 |
| `.csv` | CSV 表格 |
| `.xlsx` | Excel 2007+ |
| `.xls` | Excel 97-2003 |

## 🤝 相关项目


- [OrcaNote](https://github.com/orcanote) - 虎鲸笔记，一款本地优先的知识管理工具

## 📄 License

MIT License
