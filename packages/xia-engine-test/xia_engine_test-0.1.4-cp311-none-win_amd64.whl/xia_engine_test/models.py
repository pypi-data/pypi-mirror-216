from datetime import date
from xia_fields import StringField, IntField, CompressedStringField
from xia_fields import TimestampField, DateTimeField, TimeField, DateField, DecimalField
from xia_engine import Document
from xia_engine import DummyEngine


class DocumentBasic(Document):
    _key_fields = ["name"]
    _engine = DummyEngine

    name: str = StringField(required=True)
    age: int = IntField()
    cost = DecimalField(precision=2)
    birthday_1: date = DateField()
    birthday_2: date = TimestampField()
    birthday_3: date = DateTimeField()
    birthday_4: date = TimeField()
    data = CompressedStringField()
