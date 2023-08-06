from functools import lru_cache
from google.protobuf.descriptor_pb2 import DescriptorProto, FieldDescriptorProto, FileDescriptorProto
from google.protobuf import message_factory, descriptor_pool
from xia_fields import BaseField
from xia_fields import BooleanField, DoubleField, FloatField, StringField, ByteField, DecimalField, JsonField
from xia_fields import DateField, DateTimeField, TimestampField, TimeField
from xia_fields import Int64Field, UInt64Field, Int32Field, UInt32Field, IntField
from xia_fields import Fixed64Field, Fixed32Field, SFixed32Field, SFixed64Field, CompressedStringField
from xia_engine import Document, EmbeddedDocument, EmbeddedDocumentField, ListField


class DocToProto:
    """XIA Document to Protobuf Message Class

    Attention:
        The target protobuf format is related to Bigquery implementation
    """
    # Simple Dictionary Match
    type_dict = {
        DoubleField: 1,
        FloatField: 2,
        Int64Field: 3,
        DateField: 3,
        TimestampField: 3,
        UInt64Field: 4,
        Int32Field: 5,
        Fixed64Field: 6,
        Fixed32Field: 7,
        DateTimeField: 9,
        TimeField: 9,
        ByteField: 12,
        CompressedStringField: 12,
        UInt32Field: 13,
        SFixed32Field: 15,
        SFixed64Field: 16,
        # General Field part
        IntField: 3,
        BooleanField: 8,
        StringField: 9,
        DecimalField: 9,
        JsonField: 9,
    }
    MESSAGE = 11
    REFERENCE = 9

    # Local file descriptor library
    library = {}

    @classmethod
    def get_proto(cls, document_class: type, is_log_table: bool = False):
        """Get Proto Buf message class from document class

        Args:
            document_class: Document class
            is_log_table (bool): it is a log table, should add extra information

        Returns:
            message_class
        """
        label = document_class.__name__ if not is_log_table else document_class.__name__ + "Rlog"
        file_name = label.lower() + ".proto"

        if label in cls.library:
            file_desc = cls.library[label]
        else:
            data_desc = cls._doc_to_pb(label, document_class, is_log_table)
            file_desc = FileDescriptorProto(name=file_name, package="", syntax="proto3")
            file_desc.message_type.add().MergeFrom(data_desc)
            cls.library[label] = file_desc
        message_class = message_factory.GetMessages([file_desc])[label]
        return message_class

    @classmethod
    def _doc_to_pb(cls, label: str, document_class: type, is_log_table: bool = False):
        """Get protobuf descriptor from document class

        Args:
            label: top data class name
            document_class: Document class
            is_log_table (bool): it is a log table, should add extra information

        Returns:
            message descriptor
        """
        document_sample = document_class()
        fields, children, counter = [], [], 0
        for key in document_sample.__dir__():
            field = object.__getattribute__(document_sample, key)

            if not key.startswith("_") and isinstance(field, BaseField):
                if isinstance(field, EmbeddedDocumentField):
                    counter += 1
                    children.append(cls._doc_to_pb(key.title(), field.document_type_class))
                    fields.append(FieldDescriptorProto(name=key, number=counter, label=1, type=cls.MESSAGE,
                                                       type_name=".".join([label, key.title()])))
                elif isinstance(field, ListField):
                    if isinstance(field.field, EmbeddedDocumentField):
                        counter += 1
                        children.append(cls._doc_to_pb(key.title(), field.field.document_type_class))
                        fields.append(FieldDescriptorProto(name=key, number=counter, label=3, type=cls.MESSAGE,
                                                           type_name=".".join([label, key.title()])))
                    else:
                        for dict_class, field_type in cls.type_dict.items():
                            if isinstance(field.field, dict_class):
                                counter += 1
                                fields.append(FieldDescriptorProto(name=key, number=counter, label=3, type=field_type))
                                break
                else:
                    for dict_class, field_type in cls.type_dict.items():
                        if isinstance(field, dict_class):
                            counter += 1
                            fields.append(FieldDescriptorProto(name=key, number=counter, label=1, type=field_type))
                            break
        if is_log_table:  # Append Extra fields for log table:
            counter += 1
            fields.append(FieldDescriptorProto(name="_ins", number=counter, label=1,
                                               type=cls.type_dict[TimestampField]))
            counter += 1
            fields.append(FieldDescriptorProto(name="_op", number=counter, label=1, type=cls.type_dict[StringField]))
        descriptor = DescriptorProto(name=label.split(".")[-1], field=fields)
        for child in children:
            descriptor.nested_type.add().MergeFrom(child)
        return descriptor
