# -*- coding: utf-8 -*-
# 票根基础数据模型（E：后端开发2 票根管理）
# 字段与 Tickets 数据表一一对应，负责 pyodbc 查询行与 JSON 字典之间的转换
# 使用方式：票根接口中导入本模块，由 from_row 构造对象、to_dict 输出

class Ticket:
    """票根对象，属性与 Tickets 表字段一致"""

    def __init__(self, ticket_id, user_id, title, event_date, venue, memo, create_time):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.title = title
        self.event_date = event_date
        self.venue = venue
        self.memo = memo
        self.create_time = create_time

    @classmethod
    def from_row(cls, row):
        # 将 pyodbc 查询结果行转成 Ticket 对象，属性按列名取值
        return cls(
            row.TicketId, row.UserId, row.Title, row.EventDate,
            row.Venue, row.Memo, row.CreateTime
        )

    def to_dict(self):
        # 转成可 JSON 序列化的字典
        # 日期时间统一转字符串，空字段保留为 None
        return {
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "title": self.title,
            "event_date": str(self.event_date) if self.event_date else None,
            "venue": self.venue,
            "memo": self.memo,
            "create_time": str(self.create_time) if self.create_time else None
        }
