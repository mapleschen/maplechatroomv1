from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response, stream_with_context
from flask_socketio import SocketIO, emit, join_room, leave_room
from config import Config
import eventlet
import openai
import requests
import sys
import os

# Determine if running as a frozen application (e.g. PyInstaller)
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

app.config.from_object(Config)
socketio = SocketIO(app, async_mode='eventlet')

# In-memory storage for connected users (simple version)
users = {}

# Initialize OpenAI Client
ai_client = openai.OpenAI(
    api_key=app.config['AI_API_KEY'],
    base_url=app.config['AI_API_URL']
)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        server_url = request.form.get('server')

        if not nickname:
            return render_template('login.html', error="Nickname is required", servers=app.config['CHAT_SERVERS'])
        
        if password != '123456':
            return render_template('login.html', error="Invalid password", servers=app.config['CHAT_SERVERS'])
        
        session['nickname'] = nickname
        session['server'] = server_url
        return redirect(url_for('chat'))

    return render_template('login.html', servers=app.config['CHAT_SERVERS'])

@app.route('/chat')
def chat():
    nickname = session.get('nickname')
    if not nickname:
        return redirect(url_for('login'))
    return render_template('chat.html', nickname=nickname)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/chat/ai', methods=['POST'])
def ai_chat():
    data = request.json
    user_message = data.get('message')
    
    # Remove the @成小理 prefix for the AI prompt
    prompt = user_message.replace('@成小理', '').strip()

    def generate():
        try:
            response = ai_client.chat.completions.create(
                model=app.config['AI_MODEL_NAME'],
                messages=[
                    {"role": "system", "content": "你是一个乐于助人的AI助手，名字叫成小理。"},
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield f"data: {chunk.choices[0].delta.content}\n\n"
            
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

# --- WebSocket Events ---

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('join')
def handle_join(data):
    nickname = data.get('nickname')
    room = 'main_room'
    join_room(room)
    users[request.sid] = nickname
    emit('system_message', {'msg': f'{nickname} has joined the room.'}, room=room)
    emit('update_users', list(users.values()), room=room)

@socketio.on('send_message')
def handle_message(data):
    nickname = session.get('nickname', data.get('nickname'))
    msg = data.get('message')
    room = 'main_room'
    
    if msg:
        # Broadcast the user's message first
        emit('receive_message', {'nickname': nickname, 'msg': msg}, room=room)

        # Check for @音乐一下 command
        if msg.strip() == '@音乐一下':
            try:
                api_url = "https://www.cunyuapi.top/rwyymusic"
                found_valid_music = False
                
                # Retry up to 3 times to find a valid song
                for attempt in range(3):
                    try:
                        response = requests.get(api_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                        if response.status_code == 200:
                            music_info = response.json()
                            song_url = music_info.get('song_url')
                            
                            if song_url:
                                # Validate the song URL by checking headers
                                # Use a short timeout for validation
                                check_res = requests.head(song_url, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True, timeout=3)
                                
                                # Check if redirected to 404 or content type is not audio
                                if '404' not in check_res.url and 'html' not in check_res.headers.get('Content-Type', ''):
                                    # Found valid music
                                    music_data = {
                                        'name': music_info.get('name', '未知歌曲'),
                                        'singer': music_info.get('artists', '未知歌手'),
                                        'image': music_info.get('pic_url', ''),
                                        'url': song_url
                                    }
                                    emit('receive_music_card', {
                                        'nickname': '音乐助手',
                                        'data': music_data
                                    }, room=room)
                                    found_valid_music = True
                                    break
                                else:
                                    print(f"Attempt {attempt+1}: Invalid song URL (404 or HTML) - {song_url}")
                    except Exception as inner_e:
                        print(f"Attempt {attempt+1} failed: {str(inner_e)}")
                        continue
                
                if not found_valid_music:
                    emit('system_message', {'msg': '获取音乐失败: 连续多次获取到无效资源，请稍后重试'}, room=room)

            except Exception as e:
                emit('system_message', {'msg': f'音乐服务出错: {str(e)}'}, room=room)

        # Check for @新闻 command
        elif msg.strip() == '@新闻':
            try:
                api_url = "https://whyta.cn/api/tx/bulletin?key=738b541a5f7a"
                response = requests.get(api_url, timeout=10)
                if response.status_code == 200:
                    res_json = response.json()
                    if res_json.get('code') == 200:
                        news_list = res_json.get('result', {}).get('list', [])
                        # Limit to top 10 news items
                        news_list = news_list[:10]
                        emit('receive_news_card', {
                            'nickname': '新闻助手',
                            'data': news_list
                        }, room=room)
                    else:
                        emit('system_message', {'msg': f"获取新闻失败: {res_json.get('msg')}"}, room=room)
                else:
                    emit('system_message', {'msg': f"新闻API请求失败: {response.status_code}"}, room=room)
            except Exception as e:
                emit('system_message', {'msg': f"新闻服务出错: {str(e)}"}, room=room)

        # Check for @天气[city] command
        elif msg.strip().startswith('@天气'):
            try:
                content = msg.strip()[3:].strip()
                city = ""
                
                # Extract city from brackets [city] or just city
                if content.startswith('[') and content.endswith(']'):
                    city = content[1:-1].strip()
                else:
                    city = content.strip()
                
                if not city:
                     emit('system_message', {'msg': "请指定城市，格式：@天气[城市] 或 @天气 城市"}, room=room)
                else:
                    api_url = f"https://v2.xxapi.cn/api/weatherDetails?city={city}&key=e37895e64ff52647"
                    # Need to import quote to handle Chinese characters in URL safely if requests doesn't handle it automatically
                    # Requests usually handles params well, but let's be safe or just pass params
                    
                    # Better to use params dict for requests to handle encoding
                    response = requests.get("https://v2.xxapi.cn/api/weatherDetails", params={'city': city, 'key': 'e37895e64ff52647'}, timeout=10)
                    
                    if response.status_code == 200:
                        res_json = response.json()
                        if res_json.get('code') == 200:
                            weather_data = res_json.get('data', {})
                            emit('receive_weather_card', {
                                'nickname': '天气助手',
                                'data': weather_data
                            }, room=room)
                        else:
                             emit('system_message', {'msg': f"获取天气失败: {res_json.get('msg')}"}, room=room)
                    else:
                        emit('system_message', {'msg': f"天气API请求失败: {response.status_code}"}, room=room)

            except Exception as e:
                emit('system_message', {'msg': f"天气服务出错: {str(e)}"}, room=room)

@socketio.on('disconnect')
def handle_disconnect():
    nickname = users.pop(request.sid, None)
    if nickname:
        room = 'main_room'
        emit('system_message', {'msg': f'{nickname} has left the room.'}, room=room)
        emit('update_users', list(users.values()), room=room)

if __name__ == '__main__':
    try:
        port = 5000
        host = '0.0.0.0'
        
        # Check if running as frozen app
        is_frozen = getattr(sys, 'frozen', False)
        
        if is_frozen:
            # Production/Frozen mode
            print("-" * 50)
            print(f"Maple Chatroom Server Started")
            print(f"Access URL: http://127.0.0.1:{port}")
            print(f"LAN Access: http://{host}:{port}")
            print("-" * 50)
            print("Keep this window open while using the chatroom.")
            print("-" * 50)
            
            # Turn off debug and reloader for exe
            socketio.run(app, debug=False, use_reloader=False, host=host, port=port)
        else:
            # Development mode
            socketio.run(app, debug=True, host=host, port=port)
            
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
