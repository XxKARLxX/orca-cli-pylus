#!/usr/bin/env python3
"""
OrcaNote PyPlus - 封装 orcanote.exe 的 Python 脚本

功能：
- 支持所有 OrcaNote CLI 工具
- 参数化 JSON 输入，无需手动构造 JSON
- 支持 Markdown 文件、CSV/Excel 文件、字符串作为内容输入
- 支持仓库别名配置，简化多仓库切换
- Windows 系统优化，解决中文编码问题

作者：Karl
GitHub: https://github.com/XxKARLxX
版本：1.1.0
"""

import subprocess
import json
import sys
import os
import argparse
import pandas as pd
from pathlib import Path
from typing import Optional, List, Union

# ============================================================================
# 配置区域 - 用户可自定义
# ============================================================================

# OrcaNote CLI 可执行文件路径（用户需根据实际情况修改）
ORCANOTE_CLI_PATH = r"C:\Users\karl_\.config\opencode\skills\orcanote_skill\orcanote.exe"

# 仓库别名配置（用户可自定义）
# 未指定 --repo 参数时使用 default
REPO_CONFIG = {
    "default": "your_repoif",
    "your_repo_alias": "your_repoif",
}

def get_repo_id(alias: str = "default") -> str:
    """根据别名获取仓库 ID，未找到返回 None"""
    return REPO_CONFIG.get(alias)

# ============================================================================
# 核心类
# ============================================================================

