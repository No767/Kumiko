from sqlalchemy import BigInteger, Column, Integer, String, Text

from .db import Base


class UserWSInv(Base):

    __tablename__ = "user_ws_inv"
    item_uuid = Column(String, primary_key=True)
    user_id = Column(BigInteger)
    date_obtained = Column(String)
    name = Column(String)
    description = Column(Text)
    star_rank = Column(Integer)
    type = Column(String)
    amount = Column(Integer)

    def __iter__(self):
        yield "item_uuid", self.item_uuid
        yield "user_id", self.user_id
        yield "date_obtained", self.date_obtained
        yield "name", self.name
        yield "description", self.description
        yield "star_rank", self.star_rank
        yield "type", self.type
        yield "amount", self.amount

    def __repr__(self):
        return f"UserWSInv(item_uuid={self.item_uuid!r}, user_id={self.user_id!r}, date_obtained={self.date_obtained!r}, name={self.name!r}, description={self.description!r}, star_rank={self.star_rank!r}, type={self.type!r}, amount={self.amount!r})"


class UserWS(Base):
    __tablename__ = "user_ws"
    user_id = Column(BigInteger, primary_key=True)
    pulls = Column(BigInteger)
    date_joined = Column(String)

    def __iter__(self):
        yield "user_id", self.user_id
        yield "pulls", self.pulls
        yield "date_joined", self.date_joined

    def __repr__(self):
        return f"UserWS(user_id={self.user_id!r}, pulls={self.pulls!r}, date_joined={self.date_joined!r})"


class WSData(Base):
    __tablename__ = "ws_data"
    uuid = Column(String, primary_key=True)
    event_name = Column(String)
    name = Column(String)
    description = Column(Text)
    star_rank = Column(Integer)
    type = Column(String)

    def __iter__(self):
        yield "uuid", self.uuid
        yield "event_name", self.event_name
        yield "name", self.name
        yield "description", self.description
        yield "star_rank", self.star_rank
        yield "type", self.type

    def __repr__(self):
        return f"WSData(uuid={self.uuid!r}, event_name={self.event_name!r}, name={self.name!r}, description={self.description!r}, star_rank={self.star_rank!r}, type={self.type!r})"
