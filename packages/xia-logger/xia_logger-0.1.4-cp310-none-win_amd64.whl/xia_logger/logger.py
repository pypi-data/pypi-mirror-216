import io
import uuid
import base64
from datetime import datetime
from typing import Type
from xia_fields import StringField, TimestampField, ByteField, Int64Field, IntField
from xia_engine import MetaDocument, RamEngine
from xia_engine import BaseLogger, BaseDocument, Document
from xia_models import DataModel, DataAddress
from xia_coder import Coder
from xia_storer import FileStorer


class DataLog(Document):
    """Data log """
    domain_name: str = StringField(description="Data Domain Name")
    model_name: str = StringField(description="Data Model Name")
    model_module: str = StringField(description="Module Name Data Model")
    source_address: str = StringField(description="Source Address ID")
    target_address: str = StringField(description="Target Address ID")
    logger_name: str = StringField(description="Logger name")
    doc_id: str = StringField(description="Document ID")
    data_signature: str = StringField(description="Data package signature")
    operation_type: str = StringField(description="Operation Type", choices=["L", "I", "D", "U"])
    create_seq: str = StringField(description="Create Sequence")
    insert_timestamp: float = TimestampField(description="Insert Time")
    data_encode: str = StringField(description="Data Encode", sample="gzip")
    data_format: str = StringField(description="Data Format", sample="record")
    data_store: str = StringField(description="Data Location", sample="body")
    data_size: str = Int64Field(description="Data Size", sample=65536)
    data_content: bytes = ByteField(description="Data Content")


