def get_weather(latitude: float, longitude: float) -> float:
    # mock
    return 14.0


def send_email(recipient: str, subject: str, body: str) -> str:
    return "execution failed. recipient is not valid"


FUNCTION_MAP = {
    "get_weather": get_weather,
    "send_email": send_email,
}
