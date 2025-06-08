email_tool_config = {
    "type": "function",
    "name": "send_email",
    "description": "Send an email to the given recipient.",
    "parameters": {
        "type": "object",
        "properties": {
            "recipient": {"type": "string"},
            "subject": {"type": "string"},
            "body": {"type": "string"}
        },
        "required": ["recipient", "subject", "body"],
        "additionalProperties": False
    },
    "strict": True
}

weather_tool_config = {
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for provided coordinates in celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {"type": "number"},
            "longitude": {"type": "number"}
        },
        "required": ["latitude", "longitude"],
        "additionalProperties": False
    },
    "strict": True
}

# 全局常数通常使用大写表示
TOOL_CONFIG = [email_tool_config, weather_tool_config] 