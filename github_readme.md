# OrcaNote PyPlus

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**封装 OrcaNote 命令行工具的 Python 脚本**，解决 Windows 系统下中文编码问题，简化参数传递。

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

## 📦 安装

```bash
pip install -r requirements.txt
```

依赖：
- `pandas` - 读取 CSV/Excel
- `openpyxl` - xlsx 支持
- `xlrd` - xls 支持

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
python orca-cli-pylus.py insert-md --ref 123 --file note.md

# 使用仓库别名
python orca-cli-pylus.py --repo work insert-md --ref 123 --file note.md

# 直接指定仓库 ID
python orca-cli-pylus.py --repoid xxx insert-md --ref 123 --file note.md

# 插入 Excel 表格（指定 sheet）
python orca-cli-pylus.py insert-table --ref 123 --file data.xlsx --sheet "Sheet2"

# 搜索文本
python orca-cli-pylus.py search --text "关键词"

# 创建页面
python orca-cli-pylus.py create-page --name "新页面"

# 获取今日日记
python orca-cli-pylus.py journal
```

### Python API 模式

```python
from orca_cli_pylus import OrcaNoteCLI

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