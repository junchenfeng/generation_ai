# Prompt 对比：从统一模式到分阶段模式

## 原始 generate_code 的统一 Prompt

```python
prompt = f"""
基于以下计划为{phase.value}阶段生成Python代码：

#计划: 
{json.dumps(plan, indent=2)}

#上下文: 
{json.dumps(serializable_context, indent=2)}

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

# 输出结果
只返回python代码
"""
```

## 新的分阶段 Prompts

### 1. EDA 阶段专用 Prompt

```python
def _generate_eda_code(self, plan: Dict[str, Any], context: Dict[str, Any]) -> str:
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
    
    # 输出结果
    只返回python代码
    """
```

### 2. 特征工程阶段专用 Prompt

```python
def _generate_feature_engineering_code(self, plan: Dict[str, Any], context: Dict[str, Any]) -> str:
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
    7. 专注于特征创建、转换和选择
    8. 处理缺失值、异常值和数据预处理
    9. 进行特征缩放和编码
    
    # 输出结果
    只返回python代码
    """
```

### 3. 模型构建阶段专用 Prompt

```python
def _generate_model_building_code(self, plan: Dict[str, Any], context: Dict[str, Any]) -> str:
    prompt = f"""
    基于以下计划为模型构建(Model Building)阶段生成Python代码：
    
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
    7. 专注于模型训练、验证和评估
    8. 实现交叉验证和超参数调优
    9. 生成最终的预测结果和提交文件
    
    # 输出结果
    只返回python代码
    """
```

## 主要改进点

### 1. 架构变化
- **之前**: 一个 `generate_code` 方法处理所有阶段
- **现在**: 分阶段的方法架构，每个阶段有专门的代码生成器

```python
# 新的分发机制
phase_code_generators = {
    Phase.EDA: self._generate_eda_code,
    Phase.FEATURE_ENGINEERING: self._generate_feature_engineering_code,
    Phase.MODEL_BUILDING: self._generate_model_building_code
}
```

### 2. 专业化提示词
- **EDA阶段**: 专注于数据探索、统计分析、数据质量报告
- **特征工程阶段**: 专注于特征创建、转换、预处理、缺失值处理
- **模型构建阶段**: 专注于模型训练、验证、超参数调优、预测生成

### 3. 新增功能
- 添加了 `review_and_refine` 方法用于代码优化
- 更好的错误处理和代码质量保证
- 阶段特定的指导原则

### 4. 优势
1. **精确性**: 每个阶段的prompt更精确，更符合阶段特点
2. **可维护性**: 易于单独调整和优化每个阶段的prompt
3. **扩展性**: 容易添加新的阶段或修改现有阶段
4. **专业性**: 每个阶段都有特定的技术重点和输出要求

## 使用示例

```python
# 使用新的分阶段代码生成
code_agent = CodeAgent(api_key=api_key)

# EDA阶段
eda_code = code_agent.generate_code(Phase.EDA, plan, context)

# 特征工程阶段
fe_code = code_agent.generate_code(Phase.FEATURE_ENGINEERING, plan, context)

# 模型构建阶段
model_code = code_agent.generate_code(Phase.MODEL_BUILDING, plan, context)
``` 