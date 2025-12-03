# 开发日志 (Development Log)

本文档用于实时记录 Maple Chatroom 项目的开发过程、关键事件、重要提示词及帮助信息。

## 📅 2025-12-03 (Phase 2 - 功能完善)

### ✅ 已完成事项
1.  **@电影 功能实现**
    *   **描述**: 用户发送 `@电影 [url]`，系统自动解析并在聊天气泡中嵌入 iframe 视频播放器。
    *   **技术细节**: 修改 `chat.js`，在 `receive_message` 中拦截指令，动态生成 HTML。
    *   **解析接口**: `https://jx.m3u8.tv/jiexi/?url=`
2.  **UI 快捷键增强**
    *   **描述**: 在聊天输入框上方工具栏新增 `@电影` 和 `@新闻` 按钮。
    *   **文件**: `templates/chat.html`
3.  **服务绑定调整**
    *   **描述**: 修改 `app.py`，将 Flask-SocketIO 监听地址从默认的 `127.0.0.1` 改为 `0.0.0.0`，以支持局域网访问。
    *   **局域网地址**: `http://192.168.204.83:5000`
4.  **内网穿透配置更新**
    *   **描述**: 更新 `config.py` 中的 Public Server 地址为新的穿透域名 `http://p1vs8tg1k33r.ngrok.xiaomiqiu123.top`。
5.  **文档建设**
    *   **描述**: 创建 `README.md`，包含项目介绍、启动指南、配置说明及开发扩展指南。
6.  **@音乐一下 功能实现**
    *   **描述**: 用户发送 `@音乐一下`，系统随机获取一首音乐并以精美卡片形式展示。
    *   **API**: `https://v2.xxapi.cn/api/randomkuwo`
    *   **技术细节**: 后端 `app.py` 监听 `send_message`，触发 API 请求并通过 `receive_music_card` 事件下发数据；前端 `chat.js` 渲染音乐卡片（包含封面、歌名、歌手、播放控件）。
7.  **@新闻 功能实现**
    *   **描述**: 用户发送 `@新闻`，系统获取实时新闻并生成简报卡片。
    *   **API**: `https://whyta.cn/api/tx/bulletin`
    *   **技术细节**: 后端集成 API，前端渲染新闻列表卡片。
8.  **@天气 功能实现**
    *   **描述**: 用户发送 `@天气[城市]` 或 `@天气 城市`，系统查询并展示天气卡片。
    *   **API**: `https://v2.xxapi.cn/api/weatherDetails`
    *   **技术细节**: 支持多种指令格式解析，动态匹配天气图标渲染卡片。

### 💡 关键提示词 (Prompt History)
*   "增加一个公共服务器，名称为：Public Server..."
*   "完成@电影功能，规则为：用户发送@电影[url]..."
*   "在输入框上增加@电影、@新闻两个按键..."
*   "开启服务" (需注意 PowerShell 权限问题，使用 `python` 直接调用)
*   "程序有使用websocket协议吗？" -> 确认 Flask-SocketIO 实现。
*   "给出目前服务websocket的LAN" -> 调整 host 为 0.0.0.0。
*   "完成@音乐一下功能..." -> 集成 randomkuwo API。
*   "完成@新闻功能..." -> 集成新闻API。
*   "完成@天气[city]功能..." -> 集成天气API。

### 📝 待办事项 / 备忘
*   **历史记录**: 前端已有按钮但功能标记为 "Coming Soon"。
*   **部署注意**: 生产环境建议使用 Gunicorn + Eventlet 部署，而非 Flask 内置服务器。

---

## 🔧 常用开发指令

**启动服务 (Windows/PowerShell)**:
```powershell
.\venv\Scripts\python.exe app.py
```

**内网穿透映射**:
*   协议: HTTP (包含 WebSocket)
*   本地端口: 5000

---
*记录人: Trae AI Assistant*
