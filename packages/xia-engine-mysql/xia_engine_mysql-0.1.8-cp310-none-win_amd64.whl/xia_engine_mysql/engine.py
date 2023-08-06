from typing import Type
import datetime
import time
import pymysql
from xia_engine import BaseDocument
from xia_engine_sql import SqlEngine
from xia_fields import BaseField
from xia_fields import BooleanField, FloatField, StringField, ByteField, IntField, DecimalField, DateTimeField
from xia_fields import UInt64Field, Int64Field, OsEnvironField
from xia_fields import JsonField, TimestampField, DateField, TimeField, CompressedStringField
from xia_engine import Engine, RamEngine, BaseDocument, BaseEmbeddedDocument, EmbeddedDocument


class MysqlConnectParam(EmbeddedDocument):
    host = StringField(description="Host name of connection")
    port = IntField(description="MySQL port to use", default=3306)
    user = StringField(description="Database User name")
    database = StringField(description="Database name")
    password = OsEnvironField(description="OS Environment Variable which holds password")


class MysqlEngine(SqlEngine):
    """SQLite Engine

    Connection Parameters:
        * Should be hold in the class attribute class._sqlite = {"db": "", "path": ""}
            * db: Database name, default database name is ""
            * kwarg: Where the database should be stored, default is in memory
    """
    engine_param = "mysql"
    engine_connector = pymysql.connect
    lq = '`'
    rq = '`'

    # Simple Dictionary Match
    type_dict = {
        # Extension Type Part
        TimestampField: "TIMESTAMP",
        DateField: "DATE",
        TimeField: "TIME",
        DateTimeField: "DATETIME",
        Int64Field: "BIGINT",
        UInt64Field: "BIGINT",
        # Generic Type Part
        FloatField: "FLOAT",
        IntField: "INTEGER",
        DecimalField: "DOUBLE",
        BooleanField: "BOOL",
        StringField: "TEXT",
        CompressedStringField: "MEDIUMBLOB",
        ByteField: "MEDIUMBLOB",
        JsonField: "JSON",
    }

    # Encoder / Decoder
    encoders = {
        DecimalField: lambda x: x,
        DateField: lambda x: datetime.datetime.fromtimestamp(x * 86400).strftime("%Y-%m-%d"),
        TimestampField: lambda x: datetime.datetime.fromtimestamp(x).isoformat(),
        DateTimeField: lambda x: datetime.datetime.fromtimestamp(x).isoformat(),
        TimeField: lambda x: datetime.datetime.fromtimestamp(x + 2 * time.timezone).time().isoformat()
    }

    decoders = {
        DecimalField: lambda x: x,
        TimestampField: lambda x: x.timestamp(),
        TimeField: lambda x: x.seconds + x.microseconds / 1000000
    }

    # IF NOT EXISTS key word supports ignore table already exists error
    create_sql_template = "CREATE TABLE IF NOT EXISTS {} ( {}, PRIMARY KEY( {} ))"
    # IF EXISTS key word supports drop an not-existed table
    drop_sql_template = "DROP TABLE IF EXISTS {}"

    @classmethod
    def _create_sql_field_list(cls, field_dict: dict):
        field_types = []
        for field_name, field_info in field_dict.items():
            field_type = field_info["type"]
            if isinstance(field_info["info"], StringField):
                max_length = field_info["info"].estimate_max_length()
                if field_info["info"].max_length is not None or field_info.get("key", False):
                    field_type = "VARCHAR (" + str(max_length) + ")"
                elif max_length < 2 ** 8:
                    field_type = "TINYTEXT"
                elif max_length < 2 ** 16:
                    field_type = "TEXT"
                elif max_length < 2 ** 24:
                    field_type = "MEDIUMTEXT"
                else:
                    field_type = "LONGTEXT"
            elif isinstance(field_info["info"], DecimalField):
                precision = field_info["info"].precision
                field_type = "DOUBLE (" + str(34 - precision) + "," + str(precision) + ")"
            field_line_list = ['`' + cls._sql_safe(field_name) + '` ' + field_type]
            if field_info["info"].default is not None:
                if isinstance(field_info["info"].default, str):
                    field_line_list.append("DEFAULT ('" + cls._sql_safe(field_info["info"].default) + "')")
                elif isinstance(field_info["info"].default, (int, float)):
                    field_line_list.append("DEFAULT " + str(field_info["info"].default))
            field_line = ' '.join(field_line_list)
            field_types.append(field_line)
        return field_types

    @classmethod
    def _create(cls, db_con: pymysql.Connection, document_class: Type[BaseDocument], db_content: dict):
        sql_model, data_model = cls._parse_sql_model(document_class)
        data_content = {document_class.get_collection_name(): []}
        data_content = cls.parse_data(db_content, data_model[""], {}, data_content)
        for table_name, insert_content in data_content.items():
            table_model = sql_model[table_name]
            insert_statement = cls._get_insert_sql(table_name, table_model)
            insert_content = [cls._fill_null_line(line, list(table_model)) for line in data_content[table_name]]
            cur = db_con.cursor()
            try:
                cur.executemany(insert_statement, insert_content)
            except (pymysql.err.ProgrammingError, pymysql.err.OperationalError) as e:
                if "doesn't exist" in e.args[1] and "Table" in e.args[1]:
                    # Crisis 1: No table found, so we need to add a table
                    cls.create_table(table_name, sql_model[table_name], document_class)
                    cur.executemany(insert_statement, insert_content)
                elif "Unknown column" in e.args[1]:
                    # Crisis 2: Some extra column found
                    for column_info in cls._create_sql_field_list(sql_model[table_name]):
                        add_col_statement = cls.add_column_sql_template.format(
                            cls._sql_safe(table_name),
                            cls._sql_safe(column_info)
                        )
                        try:
                            cur.execute(add_col_statement)
                        except pymysql.err.OperationalError:
                            pass
                    cur.executemany(insert_statement, insert_content)
                else:
                    raise e
            cur.close()
        key_fields = document_class.get_meta_data()["key_fields"]
        key_values = {key: db_content[key] for key in key_fields}

        return document_class.dict_to_id(key_values)

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None):
        db_con = cls.get_connection(document_class)
        doc_id = cls._create(db_con, document_class, db_content)
        db_con.commit()  # Commit at the end
        return doc_id
