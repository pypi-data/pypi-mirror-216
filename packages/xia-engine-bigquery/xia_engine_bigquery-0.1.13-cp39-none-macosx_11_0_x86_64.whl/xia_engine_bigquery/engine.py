import json
import uuid
from typing import Type, Union
import time
from datetime import datetime, timezone, timedelta
import google.auth
from google.api_core.exceptions import PermissionDenied, NotFound, InvalidArgument, OutOfRange
from google.cloud import bigquery
from google.cloud import bigquery_storage_v1
from google.cloud.bigquery_storage_v1.types import WriteStream, AppendRowsRequest, ProtoSchema, ProtoRows
from google.cloud.bigquery_storage_v1.services.big_query_write import BigQueryWriteAsyncClient
from google.protobuf.descriptor_pb2 import DescriptorProto
from xia_easy_proto import EasyProto
from xia_fields import TimestampField, DateTimeField, TimeField
from xia_engine import Engine, BaseDocument, EmbeddedDocumentField, ListField
from xia_engine_bigquery.proto import DocToProto
from xia_engine_bigquery.schema import DocToSchema


class BigqueryEngine(Engine):
    """XIA Document Engine based on Bigquery

    """
    support_unknown = False  # Bigquery doesn't support unknown fields

    engine_param = "bigquery"
    engine_connector = engine_writer = bigquery.Client
    scan_and_fetch = True  # Scan and Fetch implemented

    default_dataset = "default"  #: Default dataset Name

    OPERATORS = {"__eq__": "=", "__lt__": "<", "__le__": "<=", "__gt__": ">", "__ge__": ">=", "__ne__": "!=",
                 "__in__": "IN", "__not_in__": "NOT IN"}

    TIME_PARTITION_CONFIG = {
        "day": bigquery.TimePartitioningType.DAY,
        "hour": bigquery.TimePartitioningType.HOUR,
        "month": bigquery.TimePartitioningType.MONTH
    }

    encoders = {
        TimestampField: lambda x: int(x*1000000),
        DateTimeField: lambda x: (datetime.utcfromtimestamp(0) + timedelta(seconds=x)).strftime('%Y-%m-%d %H:%M:%S.%f'),
        TimeField: lambda x: datetime.utcfromtimestamp(x).strftime('%H:%M:%S.%f')
    }

    decoders = {
        TimestampField: lambda x: float(x/1000000),
    }

    # Variable Name: @fields@, @table_name@, @where_condition@
    scan_sql_template = "SELECT {} FROM {} {} \nWHERE {} \n LIMIT {}"
    # Variable Name: @table_name, @key_fields, @log_table_name
    merge_sql_template = """
MERGE INTO `{}` AS origin
USING (
   SELECT * EXCEPT(_ins, _row_number) FROM (
         SELECT 
         *, ROW_NUMBER() OVER (PARTITION BY {} ORDER BY _ins DESC) as _row_number
         FROM `{}`
         WHERE {}
      ) WHERE _row_number = 1
) as log_table
ON {}
WHEN NOT MATCHED AND _op != 'D' THEN 
INSERT ({})
VALUES ({})
WHEN MATCHED AND _OP = 'D' THEN DELETE
WHEN MATCHED AND _OP != 'D' THEN 
UPDATE SET {}
    """

    @classmethod
    def connect(cls, document_class: Type[BaseDocument] = None):
        """Connect to the engine

        Args:
            document_class: (`subclass` of `BaseDocument`): Document definition

        Returns:
            Connection
        """
        address = document_class.get_address(cls) if document_class else None
        if not address:
            cls._database[""] = (
                cls.engine_connector(**cls.engine_default_connector_param),
                cls.engine_writer(**cls.engine_default_connector_param)
            )
            return cls._database[""]
        else:
            db_name = address.get("_db", "")
            connect_param = {k: v for k, v in address.items() if not k.startswith("_")}
            connect_param = cls.engine_default_connector_param if not connect_param else connect_param
            cls._database[db_name] = (
                cls.engine_connector(**connect_param),
                cls.engine_writer(**cls.engine_default_connector_param)
            )
            return cls._database[db_name]

    @classmethod
    def get_project_id(cls, document_class: Type[BaseDocument]):
        """Get project id and dataset id for the requested model

        Args:
            document_class: Document class

        Returns:
            project id and dataset id in a tuple
        """
        address = document_class.get_address(cls) if document_class else {}
        project_id = address.get("project", google.auth.default()[1])
        dataset_id = address.get("_dataset", cls.default_dataset)
        return project_id, dataset_id

    @classmethod
    def _get_proto_data(cls, message_class, payload: list):
        proto_descriptor = DescriptorProto()
        message_class().DESCRIPTOR.CopyToProto(proto_descriptor)
        proto_data = AppendRowsRequest.ProtoData({
            "rows": ProtoRows({"serialized_rows": payload}),
            "writer_schema": ProtoSchema(proto_descriptor=proto_descriptor)
        })
        return proto_data

    @classmethod
    def _write_insert(cls, writer, table_id: str, message_class, payload: list, offset: int = 0):
        """Write data to bigquery

        Args:
            writer: Bigquery Writer Client
            table_id (str): project_id.dataset_id.table_name
            message_class (type): Protobuf Message class
            payload (list): List of serialized protobuf message
            offset (int): offset to be used for exact once scenario
        """

    @classmethod
    def _sql_safe(cls, statement: str) -> str:
        return statement.replace(';', '')

    @classmethod
    def _get_sql_value_from_field_path(cls, document_class: Type[BaseDocument], field_path: str, value):
        """Get a quick map for mapping field name

        Args:
            document_class: Document class
            field_path: Field path "A.B.C.D"
            value: The value to be transformed
        """
        return value if isinstance(value, (int, float)) else "'" + value + "'"

    @classmethod
    def _get_scan_source_sql(cls, document_class: Type[BaseDocument], field_list: set):
        """Get Data Source Name

        Args:
            document_class: Document class
            field_list: The field list to be used for keys / scan criteria
        """
        source_sql_template = """(
   SELECT * EXCEPT(_ins, _op, _row_number) FROM (
      SELECT 
      *, ROW_NUMBER() OVER (PARTITION BY {} ORDER BY _ins DESC) as _row_number
      FROM (
         SELECT 
            {}, _ins, _op
            FROM {}
         UNION ALL
         SELECT
            {}, null as _ins, 'I' as _op
            FROM {}
      )
   ) WHERE _row_number = 1 AND _op != 'D'
)"""
        key_fields = document_class._key_fields
        extra_fields = [field for field in field_list if field not in key_fields]
        table_id = "`" + cls.get_bq_table_id(document_class, False) + "`"
        log_table_id = "`" + cls.get_bq_table_id(document_class, True) + "`"
        source_sql = source_sql_template.format(
            cls._sql_safe(", ".join(key_fields)),
            cls._sql_safe(", ".join(key_fields + extra_fields)),
            cls._sql_safe(log_table_id),
            cls._sql_safe(", ".join(key_fields + extra_fields)),
            cls._sql_safe(table_id),
        )
        return source_sql

    @classmethod
    def _get_unnest_sql(cls, document_class: Type[BaseDocument], field_list: set, current_path: str = ""):
        """Get unnest element of SQL

        Args:
            document_class: Document class
            current_path: current field path
        """
        unnest_list = []
        for field_name in [k for k in dir(document_class) if not k.startswith("_")]:
            field = getattr(document_class, field_name)
            if field_list and field_name not in field_list:
                continue
            if isinstance(field, EmbeddedDocumentField):
                new_path = ".".join(filter(None, [current_path, field_name]))
                unnest_list += cls._get_unnest_sql(field.document_type_class, set(), new_path)
            elif isinstance(field, ListField):
                if isinstance(field.field, EmbeddedDocumentField):
                    new_path = ".".join(filter(None, [current_path, field_name]))
                    unnest_path = new_path.replace(".", "__")
                    unnest_sql = f",\nUNNEST({new_path}) AS {unnest_path}"
                    unnest_list.append(unnest_sql)
                    unnest_list += cls._get_unnest_sql(field.field.document_type_class, set(), new_path)
                else:
                    unnest_sql = f",\nUNNEST({field_name}) AS {field_name}"
                    unnest_list.append(unnest_sql)
        return unnest_list

    @classmethod
    def scan(cls, _document_class: Type[BaseDocument], _acl_queries: list = None, _limit: int = 1000, **kwargs):
        db_con, _ = db_con, _ = cls.get_connection(_document_class)
        _acl_queries = [{}] if not _acl_queries else _acl_queries
        where_statements = ["1=1"]
        field_list = set()
        for key, value in kwargs.items():
            field, operator, order = cls.parse_search_option(key)
            field_list.add(field.split(".")[0])  # Only top level field picks
            sql_value = cls._get_sql_value_from_field_path(_document_class, field, value)
            comps = field.split(".")
            field = ".".join(filter(None, ["__".join(comps[:-1]), comps[-1]]))  # Bq specification: part1__part2.part3
            condition = " ".join([field, operator, sql_value])
            where_statements.append(condition)
        # _acl_query statements apply
        query_conditions = []
        for query in _acl_queries:
            conditions = []
            for key, value in query.items():
                field_list.add(key)
                sql_value = value if isinstance(value, (int, float)) else "'" + value + "'"
                conditions.append(f"{key} = {sql_value}")
            if conditions:
                query_conditions.append(" AND ".join(conditions))
        if query_conditions:
            where_statements.append(f"({' OR '.join(query_conditions)})")
        scan_statement = cls.scan_sql_template.format(
            cls._sql_safe("DISTINCT " + ", ".join(_document_class._key_fields)),
            cls._sql_safe(cls._get_scan_source_sql(_document_class, field_list)),
            cls._sql_safe("".join(cls._get_unnest_sql(_document_class, field_list))),
            cls._sql_safe(" AND ".join(where_statements)),
            cls._sql_safe(str(_limit))
        )
        query_job = db_con.query(scan_statement)
        result = [dict(row) for row in query_job]
        return [_document_class.dict_to_id(line) for line in result]

    @classmethod
    def search(cls, _document_class: Type[BaseDocument], *args, _acl_queries: list = None, _limit: int = 50, **kwargs):
        """It is a write-only engine, we don't support any search activities
        """
        return []

    @classmethod
    def get_table_info(cls, table_id: str):
        db_con, _ = cls.get_connection()
        try:
            table = db_con.get_table(table_id)
        except NotFound as e:
            table = None
        return table

    @classmethod
    def get_bq_table_id(cls, document_class: Type[BaseDocument], is_log_table: bool = False):
        """Get BigQuery Table ID

        Args:
            document_class (`BaseDocument`): Document class
            is_log_table (bool): it is a log table, should add extra information

        Returns
            table id as string (project.dataset.table)
        """
        table_name = document_class.get_collection_name(cls)
        project_id, dataset_id = cls.get_project_id(document_class)
        table_name = table_name if not is_log_table else table_name + "_rlog"
        table_id = ".".join([project_id, dataset_id, table_name])
        return table_id

    @classmethod
    def _insert_retry(cls, writer, retry: int, retry_reason: str, table_id, message_class, payload) -> bool:
        for _ in range(retry):
            time.sleep(1)
            try:
                cls._write_insert(writer, table_id, message_class, payload)
                return True
            except (InvalidArgument, PermissionDenied, NotFound, OutOfRange):
                print(f"{retry_reason}, wait 1 second")
        return False

    @classmethod
    def create_table(cls, document_class: Type[BaseDocument], is_log_table: bool = False):
        """Create table in Bigquery

        Args:
            document_class (`BaseDocument`): Document class
            is_log_table (bool): it is a log table, should add extra information
        """
        db_con, _ = cls.get_connection()
        table_schema = DocToSchema.get_schema_bq(document_class, is_log_table)
        table_id = cls.get_bq_table_id(document_class, is_log_table)

        new_table = bigquery.Table(table_id, table_schema)

        table_meta_data = document_class.get_meta_data()
        cluster_fields = table_meta_data.get("cluster_fields", {})
        partition_info = table_meta_data.get("partition_info", {})
        if cluster_fields:
            new_table.clustering_fields = cluster_fields
        if partition_info:
            if partition_info["type"] in cls.TIME_PARTITION_CONFIG:
                new_table.time_partitioning = bigquery.TimePartitioning(
                    type_=cls.TIME_PARTITION_CONFIG[partition_info["type"]],
                    field=partition_info["field"]
                )
        db_con.create_table(new_table, exists_ok=True)

    @classmethod
    def replicate(cls, document_class: Type[BaseDocument], task_list: list):
        """Data replication on Bigquery

        Big query is an append-only optimized database, so it is better to keep a log table aside.

        Args:
            document_class: Python class of document
            task_list:  List of dictionary with the following keys:
                * id: document id
                * content: document db form
                * op: operation type: "I" for insert, "D" for delete, "U" for update, "L" for load

        Returns:
            task_results: List of dictionary with the following keys:
                * id: document id
                * op: operation type: "I" for insert, "D" for delete, "U" for update, "L" for load
                * time: time when data is replicated
                * status: status code of HTTP protocol
        """
        db_con, db_writer = cls.get_connection()
        table_id = cls.get_bq_table_id(document_class, is_log_table=False)
        log_table_id = cls.get_bq_table_id(document_class, is_log_table=True)
        db_content_list = []
        task_result = [{"id": task.get("id", ""), "op": task["op"]} for task in task_list]
        for task in task_list:
            db_content = task["content"].copy()
            db_content.pop("_unknown", None)  # No unknown data store in bigquery
            db_content.pop("_id", None)  # No internal id store in bigquery
            db_content.update({
                "_ins": cls.encoders[TimestampField](datetime.now().timestamp()),  # Meet BQ format
                "_op": task["op"]
            })
            db_content_list.append(db_content)
        message_class = DocToProto.get_proto(document_class, is_log_table=True)
        _, payload = EasyProto.serialize(db_content_list, message_class=message_class)
        task_status, task_msg = 200, ""
        try:
            cls._write_insert(db_writer, log_table_id, message_class, payload)
        except Exception as e:
            log_table_info = cls.get_table_info(log_table_id)
            if log_table_info is None:
                # Case 1: Table doesn't exist
                cls.create_table(document_class, is_log_table=True)
                # Case 1.1: Also need to create original table
                table_info = cls.get_table_info(table_id)
                if table_info is None:
                    cls.create_table(document_class)
                # Retry to insert retry
                done = cls._insert_retry(db_writer, 120, "Table not yet created", log_table_id, message_class, payload)
            else:
                log_table_schema = DocToSchema.get_schema_bq(document_class, is_log_table=True)
                log_bq_fields = DocToSchema.get_schema_fields(log_table_info.schema)
                log_table_fields = DocToSchema.get_schema_fields(log_table_schema)
                if log_bq_fields.issubset(log_table_fields):
                    # Case 2: Need to extend schema
                    log_table_info.schema = log_table_schema
                    db_con.update_table(log_table_info, ["schema"])
                    # Case 2.1: Also need to extend schema of original schema
                    table_info = cls.get_table_info(table_id)
                    table_schema = DocToSchema.get_schema_bq(document_class)
                    table_info.schema = table_schema
                    db_con.update_table(table_info, ["schema"])
                    # Retry to insert retry
                    done = cls._insert_retry(db_writer, 120, "Field not yet added",
                                             log_table_id, message_class, payload)
                elif log_table_fields.issubset(log_bq_fields):
                    # Case 3: Compatible schema so we will retry 6 times
                    done = cls._insert_retry(db_writer, 6, "Standard Retry", log_table_id, message_class, payload)
                else:
                    done = True  # Known error
                    task_status = 400  # Document type is not good
                    task_msg = f"Document definition is different than {log_table_id}"
            if not done:  # Error is not recoverable
                task_status = 500  # Document type is not good
                task_msg = str(e)
        # Update task result
        for task in task_result:
            task["status"] = task_status
            task["msg"] = task_msg
        return task_result

    @classmethod
    def merge(cls, document_class: Type[BaseDocument], start: float = None, end: float = None,
              purge: bool = False, criteria: dict = None):
        db_con, _ = db_con, _ = cls.get_connection(document_class)
        criteria = {} if not criteria else criteria
        key_fields = document_class.get_meta_data()["key_fields"]
        stateful_fields = [k for k, v in document_class.get_all_fields().items() if v.stateful]
        no_key_fields = [k for k in stateful_fields if k not in key_fields]
        src_where_statements = [f"origin.{key} = log_table.{key}" for key in key_fields]
        log_where_statements = ["1=1"]
        purge_where_statements = ["1=1"]
        for key, value in criteria.items():
            field, operator, order = cls.parse_search_option(key)
            if "." in field:
                continue  # Only supporting top level
            sql_value = cls._get_sql_value_from_field_path(document_class, field, value)
            src_where_statements.append(" ".join([f"origin.{field}", operator, sql_value]))
            log_where_statements.append(" ".join([field, operator, sql_value]))
            purge_where_statements.append(" ".join([field, operator, sql_value]))
        purge_state = "NONE"
        # Step 1: Purge data if needed
        if purge and start:  # Only purge the historical data
            purge_sql_template = "DELETE FROM `{}` WHERE {}"
            if isinstance(start, (int, float)):
                purge_where_statements.append(f"_ins < TIMESTAMP_MICROS({int(start * 1000000)})")
            purge_statement = purge_sql_template.format(
                cls._sql_safe(cls.get_bq_table_id(document_class, True)),
                cls._sql_safe(" AND ".join(purge_where_statements))
            )
            query_job = db_con.query(purge_statement)
            query_job.result()
            purge_state = query_job.state
        # Step 2: Do merge job
        if isinstance(start, (int, float)):
            log_where_statements.append(f"_ins >= TIMESTAMP_MICROS({int(start * 1000000)})")
        if isinstance(end, (int, float)):
            log_where_statements.append(f"_ins <= TIMESTAMP_MICROS({int(end * 1000000)})")
        merge_statement = cls.merge_sql_template.format(
            cls._sql_safe(cls.get_bq_table_id(document_class, False)),
            cls._sql_safe(", ".join(key_fields)),
            cls._sql_safe(cls.get_bq_table_id(document_class, True)),
            cls._sql_safe(" AND ".join(log_where_statements)),
            cls._sql_safe("\nAND ".join(src_where_statements)),
            cls._sql_safe(", ".join(stateful_fields)),
            cls._sql_safe(", ".join(stateful_fields)),
            cls._sql_safe(", \n".join([f"origin.{key} = log_table.{key}" for key in no_key_fields]))
        )
        query_job = db_con.query(merge_statement)
        query_job.result()
        merge_result = {
            "data_model": document_class.__name__,
            "state": query_job.state,
            "purge_state": purge_state,
            "start": start if isinstance(start, (int, float)) else None,
            "end": end if isinstance(end, (int, float)) else None,
            "billed_bytes": query_job.total_bytes_billed,
            "slot_time_ms": int(query_job.slot_millis),
            "started_dt": query_job.started.strftime("%Y-%m-%dT%H:%M:%S"),
            "ended_dt": query_job.ended.strftime("%Y-%m-%dT%H:%M:%S"),
            "duration_ms": int((query_job.ended.timestamp() - query_job.started.timestamp()) * 1000),
            "processed_bytes": query_job.total_bytes_processed,
        }
        return merge_result

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None):
        """Create the document in Bigquery

        Args:
            document_class: Document class
            db_content: database content
            doc_id: provided document id

        Notes:
            If table doesn't exist, the target table will be created automatically
        """
        db_con, db_writer = cls.get_connection()
        db_content.pop("_unknown", None)  # No unknown data store in bigquery
        db_content.pop("_id", None)  # No internal id store in bigquery
        table_id = cls.get_bq_table_id(document_class, is_log_table=False)
        message_class = DocToProto.get_proto(document_class)
        _, payload = EasyProto.serialize(db_content, message_class=message_class)
        try:
            cls._write_insert(db_writer, table_id, message_class, payload)
        except Exception as e:
            table_info = cls.get_table_info(table_id)
            if table_info is None:
                # Case 1: Table doesn't exist
                cls.create_table(document_class)
                done = cls._insert_retry(db_writer, 120, "Table not yet created", table_id, message_class, payload)
            else:
                table_schema = DocToSchema.get_schema_bq(document_class)
                bq_fields = DocToSchema.get_schema_fields(table_info.schema)
                table_fields = DocToSchema.get_schema_fields(table_schema)
                if bq_fields.issubset(table_fields):
                    # Case 2: Need to extend schema
                    table_info.schema = table_schema
                    db_con.update_table(table_info, ["schema"])
                    done = cls._insert_retry(db_writer, 120, "Field not yet added", table_id, message_class, payload)
                elif table_fields.issubset(bq_fields):
                    # Case 3: Compatible schema so we will retry 6 times
                    done = cls._insert_retry(db_writer, 6, "Standard Retry", table_id, message_class, payload)
                else:
                    raise TypeError(f"Document definition is different than {table_id}")
            if not done:
                # Error is not recovered
                raise e
        # Return document id or a random id
        return str(uuid.uuid4()) if doc_id is None else doc_id

    @classmethod
    def drop(cls, document_class: Type[BaseDocument]):
        db_con, _ = cls.get_connection()
        table_id = cls.get_bq_table_id(document_class, is_log_table=False)
        log_table_id = cls.get_bq_table_id(document_class, is_log_table=True)
        db_con.delete_table(table_id, not_found_ok=True)
        db_con.delete_table(log_table_id, not_found_ok=True)