class OrcaNoteCLI:
    """OrcaNote CLI 封装类"""
    
    def __init__(self, cli_path: str = ORCANOTE_CLI_PATH, repo_id: str = None, repo_alias: str = "default"):
        """
        初始化 CLI 包装器
        
        Args:
            cli_path: orcanote.exe 的完整路径
            repo_id: 仓库 ID（直接指定）
            repo_alias: 仓库别名（从 REPO_CONFIG 获取）
        
        优先级：repo_id > repo_alias
        """
        self.cli_path = cli_path
        
        # 优先使用直接指定的 repo_id，否则根据别名获取
        if repo_id:
            self.repo_id = repo_id
        else:
            self.repo_id = get_repo_id(repo_alias)
        
        # 验证 CLI 是否存在
        if not os.path.exists(cli_path):
            raise FileNotFoundError(f"OrcaNote CLI not found: {cli_path}")
    
    def _run_command(self, tool_name: str, input_data: dict) -> dict:
        """
        执行 CLI 命令
        
        Args:
            tool_name: 工具名称（如 insert_markdown, query_blocks）
            input_data: 输入参数（不含 repoId）
        
        Returns:
            dict: CLI 返回的 JSON 结果
        """
        input_json = json.dumps(input_data, ensure_ascii=False)
        
        cmd = [
            self.cli_path,
            tool_name,
            "--repo", self.repo_id,
            "--input", input_json,
            "--json"
        ]
        
        # 执行命令，使用 UTF-8 编码
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # 解析输出
        if result.stdout:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"success": False, "error": "Invalid JSON output", "raw": result.stdout}
        
        return {"success": False, "error": result.stderr or "No output"}
    
    # ------------------------------------------------------------------------
    # 内容插入方法
    # ------------------------------------------------------------------------
    
    def insert_markdown(
        self,
        ref_block_id: int,
        text: Optional[str] = None,
        markdown_file: Optional[str] = None,
        position: str = "after"
    ) -> dict:
        """
        插入 Markdown 内容
        
        Args:
            ref_block_id: 参考块 ID
            text: 直接传入的文本内容
            markdown_file: Markdown 文件路径（.md）
            position: 插入位置（before/after/firstChild/lastChild）
        
        Returns:
            dict: 插入结果
        
        Example:
            # 从文件插入
            cli.insert_markdown(ref_block_id=123, markdown_file="content.md")
            
            # 直接插入文本
            cli.insert_markdown(ref_block_id=123, text="# Title\\nContent here")
        """
        # 获取内容
        if markdown_file:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                text = f.read()
        elif text is None:
            raise ValueError("Either text or markdown_file must be provided")
        
        input_data = {
            "refBlockId": ref_block_id,
            "position": position,
            "text": text
        }
        
        return self._run_command("insert_markdown", input_data)
    
    def insert_table(
        self,
        ref_block_id: int,
        table_file: Optional[str] = None,
        data: Optional[List[List[str]]] = None,
        headers: Optional[List[str]] = None,
        position: str = "after",
        title: Optional[str] = None,
        sheet_name: Union[str, int] = 0
    ) -> dict:
        """
        插入表格（从 CSV/Excel 或数据数组）
        
        Args:
            ref_block_id: 参考块 ID
            table_file: CSV 或 Excel 文件路径
            data: 二维数据数组（如 [["col1", "col2"], ["val1", "val2"]]）
            headers: 表头（如果 data 不包含表头）
            position: 插入位置
            title: 表格标题
            sheet_name: Excel 的 sheet 名称或索引（默认 0，第一个 sheet）
        
        Returns:
            dict: 插入结果
        
        Example:
            # 从 CSV 文件插入
            cli.insert_table(ref_block_id=123, table_file="data.csv")
            
            # 从 Excel 文件插入（第一个 sheet）
            cli.insert_table(ref_block_id=123, table_file="data.xlsx")
            
            # 从 Excel 文件插入（指定 sheet 名称）
            cli.insert_table(ref_block_id=123, table_file="data.xlsx", sheet_name="Sheet2")
            
            # 从数据数组插入
            cli.insert_table(
                ref_block_id=123,
                headers=["Name", "Age"],
                data=[["Alice", "25"], ["Bob", "30"]]
            )
        """
        # 获取数据
        if table_file:
            if table_file.endswith('.csv'):
                df = pd.read_csv(table_file, encoding='utf-8')
            elif table_file.endswith('.xlsx') or table_file.endswith('.xls'):
                df = pd.read_excel(table_file, sheet_name=sheet_name)
            else:
                raise ValueError("table_file must be CSV or Excel (.csv/.xlsx/.xls)")
            
            headers = list(df.columns)
            data = df.values.tolist()
        elif data is None:
            raise ValueError("Either table_file or data must be provided")
        
        # 构建 Markdown 表格
        md_lines = []
        
        if title:
            md_lines.append(f"### {title}")
            md_lines.append("")
        
        # 表头
        if headers:
            header_row = "| " + " | ".join(str(h) for h in headers) + " |"
            separator_row = "|" + "|".join([" --- " for _ in headers]) + "|"
            md_lines.append(header_row)
            md_lines.append(separator_row)
        
        # 数据行
        for row in data:
            row_str = "| " + " | ".join(str(cell) if cell is not None else "" for cell in row) + " |"
            md_lines.append(row_str)
        
        text = "\n".join(md_lines)
        
        return self.insert_markdown(ref_block_id, text=text, position=position)
    
    # ------------------------------------------------------------------------
    # 内容查询方法
    # ------------------------------------------------------------------------
    
    def get_blocks_text(
        self,
        block_ids: List[int],
        child_start: Optional[int] = None,
        child_end: Optional[int] = None
    ) -> dict:
        """
        获取块的文本内容
        
        Args:
            block_ids: 块 ID 列表
            child_start: 子块起始索引（1-based）
            child_end: 子块结束索引（1-based）
        
        Returns:
            dict: 块内容
        """
        input_data = {"blockIds": block_ids}
        
        if child_start is not None and child_end is not None:
            input_data["childStartIndex"] = child_start
            input_data["childEndIndex"] = child_end
        
        return self._run_command("get_blocks_text", input_data)
    
    def get_page(self, block_ids: List[int]) -> dict:
        """
        获取块所在的页面
        
        Args:
            block_ids: 块 ID 列表
        
        Returns:
            dict: 页面信息
        """
        return self._run_command("get_page", {"blockIds": block_ids})
    
    def get_tags_and_pages(self, page_num: int = 1, page_size: int = 200) -> dict:
        """
        获取标签和页面列表
        
        Args:
            page_num: 页码
            page_size: 每页数量
        
        Returns:
            dict: 标签和页面列表
        """
        return self._run_command("get_tags_and_pages", {
            "pageNum": page_num,
            "pageSize": page_size
        })
    
    def get_today_journal(self) -> dict:
        """
        获取今日日记块 ID
        
        Returns:
            dict: 包含 blockId 和 date
        """
        return self._run_command("get_today_journal", {})
    
    def search_text(self, text: str, page_size: int = 50) -> dict:
        """
        搜索文本
        
        Args:
            text: 搜索文本
            page_size: 返回数量
        
        Returns:
            dict: 搜索结果
        """
        return self._run_command("query_blocks", {
            "description": {
                "q": {"kind": 100, "conditions": [{"kind": 8, "text": text}]},
                "page": 1,
                "pageSize": page_size
            }
        })
    
    # ------------------------------------------------------------------------
    # 内容修改方法
    # ------------------------------------------------------------------------
    
    def create_page(self, name: str, include_in: Optional[List[str]] = None) -> dict:
        """
        创建页面
        
        Args:
            name: 页面名称
            include_in: 包含的页面名称列表
        
        Returns:
            dict: 创建结果
        """
        input_data = {"name": name}
        if include_in:
            input_data["includeIn"] = include_in
        return self._run_command("create_page", input_data)
    
    def delete_blocks(self, block_ids: List[int]) -> dict:
        """
        删除块
        
        Args:
            block_ids: 块 ID 列表
        
        Returns:
            dict: 删除结果
        """
        return self._run_command("delete_blocks", {"blockIds": block_ids})
    
    def move_blocks(
        self,
        block_ids: List[int],
        parent_id: int,
        left_id: Optional[int] = None
    ) -> dict:
        """
        移动块
        
        Args:
            block_ids: 要移动的块 ID 列表
            parent_id: 目标父块 ID
            left_id: 左侧兄弟块 ID
        
        Returns:
            dict: 移动结果
        """
        input_data = {
            "blockIds": block_ids,
            "parentId": parent_id
        }
        if left_id is not None:
            input_data["leftId"] = left_id
        return self._run_command("move_blocks", input_data)
    
    # ------------------------------------------------------------------------
    # 标签方法
    # ------------------------------------------------------------------------
    
    def create_tags(self, tags: List[dict]) -> dict:
        """
        创建标签
        
        Args:
            tags: 标签定义列表
        
        Returns:
            dict: 创建结果
        
        Example:
            cli.create_tags([
                {"name": "task", "properties": [
                    {"name": "priority", "type": "select", "options": ["low", "high"]}
                ]}
            ])
        """
        return self._run_command("create_tags", {"tags": tags})
    
    def insert_tags(
        self,
        block_ids: List[int],
        tags: List[Union[str, dict]]
    ) -> dict:
        """
        为块添加标签
        
        Args:
            block_ids: 块 ID 列表
            tags: 标签列表（字符串或带属性的字典）
        
        Returns:
            dict: 操作结果
        
        Example:
            # 简单标签
            cli.insert_tags(block_ids=[123], tags=["status"])
            
            # 带属性的标签
            cli.insert_tags(
                block_ids=[123],
                tags=[{"name": "related", "props": {"Blocks": [456]}}]
            )
        """
        return self._run_command("insert_tags", {
            "blockIds": block_ids,
            "tags": tags
        })
    
    def remove_tags(self, block_ids: List[int], tags: List[str]) -> dict:
        """
        移除块的标签
        
        Args:
            block_ids: 块 ID 列表
            tags: 标签名称列表
        
        Returns:
            dict: 操作结果
        """
        return self._run_command("remove_tags", {
            "blockIds": block_ids,
            "tags": tags
        })


