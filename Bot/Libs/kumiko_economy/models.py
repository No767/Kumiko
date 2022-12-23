import orjson
from pydantic.main import BaseConfig as PydanticBaseConfig
from tortoise import fields
from tortoise.models import Model


class EcoJSONConfig(PydanticBaseConfig):
    json_loads = orjson.loads
    json_dumps = orjson.dumps


class EcoUser(Model):
    user_id = fields.BigIntField(pk=True)
    user_inv: fields.ReverseRelation["EcoUserInv"]
    quest: fields.ReverseRelation["EcoQuests"]
    auction_house: fields.ReverseRelation["EcoAuctionHouse"]
    marketplace: fields.ReverseRelation["EcoMarketplace"]
    username = fields.CharField(max_length=255)
    lavender_petals = fields.BigIntField(default=0)
    rank = fields.IntField(default=0)
    date_joined = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "eco_user"

    class PydanticMeta:
        config_class = EcoJSONConfig

    def __str__(self):
        return f"EcoUser({self.user_id}, {self.user_inv}, {self.quests}, {self.auction_house}, {self.marketplace}, {self.username}, {self.lavender_petals}, {self.rank}, {self.date_joined})"


class EcoUserInv(Model):
    id = fields.UUIDField(pk=True)
    user: fields.ForeignKeyRelation["EcoUser"] = fields.ForeignKeyField(
        "models.EcoUser", related_name="user_inv", on_delete=fields.CASCADE
    )
    item_uuid = fields.UUIDField()
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    amount = fields.IntField()
    date_acquired = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "eco_user_inv"

    class PydanticMeta:
        config_class = EcoJSONConfig

    def __str__(self):
        return f"EcoUserInv({self.id}, {self.user}, {self.item_uuid}, {self.name}, {self.description}, {self.amount}, {self.date_acquired})"


class EcoQuests(Model):
    id = fields.UUIDField(pk=True)
    creator: fields.ForeignKeyRelation["EcoUser"] = fields.ForeignKeyField(
        "models.EcoUser", related_name="quest", on_delete=fields.CASCADE
    )
    claimer_id = fields.BigIntField(null=True)
    date_created = fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    end_datetime = fields.DatetimeField(auto_now_add=True)
    reward = fields.IntField()
    active = fields.BooleanField(default=True)
    claimed = fields.BooleanField(default=False)

    class Meta:
        table = "eco_quests"

    class PydanticMeta:
        config_class = EcoJSONConfig

    def __str__(self):
        return f"EcoQuests({self.id}, {self.creator}, {self.claimer_id}, {self.date_created}, {self.name}, {self.description}, {self.end_datetime}, {self.reward}, {self.active}, {self.claimed})"


class EcoAuctionHouse(Model):
    id = fields.UUIDField(pk=True)
    owner: fields.ForeignKeyRelation["EcoUser"] = fields.ForeignKeyField(
        "models.EcoUser", related_name="auction_house", on_delete=fields.CASCADE
    )
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    price = fields.IntField()
    date_added = fields.DatetimeField(auto_now_add=True)
    passed = fields.BooleanField(default=False)

    class Meta:
        table = "eco_auction_house"

    class PydanticMeta:
        config_class = EcoJSONConfig

    def __str__(self):
        return f"EcoAuctionHouse({self.id}, {self.owner}, {self.name}, {self.description}, {self.price}, {self.date_added}, {self.passed})"


class EcoMarketplace(Model):
    id = fields.UUIDField(pk=True)
    owner: fields.ForeignKeyRelation["EcoUser"] = fields.ForeignKeyField(
        "models.EcoUser", related_name="marketplace", on_delete=fields.CASCADE
    )
    owner_name = fields.CharField(max_length=255)
    date_added = fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    price = fields.IntField()
    amount = fields.IntField()
    updated_price = fields.BooleanField(default=False)

    class Meta:
        table = "eco_marketplace"

    class PydanticMeta:
        config_class = EcoJSONConfig

    def __str__(self):
        return f"EcoMarketplace({self.id}, {self.owner}, {self.owner_name}, {self.date_added}, {self.name}, {self.description}, {self.price}, {self.amount}, {self.updated_price})"
