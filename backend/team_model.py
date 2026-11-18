# -*- coding: utf-8 -*-
# 组队活动数据模型，负责 TeamActivities 查询行与接口 JSON 之间的转换。

class TeamActivity:
    def __init__(self, activity_id, user_id, title, description, event_date,
                 venue, capacity, status, signup_count, create_time):
        self.activity_id = activity_id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.event_date = event_date
        self.venue = venue
        self.capacity = capacity
        self.status = status
        self.signup_count = signup_count
        self.create_time = create_time

    @classmethod
    def from_row(cls, row):
        return cls(
            row.ActivityId, row.UserId, row.Title, row.Description,
            row.EventDate, row.Venue, row.Capacity, row.Status,
            int(row.SignupCount or 0), row.CreateTime
        )

    def to_dict(self):
        return {
            "id": self.activity_id,
            "userId": self.user_id,
            "title": self.title,
            "description": self.description,
            "eventDate": str(self.event_date) if self.event_date else None,
            "venue": self.venue,
            "capacity": self.capacity,
            "status": self.status,
            "signupCount": self.signup_count,
            "createTime": str(self.create_time) if self.create_time else None
        }
