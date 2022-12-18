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

    class Meta:
        table = "eco_user_bridge"

    def __str__(self):
        return f"EcoUserBridge({self.user_bridge_id}, {self.user}, {self.user_inv})"


class EcoUserInv(Model):
    user_id = fields.BigIntField()
    item_uuid = fields.UUIDField()
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    amount = fields.IntField()
    date_acquired = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "eco_user_inv"

    def __str__(self):
        return f"EcoUserInv({self.user_id}, {self.date_acquired}, {self.item_uuid}, {self.name}, {self.description}, {self.amount})"


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
