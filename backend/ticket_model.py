# -*- coding: utf-8 -*-
# 票根数据模型（E：后端开发2 票根管理）
# 字段与 Tickets 表一一对应，负责 pyodbc 查询行与 JSON 字典互转
# 对外字段名与前端页面实际取值一致：id、type、rating、content、createTime

class Ticket:
    """票根对象，属性对应 Tickets 表字段"""

    def __init__(self, ticket_id, user_id, title, ticket_type, rating,
                 content, event_date, venue, create_time):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.title = title
        self.ticket_type = ticket_type
        self.rating = rating
        self.content = content
        self.event_date = event_date
        self.venue = venue
        self.create_time = create_time

    @classmethod
    def from_row(cls, row):
        # 将查询结果行转成 Ticket 对象，按列名取值
        # Memo 列在接口层命名为 content，与前端“体验笔记”含义一致
        return cls(
            row.TicketId, row.UserId, row.Title, row.Type, row.Rating,
            row.Memo, row.EventDate, row.Venue, row.CreateTime
        )

    def to_dict(self):
        # 转成可 JSON 序列化的字典
        # 日期时间统一转字符串；type、rating 未填写时返回 None
        return {
            "id": self.ticket_id,
            "userId": self.user_id,
            "title": self.title,
            "type": self.ticket_type,
            "rating": self.rating,
            "content": self.content,
            "eventDate": str(self.event_date) if self.event_date else None,
            "venue": self.venue,
            "createTime": str(self.create_time) if self.create_time else None
        }
