from sqlalchemy import BigInteger, Boolean, Column, Integer, String, Text

from .db_base import Base


class AuctionHouseItem(Base):
    __tablename__ = "eco_auction_house_items"

    uuid = Column(String, primary_key=True)
    user_id = Column(BigInteger)
    name = Column(String)
    description = Column(Text)
    date_added = Column(String)
    price = Column(BigInteger)
    passed = Column(Boolean)

    def __iter__(self):
        yield "uuid", self.uuid
        yield "user_id", self.user_id
        yield "name", self.name
        yield "description", self.description
        yield "date_added", self.date_added
        yield "price", self.price
        yield "passed", self.passed

    def __repr__(self):
        return f"AuctionHouseItem(uuid={self.uuid!r}, user_id={self.user_id!r}, name={self.name!r}, description={self.description!r}, date_added={self.date_added!r}, price={self.price!r}, passed={self.passed!r})"


class KumikoEcoUser(Base):
    __tablename__ = "eco_users"

    user_id = Column(BigInteger, primary_key=True)
    lavender_petals = Column(Integer)
    rank = Column(Integer)
    date_joined = Column(String)

    def __iter__(self):
        yield "user_id", self.user_id
        yield "lavender_petals", self.lavender_petals
        yield "rank", self.rank
        yield "date_joined", self.date_joined

    def __repr__(self):
        return f"KumikoEcoUser(user_id={self.user_id}, lavender_petals={self.lavender_petals}, rank={self.rank}, date_joined={self.date_joined})"


class KumikoQuests(Base):
    __tablename__ = "eco_quests"

    uuid = Column(String, primary_key=True)
    creator = Column(BigInteger)
    claimed_by = Column(BigInteger)
    date_created = Column(String)
    end_datetime = Column(String)
    name = Column(String)
    description = Column(Text)
    reward = Column(BigInteger)
    active = Column(Boolean)
    claimed = Column(Boolean)

    def __iter__(self):
        yield "uuid", self.uuid
        yield "creator", self.creator
        yield "claimed_by", self.claimed_by
        yield "date_created", self.date_created
        yield "end_datetime", self.end_datetime
        yield "name", self.name
        yield "description", self.description
        yield "reward", self.reward
        yield "active", self.active
        yield "claimed", self.claimed

    def __repr__(self):
        return f"KumikoQuests(uuid={self.uuid!r}, creator={self.creator!r}, claimed_by={self.claimed_by!r}, date_created={self.date_created!r}, end_datetime={self.end_datetime!r}, name={self.name!r}, description={self.description!r}, reward={self.reward!r}, active={self.active!r}, claimed={self.claimed!r})"


class UserInv(Base):
    __tablename__ = "user_inv"

    user_uuid = Column(String, primary_key=True)
    user_id = Column(
        BigInteger,
    )
    date_acquired = Column(String)
    uuid = Column(String)
    name = Column(String)
    description = Column(Text)
    amount = Column(Integer)

    def __iter__(self):
        yield "user_uuid", self.user_uuid
        yield "user_id", self.user_id
        yield "date_acquired", self.date_acquired
        yield "uuid", self.uuid
        yield "name", self.name
        yield "description", self.description
        yield "amount", self.amount

    def __repr__(self):
        return f"UserInv(user_uuid={self.user_uuid!r}, user_id={self.user_id!r}, date_acquired={self.date_acquired!r}, uuid={self.uuid!r}, name={self.name!r}, description={self.description!r}, amount={self.amount!r})"
