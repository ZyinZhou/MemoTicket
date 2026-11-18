# -*- coding: utf-8 -*-
# 组队活动接口（E：后端开发2 组队活动管理）
# 采用 Blueprint 独立成模块，避免与其他成员在 app.py 中的接口相互冲突
#
# 接入方式：app.py 底部已通过 app.register_blueprint(team_bp) 注册
#
# 对接说明：
#   - 鉴权：创建活动需请求头携带 Authorization: Bearer <token>；列表与详情可匿名浏览
#   - 返回格式：{ "code": 200, "msg": "...", "data": {...} }，与现有接口一致
#   - 字段口径：返回字段名与前端页面一致（id、userId、title、description、eventDate、venue、capacity、status、signupCount、createTime）
#   - 表依赖：Users(UserId)、TeamActivities、TeamActivityApplications
#   - 报名、退出与申请审批接口属后续阶段，本模块仅提供活动基础数据与查询

import os

from flask import Blueprint, request, jsonify, current_app
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime
import pyodbc

from team_model import TeamActivity

team_bp = Blueprint('team', __name__)

# 数据库连接配置，与 app.py 保持一致
# 说明：暂复制一份，避免模块间循环导入
DB_CONFIG = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=InterestDB;'
    'UID=sa;'
    f'PWD={os.environ["MEMOTICKET_DB_PASSWORD"]};'
    'TrustServerCertificate=yes;'
)

# 活动状态取值：招募中、已关闭；本轮无修改状态接口，创建时默认招募中
ACTIVITY_STATUS_OPEN = "招募中"

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

def parse_activity_fields(data):
    # 校验组队活动字段，返回 (错误提示, 规范化字段字典)
    # 规则：title 必填且不超过100字符；description 不超过500字符；
    #       event_date 格式 YYYY-MM-DD；venue 不超过100字符；capacity 为正整数
    title = str(data.get('title') or '').strip()
    if not title:
        return "活动标题不能为空", None
    if len(title) > 100:
        return "活动标题不能超过100个字符", None

    description = str(data.get('description') or '').strip()
    if description and len(description) > 500:
        return "活动描述不能超过500个字符", None
    description = description or None

    raw_date = data.get('event_date') if 'event_date' in data else data.get('eventDate')
    raw_date = str(raw_date or '').strip()
    event_date = None
    if raw_date:
        try:
            event_date = datetime.strptime(raw_date, '%Y-%m-%d').date()
        except ValueError:
            return "活动时间格式应为 YYYY-MM-DD", None

    venue = str(data.get('venue') or '').strip() or None
    if venue and len(venue) > 100:
        return "活动地点不能超过100个字符", None

    raw_capacity = data.get('capacity')
    if raw_capacity is None:
        return "人数上限必须为正整数", None
    if isinstance(raw_capacity, bool) or (isinstance(raw_capacity, float) and not raw_capacity.is_integer()):
        return "人数上限必须为正整数", None
    try:
        capacity = int(raw_capacity)
    except (TypeError, ValueError):
        return "人数上限必须为正整数", None
    if capacity < 1:
        return "人数上限必须为正整数", None

    return "", {
        "title": title,
        "description": description,
        "event_date": event_date,
        "venue": venue,
        "capacity": capacity
    }

def load_activity_list(cursor):
    # 查询全部活动并统计报名人数；有活动时间的按时间升序，同日创建时间倒序，无时间的排最后
    # 报名人数口径：申请表全部记录；后续接入审批流后按审批状态统计
    cursor.execute(
        """SELECT a.ActivityId, a.UserId, a.Title, a.Description, a.EventDate,
                  a.Venue, a.Capacity, a.Status, a.CreateTime,
                  COUNT(ap.ApplicationId) AS SignupCount
           FROM TeamActivities a
           LEFT JOIN TeamActivityApplications ap ON ap.ActivityId = a.ActivityId
           GROUP BY a.ActivityId, a.UserId, a.Title, a.Description, a.EventDate,
                    a.Venue, a.Capacity, a.Status, a.CreateTime
           ORDER BY CASE WHEN a.EventDate IS NULL THEN 1 ELSE 0 END,
                    a.EventDate ASC, a.CreateTime DESC, a.ActivityId DESC"""
    )
    return [TeamActivity.from_row(row) for row in cursor.fetchall()]

