"""
环境设置
"""
import json
from openai import OpenAI

import logging
logging.basicConfig(
    level=logging.INFO
)  # 日志汇报级别，DEBUG/INFO/ERROR。默认INFO。将它换成DEBUG，你会看到很多信息
logger = logging.getLogger(__name__)

# 导入本地工具
from tools import FUNCTION_MAP
from tool_config import TOOL_CONFIG

client = OpenAI()

"""
Helper函数
"""


def handle_function_call(step):
    """处理function call类型的response"""
    # 获取函数名和参数
    function_name = step.name
    function_args = json.loads(step.arguments)

    # 动态调用函数
    if function_name in FUNCTION_MAP:
        result = FUNCTION_MAP[function_name](**function_args)
    else:
        raise Exception(f"Unknown function: {function_name}")
    return result  # 表示需要继续处理


def action_agent_tools_desc() -> str:
    return "\n".join([f"{x['name']}: {x['description']}" for x in TOOL_CONFIG])


"""
plan Agent，负责任务规划和进度监控，一般使用高能力模型
"""

def plan_agent(task: str, memory) -> tuple[bool, str, list]:
    """计划Agent"""

    planner_system_prompt = f"""
你是一个AI生活助理。

你可以得到action agent的帮助。action agent具备以下能力:
{action_agent_tools_desc()}

你得到的第一个输入是任务，后续输入为任务执行状态。请根据任务历史信息，为action agent制定执行计划来完成这一任务。

如果任务成功或者任务失败，都返回is_done为True；如果成功，plan为空；如果失败，plan为失败原因。

请以json输出返回内容
{{'is_done': bool, 'plan': str}}
    """

    task_prompt = f"""
    任务是：{task}
    任务历史信息是：{memory}
    """

    resp = client.responses.create(
        model="o3-mini",
        input=[
            {"role": "system", "content": planner_system_prompt},
            {"role": "user", "content": task_prompt},
        ],  # 传入历史信息
    )

    # 增加记忆
    memory.append({"role": "user", "content": task_prompt})
    memory.append({"role": "assistant", "content": resp.output_text})  # 将执行计划也增加到历史对话中

    # 处理输出结果
    plan = json.loads(resp.output_text)
    return plan["is_done"], plan["plan"], memory

"""
Action Agent，负责执行任务，一般使用低能力模型
"""

def action_agent(plan: str, memory: list) -> list:
    """执行Agent"""
    action_agent_system_prompt = f"""
你是一个AI生活助理。
你将会得到一个执行计划，请根据执行计划，使用工具来完成这一任务。
"""

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {"role": "system", "content": action_agent_system_prompt},
            {"role": "user", "content": plan},
        ],  # 传入历史信息
        tools=TOOL_CONFIG,
    )
    for step in response.output:
        memory.append(step)

        # 处理工具调用
        result = handle_function_call(step)
        memory.append(
            {
                "type": "function_call_output",
                "call_id": step.call_id,
                "output": str(result),
            }
        )
        logger.info(f"call {step.name}, result: {result}")
    return memory


"""
Agent编排，负责指挥多个Agent的协作问题
"""

def agent_runner(task: str):
    """每个步骤做一次计划/执行"""
    memory = []
    max_iterations = 10  # 防止无限循环
    iteration = 0

    while iteration < max_iterations:
        print(f"\n--- 第 {iteration + 1} 轮处理 ---")

        # 计划
        is_done, plan, memory = plan_agent(task, memory)
        logger.info(f"是否继续: {is_done},plan: {plan}")

        # 执行
        if not is_done:
            memory = action_agent(plan, memory)

        # 如果不需要继续处理，跳出循环
        if is_done:
            print("任务完成！")
            break
        iteration += 1

    if iteration >= max_iterations:
        print("达到最大迭代次数，停止处理")


if __name__ == "__main__":
    agent_runner(task="给foo发一下今天天气")
