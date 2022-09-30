from sqlalchemy import BigInteger, Column, String, Text

from .db import Base


class AdminLogs(Base):
    __tablename__ = "admin_logs"

    uuid = Column(String, primary_key=True)
    guild_id = Column(BigInteger)
    action_user = Column(BigInteger)
    type_of_action = Column(String)
    title = Column(String)
    reason = Column(Text)
    date_issued = Column(String)
    date_resolved = Column(String)
