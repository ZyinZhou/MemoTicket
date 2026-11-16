# -*- coding: utf-8 -*-
# 票根数据模型，负责 Tickets 查询行与接口 JSON 之间的转换。

class Ticket:
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
        return cls(
            row.TicketId, row.UserId, row.Title, row.Type, row.Rating,
            row.Memo, row.EventDate, row.Venue, row.CreateTime
        )

    def to_dict(self):
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
