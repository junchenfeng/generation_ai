"""
配置文件 - 包含多代理系统的各种设置
"""

import os
from typing import Dict, Any

class Config:
    """配置类"""
    
    # OpenAI API 配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    PLAN_AGENT_MODEL = "o3-mini"  # 计划代理模型
    ACTION_AGENT_MODEL = "gpt-4o-mini"  # 执行代理模型
    
    # 执行配置
    MAX_ITERATIONS = 3  # 每个阶段最大迭代次数
    EXECUTION_TIMEOUT = 600  # 代码执行超时时间（秒）
    
    # 目录配置
    DEFAULT_WORK_DIR = os.getcwd()
    DEFAULT_OUTPUT_DIR = "ml_agent/output"
    DEFAULT_DATASET_PATH = "data/kaggle_dataset"
    
    # 日志配置
    LOG_LEVEL = "INFO"
    ENABLE_DETAILED_LOGGING = True
    
    # 代理提示词模板
    SYSTEM_PROMPT = "你是一个专业的数据科学家和Python开发专家，精通机器学习、数据分析和特征工程。"
    
    # 单元测试配置
    ENABLE_UNIT_TESTS = True
    STRICT_TEST_MODE = False  # 是否严格要求所有测试通过
    
    @classmethod
    def validate(cls) -> Dict[str, Any]:
        """验证配置"""
        issues = []
        
        if not cls.OPENAI_API_KEY:
            issues.append("OPENAI_API_KEY未设置")
        
        if not os.path.exists(cls.DEFAULT_DATASET_PATH):
            issues.append(f"默认数据集路径不存在: {cls.DEFAULT_DATASET_PATH}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }