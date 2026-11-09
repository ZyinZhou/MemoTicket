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
#   - 权限：票根仅创建者可查看、修改、删除，其他用户访问返回 403
#   - 表依赖：Users(UserId)、Interests(InterestId)、Tickets、TicketInterests
#   - 关联表 TicketInterests 的写入与清理在本模块内完成，表结构变更需同步修改本模块

from flask import Blueprint, request, jsonify, current_app
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime
import pyodbc

from ticket_model import Ticket

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

def get_json_body():
    # 获取请求体 JSON，非对象类型统一返回空字典，避免后续取值报错
    body = request.get_json(silent=True)
    return body if isinstance(body, dict) else {}

def parse_ticket_fields(data):
    # 校验票根字段并返回规范化字段字典，校验失败返回 (错误提示, None)
    # 规则：Title 必填且不超过100字符；EventDate 格式 YYYY-MM-DD；
    #       Venue 不超过100字符；Memo 不超过500字符
    title = str(data.get('title') or '').strip()
    if not title:
        return "票根标题不能为空", None
    if len(title) > 100:
        return "票根标题不能超过100个字符", None

    venue = str(data.get('venue') or '').strip()
    if len(venue) > 100:
        return "活动地点不能超过100个字符", None

    memo = str(data.get('memo') or '').strip()
    if len(memo) > 500:
        return "描述不能超过500个字符", None

    event_date = None
    raw_date = str(data.get('event_date') or '').strip()
    if raw_date:
        try:
            event_date = datetime.strptime(raw_date, '%Y-%m-%d').date()
        except ValueError:
            return "日期格式应为 YYYY-MM-DD", None

    return "", {"title": title, "event_date": event_date, "venue": venue, "memo": memo}

def parse_interest_ids(data):
    # 校验 interests 字段，返回去重后的兴趣ID列表
    # 字段缺失返回空列表；类型非法返回 None
    raw = data.get('interests')
    if raw is None:
        return []
    if not isinstance(raw, list):
        return None
    result = []
    for item in raw:
        if isinstance(item, bool) or not isinstance(item, int):
            return None
        if item not in result:
            result.append(item)
    return result

def find_missing_interest_ids(cursor, interest_ids):
    # 查询兴趣表，返回不存在的兴趣ID列表
    if not interest_ids:
        return []
    placeholders = ",".join("?" for _ in interest_ids)
    cursor.execute(
        "SELECT InterestId FROM Interests WHERE InterestId IN (%s)" % placeholders,
        interest_ids
    )
    existing = {row[0] for row in cursor.fetchall()}
    return [i for i in interest_ids if i not in existing]

def load_ticket_interests(cursor, ticket_ids):
    # 批量查询票根关联的兴趣ID，返回 {票根ID: [兴趣ID]}
    result = {tid: [] for tid in ticket_ids}
    if not ticket_ids:
        return result
    placeholders = ",".join("?" for _ in ticket_ids)
    cursor.execute(
        "SELECT TicketId, InterestId FROM TicketInterests WHERE TicketId IN (%s)" % placeholders,
        ticket_ids
    )
    for row in cursor.fetchall():
        result[row.TicketId].append(row.InterestId)
    return result

def load_owned_ticket(cursor, ticket_id, user_id):
    # 查询票根并校验归属，返回 (票根对象, 错误响应)
    # 票根不存在返回 404，非本人所有返回 403
    cursor.execute(
        """SELECT TicketId, UserId, Title, EventDate, Venue, Memo, CreateTime
           FROM Tickets WHERE TicketId = ?""",
        (ticket_id,)
    )
    row = cursor.fetchone()
    if not row:
        return None, (jsonify({"code": 404, "msg": "票根不存在"}), 404)
    if row.UserId != user_id:
        return None, (jsonify({"code": 403, "msg": "无权操作该票根"}), 403)
    return Ticket.from_row(row), None

