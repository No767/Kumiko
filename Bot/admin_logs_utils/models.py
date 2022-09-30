from sqlalchemy import BigInteger, Boolean, Column, String, Text

from .db import Base


class AdminLogs(Base):
    __tablename__ = "admin_logs"

    uuid = Column(String, primary_key=True)
    guild_id = Column(BigInteger)
    action_user_id = Column(BigInteger)
    user_affected_id = Column(BigInteger)
    type_of_action = Column(String)
    title = Column(String)
    reason = Column(Text)
    date_issued = Column(String)
    date_resolved = Column(String)
    duration = Column(BigInteger)
    resolved = Column(Boolean)

    def __iter__(self):
        yield "uuid", self.uuid
        yield "guild_id", self.guild_id
        yield "action_user_id", self.action_user_id
        yield "user_affected_id", self.user_affected_id
        yield "type_of_action", self.type_of_actios
        yield "title", self.title
        yield "reason", self.reason
        yield "date_issued", self.date_issued
        yield "date_resolved", self.date_resolved
        yield "duration", self.duration
        yield "resolved", self.resolved

    def __repr__(self):
        return f"AdminLogs(uuid={self.uuid!r}, guild_id={self.guild_id!r}, action_user_id={self.action_user_id!r}, user_affected_id={self.user_affected_id!r}, type_of_action={self.type_of_action!r}, title={self.title!r}, reason={self.reason!r}, date_issued={self.date_issued!r}, date_resolved={self.date_resolved!r}, duration={self.duration!r}, resolved={self.resolved!r})"
