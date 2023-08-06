import json
from typing import Union
from google.cloud.bigquery import SchemaField
from functools import lru_cache
from xia_fields import BaseField
from xia_fields import BooleanField, FloatField, StringField, ByteField, IntField, DecimalField, DateTimeField
from xia_fields import JsonField, TimestampField, DateField, TimeField, CompressedStringField
from xia_engine import Document, EmbeddedDocument, EmbeddedDocumentField, ListField, ExternalField


class DocToSchema:
    """XIA Document to Bigquery Json Schema"""
    # Simple Dictionary Match
    type_dict = {
        # Extension Type Part
        TimestampField: "TIMESTAMP",
        DateField: "DATE",
        TimeField: "TIME",
        DateTimeField: "DATETIME",
        # Generic Type Part
        FloatField: "FLOAT",
        IntField: "INTEGER",
        DecimalField: "BIGNUMERIC",
        BooleanField: "BOOLEAN",
        StringField: "STRING",
        CompressedStringField: "BYTES",
        ByteField: "BYTES",
        JsonField: "JSON",
    }

    @classmethod
    def get_field_json(cls, key: str, field: BaseField) -> Union[dict, None]:
        """Get field basic description in json

        Args:
            key: field's given name
            field: field instance

        Returns:
            python dictionary, None means not supported field (External field for example)
        """
        field_definition = {
            "name": key,
            "mode": "REQUIRED" if field.required else "NULLABLE",
            "description": field.description if field.description else ""
        }
        if isinstance(field, ListField):
            field_definition["mode"] = "REPEATED"
            item_field = field.field
            if isinstance(item_field, EmbeddedDocumentField):
                field_definition["fields"] = cls.get_schema_json(item_field.document_type_class)
                field_definition["type"] = "RECORD"
            else:
                for dict_class, field_type in cls.type_dict.items():
                    if isinstance(item_field, dict_class):
                        field_definition["type"] = field_type
                        break
        else:
            if isinstance(field, EmbeddedDocumentField):
                field_definition["fields"] = cls.get_schema_json(field.document_type_class)
                field_definition["type"] = "RECORD"
            elif isinstance(field, ExternalField):
                return
            else:
                for dict_class, field_type in cls.type_dict.items():
                    if isinstance(field, dict_class):
                        field_definition["type"] = field_type
                        break
        return field_definition

    @classmethod
    @lru_cache(maxsize=1024)
    def get_schema_json(cls, document_class: type):
        """Get Bigquery Schema from document class

        Args:
            document_class: Document class

        Returns:
            Big query schema definition in python list
        """
        document_sample = document_class()
        fields = []
        for key in document_sample.__dir__():
            field = object.__getattribute__(document_sample, key)
            if not key.startswith("_") and isinstance(field, BaseField):
                field_json = cls.get_field_json(key, field)
                if field_json:
                    fields.append(cls.get_field_json(key, field))
        return fields

    @classmethod
    def json_to_schema(cls, json_schema: list) -> list:
        """Get field basic description in json

        Args:
            json_schema: json schema list

        Returns:
            SchemaField List
        """
        bq_schema = []
        for field_schema in json_schema:
            field_schema = field_schema.copy()
            if "fields" in field_schema:
                field_schema["fields"] = cls.json_to_schema(field_schema.pop("fields"))
            field_name = field_schema.pop("name")
            field_type = field_schema.pop("type")
            bq_schema.append(SchemaField(field_name, field_type, **field_schema))
        return bq_schema

    @classmethod
    def get_schema_bq(cls, document_class: type, is_log_table: bool = False):
        """Get Bigquery Schema from document class

        Args:
            document_class: Document class
            is_log_table (bool): it is a log table, should add extra information

        Returns:
            Big query schema definition
        """
        schema_json = cls.get_schema_json(document_class).copy()  #: result return by lru cache is mutable
        if is_log_table:  # Adding extra information for log table
            schema_json.append({"name": "_ins", "type": "TIMESTAMP", "mode": "NULLABLE", "description": "Insert ts"})
            schema_json.append({"name": "_op", "type": "STRING", "mode": "NULLABLE", "description": "Operation Type"})
        return cls.json_to_schema(schema_json)

    @classmethod
    def get_schema_fields(cls, bq_schema: list, path: str = "root") -> set:
        """Get field list of a Big Query Schema

        Args:
            bq_schema (list): Big query schema definition
            path (str): parent path prefix

        Returns:
            set of fields
        """
        result = set()
        for field_schema in bq_schema:
            if field_schema.fields:
                result |= cls.get_schema_fields(field_schema.fields, path + "." + field_schema.name)
            else:
                result.add(path + "." + field_schema.name)
        return result

