from sqlalchemy import BigInteger, Column, String, Text

from .db import Base


class AdminLogs(Base):
    __tablename__ = "admin_logs"

    uuid = Column(String, primary_key=True)
    guild_id = Column(BigInteger)
    action_user_name = Column(String)
    user_affected_name = Column(String)
    type_of_action = Column(String)
    reason = Column(Text)
    date_issued = Column(String)
    duration = Column(BigInteger)
    datetime_duration = Column(String)

    def __iter__(self):
        yield "uuid", self.uuid
        yield "guild_id", self.guild_id
        yield "action_user_name", self.action_user_name
        yield "user_affected_name", self.user_affected_name
        yield "type_of_action", self.type_of_action
        yield "reason", self.reason
        yield "date_issued", self.date_issued
        yield "duration", self.duration
        yield "date_duration", self.datetime_duration

    def __repr__(self):
        return f"AdminLogs(uuid={self.uuid!r}, guild_id={self.guild_id!r}, action_user_name={self.action_user_name!r}, user_affected_name={self.user_affected_name!r}, type_of_action={self.type_of_action!r}, reason={self.reason!r}, duration={self.duration!r}, date_duration={self.datetime_duration!r})"
