from tortoise import fields
from tortoise.models import Model


class KumikoAdminLogs(Model):
    uuid = fields.UUIDField(pk=True)
    guild_id = fields.BigIntField()
    action = fields.CharField(max_length=255)
    issuer = fields.CharField(max_length=255)
    affected_user = fields.CharField(max_length=255)
    reason = fields.TextField()
    date_issued = fields.CharField(max_length=255)
    duration = fields.IntField()

    class Meta:
        table = "admin_logs"

    def __str__(self):
        return self.name
