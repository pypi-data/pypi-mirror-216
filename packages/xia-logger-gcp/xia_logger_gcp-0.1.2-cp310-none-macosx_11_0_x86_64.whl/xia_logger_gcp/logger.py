from typing import Type
import base64
import uuid
from google.cloud import logging
from xia_fields import ByteField
from xia_engine import BaseDocument
from xia_logger import JsonLogger


class GcpLogger(JsonLogger):
    engine_param = "gcp_logging"
    engine_connector = logging.Client

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None):
        db_con = cls.get_connection().logger(__name__)
        db_con.log_struct(db_content)
        return doc_id if doc_id else str(uuid.uuid4())
