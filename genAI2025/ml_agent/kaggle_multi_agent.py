"""
AutoKaggle: Multi-Agent Framework for Autonomous Data Science Competitions
基于AutoKaggle框架设计的多代理系统，用于自动解析和处理Kaggle竞赛
"""

import os
import json

from datetime import datetime
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum
from openai import OpenAI


class Phase(Enum):
    """数据科学流程的六个关键阶段"""
    BACKGROUND_UNDERSTANDING = "background_understanding"
    EDA = "eda" 
    FEATURE_ENGINEERING = "feature_engineering"
    MODEL_BUILDING = "model_building"

@dataclass
class KaggleCompetition:
    """Kaggle竞赛信息结构"""
    name: str
    goal: str
    evaluation: str
    submission_format: str
    metadata: Dict[str, str]
    train_path: str
    test_path: str
    sample_submission_path: str

@dataclass
class ExecutionResult:
    """代码执行结果"""
    success: bool
    output: str
    error: str
    variables: Dict[str, Any]


class CodeAgent:
    """代码代理 - 负责生成Python代码"""
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.conversation_history = []

    def review_and_refine(self, code: str, code_output: str) -> str:
        """review and refine the code"""
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
        """基于计划生成Python代码 - 使用分阶段的prompt"""

        if phase == Phase.BACKGROUND_UNDERSTANDING:
            return "pass"  # 背景理解阶段不生成代码

        # 使用分阶段的prompt方法
        phase_code_generators = {
            Phase.EDA: self._generate_eda_code,
            Phase.FEATURE_ENGINEERING: self._generate_feature_engineering_code,
            Phase.MODEL_BUILDING: self._generate_model_building_code
        }
        
        # 创建可序列化的上下文副本
        
        code_generator = phase_code_generators.get(phase)
        if code_generator:
            return code_generator(plan, context)
        else:
            return "pass"  # 未知阶段返回空代码

    def _generate_eda_code(self, plan: Dict[str, Any], context: Dict[str, Any]) -> str:
        """为EDA阶段生成代码"""
        prompt = f"""
        基于以下计划为EDA(探索性数据分析)阶段生成Python代码：
        
        #计划: 
        {json.dumps(plan, indent=2)}
        
        #上下文: 
        {json.dumps(context, indent=2)}
        
        # 要求：
        1. 生成完整可执行的3.11 Python代码，除了python原生package外，python package是
            - pandas
            - numpy
            - scikit-learn
            - xgboost
            - tensorflow
        2. 包含必要的导入语句
        3. 添加详细注释说明
        4. 处理可能的异常情况
        5. 确保代码质量和性能
        6. 不要使用matplotlib或者seaborn生成任何图表
        7. 专注于数据探索和统计分析
        8. 生成数据质量报告和特征统计信息
        9. 不要输出到文件
        10. logging输出时不要缩写，因为后续要用logging向后传递context
        
        # 输出结果
        只返回python代码
        """
        
        resp = self._call_llm(prompt)
        if '```python' in resp:
            return resp.split('```python')[1].split('```')[0].strip()
        else:
            return resp.strip()

    def _generate_feature_engineering_code(self, plan:str, context: Dict[str, Any]) -> str:
        """为特征工程阶段生成代码"""
        prompt = f"""
        基于以下计划为特征工程(Feature Engineering)阶段生成Python代码：
        
        #计划: 
        {json.dumps(plan, indent=2)}
        
        #上下文: 
        {json.dumps(context, indent=2)}
        
        # 要求：
        1. 生成完整可执行的3.11 Python代码，除了python原生package外，python package是
            - pandas
            - numpy
            - scikit-learn
            - xgboost
            - tensorflow
        2. 包含必要的导入语句
        3. 添加详细注释说明
        4. 处理可能的异常情况
        5. 确保代码质量和性能
        6. 不要使用matplotlib或者seaborn生成任何图表
        7. 将处理过的train/test数据保存为feature_train.csv和feature_test.csv
        
        # 输出结果
        只返回python代码
        """
        
        resp = self._call_llm(prompt)
        if '```python' in resp:
            return resp.split('```python')[1].split('```')[0].strip()
        else:
            return resp.strip()

    def _generate_model_building_code(self, plan: str, context: Dict[str, Any]) -> str:
        """为模型构建阶段生成代码"""
        prompt = f"""
        基于以下计划为模型构建(Model Building)阶段生成Python代码：
        
        #计划: 
        {json.dumps(plan, indent=2)}
        
        #上下文: 
        {json.dumps(context, indent=2)}
        
        # 要求：
        1. 生成完整可执行的3.11 Python代码，除了python原生package外，python package是
            - pandas ==2.2.3
            - numpy ==2.1.3
            - scikit-learn == 1.6.1
            - xgboost == 3.0.0
        2. 包含必要的导入语句
        3. 添加详细注释说明
        4. 处理可能的异常情况
        5. 并行计算度最大到4核， cross validation使用3折
        
        # 输出结果
        只返回python代码
        """
        
        resp = self._call_llm(prompt)
        if '```python' in resp:
            return resp.split('```python')[1].split('```')[0].strip()
        else:
            return resp.strip()

    def _call_llm(self, prompt: str) -> str:
        """调用大语言模型"""
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
    """计划代理 - 负责分析问题、制定策略、生成代码方案"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.conversation_history = []
        
    
    def generate_phase_plan(self, phase: Phase, context: Dict[str, Any]) -> str:
        """为特定阶段生成详细计划"""
        phase_prompts = {
            Phase.BACKGROUND_UNDERSTANDING: self._get_background_prompt,
            Phase.EDA: self._get_eda_prompt,
            Phase.FEATURE_ENGINEERING: self._get_feature_engineering_prompt,
            Phase.MODEL_BUILDING: self._get_model_building_prompt
        }
        
        # 创建可序列化的上下文副本
        prompt = phase_prompts[phase](context)
        return self._call_llm(prompt)
    
    def _call_llm(self, prompt: str) -> str:
        """调用大语言模型"""
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
    
    def _get_background_prompt(self, context: Dict[str, Any]) -> str:
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
        
        response = self._call_llm(prompt)
        return response
    
    def _get_eda_prompt(self, context: Dict[str, Any]) -> str:
        return f"""
        你在这一步的目标是做探索性数据分析（exploratory data analysis， EDA）。请为为EDA生成分析计划：
        {json.dumps(context, indent=2)}

        在这一步的代码中，不要使用任何图表信息。
        
        # 输出格式是：
        ## 相关性分析
        ## 特征分布分析
        ## 与目标变量关系分析
        """
    
    def _get_feature_engineering_prompt(self, context: Dict[str, Any]) -> str:
        return f"""
        基于EDA结果生成特征工程计划：
        {json.dumps(context, indent=2)}

        # 要求
        - string类字段都需要进行one-hot编码
        - 不要创建polynomial特征
        
        # 输出格式是
        ## 新特征创建策略
        ## 特征选择方法
        ## 特征缩放需求
        """
    
    def _get_model_building_prompt(self, context: Dict[str, Any]) -> str:
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
    

class ActionAgent:
    """执行代理 - 负责执行Python代码并汇报结果"""
    
    def __init__(self, work_dir: str, timeout:int):
        self.work_dir: str = work_dir
        self.timeout: int = timeout
        self.execution_history = []
        
    
    def execute_python_file(self, file_path: str, phase: Phase) -> ExecutionResult:
        """使用subprocess执行Python文件"""
        import subprocess
        import sys
        
        try:
            # 转换为绝对路径避免路径重复问题
            if not os.path.isabs(file_path):
                abs_file_path = os.path.abspath(file_path)
            else:
                abs_file_path = file_path
                
            # 使用项目根目录作为工作目录
            
            # 使用poetry run执行Python文件
            result = subprocess.run(
                ["poetry", "run", "python", abs_file_path],
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout  # 5分钟超时
            )
            
            if result.returncode == 0:
                execution_result = ExecutionResult(
                    success=True,
                    output=result.stdout,
                    error=result.stderr if result.stderr else "",
                    variables={}  # subprocess无法直接返回变量
                )
            else:
                execution_result = ExecutionResult(
                    success=False,
                    output=result.stdout,
                    error=result.stderr,
                    variables={}
                )
                
        except subprocess.TimeoutExpired:
            execution_result = ExecutionResult(
                success=False,
                output="",
                error="执行超时（超过5分钟）",
                variables={}
            )
        except FileNotFoundError:
            execution_result = ExecutionResult(
                success=False,
                output="",
                error="找不到poetry命令，请确保已安装poetry或使用直接Python执行",
                variables={}
            )
        except Exception as e:
            execution_result = ExecutionResult(
                success=False,
                output="",
                error=f"执行失败: {str(e)}",
                variables={}
            )
        
        # 记录执行历史
        self.execution_history.append({
            "phase": phase.value,
            "timestamp": datetime.now().isoformat(),
            "result": execution_result,
            "file_path": file_path
        })
        
        return execution_result
    
    def execute_python_file_direct(self, file_path: str, phase: Phase) -> ExecutionResult:
        """直接使用python执行文件（不使用poetry）"""
        import subprocess
        import sys
        
        try:
            # 转换为绝对路径避免路径重复问题
            if not os.path.isabs(file_path):
                abs_file_path = os.path.abspath(file_path)
            else:
                abs_file_path = file_path
                            
            # 直接使用python执行
            result = subprocess.run(
                [sys.executable, abs_file_path],
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result.returncode == 0:
                execution_result = ExecutionResult(
                    success=True,
                    output=result.stdout,
                    error=result.stderr if result.stderr else "",
                    variables={}
                )
            else:
                execution_result = ExecutionResult(
                    success=False,
                    output=result.stdout,
                    error=result.stderr,
                    variables={}
                )
                
        except subprocess.TimeoutExpired:
            execution_result = ExecutionResult(
                success=False,
                output="",
                error="执行超时",
                variables={}
            )
        except Exception as e:
            execution_result = ExecutionResult(
                success=False,
                output="",
                error=f"执行失败: {str(e)}",
                variables={}
            )
        
        # 记录执行历史
        self.execution_history.append({
            "phase": phase.value,
            "timestamp": datetime.now().isoformat(),
            "result": execution_result,
            "file_path": file_path
        })
        
        return execution_result

class KaggleMultiAgent:
    """Kaggle多代理系统主控制器"""
    
    def __init__(self, api_key: str, work_dir: str, output_dir: str, timeout:int):
        self.plan_agent = PlanAgent(api_key, model='o3-mini')
        self.action_agent = ActionAgent(work_dir, timeout)
        self.code_agent = CodeAgent(api_key, model='o4-mini')
        self.work_dir = work_dir  # 执行代码的工作目录，缓存poetry文件信息等
        self.output_dir = output_dir # 中间信息的输出
        self.context = {}
        self.phase_results = {}
        
    def load_competition(self, dataset_path: str) -> KaggleCompetition:
        """加载Kaggle竞赛数据"""
        desc_path = os.path.join(dataset_path, "desc.md")
        
        # 解析描述文件
        with open(desc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 简单解析（可以优化为更robust的解析器）
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
    
    def run_competition(self, dataset_path: str, max_iterations: int = 3) -> Dict[str, Any]:
        """运行完整的竞赛解决流程"""
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
        """执行单个阶段"""
        for iteration in range(max_iterations):
            print(f"  🔄 迭代 {iteration + 1}/{max_iterations}")
            
            # 增加中间记录
            plan_cache_path = os.path.join(self.output_dir, f"{phase.value}_plan.md")
            code_cache_path = os.path.join(self.output_dir, f"{phase.value}_code.py")
            result_cache_path = os.path.join(self.output_dir, f"{phase.value}_result.md")

            # 1. 生成计划 ｜ 计划只生成一次，进行缓存
            if not os.path.exists(plan_cache_path):
                plan = self.plan_agent.generate_phase_plan(phase, self.context)
                with open(plan_cache_path, 'w', encoding='utf-8') as f:
                    f.write(plan)
            else:
                with open(plan_cache_path, 'r', encoding='utf-8') as f:
                    plan = f.read()
                    
            print(f"    📝 计划生成完成")
            
            # 2. 生成代码
            if not os.path.exists(code_cache_path):
                code: str = self.code_agent.generate_code(phase, plan, self.context)
                with open(code_cache_path, 'w', encoding='utf-8') as f:
                    f.write(code)
            else:
                with open(code_cache_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                    
            print(f"    💻 代码生成完成")
            
            # 3. 执行代码 - 使用文件执行方式
            print(f"    ⚡ 开始执行Python文件: {code_cache_path}")
            
            # 尝试使用poetry run执行，如果失败则使用直接Python执行
            result = self.action_agent.execute_python_file(code_cache_path, phase)
            
            if not result.success and "找不到poetry命令" in result.error:
                print(f"    🔄 Poetry执行失败，尝试直接Python执行...")
                result = self.action_agent.execute_python_file_direct(code_cache_path, phase)
            
            # 保存执行结果
            with open(result_cache_path, 'w', encoding='utf-8') as f:
                f.write(f"# 执行结果\n\n")
                f.write(f"**成功**: {result.success}\n\n")
                f.write(f"**输出**:\n```\n{result.output}\n```\n\n")
                if result.error:
                    f.write(f"**错误**:\n```\n{result.error}\n```\n\n")
            
            print(f"    ⚡ 代码执行{'成功' if result.success else '失败'}")
            
            if result.success:
                
                # 保存阶段结果
                self.phase_results[phase.value] = {
                    "plan": plan,
                    "code": code,
                    "result": result.__dict__,
                    "iteration": iteration + 1
                }
                
                # 更新上下文（只保留可序列化的变量）
                self.context[phase.value] = self.phase_results[phase.value]
                
                return True
            
            # 5. 代码优化 
            if iteration < max_iterations - 1:
                print(f"    🔧 开始代码优化...")
                optimized_code= self.code_agent.review_and_refine(
                    code, result.output
                )
                with open(code_cache_path, 'w', encoding='utf-8') as f:
                    f.write(optimized_code)
                print(f"    🔧 代码优化完成")
                continue
        
        return False
    
    def generate_report(self) -> str:
        """生成详细的执行报告"""
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