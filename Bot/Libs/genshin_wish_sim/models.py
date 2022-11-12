from tortoise import fields
from tortoise.models import Model


class WSData(Model):
    uuid = fields.CharField(max_length=512, pk=True)
    event_name = fields.CharField(max_length=512)
    name = fields.CharField(max_length=512)
    description = fields.TextField()
    star_rank = fields.IntField()
    type = fields.CharField(max_length=512)

    class Meta:
        table = "ws_data"

    def __str__(self):
        return self.name


class WSUser(Model):
    user_id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=512)
    pulls = fields.IntField()
    date_joined = fields.DatetimeField(null=True, auto_now_add=True)

    class Meta:
        table = "user_ws"

    def __str__(self):
        return self.name


class WSUserInv(Model):
    item_uuid = fields.CharField(max_length=512, pk=True)
    user_id = fields.BigIntField()
    date_obtained = fields.DatetimeField(null=True, auto_now_add=True)
    name = fields.CharField(max_length=512)
    description = fields.TextField()
    star_rank = fields.IntField()
    type = fields.CharField(max_length=512)
    amount = fields.IntField()

    class Meta:
        table = "user_ws_inv"

    def __str__(self):
        return self.name
