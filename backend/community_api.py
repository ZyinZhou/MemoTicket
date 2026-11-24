# -*- coding: utf-8 -*-
# 兴趣社区基础查询接口（A：Beta 第一周）
# 公共浏览接口：按兴趣查询社区动态及其可选关联票根。

import os

import pyodbc
from flask import Blueprint, current_app, jsonify, request

community_bp = Blueprint("community", __name__)

DB_CONFIG = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=InterestDB;"
    "UID=sa;"
    f'PWD={os.environ["MEMOTICKET_DB_PASSWORD"]};'
    "TrustServerCertificate=yes;"
)


def get_db_connection():
    return pyodbc.connect(DB_CONFIG)


def parse_interest_id():
    """读取并校验查询参数 interestId。"""
    raw_interest_id = request.args.get("interestId", "").strip()
    if not raw_interest_id:
        return None, "缺少兴趣ID参数 interestId"

    try:
        interest_id = int(raw_interest_id)
    except ValueError:
        return None, "兴趣ID必须为正整数"

    if interest_id <= 0:
        return None, "兴趣ID必须为正整数"

    return interest_id, ""


@community_bp.route("/api/community-posts", methods=["GET"])
def list_community_posts():
    """按兴趣查询社区动态，按发布时间倒序返回。"""
    interest_id, error = parse_interest_id()
    if error:
        return jsonify({"code": 400, "msg": error}), 400

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT InterestId FROM Interests WHERE InterestId = ?",
            (interest_id,),
        )
        if not cursor.fetchone():
            return jsonify({"code": 404, "msg": "兴趣不存在"}), 404

        cursor.execute(
            """
            SELECT
                p.PostId,
                p.UserId,
                u.Username,
                p.InterestId,
                p.Content,
                p.CreateTime,
                p.UpdateTime,
                t.TicketId,
                t.Title,
                t.Type,
                t.EventDate,
                t.Venue
            FROM CommunityPosts p
            INNER JOIN Users u ON u.UserId = p.UserId
            LEFT JOIN Tickets t ON t.TicketId = p.TicketId
            WHERE p.InterestId = ?
            ORDER BY p.CreateTime DESC, p.PostId DESC
            """,
            (interest_id,),
        )

        posts = []
        for row in cursor.fetchall():
            ticket = None
            if row.TicketId is not None:
                ticket = {
                    "id": row.TicketId,
                    "title": row.Title,
                    "type": row.Type,
                    "eventDate": str(row.EventDate) if row.EventDate else None,
                    "venue": row.Venue,
                }

            posts.append(
                {
                    "id": row.PostId,
                    "userId": row.UserId,
                    "authorName": row.Username,
                    "interestId": row.InterestId,
                    "content": row.Content,
                    "createTime": str(row.CreateTime) if row.CreateTime else None,
                    "updateTime": str(row.UpdateTime) if row.UpdateTime else None,
                    "ticket": ticket,
                }
            )

        return jsonify(
            {"code": 200, "msg": "查询成功", "data": posts}
        ), 200

    except Exception as error:
        current_app.logger.exception("查询社区动态失败")
        return jsonify({"code": 500, "msg": str(error)}), 500

    finally:
        if conn is not None:
            conn.close()