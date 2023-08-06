from xia_fields import StringField, IntField, TimestampField
from xia_fields_network import EmailField
from xia_engine import EmbeddedDocument, ListField


class AppNameField(StringField):
    """App Name field"""
    def __init__(self,
                 description="Application Name field",
                 sample="my-app-name",
                 regex="^[0-z]+(-[0-z]+)+$",
                 **kwargs):
        super().__init__(description=description, sample=sample, regex=regex, **kwargs)


class UserBasicInfo(EmbeddedDocument):
    """All information about the user

    """
    name: str = EmailField(required=True, unique=True, description="User Name")
    apps: list = ListField(StringField(), default=[], description="Application Names")
    user_id: str = StringField(description="User unique ID")
    confirm_time: float = TimestampField(description="Account confirmed date")
