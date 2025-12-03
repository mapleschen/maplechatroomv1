# Maple Chatroom

一个基于 Python Flask 和 WebSocket 的实时网页聊天室应用。支持多用户群聊、AI 助手对话、多媒体内容解析等功能。

## 🚀 功能特性

*   **实时聊天**：基于 WebSocket (Flask-SocketIO) 的低延迟消息传输。
*   **响应式设计**：基于 Tailwind CSS，适配桌面和移动端设备。
*   **多服务器配置**：支持在登录页选择不同的服务器节点（支持内网穿透地址）。

### 🛠️ 工具栏功能使用说明

聊天输入框上方集成了五个快捷功能按键，使用方法如下：

1.  **@成小理 (AI 助手)**
    *   **指令**: `@成小理 [你的问题]`
    *   **描述**: 呼叫内置 AI 助手，支持流式对话，可回答各类问题。

2.  **@音乐一下 (随机音乐)**
    *   **指令**: `@音乐一下`
    *   **描述**: 随机获取一首热门歌曲，以卡片形式展示封面、歌名并支持直接播放。

3.  **@电影 (视频解析)**
    *   **指令**: `@电影 [视频链接]`
    *   **描述**: 解析 m3u8 或 mp4 视频链接，在聊天窗口直接嵌入播放器。

4.  **@新闻 (热点简报)**
    *   **指令**: `@新闻`
    *   **描述**: 获取今日 Top 10 热点新闻摘要，以列表卡片形式展示。

5.  **@天气 (实时天气)**
    *   **指令**: `@天气 [城市名]` 或 `@天气 城市名`
    *   **示例**: `@天气[北京]`
    *   **描述**: 查询指定城市的实时天气信息，展示温度、天气状况及风向数据。

## 🛠️ 技术栈

*   **后端**：Python 3, Flask, Flask-SocketIO, Eventlet
*   **前端**：HTML5, Tailwind CSS (CDN), jQuery, Socket.IO Client
*   **AI 服务**：SiliconFlow API (Qwen/Qwen2.5-7B-Instruct)
*   **头像服务**：UI Avatars API

## ⚙️ 安装与启动

### 1. 环境准备
确保已安装 Python 3.8+。

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 启动服务
```bash
python app.py
```
*   服务默认运行在 `http://0.0.0.0:5000`
*   **本地访问**: `http://127.0.0.1:5000`
*   **局域网访问**: `http://<本机局域网IP>:5000`

## 📝 配置说明 (config.py)

项目的主要配置位于 `config.py` 文件中：

### 服务器列表配置
修改 `CHAT_SERVERS` 列表以更新登录页面的服务器选项：
```python
CHAT_SERVERS = [
    {"name": "Default Server", "url": "http://127.0.0.1:5000"},
    {"name": "Public Server", "url": "http://你的穿透域名"} # 用于内网穿透
]
```

### AI 配置
修改以下常量以切换 AI 模型或提供商：
```python
AI_API_KEY = "your-api-key"
AI_MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
AI_API_URL = "https://api.siliconflow.cn/v1"
```

## 🌐 内网穿透指南

本项目使用 **单端口 (5000)** 同时提供 Web 和 WebSocket 服务。

*   **本地协议**: HTTP + WebSocket
*   **本地端口**: `5000`
*   **映射配置**:
    *   将公网 HTTP 流量映射到本地 `127.0.0.1:5000`。
    *   确保穿透工具支持 WebSocket 协议。

## 💻 开发指南

### 目录结构
*   `app.py`: 后端主程序，处理路由和 Socket 事件。
*   `config.py`: 配置文件。
*   `static/js/chat.js`: 前端核心逻辑（Socket通信、UI交互、指令解析）。
*   `templates/`: HTML 模板文件。

### 添加新指令功能
如需添加新的指令（如 `@新闻`）：

1.  **前端 (`templates/chat.html`)**:
    在工具栏添加快捷按钮：
    ```html
    <button onclick="insertText('@新闻 ')">@新闻</button>
    ```

2.  **前端逻辑 (`static/js/chat.js`)**:
    在 `receive_message` 函数中添加解析逻辑：
    ```javascript
    if (data.msg.startsWith('@新闻')) {
        // 处理新闻逻辑，如调用 API 或显示特定 UI
    }
    ```

3.  **后端逻辑 (可选)**:
    如果需要后端处理（如 AI 生成），参考 `app.py` 中的 `/api/chat/ai` 路由实现新的接口，或在 WebSocket `handle_message` 中拦截处理。

### 4. 打包为 EXE (Windows)

本项目包含一个自动构建脚本 `build.py`，用于解决 PyInstaller 打包 Flask-SocketIO 和 Eventlet 时常见的依赖丢失问题。

1.  确保虚拟环境已激活并安装了所有依赖（包括 `pyinstaller`）。
2.  运行构建脚本：
    ```bash
    python build.py
    ```
3.  打包完成后，可执行文件位于 `dist/MapleChatroom.exe`。
    *   双击运行即可启动服务器。
    *   启动后保持黑色控制台窗口开启。
    *   在浏览器访问 `http://127.0.0.1:5000` 使用。

## 🤝 贡献指南
