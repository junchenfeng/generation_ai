"""
ReAct Single Agent DEMO
"""


"""
环境设置
"""
import json
from openai import OpenAI

# 工程化代码中一般不用print，使用logging
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
业务逻辑
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


def process_response(response, messages):
    """
    统一处理response的策略函数
    返回True表示需要继续处理，False表示任务完成
    """
    should_continue = True

    for step in response.output:
        messages.append(step)  # NOTE：在同一个命名空间下，在函数里进行append，在外层agent_main里也能看到

        # 策略模式：根据step类型选择处理函数
        if step.type == "function_call":
            # 处理工具调用
            result = handle_function_call(step)
            messages.append(
                {
                    "type": "function_call_output",
                    "call_id": step.call_id,
                    "output": str(result),
                }
            )
            logger.info(
                f"call {step.name}, result: {result}"
            )  # 如果把这里改成logger.debug，你在默认INFO级别下就看不到消息了
        elif step.type == "message":
            # 处理消息。
            logger.info(f"assisstant replies: {step.content[0].text}")
            should_continue = False  # NOTE： 在这里我们默认当assistant reply时，任务就完成了。这是一个很强的假设
        else:
            raise Exception(f"Unknown step type: {step.type}")

    return should_continue


def agent_runner(task):
    """运行Agent"""
    messages = [{"role": "user", "content": task}]

    max_iterations = 10  # 防止无限循环
    iteration = 0

    while iteration < max_iterations:
        print(f"\n--- 第 {iteration + 1} 轮处理 ---")

        # 创建response
        response = client.responses.create(
            model="gpt-4.1", input=messages, tools=TOOL_CONFIG  # 传入历史信息
        )

        # 处理response
        should_continue = process_response(response, messages)

        iteration += 1

        # 如果不需要继续处理，跳出循环
        if not should_continue:
            print("任务完成！")
            break

    if iteration >= max_iterations:
        print("达到最大迭代次数，停止处理")


if __name__ == "__main__":
    # NOTE： 这下面的代码在包引用时不会调用，但是在命令行直接执行时会调用。这是进行调试的常用方法
    agent_runner(task="查下北京的天气，然后给foo@bar.com发一封邮件告知内容")
