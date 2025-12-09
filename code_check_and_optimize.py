"""
代码检查和优化脚本
检查代码质量、潜在问题并提供优化建议
"""
import ast
import os
import re
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict

# 项目根目录
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"

# 问题收集
issues = defaultdict(list)
warnings = defaultdict(list)
suggestions = defaultdict(list)


def check_file(file_path: Path) -> Dict[str, Any]:
    """检查单个Python文件"""
    file_issues = []
    file_warnings = []
    file_suggestions = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        return {
            'error': f"无法读取文件: {e}",
            'issues': [],
            'warnings': [],
            'suggestions': []
        }
    
    # 检查1: 导入不存在的模块
    if 'instagram' in content and 'src.instagram' in content:
        # 检查文件是否存在
        instagram_files = [
            'src/instagram/webhook_handler.py',
            'src/instagram/register.py'
        ]
        for inst_file in instagram_files:
            if not (PROJECT_ROOT / inst_file).exists():
                file_issues.append(f"导入不存在的模块: {inst_file}")
    
    if 'facebook.register' in content:
        if not (PROJECT_ROOT / 'src/facebook/register.py').exists():
            file_issues.append("导入不存在的模块: src.facebook.register")
    
    if 'platforms.registry' in content or 'platforms.base' in content:
        if not (PROJECT_ROOT / 'src/platforms/registry.py').exists():
            file_warnings.append("导入可能不存在的模块: src.platforms.registry")
        if not (PROJECT_ROOT / 'src/platforms/base.py').exists():
            file_warnings.append("导入可能不存在的模块: src.platforms.base")
    
    # 检查2: 使用print而不是logger
    for i, line in enumerate(lines, 1):
        if re.search(r'\bprint\s*\(', line) and 'logger' not in line.lower():
            if 'src/config/loader.py' in str(file_path) or 'src/config/page_settings.py' in str(file_path):
                file_suggestions.append(f"第{i}行: 考虑使用logger代替print: {line.strip()[:60]}")
    
    # 检查3: 过于宽泛的异常捕获
    for i, line in enumerate(lines, 1):
        if re.search(r'except\s+Exception\s*:', line) or re.search(r'except\s*:', line):
            file_suggestions.append(f"第{i}行: 考虑使用更具体的异常类型: {line.strip()[:60]}")
    
    # 检查4: 未使用的导入
    try:
        tree = ast.parse(content)
        imports = set()
        used_names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
            elif isinstance(node, ast.Name):
                used_names.add(node.id.split('.')[0])
        
        # 检查未使用的标准库导入
        stdlib_imports = {'asyncio', 'time', 'typing'}
        for imp in stdlib_imports:
            if imp in imports and imp not in used_names:
                if imp == 'asyncio' and 'async def' in content:
                    continue  # asyncio可能用于装饰器
                file_suggestions.append(f"可能未使用的导入: {imp}")
    except SyntaxError:
        pass  # 忽略语法错误，可能是模板文件
    
    # 检查5: 硬编码的字符串
    if 'graph.facebook.com/v18.0' in content:
        file_suggestions.append("考虑将API版本号提取为配置常量")
    
    # 检查6: 缺少类型提示
    async_defs = re.findall(r'async def (\w+)', content)
    defs = re.findall(r'^\s*def (\w+)', content, re.MULTILINE)
    for func_name in async_defs + defs:
        # 检查是否有类型提示
        func_pattern = rf'async def {func_name}|def {func_name}'
        matches = re.finditer(func_pattern, content)
        for match in matches:
            func_def = content[match.start():match.start()+200]
            if '->' not in func_def and func_name not in ['__init__', '__getattr__']:
                file_suggestions.append(f"函数 {func_name} 缺少返回类型提示")
    
    return {
        'issues': file_issues,
        'warnings': file_warnings,
        'suggestions': file_suggestions
    }


