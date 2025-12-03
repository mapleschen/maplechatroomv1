import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'maple-secret-key-12345'
    # WebSocket server addresses as requested
    # In a real B/S distributed system, these might point to different backend nodes.
    # For this local demo, they point to the same instance.
    CHAT_SERVERS = [
        {"name": "Default Server", "url": "http://127.0.0.1:5000"},
        {"name": "Backup Server", "url": "http://localhost:5000"},
        {"name": "Public Server", "url": "http://p1vs8tg1k33r.ngrok.xiaomiqiu123.top"}
    ]

    # AI Configuration
    AI_API_KEY = "sk-czegptwmtpgdfwuqhlfshhnyignpneekudwopvyyughxyicc"
    AI_MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
    AI_API_URL = "https://api.siliconflow.cn/v1" # Assuming v1 based on common practices, but will try without if fails.
