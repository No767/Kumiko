from tortoise import fields
from tortoise.models import Model


# There will be more added later...
class KumikoUser(Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255)
    number_of_warnings = fields.IntField()

    class Meta:
        table = "users"

    def __str__(self):
        return self.name
