from flask import Flask, render_template, request  # 修复：添加request导入
from flask_socketio import SocketIO, emit, join_room, leave_room
import time
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'responder_system_secret'
socketio = SocketIO(app, cors_allowed_origins="*")  # 允许跨域访问

# 全局状态管理
game_state = {
    "is_started": False,  # 抢答是否开始
    "winner": None,       # 抢答成功者（客户端ID+名称）
    "start_time": None,   # 抢答开始时间
    "connected_clients": {},  # 已连接的客户端 {client_id: {"name": 名称, "join_time": 时间}}
    "client_count": 0     # 已连接客户端数量
}

# 主页（服务端监控页面）
@app.route('/')
def index():
    return render_template('server.html', 
                           connected_clients=game_state["connected_clients"],
                           client_count=game_state["client_count"])

# 手机客户端页面
@app.route('/client')
def client_page():
    return render_template('client.html')

# 客户端连接事件
@socketio.on('connect')
def handle_connect():
    global game_state  # 明确使用全局变量
    client_id = request.sid  # 获取客户端唯一ID
    game_state["client_count"] = len(game_state["connected_clients"]) + 1
    game_state["connected_clients"][client_id] = {
        "name": f"选手{game_state['client_count']}号",  # 默认名称
        "join_time": datetime.now().strftime("%H:%M:%S")
    }
    
    print(f"✅ 新客户端连接：{client_id} - {game_state['connected_clients'][client_id]['name']}")
    # 向所有客户端广播连接状态更新
    emit('update_clients', {
        "clients": game_state["connected_clients"],
        "count": game_state["client_count"]
    }, broadcast=True)
    # 向当前连接的客户端发送其ID和默认名称
    emit('init_client', {
        "client_id": client_id,
        "default_name": game_state["connected_clients"][client_id]["name"]
    })

# 客户端断开连接事件
@socketio.on('disconnect')
def handle_disconnect():
    global game_state
    client_id = request.sid
    if client_id in game_state["connected_clients"]:
        print(f"❌ 客户端断开：{client_id} - {game_state['connected_clients'][client_id]['name']}")
        del game_state["connected_clients"][client_id]
        game_state["client_count"] = len(game_state["connected_clients"])
        # 广播连接状态更新
        emit('update_clients', {
            "clients": game_state["connected_clients"],
            "count": game_state["client_count"]
        }, broadcast=True)

# 客户端修改名称
@socketio.on('set_name')
def handle_set_name(data):
    global game_state
    client_id = request.sid
    new_name = data.get("name", "").strip()
    if new_name and len(new_name) <= 10 and client_id in game_state["connected_clients"]:
        old_name = game_state["connected_clients"][client_id]["name"]
        game_state["connected_clients"][client_id]["name"] = new_name
        print(f"📛 客户端重命名：{client_id} {old_name} -> {new_name}")
        # 广播给所有客户端更新列表
        emit('update_clients', {
            "clients": game_state["connected_clients"],
            "count": game_state["client_count"]
        }, broadcast=True)
        # 给当前客户端返回确认反馈
        emit('name_set_success', {
            "new_name": new_name,
            "message": "名称修改成功！"
        })
    else:
        # 返回错误反馈
        emit('name_set_failed', {
            "message": "名称不能为空且长度不能超过10字！"
        })

# 主持人开始抢答
@socketio.on('start_game')
def handle_start_game():
    global game_state
    game_state["is_started"] = True
    game_state["winner"] = None
    game_state["start_time"] = time.time()
    print(f"🎬 抢答开始！时间：{game_state['start_time']}")
    # 向所有客户端广播抢答开始
    emit('game_started', broadcast=True)
    # 同时更新服务端页面状态
    emit('update_game_status', {
        "is_started": True,
        "status": "抢答进行中..."
    }, broadcast=True)

# 主持人重置抢答
@socketio.on('reset_game')
def handle_reset_game():
    global game_state
    game_state["is_started"] = False
    game_state["winner"] = None
    game_state["start_time"] = None
    print(f"🔄 抢答已重置")
    # 向所有客户端广播抢答重置
    emit('game_reset', broadcast=True)
    # 更新服务端页面状态
    emit('update_game_status', {
        "is_started": False,
        "status": "已重置，等待中"
    }, broadcast=True)

# 客户端抢答
@socketio.on('answer')
def handle_answer():
    global game_state
    # 只有抢答开始且无人抢答时才有效
    if not game_state["is_started"] or game_state["winner"]:
        return
    
    client_id = request.sid
    if client_id not in game_state["connected_clients"]:
        return
    
    # 计算响应时间（毫秒）
    response_time = round((time.time() - game_state["start_time"]) * 1000, 2)
    winner_name = game_state["connected_clients"][client_id]["name"]
    
    # 记录获胜者
    game_state["winner"] = {
        "client_id": client_id,
        "name": winner_name,
        "response_time": response_time,
        "time": datetime.now().strftime("%H:%M:%S")
    }
    
    print(f"🏆 抢答成功：{winner_name} - 响应时间：{response_time}ms")
    # 向所有客户端广播抢答结果
    emit('answer_result', game_state["winner"], broadcast=True)
    # 更新服务端页面状态
    emit('update_game_status', {
        "is_started": False,
        "status": f"🎉 恭喜 {winner_name} 抢答成功！响应时间：{response_time}ms"
    }, broadcast=True)

if __name__ == '__main__':
    # 获取电脑局域网IP（自动识别）
    import socket
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
    
    local_ip = get_local_ip()
    print("=" * 60)
    print("          局域网抢答器服务端已启动")
    print("=" * 60)
    print(f"服务端IP：{local_ip}")
    print(f"服务端端口：5000")
    print("-" * 60)
    print("使用说明：")
    print(f"1. 主持人打开浏览器访问：http://{local_ip}:5000")
    print(f"2. 选手用手机浏览器访问：http://{local_ip}:5000/client")
    print("3. 所有设备必须连接到同一个局域网")
    print("=" * 60)
    
    # 启动服务（允许外部访问）
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)