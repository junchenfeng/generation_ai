"""
配置文件 - 多代理系统的基础设置
适合Python初学者阅读和理解
"""

import os
from typing import Dict, Any

class Config:
    """
    配置类 - 存储所有系统设置
    这个类包含了运行多代理系统所需的所有配置参数
    """
    
    # ========== OpenAI API 设置 ==========
    # 从环境变量获取 OpenAI API 密钥
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # 使用的 AI 模型名称
    PLAN_AGENT_MODEL = "o3-mini"      # 负责制定计划的模型
    CODE_AGENT_MODEL = "o4-mini"  # 负责生成代码的模型
    
    # ========== 执行控制设置 ==========
    # 每个阶段最多尝试几次（如果失败会重试）
    MAX_ITERATIONS = 3
    
    # 代码执行最大等待时间（秒）- 防止程序卡死
    EXECUTION_TIMEOUT = 600  # 10分钟
    
    # ========== 文件路径设置 ==========
    # 当前工作目录（执行代码的地方）
    DEFAULT_WORK_DIR = os.getcwd()
    
    # 输出结果保存目录
    DEFAULT_OUTPUT_DIR = "ml_agent/output"
    
    # 数据集存放目录  
    DEFAULT_DATASET_PATH = "data/kaggle_dataset"
    
    @classmethod
    def validate(cls) -> Dict[str, Any]:
        """
        检查配置是否正确
        返回检查结果和发现的问题
        """
        problems = []  # 存储发现的问题
        
        # 检查 API 密钥是否设置
        if not cls.OPENAI_API_KEY:
            problems.append("请设置 OPENAI_API_KEY 环境变量")
        
        # 检查数据集目录是否存在
        if not os.path.exists(cls.DEFAULT_DATASET_PATH):
            problems.append(f"数据集目录不存在: {cls.DEFAULT_DATASET_PATH}")
        
        # 返回检查结果
        return {
            "valid": len(problems) == 0,  # 没有问题就是有效的
            "issues": problems
        }
    
    @classmethod
    def get_summary(cls) -> str:
        """
        获取配置摘要信息
        方便调试和检查设置是否正确
        """
        return f"""
配置摘要:
- API 密钥: {'已设置' if cls.OPENAI_API_KEY else '未设置'}
- 工作目录: {cls.DEFAULT_WORK_DIR}
- 数据集路径: {cls.DEFAULT_DATASET_PATH}
- 输出目录: {cls.DEFAULT_OUTPUT_DIR}
- 最大重试次数: {cls.MAX_ITERATIONS}
- 执行超时: {cls.EXECUTION_TIMEOUT}秒
        """.strip()