"""
基于AutoKaggle框架设计的多代理系统，用于自动解析和处理Kaggle竞赛

这个文件包含了多代理系统的核心类：
- CodeAgent: 负责生成Python代码
- PlanAgent: 负责制定计划和策略
- ActionAgent: 负责执行代码
- KaggleMultiAgent: 主控制器，协调各个代理
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from openai import OpenAI


# ========== 数据结构定义 ==========

class Phase(Enum):
    """
    数据科学流程的四个关键阶段
    每个阶段都有特定的目标和任务
    """
    BACKGROUND_UNDERSTANDING = "background_understanding"  # 背景理解
    EDA = "eda"                                           # 探索性数据分析
    FEATURE_ENGINEERING = "feature_engineering"           # 特征工程
    MODEL_BUILDING = "model_building"                     # 模型构建

@dataclass
class KaggleCompetition:
    """
    Kaggle竞赛信息结构
    存储竞赛的基本信息和文件路径
    """
    name: str                    # 竞赛名称
    goal: str                    # 竞赛目标
    evaluation: str              # 评估方式
    submission_format: str       # 提交格式
    metadata: Dict[str, str]     # 元数据信息
    train_path: str             # 训练数据路径
    test_path: str              # 测试数据路径
    sample_submission_path: str  # 示例提交文件路径

@dataclass
class ExecutionResult:
    """
    代码执行结果
    包含执行状态和输出信息
    """
    success: bool                # 是否执行成功
    output: str                 # 标准输出内容
    error: str                  # 错误信息
    variables: Dict[str, Any]   # 执行后的变量（暂不使用）


# ========== 工具函数 ==========

class FileManager:
    """
    文件管理工具类
    负责处理所有文件读写操作，让主要逻辑更清晰
    """
    
    @staticmethod
    def read_text_file(file_path: str) -> str:
        """
        读取文本文件内容
        参数: file_path - 文件路径
        返回: 文件内容字符串
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"读取文件失败: {str(e)}"
    
    @staticmethod
    def write_text_file(file_path: str, content: str) -> bool:
        """
        写入文本文件
        参数: 
            file_path - 文件路径
            content - 要写入的内容
        返回: 是否写入成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            return False
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """检查文件是否存在"""
        return os.path.exists(file_path)
    
    @staticmethod
    def get_cached_content(file_path: str) -> Optional[str]:
        """
        获取缓存文件内容（如果存在）
        返回: 文件内容或None
        """
        if FileManager.file_exists(file_path):
            return FileManager.read_text_file(file_path)
        return None


# ========== 代理类 ==========

class CodeAgent:
    """
    代码代理 - 负责生成Python代码
    
    这个代理的主要职责：
    1. 根据计划生成对应阶段的Python代码
    2. 根据执行结果优化和修复代码
    3. 处理与AI模型的交互
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        初始化代码代理
        参数:
            api_key - OpenAI API密钥
            model - 使用的AI模型名称
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def review_and_refine(self, code: str, code_output: str) -> str:
        """
        检查和改进代码
        当代码执行失败时，根据错误信息修复代码
        """
        prompt = f"""
        你是一个Python开发专家，请根据以下代码和执行结果，进行代码修复：
        # 代码:
        {code}
        # 执行结果:
        {code_output}

        请直接输出完整代码，不要输出任何解释。
        
        """
        return self._call_llm(prompt)

    def generate_code(self, phase: Phase, plan: str, context: Dict[str, Any]) -> str:
        """
        基于计划生成Python代码
        
        参数:
            phase - 当前阶段
            plan - 计划内容
            context - 上下文信息
        返回: 生成的Python代码
        """
        if phase == Phase.BACKGROUND_UNDERSTANDING:
            return "pass"  # 背景理解阶段不生成代码

        # 根据不同阶段调用对应的代码生成方法
        code_generators = {
            Phase.EDA: self._generate_eda_code,
            Phase.FEATURE_ENGINEERING: self._generate_feature_engineering_code,
            Phase.MODEL_BUILDING: self._generate_model_building_code
        }
        
        generator = code_generators.get(phase)
        if generator:
            return generator(plan, context)
        else:
            return "pass"  # 未知阶段返回空代码

    def _generate_eda_code(self, plan: str, context: Dict[str, Any]) -> str:
        """为EDA阶段生成代码（保持原有prompt不变）"""
        prompt = f"""
        基于以下计划为EDA(探索性数据分析)阶段生成Python代码：
        
        #计划: 
        {json.dumps(plan, indent=2)}
        
        #上下文: 
        {json.dumps(context, indent=2)}
        
        # 环境要求：
        1. 生成完整可执行的3.11 Python代码，除了python原生package外，python package是
            - pandas ==2.2.3
            - numpy ==2.1.3
            - scikit-learn == 1.6.1
            - xgboost == 3.0.0
        
        # 代码风格要求
        1. 包含必要的导入语句
        2. 添加详细注释说明
        3. 处理可能的异常情况
        4. 确保代码质量和性能

        # 逻辑要求
        1. 不要使用matplotlib或者seaborn生成任何图表
        2. 不要输出到文件
        3. logging输出时不要缩写，因为后续要用logging向后传递context
        
        # 输出结果
        只返回python代码
        """
        return self._extract_code_from_response(self._call_llm(prompt))

    def _generate_feature_engineering_code(self, plan: str, context: Dict[str, Any]) -> str:
        """为特征工程阶段生成代码（保持原有prompt不变）"""
        prompt = f"""
        基于以下计划为特征工程(Feature Engineering)阶段生成Python代码：
        
        #计划: 
        {json.dumps(plan, indent=2)}
        
        #上下文: 
        {json.dumps(context, indent=2)}
        
        # 环境要求：
        1. 生成完整可执行的3.11 Python代码，除了python原生package外，python package是
            - pandas ==2.2.3
            - numpy ==2.1.3
            - scikit-learn == 1.6.1
            - xgboost == 3.0.0
        
        # 代码风格要求
        1. 包含必要的导入语句
        2. 添加详细注释说明
        3. 处理可能的异常情况
        4. 确保代码质量和性能

        # 业务逻辑要求
        1. 将处理过的train/test数据保存为feature_train.csv和feature_test.csv
        2. 输出文件需要使用配置中指定的output_dir，而不是存在根目录中
        
        # 输出结果
        只返回python代码
        """
        return self._extract_code_from_response(self._call_llm(prompt))

    def _generate_model_building_code(self, plan: str, context: Dict[str, Any]) -> str:
        """为模型构建阶段生成代码（保持原有prompt不变）"""
        prompt = f"""
        基于以下计划为模型构建(Model Building)阶段生成Python代码：
        
        #计划: 
        {json.dumps(plan, indent=2)}
        
        #上下文: 
        {json.dumps(context, indent=2)}
        
        # 环境要求：
        1. 生成完整可执行的3.11 Python代码，除了python原生package外，python package是
            - pandas ==2.2.3
            - numpy ==2.1.3
            - scikit-learn == 1.6.1
            - xgboost == 3.0.0
        
        # 代码风格要求
        1. 包含必要的导入语句
        2. 添加详细注释说明
        3. 处理可能的异常情况
        4. 确保代码质量和性能

        # 业务逻辑要求
        1. 并行计算度最大到4核， cross validation使用3折
        
        # 输出结果
        只返回python代码
        """
        return self._extract_code_from_response(self._call_llm(prompt))

    def _extract_code_from_response(self, response: str) -> str:
        """
        从AI响应中提取Python代码
        处理可能的markdown格式包装
        """
        if '```python' in response:
            return response.split('```python')[1].split('```')[0].strip()
        else:
            return response.strip()

    def _call_llm(self, prompt: str) -> str:
        """
        调用大语言模型
        处理API调用和错误
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个Python开发专家。"},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            return content if content is not None else "LLM返回内容为空"
        except Exception as e:
            return f"LLM调用失败: {str(e)}"


class PlanAgent:
    """
    计划代理 - 负责分析问题、制定策略、生成代码方案
    
    这个代理的主要职责：
    1. 分析竞赛背景和要求
    2. 为每个阶段制定详细计划
    3. 提供数据科学专业建议
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        初始化计划代理
        参数:
            api_key - OpenAI API密钥
            model - 使用的AI模型名称
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        
    def generate_phase_plan(self, phase: Phase, context: Dict[str, Any]) -> str:
        """
        为特定阶段生成详细计划
        
        参数:
            phase - 当前阶段
            context - 上下文信息
        返回: 计划内容
        """
        # 根据阶段选择对应的prompt生成器
        prompt_generators = {
            Phase.BACKGROUND_UNDERSTANDING: self._get_background_prompt,
            Phase.EDA: self._get_eda_prompt,
            Phase.FEATURE_ENGINEERING: self._get_feature_engineering_prompt,
            Phase.MODEL_BUILDING: self._get_model_building_prompt
        }
        
        prompt_generator = prompt_generators.get(phase)
        if prompt_generator:
            prompt = prompt_generator(context)
            return self._call_llm(prompt)
        else:
            return f"未知阶段: {phase.value}"
    
    def _get_background_prompt(self, context: Dict[str, Any]) -> str:
        """生成背景理解阶段的prompt（保持原有prompt不变）"""
        prompt = f"""
        作为数据科学专家，请分析以下Kaggle竞赛信息：
        {json.dumps(context, indent=2)}

        请提供：
        1. 目标变量
        2. 问题类型分析（分类/回归/时间序列等）和评估标准
        3. 关键特征识别
        4. 可能的挑战和注意事项
        5. 建议的建模策略
        """
        return prompt
    
    def _get_eda_prompt(self, context: Dict[str, Any]) -> str:
        """生成EDA阶段的prompt（保持原有prompt不变）"""
        return f"""
        你在这一步的目标是做探索性数据分析（exploratory data analysis， EDA）。请为为EDA生成分析计划：
        {json.dumps(context, indent=2)}

        # 要求
        - 在这一步的代码中，不要使用任何图表信息。
        
        # 输出格式是：
        ## 相关性分析
        ## 特征分布分析
        ## 与目标变量关系分析
        """
    
    def _get_feature_engineering_prompt(self, context: Dict[str, Any]) -> str:
        """生成特征工程阶段的prompt（保持原有prompt不变）"""
        return f"""
        基于EDA结果生成特征工程计划：
        {json.dumps(context, indent=2)}

        # 要求
        - 要观察之前EDA阶段的结果来生成相对应的特征工程
        - string类字段都需要进行one-hot编码
        - 不要创建polynomial特征
        
        # 输出格式是
        ## 新特征创建策略
        ## 特征选择方法
        ## 特征缩放需求
        """
    
    def _get_model_building_prompt(self, context: Dict[str, Any]) -> str:
        """生成模型构建阶段的prompt（保持原有prompt不变）"""
        return f"""
        生成模型构建和验证计划：
        {json.dumps(context, indent=2)}

        # 要求：
        - 请使用random forest来构建分类器
        - 使用feature_train.csv和feature_test.csv进行模型训练和预测，不要使用原始的train/test数据
        
        # 输出格式是
        ## 模型选择策略
        ## 验证策略
        ## 超参数调优方法
        """
    
    def _call_llm(self, prompt: str) -> str:
        """
        调用大语言模型
        处理API调用和错误
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的数据科学家。"},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            return content if content is not None else "LLM返回内容为空"
        except Exception as e:
            return f"LLM调用失败: {str(e)}"


class ActionAgent:
    """
    执行代理 - 负责执行Python代码并汇报结果
    
    这个代理的主要职责：
    1. 执行生成的Python代码文件
    2. 捕获执行结果和错误信息
    3. 记录执行历史
    """
    
    def __init__(self, work_dir: str, timeout: int):
        """
        初始化执行代理
        参数:
            work_dir - 工作目录
            timeout - 执行超时时间（秒）
        """
        self.work_dir = work_dir
        self.timeout = timeout
        self.execution_history = []  # 执行历史记录
        
    def execute_python_file(self, file_path: str, phase: Phase) -> ExecutionResult:
        """
        执行Python文件
        首先尝试使用poetry run，失败则使用直接python执行
        
        参数:
            file_path - Python文件路径
            phase - 当前执行阶段
        返回: 执行结果
        """
        print(f"    ⚡ 开始执行Python文件: {file_path}")
        
        # 转换为绝对路径
        if not os.path.isabs(file_path):
            abs_file_path = os.path.abspath(file_path)
        else:
            abs_file_path = file_path
        
        # 首先尝试使用poetry run执行
        result = self._run_with_poetry(abs_file_path)
        
        # 如果poetry执行失败，尝试直接使用python执行
        if not result.success and "找不到poetry命令" in result.error:
            print(f"    🔄 Poetry执行失败，尝试直接Python执行...")
            result = self._run_with_python(abs_file_path)
        
        # 记录执行历史
        self._record_execution(phase, result, file_path)
        
        return result
    
    def _run_with_poetry(self, file_path: str) -> ExecutionResult:
        """使用poetry run执行Python文件"""
        try:
            result = subprocess.run(
                ["poetry", "run", "python", file_path],
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            return self._create_execution_result(result)
        except subprocess.TimeoutExpired:
            return ExecutionResult(False, "", "执行超时", {})
        except FileNotFoundError:
            return ExecutionResult(False, "", "找不到poetry命令，请确保已安装poetry", {})
        except Exception as e:
            return ExecutionResult(False, "", f"Poetry执行失败: {str(e)}", {})
    
    def _run_with_python(self, file_path: str) -> ExecutionResult:
        """直接使用python执行文件"""
        try:
            result = subprocess.run(
                [sys.executable, file_path],
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            return self._create_execution_result(result)
        except subprocess.TimeoutExpired:
            return ExecutionResult(False, "", "执行超时", {})
        except Exception as e:
            return ExecutionResult(False, "", f"Python执行失败: {str(e)}", {})
    
    def _create_execution_result(self, subprocess_result) -> ExecutionResult:
        """
        根据subprocess结果创建ExecutionResult对象
        """
        if subprocess_result.returncode == 0:
            return ExecutionResult(
                success=True,
                output=subprocess_result.stdout,
                error=subprocess_result.stderr if subprocess_result.stderr else "",
                variables={}
            )
        else:
            return ExecutionResult(
                success=False,
                output=subprocess_result.stdout,
                error=subprocess_result.stderr,
                variables={}
            )
    
    def _record_execution(self, phase: Phase, result: ExecutionResult, file_path: str):
        """记录执行历史"""
        self.execution_history.append({
            "phase": phase.value,
            "timestamp": datetime.now().isoformat(),
            "result": result,
            "file_path": file_path
        })


class KaggleMultiAgent:
    """
    Kaggle多代理系统主控制器
    
    这是系统的核心类，负责：
    1. 协调各个代理的工作
    2. 管理执行流程
    3. 处理竞赛数据加载
    4. 生成最终报告
    """
    
    def __init__(self, api_key: str, work_dir: str, output_dir: str, timeout: int, plan_agent_model: str, code_agent_model: str):
        """
        初始化多代理系统
        
        参数:
            api_key - OpenAI API密钥
            work_dir - 工作目录
            output_dir - 输出目录
            timeout - 执行超时时间
        """
        self.plan_agent = PlanAgent(api_key, model=plan_agent_model)
        self.code_agent = CodeAgent(api_key, model=code_agent_model)
        self.action_agent = ActionAgent(work_dir, timeout)
        self.work_dir = work_dir
        self.output_dir = output_dir
        self.context = {}
        self.phase_results = {}
        
    def load_competition(self, dataset_path: str) -> KaggleCompetition:
        """
        加载Kaggle竞赛数据
        从desc.md文件解析竞赛信息
        
        参数: dataset_path - 数据集路径
        返回: KaggleCompetition对象
        """
        desc_path = os.path.join(dataset_path, "desc.md")
        content = FileManager.read_text_file(desc_path)
        
        # 解析描述文件内容
        goal, evaluation, submission_format, metadata = self._parse_competition_desc(content)
        
        return KaggleCompetition(
            name=os.path.basename(dataset_path),
            goal=goal.strip(),
            evaluation=evaluation.strip(),
            submission_format=submission_format.strip(),
            metadata=metadata,
            train_path=os.path.join(dataset_path, "train.csv"),
            test_path=os.path.join(dataset_path, "test.csv"),
            sample_submission_path=os.path.join(dataset_path, "sample_submission.csv")
        )
    
    def _parse_competition_desc(self, content: str) -> Tuple[str, str, str, Dict[str, str]]:
        """
        解析竞赛描述文件
        提取目标、评估方式、提交格式和元数据
        """
        lines = content.split('\n')
        goal = ""
        evaluation = ""
        submission_format = ""
        metadata = {}
        
        current_section = None
        for line in lines:
            line = line.strip()
            if line.startswith('# Goal'):
                current_section = 'goal'
            elif line.startswith('# Evaluation'):
                current_section = 'evaluation'
            elif line.startswith('# Submission File'):
                current_section = 'submission'
            elif line.startswith('# Metadata'):
                current_section = 'metadata'
            elif line and not line.startswith('#'):
                if current_section == 'goal':
                    goal += line + " "
                elif current_section == 'evaluation':
                    evaluation += line + " "
                elif current_section == 'submission':
                    submission_format += line + " "
                elif current_section == 'metadata' and ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        
        return goal, evaluation, submission_format, metadata
    
    def run_competition(self, dataset_path: str, max_iterations: int = 3) -> Dict[str, Any]:
        """
        运行完整的竞赛解决流程
        
        参数:
            dataset_path - 数据集路径
            max_iterations - 每个阶段最大重试次数
        返回: 各阶段执行结果
        """
        # 加载竞赛信息
        competition = self.load_competition(dataset_path)
        print(f"🏆 开始处理竞赛: {competition.name}")
        
        # 初始化上下文
        self.context = {
            "competition": competition.__dict__,
            "dataset_path": dataset_path,
            "work_dir": self.work_dir,
            "output_dir": self.output_dir
        }
        
        # 按阶段执行
        phases = list(Phase)
        for phase in phases:
            print(f"\n📋 开始阶段: {phase.value}")
            success = self._execute_phase(phase, max_iterations)
            
            if not success:
                print(f"❌ 阶段 {phase.value} 执行失败")
                break
            else:
                print(f"✅ 阶段 {phase.value} 执行成功")
        
        return self.phase_results
    
    def _execute_phase(self, phase: Phase, max_iterations: int) -> bool:
        """
        执行单个阶段
        包含计划生成、代码生成、代码执行、错误修复的完整流程
        """
        # 设置文件路径
        plan_file = os.path.join(self.output_dir, f"{phase.value}_plan.md")
        code_file = os.path.join(self.output_dir, f"{phase.value}_code.py")
        result_file = os.path.join(self.output_dir, f"{phase.value}_result.md")
        
        for iteration in range(max_iterations):
            print(f"  🔄 迭代 {iteration + 1}/{max_iterations}")
            
            # 步骤1: 生成或加载计划
            plan = self._get_or_generate_plan(phase, plan_file)
            print(f"    📝 计划准备完成")
            
            # 步骤2: 生成或加载代码
            code = self._get_or_generate_code(phase, plan, code_file)
            print(f"    💻 代码准备完成")
            
            # 步骤3: 执行代码
            result = self.action_agent.execute_python_file(code_file, phase)
            
            # 步骤4: 保存执行结果
            self._save_execution_result(result, result_file)
            print(f"    ⚡ 代码执行{'成功' if result.success else '失败'}")
            
            if result.success:
                # 执行成功，保存阶段结果并更新上下文
                self.phase_results[phase.value] = {
                    "plan": plan,
                    "code": code,
                    "result": result.__dict__,
                    "iteration": iteration + 1
                }
                self.context[phase.value] = self.phase_results[phase.value]
                return True
            
            # 执行失败，尝试优化代码（如果还有重试机会）
            if iteration < max_iterations - 1:
                print(f"    🔧 开始代码优化...")
                optimized_code = self.code_agent.review_and_refine(code, result.output)
                FileManager.write_text_file(code_file, optimized_code)
                print(f"    🔧 代码优化完成")
        
        return False
    
    def _get_or_generate_plan(self, phase: Phase, plan_file: str) -> str:
        """获取缓存的计划或生成新计划"""
        cached_plan = FileManager.get_cached_content(plan_file)
        if cached_plan:
            return cached_plan
        
        # 生成新计划
        plan = self.plan_agent.generate_phase_plan(phase, self.context)
        FileManager.write_text_file(plan_file, plan)
        return plan
    
    def _get_or_generate_code(self, phase: Phase, plan: str, code_file: str) -> str:
        """获取缓存的代码或生成新代码"""
        cached_code = FileManager.get_cached_content(code_file)
        if cached_code:
            return cached_code
        
        # 生成新代码
        code = self.code_agent.generate_code(phase, plan, self.context)
        FileManager.write_text_file(code_file, code)
        return code
    
    def _save_execution_result(self, result: ExecutionResult, result_file: str):
        """保存执行结果到文件"""
        result_content = f"""# 执行结果

**成功**: {result.success}

**输出**:
```
{result.output}
```

"""
        if result.error:
            result_content += f"""**错误**:
```
{result.error}
```

"""
        FileManager.write_text_file(result_file, result_content)
    
    def generate_report(self) -> str:
        """
        生成详细的执行报告
        总结整个执行过程和结果
        """
        report = f"""
# Kaggle竞赛自动化执行报告

## 竞赛信息
- 名称: {self.context['competition']['name']}
- 目标: {self.context['competition']['goal']}
- 评估: {self.context['competition']['evaluation']}

## 执行阶段总结
"""
        
        for phase_name, phase_result in self.phase_results.items():
            report += f"""
### {phase_name}
- 执行迭代: {phase_result['iteration']}
- 状态: {'✅ 成功' if phase_result['result']['success'] else '❌ 失败'}
"""
        
        report += f"""
## 最终输出
- 执行历史: {len(self.action_agent.execution_history)} 次代码执行
- 成功阶段: {len(self.phase_results)}/{len(list(Phase))}
"""
        
        return report