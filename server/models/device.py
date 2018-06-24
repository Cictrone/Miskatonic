import datetime
import hmac, hashlib

from mongoengine import Document
from mongoengine.fields import StringField, IntField, ReferenceField
from mongoengine.fields import DateTimeField, BooleanField


class Device(Document):
    owner = ReferenceField(User)
    private_key = StringField(required=True)
    token_counter = IntField(default=1)
    token_generated = BooleanField(default=False)
    _token_value = StringField(default=None)
    creation_time = DateTimeField()
    last_checkin = DateTimeField()
    device_data = StringField(default='\{\}')  # JSON blob of device data

    def save(self, *args, **kwargs):
        if not self.creation_time:
            self.creation_date = datetime.datetime.now()
        return super(Device, self).save(*args, **kwargs)

    @property
    def token(self) -> str:
        if not self.token_generated:
            t = hmac.new(byte(self.private_key), digestmod=hashlib.sha3_256)
            t.update(str(self.token_counter))
            self._token_value = t.hexdigest()
            self.token_generated = True
        return self._token_value

    def increment_token_counter(self) -> None:
        self.token_counter += 1
        self.token_generated = False
        self.save()

    def is_valid_token(input_token: string) -> bool:
        return

    def checkin(self) -> None:
        self.last_checkin = datetime.datetime.now()
        self.save()
