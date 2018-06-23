import hmac, hashlib

from mongoengine import Document
from mongoengine.fields import StringField, IntField


class User(Document):
    username = StringField(unique=True, required=True)
    private_key = StringField(required=True)
    token_counter = IntField(default=1)

    @property
    def token(self) -> str:
        t = hmac.new(byte(self.private_key), digestmod=hashlib.sha3_256)
        t.update(str(self.token_counter))
        return t.hexdigest()

    def increment_token_counter(self) -> None:
        self.token_counter += 1
        self.save()
