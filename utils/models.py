from tortoise import fields
from tortoise.models import Model

__all__ = ("TagModel", "UserModel")

class TagModel(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    content = fields.TextField()

    def __str__(self):
        return self.content

class UserModel(Model):
    id = fields.IntField(pk=True)
    balance = fields.IntField()
    bank = fields.IntField()
    bank_limit = fields.IntField()
