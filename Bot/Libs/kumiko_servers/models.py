from tortoise import fields
from tortoise.models import Model


class KumikoServer(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255)
    admin_logs = fields.BooleanField(default=False)
    announcements = fields.BooleanField(default=False)  # possible new feature?

    class Meta:
        table = "servers"

    def __str__(self):
        return self.name
