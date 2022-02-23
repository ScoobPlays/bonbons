from tortoise import fields
from tortoise.models import Model

__all__ = ("TagModel")

class TagModel(Model):
    name = fields.TextField()
    author_id = fields.IntField()
    content = fields.TextField()

    def __str__(self):
        return self.content