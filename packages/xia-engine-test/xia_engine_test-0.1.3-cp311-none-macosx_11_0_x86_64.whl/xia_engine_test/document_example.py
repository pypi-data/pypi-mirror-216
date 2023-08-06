from datetime import date
from xia_engine import Base, Document, EmbeddedDocument
from xia_fields import StringField, CompressedStringField, IntField, DateField
from xia_engine import EmbeddedDocumentField, ListField, ExternalField


class MessageHello(EmbeddedDocument):
    msg: str = StringField()


class MessageStatus(EmbeddedDocument):
    msg: str = StringField()


class External(Document):
    _meta = {"collection_name": "External"}
    _actions = {"set_ok": {"out": MessageStatus}}
    name = StringField(required=True)
    profession = StringField()

    @classmethod
    def set_ok(cls, _acl=None):
        return MessageStatus.from_display(msg="External OK")


class DeepStatus(EmbeddedDocument):
    _actions = {"set_ok": {"out": MessageStatus}}
    description = StringField(required=True)

    @staticmethod
    def show_data():
        return "Data"

    @classmethod
    def set_ok(cls, _acl=None):
        return MessageStatus.from_display(msg="Deep Status OK")


class Status(EmbeddedDocument):
    current = StringField(required=True)
    details = EmbeddedDocumentField(document_type=DeepStatus)
    _actions = {"set_ok": {"out": MessageStatus}}
    
    @classmethod
    def set_ok(cls, _acl=None):
        return MessageStatus.from_display(msg="Status OK")


class DocumentSimple(Document):
    _meta = {"collection_name": "DocumentSimple"}
    _actions = {"say_hello": {"out": MessageHello}, "say_hi": {"out": MessageHello}}
    _key_fields = ["name"]
    name: str = StringField(required=True)
    ext_id: str = StringField(description="Extra ID", unique=True)
    years_id: str = StringField(description="Id of year", unique_with=["age"])
    age: int = IntField()
    birthday: date = DateField()
    data = CompressedStringField()
    data_list = ListField(CompressedStringField())
    status: object = EmbeddedDocumentField(document_type=Status)
    status_list = ListField(EmbeddedDocumentField(document_type=Status))
    external = ExternalField(document_type=External, field_map={"name": "name"})
    external_list = ExternalField(document_type=External, field_map={"name": "name"}, list_length=1)

    @classmethod
    def say_hello(cls, _acl=None):
        return MessageHello.from_display(msg="Hello World")

    def say_hi(self, _acl=None):
        return MessageHello.from_display(msg="Hello World")