def check_all_files():
    """检查所有Python文件"""
    python_files = list(SRC_DIR.rglob('*.py'))
    
    print("=" * 80)
    print("代码检查和优化报告")
    print("=" * 80)
    print(f"\n检查 {len(python_files)} 个Python文件...\n")
    
    total_issues = 0
    total_warnings = 0
    total_suggestions = 0
    
    for file_path in python_files:
        # 跳过测试和缓存文件
        if 'test' in str(file_path) or '__pycache__' in str(file_path):
            continue
        
        result = check_file(file_path)
        
        if result.get('error'):
            print(f"[ERROR] {file_path.relative_to(PROJECT_ROOT)}: {result['error']}")
            continue
        
        if result['issues'] or result['warnings'] or result['suggestions']:
            rel_path = file_path.relative_to(PROJECT_ROOT)
            print(f"\n[FILE] {rel_path}")
            
            if result['issues']:
                print("  [ERROR] 问题:")
                for issue in result['issues']:
                    print(f"    - {issue}")
                    total_issues += 1
                    issues[rel_path].append(issue)
            
            if result['warnings']:
                print("  [WARN] 警告:")
                for warning in result['warnings']:
                    print(f"    - {warning}")
                    total_warnings += 1
                    warnings[rel_path].append(warning)
            
            if result['suggestions']:
                print("  [SUGGEST] 建议:")
                for suggestion in result['suggestions'][:5]:  # 只显示前5个
                    print(f"    - {suggestion}")
                    total_suggestions += 1
                    suggestions[rel_path].append(suggestion)
    
    print("\n" + "=" * 80)
    print("检查总结")
    print("=" * 80)
    print(f"总问题数: {total_issues}")
    print(f"总警告数: {total_warnings}")
    print(f"总建议数: {total_suggestions}")
    
    return {
        'issues': dict(issues),
        'warnings': dict(warnings),
        'suggestions': dict(suggestions),
        'total_issues': total_issues,
        'total_warnings': total_warnings,
        'total_suggestions': total_suggestions
    }


def generate_optimization_report(results: Dict[str, Any]):
    """生成优化报告"""
    report_path = PROJECT_ROOT / "CODE_OPTIMIZATION_REPORT.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 代码优化报告\n\n")
        f.write(f"**检查时间**: {Path(__file__).stat().st_mtime}\n\n")
        f.write(f"**总问题数**: {results['total_issues']}\n")
        f.write(f"**总警告数**: {results['total_warnings']}\n")
        f.write(f"**总建议数**: {results['total_suggestions']}\n\n")
        
        if results['issues']:
            f.write("## ❌ 需要修复的问题\n\n")
            for file_path, file_issues in results['issues'].items():
                f.write(f"### {file_path}\n\n")
                for issue in file_issues:
                    f.write(f"- {issue}\n")
                f.write("\n")
        
        if results['warnings']:
            f.write("## ⚠️  警告\n\n")
            for file_path, file_warnings in results['warnings'].items():
                f.write(f"### {file_path}\n\n")
                for warning in file_warnings:
                    f.write(f"- {warning}\n")
                f.write("\n")
        
        if results['suggestions']:
            f.write("## 💡 优化建议\n\n")
            for file_path, file_suggestions in results['suggestions'].items():
                f.write(f"### {file_path}\n\n")
                for suggestion in file_suggestions[:10]:  # 每个文件最多10个建议
                    f.write(f"- {suggestion}\n")
                f.write("\n")
        
        f.write("## 优化优先级\n\n")
        f.write("1. **高优先级**: 修复导入不存在的模块问题\n")
        f.write("2. **中优先级**: 替换print为logger\n")
        f.write("3. **低优先级**: 改进异常处理和类型提示\n\n")
    
    print(f"\n[OK] 优化报告已保存到: {report_path}")


if __name__ == "__main__":
    results = check_all_files()
    generate_optimization_report(results)
    
    # 如果有严重问题，返回非零退出码
    if results['total_issues'] > 0:
        print("\n[WARN] 发现需要修复的问题，请查看报告")
        exit(1)
    else:
        print("\n[OK] 代码检查完成，未发现严重问题")