# ============================================================================
# 命令行入口
# ============================================================================

def create_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="OrcaNote PyPlus - OrcaNote CLI 封装工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 插入 Markdown 文件
  python orcanote_pyplus.py insert-md --ref 123 --file content.md
  
  # 插入 Excel 表格（指定 sheet）
  python orcanote_pyplus.py insert-table --ref 123 --file data.xlsx --sheet "Sheet2"
  
  # 获取块内容
  python orcanote_pyplus.py get --blocks 123,456
  
  # 创建页面
  python orcanote_pyplus.py create-page --name "New Page"
  
  # 删除块
  python orcanote_pyplus.py delete --blocks 123,456
        """
    )
    
    # 全局参数
    parser.add_argument("--repo", default="default", help="仓库别名（从 REPO_CONFIG 获取，默认 default)")
    parser.add_argument("--repoid", help="直接指定仓库 ID（优先级高于 --repo)")
    parser.add_argument("--cli-path", default=ORCANOTE_CLI_PATH, help="orcanote.exe 路径")
    
    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # insert-md 命令
    insert_md_parser = subparsers.add_parser("insert-md", help="插入 Markdown")
    insert_md_parser.add_argument("--ref", type=int, required=True, help="参考块 ID")
    insert_md_parser.add_argument("--file", help="Markdown 文件路径")
    insert_md_parser.add_argument("--text", help="直接传入的文本")
    insert_md_parser.add_argument("--position", default="after", 
                                   choices=["before", "after", "firstChild", "lastChild"],
                                   help="插入位置")
    
    # insert-table 命令
    insert_table_parser = subparsers.add_parser("insert-table", help="插入表格")
    insert_table_parser.add_argument("--ref", type=int, required=True, help="参考块 ID")
    insert_table_parser.add_argument("--file", help="CSV/Excel 文件路径")
    insert_table_parser.add_argument("--title", help="表格标题")
    insert_table_parser.add_argument("--position", default="after", help="插入位置")
    insert_table_parser.add_argument("--sheet", default=0, help="Excel sheet 名称或索引（默认 0，第一个 sheet)")
    
    # get 命令
    get_parser = subparsers.add_parser("get", help="获取块内容")
    get_parser.add_argument("--blocks", required=True, help="块 ID（逗号分隔）")
    get_parser.add_argument("--child-start", type=int, help="子块起始索引")
    get_parser.add_argument("--child-end", type=int, help="子块结束索引")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索文本")
    search_parser.add_argument("--text", required=True, help="搜索文本")
    search_parser.add_argument("--limit", type=int, default=50, help="返回数量")
    
    # create-page 命令
    create_page_parser = subparsers.add_parser("create-page", help="创建页面")
    create_page_parser.add_argument("--name", required=True, help="页面名称")
    create_page_parser.add_argument("--include", nargs="+", help="包含的页面")
    
    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除块")
    delete_parser.add_argument("--blocks", required=True, help="块 ID（逗号分隔）")
    
    # move 命令
    move_parser = subparsers.add_parser("move", help="移动块")
    move_parser.add_argument("--blocks", required=True, help="要移动的块 ID")
    move_parser.add_argument("--parent", type=int, required=True, help="目标父块 ID")
    move_parser.add_argument("--left", type=int, help="左侧兄弟块 ID")
    
    # tags 命令
    tags_parser = subparsers.add_parser("tags", help="添加标签")
    tags_parser.add_argument("--blocks", required=True, help="块 ID")
    tags_parser.add_argument("--tag-names", nargs="+", required=True, help="标签名称")
    
    # journal 命令
    subparsers.add_parser("journal", help="获取今日日记")
    
    return parser


def main():
    """主函数"""
    
    # 确保输出编码
    sys.stdout.reconfigure(encoding='utf-8')
    
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 初始化 CLI（优先使用 --repoid，否则使用 --repo 别名）
    if args.repoid:
        cli = OrcaNoteCLI(cli_path=args.cli_path, repo_id=args.repoid)
    else:
        cli = OrcaNoteCLI(cli_path=args.cli_path, repo_alias=args.repo)
    
    # 执行命令
    result = None
    
    if args.command == "insert-md":
        result = cli.insert_markdown(
            ref_block_id=args.ref,
            markdown_file=args.file,
            text=args.text,
            position=args.position
        )
    
    elif args.command == "insert-table":
        result = cli.insert_table(
            ref_block_id=args.ref,
            table_file=args.file,
            title=args.title,
            position=args.position,
            sheet_name=args.sheet
        )
    
    elif args.command == "get":
        block_ids = [int(x) for x in args.blocks.split(",")]
        result = cli.get_blocks_text(
            block_ids=block_ids,
            child_start=args.child_start,
            child_end=args.child_end
        )
    
    elif args.command == "search":
        result = cli.search_text(text=args.text, page_size=args.limit)
    
    elif args.command == "create-page":
        result = cli.create_page(name=args.name, include_in=args.include)
    
    elif args.command == "delete":
        block_ids = [int(x) for x in args.blocks.split(",")]
        result = cli.delete_blocks(block_ids=block_ids)
    
    elif args.command == "move":
        block_ids = [int(x) for x in args.blocks.split(",")]
        result = cli.move_blocks(
            block_ids=block_ids,
            parent_id=args.parent,
            left_id=args.left
        )
    
    elif args.command == "tags":
        block_ids = [int(x) for x in args.blocks.split(",")]
        result = cli.insert_tags(
            block_ids=block_ids,
            tags=args.tag_names
        )
    
    elif args.command == "journal":
        result = cli.get_today_journal()
    
    # 输出结果
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
