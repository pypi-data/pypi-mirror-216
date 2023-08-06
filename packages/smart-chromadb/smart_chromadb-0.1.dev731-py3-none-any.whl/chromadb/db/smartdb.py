# type: ignore
from chromadb.config import System
from chromadb.api.types import Documents, Embeddings, IDs, Metadatas
from chromadb.db.clickhouse import (
    Clickhouse,
    db_schema_to_keys,
)
from typing import List, Optional, Sequence
import pandas as pd
import json
import uuid
import logging
from uuid import UUID
from overrides import override
from chromadb.api.types import Metadata
from smart_chart.common.connect_db import DB_conn

logger = logging.getLogger(__name__)


class StarRocksDB(Clickhouse):
    _conn: object

    def __init__(self, system: System):
        self._conn = DB_conn()
        self._settings = system.settings
        self._settings.require("db_config")
        connect_dict = self._settings.db_config
        connect_dict['dbtype'] = 'starrocks'
        self._connect_dict = connect_dict
        self._create_table_collections(None)
        self._create_table_embeddings(None)
        self._settings = system.settings
        self._load_dict = None
        load_host = self._connect_dict.get('load_host')
        if load_host:
            self._load_dict = {**connect_dict, 'host': load_host}
        self._dependencies = set()

    def _execute_sql(self, sql):
        return self._conn.execute_sql_list([sql], self._connect_dict)

    def _execute_load(self, contents, table):
        if self._load_dict:
            table = f"{self._connect_dict['db']}.{table}"
            contents[0][0] = '__' + contents[0][0]
            self._conn.insert_contents(contents, table, 100, self._load_dict)
        else:
            table = f"{table}({','.join(contents[0])})"
            contents = contents[1:]
            self._conn.insert_contents_mysql(contents, table, 100, self._connect_dict)

    @override
    def _create_table_collections(self, conn):
        sql = """CREATE TABLE IF NOT EXISTS collections (
            uuid String, name String, metadata String
        )PRIMARY KEY (uuid) comment 'collections' DISTRIBUTED BY HASH(uuid) BUCKETS 12 """
        self._execute_sql(sql)

    # duckdb has different types, so we want to convert the clickhouse schema to duckdb schema
    @override
    def _create_table_embeddings(self, conn):
        sql = """CREATE TABLE IF NOT EXISTS embeddings(uuid String, collection_uuid String, embedding Array<FLOAT>, document String, id String, metadata String)
        PRIMARY KEY (uuid) comment 'embeddings' DISTRIBUTED BY HASH(uuid) BUCKETS 12"""
        self._execute_sql(sql)

    #  UTILITY METHODS
    #
    @override
    def get_collection_uuid_from_name(self, collection_name: str) -> UUID:
        sql = f"SELECT uuid FROM collections WHERE name = {collection_name}"
        return self._execute_sql(sql)[1][0]

    #
    #  COLLECTION METHODS
    #
    @override
    def create_collection(
            self,
            name: str,
            metadata: Optional[Metadata] = None,
            get_or_create: bool = False,
    ) -> Sequence:
        # poor man's unique constraint
        dupe_check = self.get_collection(name)
        if len(dupe_check) > 0:
            if get_or_create is True:
                if dupe_check[0][2] != metadata:
                    self.update_collection(
                        dupe_check[0][0], new_name=name, new_metadata=metadata
                    )
                    dupe_check = self.get_collection(name)

                logger.info(
                    f"collection with name {name} already exists, returning existing collection"
                )
                return dupe_check
            else:
                raise ValueError(f"Collection with name {name} already exists")

        collection_uuid = uuid.uuid4()
        sql = f"""INSERT INTO collections (uuid, name, metadata) VALUES ('{collection_uuid}','{name}','{json.dumps(metadata)}')"""
        self._execute_sql(sql)
        return [[str(collection_uuid), name, metadata]]

    @override
    def get_collection(self, name: str) -> Sequence:
        sql = f"""SELECT * FROM collections WHERE name = '{name}'"""
        res = self._execute_sql(sql)[1:]
        # json.loads the metadata
        return [[x[0], x[1], json.loads(x[2])] for x in res]

    @override
    def get_collection_by_id(self, collection_uuid: str):
        sql = f"""SELECT * FROM collections WHERE uuid = '{collection_uuid}'"""
        res = self._execute_sql(sql)[1]
        return [res[0], res[1], json.loads(res[2])]

    @override
    def list_collections(self) -> Sequence:
        sql = f"""SELECT * FROM collections"""
        res = self._execute_sql(sql)[1:]
        return [[x[0], x[1], json.loads(x[2])] for x in res]

    @override
    def delete_collection(self, name: str):
        collection_uuid = self.get_collection_uuid_from_name(name)
        sql = f"""DELETE FROM embeddings WHERE collection_uuid = '{collection_uuid}'"""
        self._execute_sql(sql)
        sql = f"""DELETE FROM collections WHERE name = '{name}'"""
        self._execute_sql(sql)

    @override
    def update_collection(
            self,
            id: UUID,
            new_name: Optional[str] = None,
            new_metadata: Optional[Metadata] = None,
    ):
        if new_name is not None:
            dupe_check = self.get_collection(new_name)
            if len(dupe_check) > 0 and dupe_check[0][0] != str(id):
                raise ValueError(f"Collection with name {new_name} already exists")

            sql = f"""UPDATE collections SET name = '{new_name}' WHERE uuid = '{id}'"""
            self._execute_sql(sql)

        if new_metadata is not None:
            sql = f"""UPDATE collections SET metadata = '{json.dumps(new_metadata)}' WHERE uuid = '{id}'"""
            self._execute_sql(sql)

    #
    #  ITEM METHODS
    #
    # the execute many syntax is different than clickhouse, the (?,?) syntax is different than clickhouse
    @override
    def add(self, collection_uuid, embeddings, metadatas, documents, ids) -> List[UUID]:
        data_to_insert = [
            [
                str(collection_uuid),
                str(uuid.uuid4()),
                str(embedding),
                json.dumps(metadatas[i]) if metadatas else '',
                documents[i] if documents else '',
                ids[i],
            ]
            for i, embedding in enumerate(embeddings)
        ]

        insert_string = "collection_uuid, uuid, embedding, metadata, document, id"
        data_to_insert = [insert_string.split(',')] + data_to_insert
        self._execute_load(data_to_insert, 'embeddings')
        return [uuid.UUID(x[1]) for x in data_to_insert[1:]]  # return uuids

    @override
    def count(self, collection_id: UUID) -> int:
        where_string = f"WHERE collection_uuid = '{collection_id}'"
        sql = f"SELECT COUNT(*) FROM embeddings {where_string}"
        return self._execute_sql(sql)[1][0]

    @override
    def _format_where(self, where, result):
        for key, value in where.items():
            # Shortcut for $eq
            if type(value) == str:
                result.append(f" get_json_string(metadata,'$.{key}') = '{value}'")
            if type(value) == int:
                result.append(
                    f" CAST(get_json_string(metadata,'$.{key}') AS INT) = {value}"
                )
            if type(value) == float:
                result.append(
                    f" CAST(get_json_string(metadata,'$.{key}') AS DOUBLE) = {value}"
                )
            # Operator expression
            elif type(value) == dict:
                operator, operand = list(value.items())[0]
                if operator == "$gt":
                    result.append(
                        f" CAST(get_json_string(metadata,'$.{key}') AS DOUBLE) > {operand}"
                    )
                elif operator == "$lt":
                    result.append(
                        f" CAST(get_json_string(metadata,'$.{key}') AS DOUBLE) < {operand}"
                    )
                elif operator == "$gte":
                    result.append(
                        f" CAST(get_json_string(metadata,'$.{key}') AS DOUBLE) >= {operand}"
                    )
                elif operator == "$lte":
                    result.append(
                        f" CAST(get_json_string(metadata,'$.{key}') AS DOUBLE) <= {operand}"
                    )
                elif operator == "$ne":
                    if type(operand) == str:
                        return result.append(
                            f" get_json_string(metadata,'$.{key}') != '{operand}'"
                        )
                    return result.append(
                        f" CAST(get_json_string(metadata,'$.{key}') AS DOUBLE) != {operand}"
                    )
                elif operator == "$eq":
                    if type(operand) == str:
                        return result.append(
                            f" get_json_string(metadata,'$.{key}') = '{operand}'"
                        )
                    return result.append(
                        f" CAST(get_json_string(metadata,'$.{key}') AS DOUBLE) = {operand}"
                    )
                else:
                    raise ValueError(f"Operator {operator} not supported")
            elif type(value) == list:
                all_subresults = []
                for subwhere in value:
                    subresults = []
                    self._format_where(subwhere, subresults)
                    all_subresults.append(subresults[0])
                if key == "$or":
                    result.append(f"({' OR '.join(all_subresults)})")
                elif key == "$and":
                    result.append(f"({' AND '.join(all_subresults)})")
                else:
                    raise ValueError(
                        f"Operator {key} not supported with a list of where clauses"
                    )

    @override
    def _format_where_document(self, where_document, results):
        operator = list(where_document.keys())[0]
        if operator == "$contains":
            results.append(f"position('{where_document[operator]}' in document) > 0")
        elif operator == "$and" or operator == "$or":
            all_subresults = []
            for subwhere in where_document[operator]:
                subresults = []
                self._format_where_document(subwhere, subresults)
                all_subresults.append(subresults[0])
            if operator == "$or":
                results.append(f"({' OR '.join(all_subresults)})")
            if operator == "$and":
                results.append(f"({' AND '.join(all_subresults)})")
        else:
            raise ValueError(f"Operator {operator} not supported")

    @override
    def _get(self, where, columns: Optional[List] = None):
        select_columns = db_schema_to_keys() if columns is None else columns
        sql = f"""SELECT {",".join(select_columns)} FROM embeddings {where}"""
        val = self._execute_sql(sql)[1:]
        for i in range(len(val)):
            val[i] = list(val[i])
            if "collection_uuid" in select_columns:
                collection_uuid_column_index = select_columns.index("collection_uuid")
                val[i][collection_uuid_column_index] = uuid.UUID(
                    val[i][collection_uuid_column_index]
                )
            if "uuid" in select_columns:
                uuid_column_index = select_columns.index("uuid")
                val[i][uuid_column_index] = uuid.UUID(val[i][uuid_column_index])
            if "metadata" in select_columns:
                metadata_column_index = select_columns.index("metadata")
                val[i][metadata_column_index] = (
                    json.loads(val[i][metadata_column_index])
                    if val[i][metadata_column_index]
                    else None
                )

        return val

    #:TODO 还没转化, 尽量不用 update
    @override
    def _update(
            self,
            collection_uuid,
            ids: IDs,
            embeddings: Optional[Embeddings],
            metadatas: Optional[Metadatas],
            documents: Optional[Documents],
    ):
        update_data = []
        for i in range(len(ids)):
            data = []
            update_data.append(data)
            if embeddings is not None:
                data.append(embeddings[i])
            if metadatas is not None:
                data.append(json.dumps(metadatas[i]))
            if documents is not None:
                data.append(documents[i])
            data.append(ids[i])

        update_fields = []
        if embeddings is not None:
            update_fields.append("embedding = ?")
        if metadatas is not None:
            update_fields.append("metadata = ?")
        if documents is not None:
            update_fields.append("document = ?")

        update_statement = f"""
        UPDATE
            embeddings
        SET
            {", ".join(update_fields)}
        WHERE
            id = ? AND
            collection_uuid = '{collection_uuid}';
        """
        self._conn.executemany(update_statement, update_data)

    @override
    def _delete(self, where_str: Optional[str] = None) -> List:
        sql = f"""SELECT uuid FROM embeddings {where_str}"""
        uuids_deleted = self._execute_sql(sql)[1:]
        sql = f"""DELETE FROM embeddings {where_str}"""
        self._execute_sql(sql)
        return [uuid.UUID(x[0]) for x in uuids_deleted]

    @override
    def get_by_ids(
            self, uuids: List[UUID], columns: Optional[List[str]] = None
    ) -> Sequence:
        # select from duckdb table where ids are in the list
        if not isinstance(uuids, list):
            raise TypeError(f"Expected ids to be a list, got {uuids}")

        if not uuids:
            # create an empty pandas dataframe
            return pd.DataFrame()

        columns = columns + ["uuid"] if columns else ["uuid"]

        select_columns = db_schema_to_keys() if columns is None else columns
        sql = f"""
            SELECT
                {",".join(select_columns)}
            FROM
                embeddings
            WHERE
                uuid IN ({','.join([("'" + str(x) + "'") for x in uuids])})
        """
        response = self._execute_sql(sql)[1:]

        # sort db results by the order of the uuids
        response = sorted(
            response, key=lambda obj: uuids.index(uuid.UUID(obj[len(columns) - 1]))
        )

        return response

    @override
    def raw_sql(self, raw_sql):
        return self._execute_sql(raw_sql)[1:].df()

    # TODO: This method should share logic with clickhouse impl
    @override
    def reset(self):
        self._conn.execute("DROP TABLE collections")
        self._conn.execute("DROP TABLE embeddings")
        self._create_table_collections()
        self._create_table_embeddings()

    def __del__(self):
        logger.info("Exiting: Cleaning up .chroma directory")
        self.reset_indexes()

    @override
    def persist(self) -> None:
        raise NotImplementedError(
            "Set chroma_db_impl='starrocks' to get persistence functionality"
        )