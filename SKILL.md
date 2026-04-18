## Windows Python Wrapper

**推荐在 Windows 系统使用 Python 封装脚本**，解决中文编码问题。

### 脚本位置

```
scripts/orcanote_pylus.py
```

### 安装依赖

```bash
pip install -r scripts/requirements.txt
```

### 配置

在脚本顶部修改仓库别名：

```python
REPO_CONFIG = {
    "default": "5bbuf6k97h79i",  # 默认仓库
    "oppo": "5bbuf6k97h79i",     # OPPO 测试仓库
    # 用户可添加其他仓库别名
}
```

### 使用示例

```python
from orcanote_pylus import OrcaNoteCLI

# 使用默认仓库（default 别名）
cli = OrcaNoteCLI()

# 使用仓库别名
cli = OrcaNoteCLI(repo_alias="oppo")

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
python scripts/orcanote_pylus.py --repo oppo insert-md --ref 123 --file content.md

# 直接指定仓库 ID
python scripts/orcanote_pylus.py --repoid other_repo_id insert-md --ref 123 --file content.md

# 插入 Excel 指定 sheet
python scripts/orcanote_pylus.py insert-table --ref 123 --file data.xlsx --sheet "Sheet2"

# 搜索
python scripts/orcanote_pylus.py search --text "keyword"

# 更多命令见 scripts/README.md
```