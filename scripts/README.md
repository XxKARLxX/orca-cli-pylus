# OrcaNote Pylus

封装 OrcaNote 命令行工具的 Python 脚本，解决 Windows 系统下中文编码问题，简化参数传递。

## 功能特点

- ✅ 支持所有 OrcaNote CLI 工具
- ✅ 参数化 JSON 输入，无需手动构造 JSON
- ✅ 支持 Markdown 文件、CSV/Excel 文件作为内容输入
- ✅ 支持 Pandas DataFrame 数据直接插入表格
- ✅ 支持 Excel 指定 sheet（名称或索引）
- ✅ 支持仓库别名配置，简化多仓库切换
- ✅ Windows 系统优化，自动处理 UTF-8 编码
- ✅ 提供类 API 和命令行两种使用方式

## 安装依赖

```bash
pip install -r requirements.txt
```

依赖说明：
- `pandas`: 用于读取 CSV/Excel 文件并转换为表格
- `openpyxl`: 用于读取 .xlsx 格式的 Excel 文件
- `xlrd`: 用于读取旧版 .xls 格式的 Excel 文件

## 配置

在脚本顶部修改仓库别名：

```python
# 仓库别名配置
REPO_CONFIG = {
    "default": "repo_id",  # 默认仓库
    "repo_alias": "repo_id",     # OPPO 测试仓库
    # 用户可添加其他仓库别名
}
```

未指定 `--repo` 参数时默认使用 `default` 别名。

## 使用方式

### 方式一：作为 Python 类使用

```python
from orcanote_pylus import OrcaNoteCLI

# 使用默认仓库（default 别名）
cli = OrcaNoteCLI()

# 使用仓库别名
cli = OrcaNoteCLI(repo_alias="oppo")

# 直接指定仓库 ID（优先级最高）
cli = OrcaNoteCLI(repo_id="other_repo_id")

# 插入 Markdown 文件
cli.insert_markdown(ref_block_id=123, markdown_file="content.md")

# 直接插入文本
cli.insert_markdown(ref_block_id=123, text="# Title\nContent here")

# 插入表格（从 CSV）
cli.insert_table(ref_block_id=123, table_file="data.csv", title="数据表格")

# 插入表格（从 Excel，默认第一个 sheet）
cli.insert_table(ref_block_id=123, table_file="data.xlsx")

# 插入表格（指定 sheet 名称或索引）
cli.insert_table(ref_block_id=123, table_file="data.xlsx", sheet_name="Sheet2")
cli.insert_table(ref_block_id=123, table_file="data.xlsx", sheet_name=1)  # 第二个 sheet

# 搜索文本
cli.search_text("deadline")

# 创建页面
cli.create_page(name="New Page")

# 获取今日日记
cli.get_today_journal()

# 删除块
cli.delete_blocks(block_ids=[123, 456])
```

### 方式二：命令行使用

```bash
# 使用默认仓库
python orcanote_pylus.py insert-md --ref 123 --file content.md

# 使用仓库别名
python orcanote_pylus.py --repo oppo insert-md --ref 123 --file content.md

# 直接指定仓库 ID（优先级最高）
python orcanote_pylus.py --repoid other_repo_id insert-md --ref 123 --file content.md

# 直接插入文本
python orcanote_pylus.py insert-md --ref 123 --text "# Title"

# 插入表格（CSV）
python orcanote_pylus.py insert-table --ref 123 --file data.csv --title "数据表格"

# 插入表格（Excel，默认第一个 sheet）
python orcanote_pylus.py insert-table --ref 123 --file data.xlsx

# 插入表格（指定 sheet）
python orcanote_pylus.py insert-table --ref 123 --file data.xlsx --sheet "Sheet2"

# 搜索文本
python orcanote_pylus.py search --text "deadline"

# 获取块内容
python orcanote_pylus.py get --blocks 123,456

# 创建页面
python orcanote_pylus.py create-page --name "New Page"

# 删除块
python orcanote_pylus.py delete --blocks 123,456

# 添加标签
python orcanote_pylus.py tags --blocks 123 --tag-names task important

# 获取今日日记
python orcanote_pylus.py journal
```

## 命令详解

### 全局参数

