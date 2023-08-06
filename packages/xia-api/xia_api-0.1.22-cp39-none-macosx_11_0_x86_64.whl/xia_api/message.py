import uuid
import decimal
from xia_fields import StringField, IntField, BooleanField, DictField, ByteField
from xia_fields import TimestampField, FloatField, DecimalField
from xia_engine import EmbeddedDocumentField, ListField
from xia_engine import Document, EmbeddedDocument


class XiaActionResult(EmbeddedDocument):
    successful: bool = BooleanField(description="Action is successful?", required=True)
    message: str = StringField(description="Action Message")


class XiaRecordItem(EmbeddedDocument):
    name: str = StringField()
    int_value: int = IntField()
    float_value: float = FloatField()
    decimal_value: decimal.Decimal = DecimalField()


class XiaRecordBook(Document):
    """Record the cost of an API call

    """
    _meta = {"collection_name": "xia_recorder"}
    _cluster_fields = ["app_name", "class_name", "method_name"]
    _partition_info = {"type": "hour", "field": "start_time"}
    app_name: str = StringField()
    class_name: str = StringField()
    method_type: str = StringField()
    method_name: str = StringField()
    start_time: float = TimestampField()
    transaction_id: str = StringField()
    user_name: str = StringField()
    api_key_id: str = StringField()
    remote_ip: str = StringField()
    status_code: int = IntField()
    consumption: list = ListField(EmbeddedDocumentField(document_type=XiaRecordItem))


class XiaFileMsg(Document):
    file_name: str = StringField()
    mime_type: str = StringField(default="application/octet-stream")
    file_content: bytes = ByteField()


class XiaDocumentDeleteMsg(EmbeddedDocument):
    collection: str = StringField(sample="Collection A")
    id: str = StringField(sample=str(uuid.uuid4()))
    result: int = IntField(sample=200)
    message: str = StringField(description="Extra message about the delete", sample="Successful")


class XiaCollectionDeleteMsg(Document):
    collection: str = StringField(sample="Collection A")
    drop: bool = BooleanField()
    deleted: list = ListField(EmbeddedDocumentField(document_type=XiaDocumentDeleteMsg))
    ignored: dict = DictField(sample={"Collection B": {400: 1, 403: 2}})


class XiaErrorMessage(EmbeddedDocument):
    type: str = StringField(sample="Error Type")
    message: str = StringField(sample="Error Message")
    trace: str = StringField(sample="Error trace")
    