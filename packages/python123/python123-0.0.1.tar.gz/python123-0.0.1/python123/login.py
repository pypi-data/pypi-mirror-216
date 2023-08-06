import requests


def login(email: str, password: str):
    """登录"""
    data = {"email": email, "pass": password}
    r = requests.put("https://www.python123.io/api/v1/session", data=data)
    result = r.json()
    print(result)