| 参数 | 说明 | 必需 |
|------|------|------|
| `--repo` | 仓库别名（从 REPO_CONFIG 获取，默认 default） | ❌ |
| `--repoid` | 直接指定仓库 ID（优先级高于 --repo） | ❌ |
| `--cli-path` | orcanote.exe 路径 | ❌ |

**优先级**：`--repoid` > `--repo`

### insert-md（插入 Markdown）

| 参数 | 说明 | 必需 |
|------|------|------|
| `--ref` | 参考块 ID | ✅ |
| `--file` | Markdown 文件路径 | ❌ |
| `--text` | 直接传入的文本 | ❌ |
| `--position` | 插入位置（before/after/firstChild/lastChild） | ❌（默认 after） |

**注意**：`--file` 和 `--text` 必须提供其中一个。

### insert-table（插入表格）

| 参数 | 说明 | 必需 |
|------|------|------|
| `--ref` | 参考块 ID | ✅ |
| `--file` | CSV/Excel 文件路径 | ✅ |
| `--title` | 表格标题 | ❌ |
| `--position` | 插入位置 | ❌（默认 after） |
| `--sheet` | Excel sheet 名称或索引 | ❌（默认 0，第一个 sheet） |

支持的文件格式：
- `.csv` - CSV 文件
- `.xlsx` / `.xls` - Excel 文件

### get（获取块内容）

| 参数 | 说明 | 必需 |
|------|------|------|
| `--blocks` | 块 ID（逗号分隔，如 `123,456`） | ✅ |
| `--child-start` | 子块起始索引（1-based） | ❌ |
| `--child-end` | 子块结束索引（1-based） | ❌ |

### search（搜索文本）

| 参数 | 说明 | 必需 |
|------|------|------|
| `--text` | 搜索文本 | ✅ |
| `--limit` | 返回数量限制 | ❌（默认 50） |

### create-page（创建页面）

| 参数 | 说明 | 必需 |
|------|------|------|
| `--name` | 页面名称 | ✅ |
| `--include` | 包含的页面名称列表 | ❌ |

### delete（删除块）

| 参数 | 说明 | 必需 |
|------|------|------|
| `--blocks` | 块 ID（逗号分隔） | ✅ |

### move（移动块）

| 参数 | 说明 | 必需 |
|------|------|------|
| `--blocks` | 要移动的块 ID | ✅ |
| `--parent` | 目标父块 ID | ✅ |
| `--left` | 左侧兄弟块 ID | ❌ |

### tags（添加标签）

| 参数 | 说明 | 必需 |
|------|------|------|
| `--blocks` | 块 ID | ✅ |
| `--tag-names` | 标签名称列表 | ✅ |

### journal（获取今日日记）

无参数，返回今日日记块 ID。

## 返回值格式

所有命令返回 JSON 格式：

```json
// 成功
{"success": true, "blockId": 123, "insertedCount": 10}

// 失败
{"success": false, "error": "Error message"}
```

## 常见问题

### Q: 中文乱码怎么办？

A: 脚本已自动处理 UTF-8 编码，确保：
- Python 文件保存为 UTF-8 编码
- Markdown/CSV 文件保存为 UTF-8 编码

### Q: 找不到 orcanote.exe？

A: 检查 `ORCANOTE_CLI_PATH` 配置是否正确，或使用 `--cli-path` 参数指定路径。

### Q: Excel 文件读取失败？

A: 确保已安装 `openpyxl`（.xlsx）或 `xlrd`（.xls）：
```bash
pip install openpyxl xlrd
```

## 文件结构

```
scripts/
├── orcanote_pylus.py    # 主脚本
├── requirements.txt   # Python 依赖
└── README.md          # 使用说明
```

## 相关文档

- [OrcaNote CLI 工具参考](../references/tools.md)
- [查询语法参考](../references/query-blocks.md)

## 更新日志

### v1.1.0 (2026-04-18)

- 新增仓库别名配置（REPO_CONFIG）
- 支持 `--repo` 使用别名，`--repoid` 直接指定仓库 ID
- 新增 Excel `--sheet` 参数，支持指定 sheet 名称或索引
- 移除 DEFAULT_REPO_ID 配置，统一使用 REPO_CONFIG

### v1.0.0 (2026-04-18)

- 初始版本
- 支持所有 OrcaNote CLI 工具
- 支持 Markdown/CSV/Excel 文件输入
- 提供类 API 和命令行两种使用方式