# ================= 4. 创建票根接口 =================
# 请求方式：POST /api/tickets
# 请求体：
#   {
#     "title": "五月天演唱会",        // 必填，活动名称
#     "event_date": "2026-10-01",    // 可选，活动日期
#     "venue": "国家体育场",          // 可选，活动地点
#     "memo": "第一次看演唱会",       // 可选，描述
#     "interests": [1, 2]            // 可选，关联兴趣ID数组
#   }
# 返回：创建成功的票根ID与创建时间
@ticket_bp.route('/api/tickets', methods=['POST'])
def create_ticket():
    user_id = get_current_user_id()
    if user_id is None:
        return jsonify({"code": 401, "msg": "未登录或登录已过期"}), 401

    data = get_json_body()
    error, fields = parse_ticket_fields(data)
    if error:
        return jsonify({"code": 400, "msg": error}), 400

    interest_ids = parse_interest_ids(data)
    if interest_ids is None:
        return jsonify({"code": 400, "msg": "兴趣ID必须为整数数组"}), 400

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        missing = find_missing_interest_ids(cursor, interest_ids)
        if missing:
            msg = "存在无效的兴趣ID：" + ",".join(str(i) for i in missing)
            return jsonify({"code": 400, "msg": msg}), 400

        cursor.execute(
            """INSERT INTO Tickets (UserId, Title, EventDate, Venue, Memo)
               OUTPUT INSERTED.TicketId, INSERTED.CreateTime
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, fields['title'], fields['event_date'],
             fields['venue'], fields['memo'])
        )
        row = cursor.fetchone()

        for interest_id in interest_ids:
            cursor.execute(
                "INSERT INTO TicketInterests (TicketId, InterestId) VALUES (?, ?)",
                (row.TicketId, interest_id)
            )

        conn.commit()
        return jsonify({
            "code": 200,
            "msg": "创建成功",
            "data": {"ticket_id": row.TicketId, "create_time": str(row.CreateTime)}
        }), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        if conn:
            conn.close()

# ================= 5. 查询个人票根列表接口 =================
# 请求方式：GET /api/tickets
# 请求头：Authorization: Bearer <token>
# 返回当前用户创建的全部票根，按创建时间倒序，附带关联兴趣ID
@ticket_bp.route('/api/tickets', methods=['GET'])
def list_tickets():
    user_id = get_current_user_id()
    if user_id is None:
        return jsonify({"code": 401, "msg": "未登录或登录已过期"}), 401

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT TicketId, UserId, Title, EventDate, Venue, Memo, CreateTime
               FROM Tickets WHERE UserId = ?
               ORDER BY CreateTime DESC, TicketId DESC""",
            (user_id,)
        )
        tickets = [Ticket.from_row(row) for row in cursor.fetchall()]
        interest_map = load_ticket_interests(cursor, [t.ticket_id for t in tickets])

        data = []
        for ticket in tickets:
            item = ticket.to_dict()
            item['interests'] = interest_map.get(ticket.ticket_id, [])
            data.append(item)

        return jsonify({"code": 200, "msg": "查询成功", "data": data}), 200
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        if conn:
            conn.close()

# ================= 6. 查询票根详情接口 =================
# 请求方式：GET /api/tickets/<ticket_id>
# 返回票根完整信息与关联兴趣ID，仅创建者可查看
@ticket_bp.route('/api/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket_detail(ticket_id):
    user_id = get_current_user_id()
    if user_id is None:
        return jsonify({"code": 401, "msg": "未登录或登录已过期"}), 401

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        ticket, error_response = load_owned_ticket(cursor, ticket_id, user_id)
        if error_response:
            return error_response

        interest_map = load_ticket_interests(cursor, [ticket.ticket_id])
        item = ticket.to_dict()
        item['interests'] = interest_map.get(ticket.ticket_id, [])
        return jsonify({"code": 200, "msg": "查询成功", "data": item}), 200
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        if conn:
            conn.close()

# ================= 7. 修改票根接口 =================
# 请求方式：PUT /api/tickets/<ticket_id>
# 请求体与创建接口一致，title 必填
# interests 传入时整体替换原有兴趣关联，不传则保持不变
@ticket_bp.route('/api/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    user_id = get_current_user_id()
    if user_id is None:
        return jsonify({"code": 401, "msg": "未登录或登录已过期"}), 401

    data = get_json_body()
    error, fields = parse_ticket_fields(data)
    if error:
        return jsonify({"code": 400, "msg": error}), 400

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        ticket, error_response = load_owned_ticket(cursor, ticket_id, user_id)
        if error_response:
            return error_response

        # 仅在请求包含 interests 字段时校验并替换关联
        if 'interests' in data:
            interest_ids = parse_interest_ids(data)
            if interest_ids is None:
                return jsonify({"code": 400, "msg": "兴趣ID必须为整数数组"}), 400
            missing = find_missing_interest_ids(cursor, interest_ids)
            if missing:
                msg = "存在无效的兴趣ID：" + ",".join(str(i) for i in missing)
                return jsonify({"code": 400, "msg": msg}), 400

        cursor.execute(
            """UPDATE Tickets SET Title = ?, EventDate = ?, Venue = ?, Memo = ?
               WHERE TicketId = ?""",
            (fields['title'], fields['event_date'], fields['venue'],
             fields['memo'], ticket_id)
        )

        if 'interests' in data:
            cursor.execute("DELETE FROM TicketInterests WHERE TicketId = ?", (ticket_id,))
            for interest_id in interest_ids:
                cursor.execute(
                    "INSERT INTO TicketInterests (TicketId, InterestId) VALUES (?, ?)",
                    (ticket_id, interest_id)
                )

        conn.commit()
        return jsonify({"code": 200, "msg": "修改成功"}), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        if conn:
            conn.close()

# ================= 8. 删除票根接口 =================
# 请求方式：DELETE /api/tickets/<ticket_id>
# 删除前先清理该票根的兴趣关联记录，两步在同一事务内完成
@ticket_bp.route('/api/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    user_id = get_current_user_id()
    if user_id is None:
        return jsonify({"code": 401, "msg": "未登录或登录已过期"}), 401

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        ticket, error_response = load_owned_ticket(cursor, ticket_id, user_id)
        if error_response:
            return error_response

        cursor.execute("DELETE FROM TicketInterests WHERE TicketId = ?", (ticket_id,))
        cursor.execute("DELETE FROM Tickets WHERE TicketId = ?", (ticket_id,))
        conn.commit()
        return jsonify({"code": 200, "msg": "删除成功"}), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        if conn:
            conn.close()
