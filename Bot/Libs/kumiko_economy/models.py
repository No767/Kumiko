from tortoise import fields
from tortoise.models import Model


# Bridging table used for one-to-many relationship
class EcoUserBridge(Model):
    user_bridge_id = fields.BigIntField(pk=True)
    user: fields.ForeignKeyRelation["EcoUser"] = fields.ForeignKeyField(
        "models.EcoUser"
    )
    user_inv: fields.ForeignKeyRelation["EcoUserInv"] = fields.ForeignKeyField(
        "models.EcoUserInv", null=True
    )
    quests: fields.ForeignKeyRelation["EcoQuests"] = fields.ForeignKeyField(
        "models.EcoQuests", null=True
    )
    auction_house: fields.ForeignKeyRelation[
        "EcoAuctionHouse"
    ] = fields.ForeignKeyField("models.EcoAuctionHouse", null=True)
    marketplace: fields.ForeignKeyRelation["EcoMarketplace"] = fields.ForeignKeyField(
        "models.EcoMarketplace", null=True
    )

    class Meta:
        table = "eco_user_bridge"

    def __str__(self):
        return f"EcoUserBridge({self.user_bridge_id}, {self.user}, {self.user_inv}, {self.quests}, {self.auction_house}, {self.marketplace})"


class EcoUserInv(Model):
    id = fields.UUIDField(pk=True)
    user_id = fields.BigIntField()
    item_uuid = fields.UUIDField()
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    amount = fields.IntField()
    date_acquired = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "eco_user_inv"

    def __str__(self):
        return f"EcoUserInv({self.id}, {self.user_id}, {self.item_uuid}, {self.name}, {self.description}, {self.amount}, {self.date_acquired})"


class EcoUser(Model):
    user_id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=255)
    lavender_petals = fields.BigIntField(default=0)
    rank = fields.IntField(default=0)
    date_joined = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "eco_users"

    def __str__(self):
        return f"EcoUser({self.user_id}, {self.username}, {self.lavender_petals}, {self.rank}, {self.date_joined})"


class EcoQuests(Model):
    id = fields.UUIDField(pk=True)
    creator_id = fields.BigIntField()
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

    def __str__(self):
        return f"EcoQuests({self.id}, {self.creator_id}, {self.claimer_id}, {self.date_created}, {self.name}, {self.description}, {self.end_datetime}, {self.reward}, {self.active}, {self.claimed})"


class EcoAuctionHouse(Model):
    id = fields.UUIDField(pk=True)
    owner_id = fields.BigIntField()
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    price = fields.IntField()
    date_added = fields.DatetimeField(auto_now_add=True)
    passed = fields.BooleanField(default=False)

    class Meta:
        table = "eco_auction_house"

    def __str__(self):
        return f"EcoAuctionHouse({self.id}, {self.owner_id}, {self.name}, {self.description}, {self.price}, {self.date_added}, {self.passed})"


class EcoMarketplace(Model):
    id = fields.UUIDField(pk=True)
    owner_id = fields.BigIntField()
    owner_name = fields.CharField(max_length=255)
    date_added = fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    price = fields.IntField()
    amount = fields.IntField()
    updated_price = fields.BooleanField(default=False)

    class Meta:
        table = "eco_marketplace"

    def __str__(self):
        return f"EcoMarketplace({self.id}, {self.owner_id}, {self.owner_name}, {self.date_added}, {self.name}, {self.description}, {self.price}, {self.amount}, {self.updated_price})"