class BigqueryWriteEngine(BigqueryEngine):
    """Bigquery Engine Writer Using Exact-Once strategy"""
    engine_writer = bigquery_storage_v1.BigQueryWriteClient

    @classmethod
    def _get_write_stream(cls, writer, table_id: str):
        write_path = writer.table_path(*table_id.split("."))
        write_stream = WriteStream()
        write_stream.type_ = WriteStream.Type.COMMITTED
        return writer.create_write_stream(parent=write_path, write_stream=write_stream).name

    @classmethod
    def _write_insert(cls, writer, table_id, message_class, payload, offset: int = 0):
        stream_name = cls._get_write_stream(writer, table_id)
        proto_data = cls._get_proto_data(message_class, payload)
        append_request = AppendRowsRequest({"offset": offset, "write_stream": stream_name, "proto_rows": proto_data})
        writer.append_rows(iter([append_request]))


class BigqueryStreamEngine(BigqueryWriteEngine):
    @classmethod
    def _get_write_stream(cls, writer, table_id: str):
        return writer.write_stream_path(*table_id.split("."), "_default")

    @classmethod
    def _write_insert(cls, writer, table_id, message_class, payload, offset: int = 0):
        stream_name = cls._get_write_stream(writer, table_id)
        proto_data = cls._get_proto_data(message_class, payload)
        append_request = AppendRowsRequest({"write_stream": stream_name, "proto_rows": proto_data})
        writer.append_rows(iter([append_request]))


