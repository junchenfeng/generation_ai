#!/usr/bin/env python3
"""
Kaggle多代理系统使用示例
这个文件展示如何使用多代理系统来自动解决Kaggle竞赛
适合Python初学者学习
"""

import os
import sys
from pathlib import Path

# 添加当前目录到Python路径，这样可以导入我们自己的模块
sys.path.append(str(Path(__file__).parent))

from kaggle_multi_agent import KaggleMultiAgent, Phase
from config import Config

def check_environment():
    """
    检查运行环境是否准备好
    返回: True表示环境正常，False表示有问题
    """
    print("🔍 检查运行环境...")
    
    # 验证配置
    validation_result = Config.validate()
    if not validation_result["valid"]:
        print("❌ 环境检查失败:")
        for problem in validation_result["issues"]:
            print(f"   - {problem}")
        print("\n💡 解决方案:")
        print("1. 设置环境变量: export OPENAI_API_KEY='your-key-here'")
        print("2. 确保数据集路径存在")
        return False
    
    print("✅ 环境检查通过")
    return True

def setup_directories(dataset_name):
    """
    设置和创建必要的目录
    参数: dataset_name - 数据集名称
    返回: (数据集路径, 输出目录路径)
    """
    print(f"📁 设置目录结构...")
    
    # 构建路径
    dataset_path = os.path.join(Config.DEFAULT_DATASET_PATH, dataset_name)
    output_dir = os.path.join(Config.DEFAULT_OUTPUT_DIR, dataset_name)
    
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 显示路径信息
    print(f"   📂 数据集路径: {dataset_path}")
    print(f"   📂 工作目录: {Config.DEFAULT_WORK_DIR}")
    print(f"   📂 输出目录: {output_dir}")
    
    # 检查数据集是否存在
    if not os.path.exists(dataset_path):
        print(f"❌ 数据集不存在: {dataset_path}")
        return None, None
    
    return dataset_path, output_dir

def create_agent_system(output_dir):
    """
    创建多代理系统
    参数: output_dir - 输出目录
    返回: 多代理系统对象，失败则返回None
    """
    print("🤖 创建多代理系统...")
    
    try:
        agent_system = KaggleMultiAgent(
            api_key=Config.OPENAI_API_KEY,
            work_dir=Config.DEFAULT_WORK_DIR,
            output_dir=output_dir,
            timeout=Config.EXECUTION_TIMEOUT,
            plan_agent_model=Config.PLAN_AGENT_MODEL,
            code_agent_model=Config.CODE_AGENT_MODEL
        )
        print("✅ 多代理系统创建成功")
        return agent_system
    except Exception as error:
        print(f"❌ 创建失败: {str(error)}")
        return None

def run_competition_and_save_report(agent_system, dataset_path, output_dir):
    """
    运行竞赛并保存报告
    参数: 
        agent_system - 多代理系统
        dataset_path - 数据集路径
        output_dir - 输出目录
    """
    print("🏁 开始自动化竞赛解决...")
    
    try:
        # 运行竞赛
        results = agent_system.run_competition(
            dataset_path=dataset_path,
            max_iterations=Config.MAX_ITERATIONS
        )
        
        # 生成报告
        print("📊 生成执行报告...")
        report = agent_system.generate_report()
        
        # 显示报告摘要
        print("\n" + "="*50)
        print("📋 执行报告摘要")
        print("="*50)
        print(report)
        
        # 保存详细报告到文件
        report_file = os.path.join(output_dir, "execution_report.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"💾 详细报告已保存: {report_file}")
        
        # 显示统计信息
        show_execution_statistics(results, agent_system, output_dir)
        
        print("🎉 执行完成!")
        
    except KeyboardInterrupt:
        print("\n⚠️  用户中断执行")
    except Exception as error:
        print(f"\n❌ 执行过程出错: {str(error)}")

def show_execution_statistics(results, agent_system, output_dir):
    """
    显示执行统计信息
    """
    print("\n📈 执行统计:")
    print(f"   - 成功阶段: {len(results)}/{len(list(Phase))}")
    print(f"   - 总执行次数: {len(agent_system.action_agent.execution_history)}")
    
    # 检查是否生成了提交文件
    submission_files = [
        f for f in os.listdir(output_dir) 
        if f.startswith('submission') and f.endswith('.csv')
    ]
    
    if submission_files:
        print(f"   - 生成提交文件: {len(submission_files)} 个")
        for file in submission_files:
            print(f"     📄 {file}")
    else:
        print("   - ⚠️  未生成提交文件")

def main():
    """
    主函数 - 程序的入口点
    """
    print("🚀 Kaggle多代理系统启动")
    print("="*50)
    
    # 第1步: 检查环境
    if not check_environment():
        return
    
    # 第2步: 设置目录
    dataset_name = "predict_rainfall"  # 可以修改为其他数据集名称
    dataset_path, output_dir = setup_directories(dataset_name)
    if dataset_path is None:
        return
    
    # 第3步: 创建多代理系统
    agent_system = create_agent_system(output_dir)
    if agent_system is None:
        return
    
    # 第4步: 运行竞赛并保存报告
    run_competition_and_save_report(agent_system, dataset_path, output_dir)

# 如果直接运行这个文件，就执行main函数
if __name__ == "__main__":
    main() 