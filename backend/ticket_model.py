
# -*- coding: utf-8 -*-
# 票根基础数据模型（E：后端开发2 票根管理）
# 字段与 Tickets 数据表对应，负责 pyodbc 查询行与 JSON 字典之间的转换

class Ticket:
    """票根对象，属性与 Tickets 表字段一致"""

    def __init__(
        self, ticket_id, user_id, title, event_date,
        venue, memo, create_time, ticket_type=None, rating=None
    ):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.title = title
        self.event_date = event_date
        self.venue = venue
        self.memo = memo
        self.create_time = create_time
        self.type = ticket_type
        self.rating = rating

    @classmethod
    def from_row(cls, row):
        # 兼容尚未查询 Type 和 Rating 的旧 SQL
        return cls(
            row.TicketId,
            row.UserId,
            row.Title,
            row.EventDate,
            row.Venue,
            row.Memo,
            row.CreateTime,
            getattr(row, 'Type', None),
            getattr(row, 'Rating', None)
        )

    def to_dict(self):
        # 转换成可 JSON 序列化的字典
        return {
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "title": self.title,
            "type": self.type,
            "rating": self.rating,
            "event_date": str(self.event_date) if self.event_date else None,
            "venue": self.venue,
            "memo": self.memo,
            "create_time": str(self.create_time) if self.create_time else None
        }
