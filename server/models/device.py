import datetime
import hmac, hashlib

from mongoengine import Document
from mongoengine.fields import StringField, IntField, ReferenceField
from mongoengine.fields import DateTimeField, BooleanField


class Device(Document):
    private_key = StringField(required=True)
    public_cert = StringField(required=True)
    token_counter = IntField(default=1)
    token_generated = BooleanField(default=False)
    _token_value = StringField(default=None)
    creation_time = DateTimeField()
    last_checkin = DateTimeField()
    device_data = StringField(default='\{\}')  # JSON blob of device data
    auth_requested = BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.creation_time:
            self.creation_date = datetime.datetime.now()
        return super(Device, self).save(*args, **kwargs)

    @staticmethod
    def get_device(device) -> Device:
        return Device.objects.get(id=device)

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

    def set_auth_requested() -> None:
        self.auth_requested = True
        self.save()

    def unset_auth_requested() -> None:
        self.auth_requested = False
        self.save()

    def decrypt(encrypted_blob: string) -> string:
        # no crypto for now :(
        return encrypted_blob

    def is_valid_token(encrypted_token: string) -> bool:
        token = self.decrypt(encrypted_token)
        valid = token == self.token
        if valid:
            self.increment_token_counter()
            self.check_in()
            self.unset_auth_requested()
        return valid

    def check_in(self) -> None:
        self.last_checkin = datetime.datetime.now()
        self.save()