class BigqueryAppendOnlyEngine(BigqueryStreamEngine):
    @classmethod
    def _get_scan_source_sql(cls, document_class: Type[BaseDocument], field_list: set):
        return "`" + cls.get_bq_table_id(document_class, False) + "`"

    @classmethod
    def replicate(cls, document_class: Type[BaseDocument], task_list: list):
        task_result = []
        for task in [item for item in task_list if item["op"] in ["I", "L"]]:
            # AppendOnly Engine do not support update or delete operation
            try:
                cls.create(document_class, task["content"])
                task_result.append({"id": task["id"], "op": task["op"],
                                    "time": datetime.now().timestamp(), "status": 200})
            except Exception as e:
                task_result.append({"id": task["id"], "op": task["op"], "msg": str(e),
                                    "time": datetime.now().timestamp(), "status": 500})
        return task_result

    @classmethod
    def merge(cls, document_class: Type[BaseDocument], start: float = None, end: float = None,
              purge: bool = False, criteria: dict = None):
        # AppendOnly merge doesn't need to be merged
        return {"state": "DONE"}


class BigqueryAsyncWriteEngine(BigqueryEngine):
    """Bigquery Engine Writer Using Streaming strategy"""
    engine_writer = BigQueryWriteAsyncClient

    @classmethod
    def _get_write_stream(cls, writer, table_id: str):
        return writer.write_stream_path(*table_id.split("."), "_default")

    @classmethod
    async def _async_insert(cls, writer, table_id: str, message_class, payload, offset: int):
        stream_name = cls._get_write_stream(writer, table_id)
        proto_data = cls._get_proto_data(message_class, payload)
        append_request = AppendRowsRequest({"offset": offset, "write_stream": stream_name, "proto_rows": proto_data})
        result = await writer.append_rows(iter([append_request]))
        async for _ in result:
            pass  # Get the job done


