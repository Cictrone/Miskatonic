from mongoengine import Document
from mongoengine.fields import StringField, BooleanField


class User(Document):
    username = StringField(unique=True, required=True)
