#!/usr/bin/env python3
"""
Kaggle多代理系统使用示例
简化版本，演示如何使用multi-agent系统解决Kaggle竞赛
"""

import os
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.append(str(Path(__file__).parent))

from kaggle_multi_agent import KaggleMultiAgent, Phase
from config import Config

def main():
    """主函数示例"""
    print("🚀 Kaggle多代理系统启动")
    print("="*50)
    
    # 1. 验证配置
    validation = Config.validate()
    if not validation["valid"]:
        print("❌ 配置验证失败:")
        for issue in validation["issues"]:
            print(f"   - {issue}")
        print("\n解决方案:")
        print("1. 设置环境变量: export OPENAI_API_KEY='your-key-here'")
        print("2. 确保数据集路径存在")
        return
    
    print("✅ 配置验证通过")
    
    # 2. 设置路径
    dataset_name = "predict_rainfall"
    dataset_path = os.path.join(Config.DEFAULT_DATASET_PATH, dataset_name)
    output_dir = os.path.join(Config.DEFAULT_OUTPUT_DIR, dataset_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    print(f"📁 数据集路径: {dataset_path}")
    print(f"📁 工作目录: {Config.DEFAULT_WORK_DIR}")
    print(f"📁 缓存目录: {output_dir}")
    
    # 3. 检查数据集是否存在
    if not os.path.exists(dataset_path):
        print(f"❌ 数据集不存在: {dataset_path}")
        print("请确保数据集路径正确")
        return
    
    # 4. 初始化多代理系统
    print("\n🤖 初始化多代理系统...")
    try:
        agent_system = KaggleMultiAgent(
            api_key=Config.OPENAI_API_KEY,
            work_dir=Config.DEFAULT_WORK_DIR,
            output_dir=output_dir,
            timeout=Config.EXECUTION_TIMEOUT
        )
        print("✅ 多代理系统初始化成功")
    except Exception as e:
        print(f"❌ 初始化失败: {str(e)}")
        return
    
    # 5. 运行竞赛解决流程
    print("\n🏁 开始自动化竞赛解决...")
    try:
        results = agent_system.run_competition(
            dataset_path=dataset_path,
            max_iterations=Config.MAX_ITERATIONS
        )
        
        # 6. 生成和保存报告
        print("\n📊 生成执行报告...")
        report = agent_system.generate_report()
        
        # 显示报告
        print("\n" + "="*50)
        print("📋 执行报告摘要")
        print("="*50)
        print(report)
        
        # 保存详细报告
        report_path = os.path.join(output_dir, "execution_report.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n💾 详细报告已保存到: {report_path}")
        
        # 7. 输出结果统计
        print("\n📈 执行统计:")
        print(f"   - 成功阶段: {len(results)}/{len(list(Phase))}")
        print(f"   - 总执行次数: {len(agent_system.action_agent.execution_history)}")
        
        # 检查是否有提交文件生成
        submission_files = [f for f in os.listdir(output_dir) if f.startswith('submission') and f.endswith('.csv')]
        if submission_files:
            print(f"   - 生成提交文件: {len(submission_files)} 个")
            for file in submission_files:
                print(f"     📄 {file}")
        else:
            print("   - ⚠️  未生成提交文件")
        
        print("\n🎉 执行完成!")
        
    except KeyboardInterrupt:
        print("\n⚠️  用户中断执行")
    except Exception as e:
        print(f"\n❌ 执行过程中出现错误: {str(e)}")

if __name__ == "__main__":

    main() 