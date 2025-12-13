"""测试报告生成器"""
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import subprocess


def run_pytest_with_coverage() -> Dict[str, Any]:
    """运行pytest并获取覆盖率"""
    try:
        result = subprocess.run(
            ["pytest", "tests/", "-v", "--cov=src", "--cov-report=json", "--cov-report=term"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # 解析覆盖率JSON
        coverage_file = Path("coverage.json")
        if coverage_file.exists():
            with open(coverage_file, "r", encoding="utf-8") as f:
                coverage_data = json.load(f)
                total_coverage = coverage_data.get("totals", {}).get("percent_covered", 0)
        else:
            total_coverage = 0
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "coverage": total_coverage,
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "coverage": 0
        }


def run_system_tests() -> Dict[str, Any]:
    """运行系统功能测试"""
    try:
        result = subprocess.run(
            [sys.executable, "tests/test_system_functionality.py"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # 解析输出，统计通过/失败
        output = result.stdout
        passed = output.count("✅") + output.count("[PASS]")
        failed = output.count("❌") + output.count("[FAIL]")
        skipped = output.count("⏭️") + output.count("[SKIP]")
        
        return {
            "success": result.returncode == 0,
            "stdout": output,
            "stderr": result.stderr,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "passed": 0,
            "failed": 0,
            "skipped": 0
        }


def run_production_readiness() -> Dict[str, Any]:
    """运行生产就绪性测试"""
    try:
        result = subprocess.run(
            [sys.executable, "tests/test_production_readiness.py"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        output = result.stdout
        passed = output.count("[PASS]")
        failed = output.count("[FAIL]")
        warned = output.count("[WARN]")
        skipped = output.count("[SKIP]")
        
        return {
            "success": result.returncode == 0,
            "stdout": output,
            "stderr": result.stderr,
            "passed": passed,
            "failed": failed,
            "warned": warned,
            "skipped": skipped,
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "passed": 0,
            "failed": 0,
            "warned": 0,
            "skipped": 0
        }


def generate_html_report(report_data: Dict[str, Any]) -> str:
    """生成HTML测试报告"""
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>系统1.0版本测试报告</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .card h3 {{
            margin: 0 0 10px 0;
            color: #666;
            font-size: 14px;
        }}
        .card .value {{
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }}
        .pass {{ color: #4caf50; }}
        .fail {{ color: #f44336; }}
        .warn {{ color: #ff9800; }}
        .section {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            margin-top: 0;
            color: #333;
        }}
        pre {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>系统1.0版本测试报告</h1>
        <p>生成时间: {report_data.get('timestamp', datetime.now().isoformat())}</p>
    </div>
    
    <div class="summary">
        <div class="card">
            <h3>测试覆盖率</h3>
            <div class="value">{report_data.get('pytest', {}).get('coverage', 0):.1f}%</div>
        </div>
        <div class="card">
            <h3>系统测试通过</h3>
            <div class="value pass">{report_data.get('system_tests', {}).get('passed', 0)}</div>
        </div>
        <div class="card">
            <h3>系统测试失败</h3>
            <div class="value fail">{report_data.get('system_tests', {}).get('failed', 0)}</div>
        </div>
        <div class="card">
            <h3>生产就绪性</h3>
            <div class="value {'pass' if report_data.get('production', {}).get('success') else 'fail'}">
                {'✓' if report_data.get('production', {}).get('success') else '✗'}
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>Pytest单元测试</h2>
        <p><strong>状态:</strong> {'通过' if report_data.get('pytest', {}).get('success') else '失败'}</p>
        <p><strong>覆盖率:</strong> {report_data.get('pytest', {}).get('coverage', 0):.1f}%</p>
        <pre>{report_data.get('pytest', {}).get('stdout', '无输出')[:1000]}</pre>
    </div>
    
    <div class="section">
        <h2>系统功能测试</h2>
        <p><strong>通过:</strong> {report_data.get('system_tests', {}).get('passed', 0)}</p>
        <p><strong>失败:</strong> {report_data.get('system_tests', {}).get('failed', 0)}</p>
        <p><strong>跳过:</strong> {report_data.get('system_tests', {}).get('skipped', 0)}</p>
        <pre>{report_data.get('system_tests', {}).get('stdout', '无输出')[:2000]}</pre>
    </div>
    
    <div class="section">
        <h2>生产就绪性测试</h2>
        <p><strong>状态:</strong> {'通过' if report_data.get('production', {}).get('success') else '失败'}</p>
        <p><strong>通过:</strong> {report_data.get('production', {}).get('passed', 0)}</p>
        <p><strong>失败:</strong> {report_data.get('production', {}).get('failed', 0)}</p>
        <p><strong>警告:</strong> {report_data.get('production', {}).get('warned', 0)}</p>
        <pre>{report_data.get('production', {}).get('stdout', '无输出')[:2000]}</pre>
    </div>
    
    <div class="section">
        <h2>总结</h2>
        <p><strong>总体状态:</strong> 
            <span class="{'pass' if report_data.get('overall_success') else 'fail'}">
                {'✓ 系统可以正常运行' if report_data.get('overall_success') else '✗ 系统存在问题，需要修复'}
            </span>
        </p>
        <p><strong>建议:</strong></p>
        <ul>
            {''.join([f'<li>{s}</li>' for s in report_data.get('recommendations', [])])}
        </ul>
    </div>
</body>
</html>
"""
    return html


def main():
    """主函数"""
    print("=" * 80)
    print("生成系统1.0版本测试报告")
    print("=" * 80)
    print()
    
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "pytest": {},
        "system_tests": {},
        "production": {}
    }
    
    # 运行pytest测试
    print("1. 运行pytest单元测试...")
    report_data["pytest"] = run_pytest_with_coverage()
    print(f"   覆盖率: {report_data['pytest'].get('coverage', 0):.1f}%")
    
    # 运行系统功能测试
    print("\n2. 运行系统功能测试...")
    report_data["system_tests"] = run_system_tests()
    print(f"   通过: {report_data['system_tests'].get('passed', 0)}, "
          f"失败: {report_data['system_tests'].get('failed', 0)}")
    
    # 运行生产就绪性测试
    print("\n3. 运行生产就绪性测试...")
    report_data["production"] = run_production_readiness()
    print(f"   通过: {report_data['production'].get('passed', 0)}, "
          f"失败: {report_data['production'].get('failed', 0)}")
    
    # 判断总体状态
    report_data["overall_success"] = (
        report_data["pytest"].get("success", False) and
        report_data["system_tests"].get("success", False) and
        report_data["production"].get("success", False)
    )
    
    # 生成建议
    recommendations = []
    if report_data["pytest"].get("coverage", 0) < 60:
        recommendations.append("测试覆盖率低于60%，建议增加更多单元测试")
    if report_data["system_tests"].get("failed", 0) > 0:
        recommendations.append(f"系统测试有{report_data['system_tests']['failed']}个失败项，需要修复")
    if report_data["production"].get("failed", 0) > 0:
        recommendations.append(f"生产就绪性测试有{report_data['production']['failed']}个失败项，需要修复")
    if not recommendations:
        recommendations.append("所有测试通过，系统可以正常运行")
    
    report_data["recommendations"] = recommendations
    
    # 保存JSON报告
    report_dir = Path("data/test_reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    json_file = report_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    print(f"\nJSON报告已保存: {json_file}")
    
    # 生成HTML报告
    html_content = generate_html_report(report_data)
    html_file = report_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML报告已保存: {html_file}")
    
    # 打印总结
    print("\n" + "=" * 80)
    print("测试报告总结")
    print("=" * 80)
    print(f"测试覆盖率: {report_data['pytest'].get('coverage', 0):.1f}%")
    print(f"系统测试: 通过 {report_data['system_tests'].get('passed', 0)}, "
          f"失败 {report_data['system_tests'].get('failed', 0)}")
    print(f"生产就绪性: {'通过' if report_data['production'].get('success') else '失败'}")
    print(f"\n总体状态: {'✓ 系统可以正常运行' if report_data['overall_success'] else '✗ 系统存在问题'}")
    print()
    
    return 0 if report_data["overall_success"] else 1


if __name__ == "__main__":
    sys.exit(main())