class BigqueryBatchEngine(BigqueryWriteEngine):
    """Bigquery Engine Writer Using Batch strategy

    """

    @classmethod
    def _get_write_stream(cls, writer, table_id: str):
        write_path = writer.table_path(*table_id.split("."))
        write_stream = WriteStream()
        write_stream.type_ = WriteStream.Type.PENDING
        return writer.create_write_stream(parent=write_path, write_stream=write_stream)

    @classmethod
    def _write_insert(cls, writer, table_id, message_class, payload, offset: int = 0):
        """

        Args:
            writer:
            table_id:
            message_class:
            payload:
            offset:

        Returns:

        """
        """
        write_client = cls.get_writer()
        write_path = write_client.table_path(*table_id.split("."))
        write_stream = types.WriteStream()
        write_stream.type_ = types.WriteStream.Type.PENDING
        write_stream = write_client.create_write_stream(parent=write_path, write_stream=write_stream)
        stream_name = write_stream.name
        print(stream_name)

        request_template = types.AppendRowsRequest()
        request_template.write_stream = stream_name

        proto_schema = types.ProtoSchema()
        proto_descriptor = descriptor_pb2.DescriptorProto()
        message_class().DESCRIPTOR.CopyToProto(proto_descriptor)
        proto_schema.proto_descriptor = proto_descriptor

        proto_data = types.AppendRowsRequest.ProtoData()
        proto_data.writer_schema = proto_schema
        request_template.proto_rows = proto_data
        append_rows_stream = writer.AppendRowsStream(write_client, request_template)

        proto_rows = types.ProtoRows()
        for serialized_line in payload:
            proto_rows.serialized_rows.append(serialized_line)

        request = types.AppendRowsRequest()
        request.offset = 0
        proto_data = types.AppendRowsRequest.ProtoData()
        proto_data.rows = proto_rows
        request.proto_rows = proto_data

        response_future_1 = append_rows_stream.send(request)

        print(response_future_1.result())

        append_rows_stream.close()

        write_client.finalize_write_stream(name=write_stream.name)

        batch_commit_write_streams_request = BatchCommitWriteStreamsRequest()
        batch_commit_write_streams_request.parent = write_path
        batch_commit_write_streams_request.write_streams = [write_stream.name]
        write_client.batch_commit_write_streams(batch_commit_write_streams_request)

        print(f"Writes to stream: '{write_stream.name}' have been committed.")
        """
