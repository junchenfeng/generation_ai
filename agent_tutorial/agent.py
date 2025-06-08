
'''
环境设置
'''
import os
from dotenv import load_dotenv
from openai import OpenAI

# 导入本地工具
from tools import get_weather, send_email
from tool_config import TOOL_CONFIG

load_dotenv()  # 敏感信息不能明文展示
api_key = os.getenv('OPENAI_SECRET')
if not api_key:
    raise ValueError("OPENAI_SECRET is not set")

client = OpenAI(api_key=api_key)

'''
业务逻辑
'''

def agent_main():
    new_input_messages = [{"role": "user", "content": "查下北京的天气，然后给foo@bar.com发一封邮件告知内容"}]


    response = client.responses.create(
        model="gpt-4.1",
        input=new_input_messages,
        tools=TOOL_CONFIG
    )

    for step in response.output:
        new_input_messages.append(step)
        result = eval(f"{step.name}(**{step.arguments})")
        new_input_messages.append({                               # append result message
            "type": "function_call_output",
            "call_id": step.call_id,
            "output": str(result)
        })

    response_2 = client.responses.create(
        model="gpt-4.1",
        input=new_input_messages,
        tools=TOOL_CONFIG,
    )

    for step in response_2.output:
        new_input_messages.append(step)
        result = eval(f"{step.name}(**{step.arguments})")
        new_input_messages.append({                               # append result message
            "type": "function_call_output",
            "call_id": step.call_id,
            "output": str(result)
        })

    response_3 = client.responses.create(
        model="gpt-4.1",
        input=new_input_messages,
        tools=TOOL_CONFIG,
    )
    print(response_3.output)

if __name__ == "__main__":
    agent_main()

