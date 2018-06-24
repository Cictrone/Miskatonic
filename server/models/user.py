from typing import List

from .device import Device

from mongoengine import Document
from mongoengine.fields import StringField, ListField


class User(Document):
    username = StringField(unique=True, required=True)
    devices = ListField(Device, default=[])

    @staticmethod
    def get_user(username) -> User:
        return User.objects.get(username=username)

    def get_devices() -> List[Device]:
        return self.devices