class Logger(BaseLogger):
    coder_dict = {
        ("gzip", "record"): Coder,
    }
    storer_dict = {
        "file": FileStorer
    }

    default_encode = "gzip"
    default_format = "record"
    default_store = "body"

    model_manager: Type[DataModel] = DataModel
    address_manager: Type[DataAddress] = DataAddress

    @classmethod
    def generate_log_class_if_not_exists(cls, parent_class: Type[DataLog]):
        class_name = cls.__name__ + "DataLog"
        engine = RamEngine if cls == Logger else cls
        if cls.log_class is None:
            new_class = MetaDocument(
                class_name,
                (parent_class,),
                {"_engine": engine}
            )
            cls.log_class = new_class

    @classmethod
    def generate_log(cls,
                     doc: BaseDocument,
                     operation_type: str,
                     *,
                     insert_timestamp: float = None,
                     with_data: bool = False,
                     logger_name: str = None,
                     data_encode: str = None,
                     data_format: str = None,
                     data_store: str = None):
        """Generate log from document or a list of document

        Args:
            doc: document or document list
            operation_type: Type of operation
            insert_timestamp: Timestamp of data insertion
            with_data: Extract data with log
            logger_name: could specify logger name
            data_encode: Wanted data encode
            data_format: Wanted data format
            data_store: Where the data should be stored

        Returns:
            Logger Object Ready to save
        """
        doc_meta = doc.get_meta_data()
        logger_name = logger_name if logger_name else doc_meta["logger_name"]
        cls.generate_log_class_if_not_exists(DataLog)
        domain_name = doc_meta["domain_name"]
        model_name = doc.__class__.__name__
        model_module = doc.__class__.__module__
        source_address = doc.get_address().get("_db", "")
        insert_timestamp = datetime.now().timestamp() if not insert_timestamp else insert_timestamp
        data_encode = cls.default_encode if not data_encode else data_encode
        data_format = cls.default_format if not data_format else data_format
        data_store = cls.default_store if not data_store else data_store
        log_params = {
            "domain_name": domain_name,
            "model_name": model_name,
            "model_module": model_module,
            "source_address": source_address,
            "logger_name": logger_name,
            "data_signature": str(uuid.uuid4()),  #: We just need a unique id for data
            "operation_type": operation_type,
            "insert_timestamp": insert_timestamp
        }
        if with_data:
            # Step 1: Preparation
            create_seq = cls.get_start_sequence(doc)
            doc_class = doc[0].__class__ if isinstance(doc, list) else doc.__class__
            doc_list = doc if isinstance(doc, list) else [doc]
            active_coder = cls.coder_dict.get((data_encode, data_format), None)
            if not active_coder:
                raise TypeError(f"Encode: {data_encode} + Format: {data_format} Combo needs coder-extension")
            active_storer = cls.storer_dict.get(data_store, None)
            if data_store != "body" and not active_storer:
                raise TypeError(f"Store: {data_store} needs storer-extension")
            encoder = active_coder(doc_class, data_encode=data_encode, data_format=data_format)
            # Step 2: Encode
            if data_store == "body":
                file_obj = io.BytesIO(b"")
                data_size = encoder.encode(doc_list, file_obj)
                data_content = file_obj.getvalue()
            else:
                location = active_storer.get_log_location(domain_name, model_name, source_address, create_seq)
                storer = active_storer(location=location, data_store=data_store)
                data_content = None
                data_size = 0
                for file_obj in storer.get_write_fp():
                    data_size = encoder.encode(doc_list, file_obj)
                    data_content = location.encode()
            log_params.update({
                "create_seq": create_seq,
                "data_encode": data_encode,
                "data_format": data_format,
                "data_store": data_store,
                "data_size": data_size,
                "data_content": data_content
            })
        else:
            # If there is no data content, we should provide the document id
            log_params["doc_id"] = doc.get_id()
        return cls.log_class.from_display(**log_params)

    @classmethod
    def migrate_log(cls, data_log: DataLog, logger_name: str) -> DataLog:
        """Migrate the old log with the new engine

        Args:
            data_log: Old data log object
            logger_name: new logger name

        Returns:
            New datalog object
        """
        cls.generate_log_class_if_not_exists(DataLog)
        new_data_log = cls.log_class()
        new_data_log._data = data_log._data  # Internal data migration
        new_data_log.logger_name = logger_name
        return new_data_log

    @classmethod
    def parse_log(cls, data_log: DataLog, given_class: Type[Document] = None):
        """Parse log content

        Args:
            data_log: Saved log object
            given_class: Given document class => Override the model given by model_manager

        Returns:
            There is no need to repeat the header in the case of massive content so return Iterator of sets:
                * position 1: header (Datalog)
                * position 2: document (Document)
        """
        raw_content = data_log._data  # Attention, we get the reference of datalog object
        data_content = raw_content.pop("data_content", None)  # Saving memory
        if not data_content:
            # No database content, and after yielding delete log => job is done
            return
        cls.generate_log_class_if_not_exists(DataLog)
        data_log = cls.log_class()  # Create a new data log object using current engine
        data_log._data = raw_content  # Pass back the reference
        if not isinstance(given_class, type) or not issubclass(given_class, Document):
            doc_class = cls.model_manager.get_class(
                domain_name=data_log.domain_name,
                model_name=data_log.model_name,
                model_module=data_log.model_module
            )
        else:
            doc_class = given_class
        if not doc_class:  # No class found, we cannot
            raise TypeError(f"{data_log.domain_name}/{data_log.model_module}.{data_log.model_name} cannot be loaded")
        data_encode = data_log.data_encode
        data_format = data_log.data_format
        data_store = data_log.data_store
        active_coder = cls.coder_dict.get((data_encode, data_format), None)
        if not active_coder:
            raise TypeError(f"Encode: {data_encode} + Format: {data_format} Combo needs coder-extension")
        active_storer = cls.storer_dict.get(data_store, None)
        if data_store != "body" and not active_storer:
            raise TypeError(f"Store: {data_store} needs storer-extension")
        decoder = active_coder(doc_class, data_encode=data_encode, data_format=data_format)
        if data_store == "body":
            file_obj = io.BytesIO(data_content)
            for doc in decoder.parse_content(file_obj):
                yield data_log, doc
        else:  # Will use storer / decoder combo to get data
            storer = active_storer(location=data_content.decode(), data_store=data_store)
            for file_obj in storer.get_read_fp():
                for doc in decoder.parse_content(file_obj):
                    yield data_log, doc

    @classmethod
    def streaming(cls, callback, **kwargs):
        """Streaming log reception

        Args:
            callback (callable): sync callback function

        Notes:
            callback function should have three parameters:
                * document: Document object
                * op: Operation Type
                * seq: Create Sequence
        """

    @classmethod
    async def streaming_async(cls, callback, **kwargs):
        """Streaming log reception

        Args:
            callback (coroutine): async callback function

        Notes:
            callback function should have three parameters:
                * document: Document object
                * op: Operation Type
                * seq: Create Sequence
        """

    @classmethod
    def search(cls, _document_class: Type[BaseDocument], *args, **kwargs):
        """It is a write-only engine, we don't support any search activities
        """
        return []


class HttpLogger(Logger):
    """Http logger, all header fields are string type"""
    encoders = {
        # ByteField: lambda x: b" " if x == b"" else x,
        TimestampField: lambda x: str(x),
        IntField: lambda x: str(x)
    }

    decoders = {
        # ByteField: lambda x: b"" if x == b" " else x,
        TimestampField: lambda x: float(x),
        IntField: lambda x: int(x)
    }


class JsonLogger(Logger):
    """Json Logger, base64 coded data contents"""
    encoders = {
        ByteField: lambda x: base64.b64encode(x).decode()
    }

    decoders = {
        ByteField: lambda x: base64.b64decode(x.encode())
    }
