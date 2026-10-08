"""Command-line interface for cash flow report generation."""

import argparse
from pathlib import Path

from KingdeeZwyCashFlowGenerator.configuration.settings import Environment
from KingdeeZwyCashFlowGenerator.core.generator import CashFlowReportGenerator
from KingdeeZwyCashFlowGenerator.core.paths import PROJECT_ROOT


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='现金流量报表生成器')
    parser.add_argument('--mode', '-m', 
                        choices=['full', 'template', 'fill', 'report', 'summary'],
                        default='full', 
                        help='运行模式: full(完整流程), template(仅生成模板), fill(仅填入数据), report(仅生成报表), summary(汇总模式)')
    parser.add_argument('--input', '-i', 
                        help='输入文件路径（指定则跳过文件选择）')
    parser.add_argument('--template', '-t', 
                        help='模板文件路径（fill模式使用）')
    parser.add_argument('--output', '-o', 
                        help='输出文件路径')
    parser.add_argument('--quarter', '-q', 
                        default='Q2', 
                        help='目标季度 (默认: Q2)')
    parser.add_argument('--env', 
                        choices=['dev', 'test', 'prod'],
                        default='dev', 
                        help='运行环境')
    
    args = parser.parse_args()
    
    env_map = {
        'dev': Environment.DEVELOPMENT,
        'test': Environment.TESTING,
        'prod': Environment.PRODUCTION
    }
    env = env_map.get(args.env, Environment.DEVELOPMENT)
    
    generator = CashFlowReportGenerator(env)
    
    print("=" * 60)
    print("    现金流量报表生成器")
    print(f"    环境: {env.value}")
    print(f"    模式: {args.mode}")
    print(f"    项目根目录: {PROJECT_ROOT}")
    print("=" * 60)
    
    input_dir = generator.get_input_dir()
    if not input_dir.exists():
        input_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n📁 已创建 input 目录: {input_dir}")
        print(f"   请将明细账文件放入该目录")
        return 1
    
    output_dir = generator.get_output_dir()
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.mode == 'summary':
        # 汇总模式
        print("\n" + "=" * 60)
        print("    模式: 汇总模式")
        print("=" * 60)
        
        if args.input:
            input_files = [Path(args.input)]
        else:
            input_files = generator.scan_input_files()
            if not input_files:
                print("❌ 没有找到Excel文件")
                return 1
        
        result = generator.run_summary(input_files, Path(args.output) if args.output else None)
        return 0 if result else 1
    
    if args.input:
        input_file = Path(args.input)
        if not input_file.exists():
            print(f"❌ 指定的输入文件不存在: {input_file}")
            return 1
        print(f"\n📁 使用指定的文件: {input_file}")
    else:
        input_file = generator.select_input_file()
        if input_file is None:
            return 1
    
    if args.mode == 'template':
        print("\n" + "=" * 60)
        print("    模式: 仅生成模板")
        print("=" * 60)
        
        result = generator.generate_template(input_file)
        if result:
            print(f"\n✅ 模板生成成功: {result}")
        return 0
    
    if args.mode == 'fill':
        print("\n" + "=" * 60)
        print("    模式: 仅填入数据")
        print("=" * 60)
        
        transactions = generator.load_transactions(input_file)
        if not generator.validate_transactions(transactions):
            return 1
        
        template_path = args.template or generator.template_path or str(generator.get_template_path())
        if not Path(template_path).exists():
            print(f"❌ 模板文件不存在: {template_path}")
            print(f"   请先运行模板生成模式，或使用 -t 指定模板文件")
            return 1
        
        result = generator.fill_data(template_path, transactions, args.quarter)
        if result:
            print(f"\n✅ 数据填入成功: {result}")
        return 0
    
    if args.mode == 'report':
        print("\n" + "=" * 60)
        print("    模式: 仅生成报表")
        print("=" * 60)
        
        transactions = generator.load_transactions(input_file)
        if not generator.validate_transactions(transactions):
            return 1
        
        result = generator.generate_report(transactions, args.output)
        if result:
            print(f"\n✅ 报表生成成功: {result}")
        return 0
    
    # 完整流程 (默认)
    success = generator.run_full_flow(input_file, args.quarter)
    return 0 if success else 1




if __name__ == "__main__":
    raise SystemExit(main())
