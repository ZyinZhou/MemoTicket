# -*- coding: utf-8 -*-
# 票根管理接口（E：后端开发2 票根管理）
# 采用 Blueprint 独立成模块，避免与其他成员在 app.py 中的接口相互冲突
#
# 接入方式：app.py 底部已通过 app.register_blueprint(ticket_bp) 注册
#
# 对接说明：
#   - 鉴权：请求头携带 Authorization: Bearer <token>，token 来自登录接口
#   - 返回格式：{ "code": 200, "msg": "...", "data": {...} }，与现有接口一致
#   - 前端 baseURL 已指向 http://127.0.0.1:5000，请求拦截器会自动附带 token

from flask import Blueprint, request, jsonify, current_app
from itsdangerous import URLSafeTimedSerializer
import pyodbc

ticket_bp = Blueprint('ticket', __name__)

# 数据库连接配置，与 app.py 保持一致
# 说明：暂复制一份，避免模块间循环导入
DB_CONFIG = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost\\SQLEXPRESS;'
    'DATABASE=InterestDB;'
    'UID=sa;'
    'PWD=JohnTitor488;'
)

def get_db_connection():
    return pyodbc.connect(DB_CONFIG)

def get_current_user_id():
    # 从请求头 Authorization 解析当前用户ID，token 有效期 24 小时，与登录接口一致
    # 解析失败返回 None，由调用方返回 401
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth[7:]
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token, max_age=86400)
        return data.get('user_id')
    except Exception:
        return None

# ================= 4. 创建票根接口 =================
# 请求方式：POST /api/tickets
# 请求体示例：
#   {
#     "title": "五月天演唱会",   // 必填
#     "memo": "第一次看演唱会"   // 可选
#   }
# 返回成功示例：
#   { "code": 200, "msg": "创建成功",
#     "data": { "ticket_id": 1, "create_time": "2026-11-03 10:00:00" } }
# 返回失败示例：
#   { "code": 400, "msg": "票根标题不能为空" }
#   { "code": 401, "msg": "未登录或登录已过期" }
@ticket_bp.route('/api/tickets', methods=['POST'])
def create_ticket():
    user_id = get_current_user_id()
    if user_id is None:
        return jsonify({"code": 401, "msg": "未登录或登录已过期"}), 401

    data = request.get_json(silent=True) or {}
    title = (data.get('title') or '').strip()
    if not title:
        return jsonify({"code": 400, "msg": "票根标题不能为空"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO Tickets (UserId, Title, Memo)
               OUTPUT INSERTED.TicketId, INSERTED.CreateTime
               VALUES (?, ?, ?)""",
            (user_id, title, data.get('memo'))
        )
        row = cursor.fetchone()
        conn.commit()
        return jsonify({
            "code": 200,
            "msg": "创建成功",
            "data": {"ticket_id": row.TicketId, "create_time": str(row.CreateTime)}
        }), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        conn.close()