def load_activity(cursor, activity_id):
    # 查询单个活动并统计报名人数，不存在返回 None
    cursor.execute(
        """SELECT a.ActivityId, a.UserId, a.Title, a.Description, a.EventDate,
                  a.Venue, a.Capacity, a.Status, a.CreateTime,
                  COUNT(ap.ApplicationId) AS SignupCount
           FROM TeamActivities a
           LEFT JOIN TeamActivityApplications ap ON ap.ActivityId = a.ActivityId
           WHERE a.ActivityId = ?
           GROUP BY a.ActivityId, a.UserId, a.Title, a.Description, a.EventDate,
                    a.Venue, a.Capacity, a.Status, a.CreateTime""",
        (activity_id,)
    )
    row = cursor.fetchone()
    return TeamActivity.from_row(row) if row else None

# ================= 9. 创建组队活动接口 =================
# 请求方式：POST /api/activities
# 请求头：Authorization: Bearer <token>
# 请求体：
#   {
#     "title": "周末剧本杀组队",          // 必填，活动名称
#     "description": "缺两位推理爱好者",  // 可选，活动描述，不超过500字
#     "event_date": "2026-11-22",        // 可选，活动时间 YYYY-MM-DD
#     "venue": "迷之屋体验馆",            // 可选，活动地点
#     "capacity": 4                       // 必填，人数上限，正整数
#   }
# 返回：创建成功的活动ID与创建时间
@team_bp.route('/api/activities', methods=['POST'])
def create_activity():
    user_id = get_current_user_id()
    if user_id is None:
        return jsonify({"code": 401, "msg": "未登录或登录已过期"}), 401

    data = get_json_body()
    error, fields = parse_activity_fields(data)
    if error:
        return jsonify({"code": 400, "msg": error}), 400

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO TeamActivities
               (UserId, Title, Description, EventDate, Venue, Capacity, Status)
               OUTPUT INSERTED.ActivityId, INSERTED.CreateTime
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, fields['title'], fields['description'], fields['event_date'],
             fields['venue'], fields['capacity'], ACTIVITY_STATUS_OPEN)
        )
        row = cursor.fetchone()
        conn.commit()
        return jsonify({
            "code": 200,
            "msg": "创建成功",
            "data": {"id": row.ActivityId, "createTime": str(row.CreateTime)}
        }), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        if conn:
            conn.close()

# ================= 10. 组队活动列表接口 =================
# 请求方式：GET /api/activities
# 说明：可匿名浏览；返回全部活动，附带报名人数；有活动时间的按时间升序，同日创建时间倒序，无时间的排最后
@team_bp.route('/api/activities', methods=['GET'])
def list_activities():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        activities = load_activity_list(cursor)
        return jsonify({
            "code": 200,
            "msg": "查询成功",
            "data": [a.to_dict() for a in activities]
        }), 200
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        if conn:
            conn.close()

# ================= 11. 组队活动详情接口 =================
# 请求方式：GET /api/activities/<activity_id>
# 说明：可匿名浏览，返回活动完整信息与当前报名人数
@team_bp.route('/api/activities/<int:activity_id>', methods=['GET'])
def get_activity_detail(activity_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        activity = load_activity(cursor, activity_id)
        if activity is None:
            return jsonify({"code": 404, "msg": "活动不存在"}), 404
        return jsonify({"code": 200, "msg": "查询成功", "data": activity.to_dict()}), 200
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        if conn:
            conn.close()
