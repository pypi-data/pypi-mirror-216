from . import (
    _encode,
    _new,
)
from ._assert import (
    to_column,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    PureIter,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.pure_iter.transform import (
    consume,
)
from redshift_client.core.column import (
    Column,
    ColumnId,
    ColumnObj,
)
from redshift_client.core.id_objs import (
    DbTableId,
    Identifier,
    TableId,
)
from redshift_client.core.table import (
    ManifestId,
    Table,
    TableAttrs,
)
from redshift_client.sql_client import (
    QueryValues,
    RowData,
    SqlClient,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from redshift_client.sql_client.query import (
    dynamic_query,
    new_query,
)
from typing import (
    Dict,
    TypeVar,
)

_T = TypeVar("_T")


def _assert_bool(raw: _T) -> bool:
    if isinstance(raw, bool):
        return raw
    raise TypeError("Expected bool")


@dataclass(frozen=True)
class TableClient:
    _db_client: SqlClient

    def unload(
        self, table: DbTableId, prefix: str, role: str
    ) -> Cmd[ManifestId]:
        """
        prefix: a s3 uri prefix
        role: an aws role id-arn
        """
        stm = """
            UNLOAD ('SELECT * FROM {schema}.{table}')
            TO %(prefix)s iam_role %(role)s MANIFEST ESCAPE
        """
        args: Dict[str, PrimitiveVal] = {"prefix": prefix, "role": role}
        return self._db_client.execute(
            dynamic_query(
                stm,
                FrozenDict(
                    {
                        "schema": table.schema.name.to_str(),
                        "table": table.table.name.to_str(),
                    }
                ),
            ),
            QueryValues(FrozenDict(args)),
        ).map(lambda _: ManifestId(f"{prefix}manifest"))

    def load(
        self,
        table: DbTableId,
        manifest: ManifestId,
        role: str,
        nan_handler: bool = True,
    ) -> Cmd[None]:
        """
        If `nan_handler` is disabled, ensure that the table does not contain NaN values on float columns
        """
        nan_fix = "NULL AS 'nan'" if nan_handler else ""
        stm = f"""
            COPY {{schema}}.{{table}} FROM %(manifest_file)s
            iam_role %(role)s MANIFEST ESCAPE {nan_fix}
        """
        args: Dict[str, PrimitiveVal] = {
            "manifest_file": manifest.uri,
            "role": role,
        }
        return self._db_client.execute(
            dynamic_query(
                stm,
                FrozenDict(
                    {
                        "schema": table.schema.name.to_str(),
                        "table": table.table.name.to_str(),
                    }
                ),
            ),
            QueryValues(FrozenDict(args)),
        )

    def get(self, table: DbTableId) -> Cmd[Table]:
        stm = """
            SELECT ordinal_position,
                column_name,
                data_type,
                CASE WHEN character_maximum_length IS not null
                        THEN character_maximum_length
                        ELSE numeric_precision end AS max_length,
                numeric_scale,
                is_nullable,
                column_default AS default_value
            FROM information_schema.columns
            WHERE table_schema = %(table_schema)s
                AND table_name = %(table_name)s
            ORDER BY ordinal_position
        """
        args: Dict[str, PrimitiveVal] = {
            "table_schema": table.schema.name.to_str(),
            "table_name": table.table.name.to_str(),
        }
        exe = self._db_client.execute(
            new_query(stm),
            QueryValues(FrozenDict(args)),
        )
        results = self._db_client.fetch_all()

        def _extract(raw: FrozenList[RowData]) -> Table:
            columns_pairs = tuple(to_column(column.data) for column in raw)
            columns = FrozenDict(dict(columns_pairs))
            order = tuple(i for i, _ in columns_pairs)
            return Table.new(order, columns, frozenset()).unwrap()

        return (exe + results).map(_extract)

    def exist(self, table: DbTableId) -> Cmd[bool]:
        stm = """
            SELECT EXISTS (
                SELECT * FROM information_schema.tables
                WHERE table_schema = %(table_schema)s
                AND table_name = %(table_name)s
            );
        """
        args: Dict[str, PrimitiveVal] = {
            "table_schema": table.schema.name.to_str(),
            "table_name": table.table.name.to_str(),
        }
        return self._db_client.execute(
            new_query(stm), QueryValues(FrozenDict(args))
        ) + self._db_client.fetch_one().map(
            lambda m: m.map(lambda i: _assert_bool(i.data[0]))
            .to_result()
            .alt(lambda _: TypeError("Expected not None"))
            .unwrap()
        )

    def insert(
        self,
        table_id: DbTableId,
        table: Table,
        items: PureIter[RowData],
        limit: int,
    ) -> Cmd[None]:
        _fields = ",".join(f"{{field_{i}}}" for i, _ in enumerate(table.order))
        stm = f"""
            INSERT INTO {{schema}}.{{table}} ({_fields}) VALUES %s
        """
        identifiers: Dict[str, str] = {
            "schema": table_id.schema.name.to_str(),
            "table": table_id.table.name.to_str(),
        }
        for i, c in enumerate(table.order):
            identifiers[f"field_{i}"] = c.name.to_str()
        return self._db_client.values(
            dynamic_query(stm, FrozenDict(identifiers)), items, limit
        )

    def rename(self, table_id: DbTableId, new_name: str) -> Cmd[TableId]:
        stm = """
            ALTER TABLE {schema}.{table} RENAME TO {new_name}
        """
        identifiers: Dict[str, str] = {
            "schema": table_id.schema.name.to_str(),
            "table": table_id.table.name.to_str(),
            "new_name": new_name,
        }
        return self._db_client.execute(
            dynamic_query(stm, FrozenDict(identifiers)), None
        ).map(lambda _: TableId(Identifier.new(new_name)))

    def _delete(self, table_id: DbTableId, cascade: bool) -> Cmd[None]:
        _cascade = "CASCADE" if cascade else ""
        stm = f"""
            DROP TABLE {{schema}}.{{table}} {_cascade}
        """
        identifiers: Dict[str, str] = {
            "schema": table_id.schema.name.to_str(),
            "table": table_id.table.name.to_str(),
        }
        return self._db_client.execute(
            dynamic_query(stm, FrozenDict(identifiers)), None
        )

    def delete(self, table_id: DbTableId) -> Cmd[None]:
        return self._delete(table_id, False)

    def delete_cascade(self, table_id: DbTableId) -> Cmd[None]:
        return self._delete(table_id, True)

    def add_column(self, table_id: DbTableId, column: ColumnObj) -> Cmd[None]:
        stm = f"""
            ALTER TABLE {{table_schema}}.{{table_name}}
            ADD COLUMN {{column_name}}
            {_encode.encode_data_type(column.column.data_type)} DEFAULT %(default_val)s
        """
        identifiers: Dict[str, str] = {
            "table_schema": table_id.schema.name.to_str(),
            "table_name": table_id.table.name.to_str(),
            "column_name": column.id_obj.name.to_str(),
        }
        args: Dict[str, PrimitiveVal] = {
            "default_val": column.column.default,
        }
        return self._db_client.execute(
            dynamic_query(stm, FrozenDict(identifiers)),
            QueryValues(FrozenDict(args)),
        )

    def add_columns(
        self,
        table: DbTableId,
        columns: FrozenDict[ColumnId, Column],
    ) -> Cmd[None]:
        return (
            from_flist(tuple(columns.items()))
            .map(lambda c: ColumnObj(c[0], c[1]))
            .map(lambda c: self.add_column(table, c))
            .transform(lambda x: consume(x))
        )

    def new(
        self,
        table_id: DbTableId,
        table: Table,
        attrs: TableAttrs,
        if_not_exist: bool = False,
    ) -> Cmd[None]:
        return _new.new(self._db_client, table_id, table, if_not_exist)

    def create_like(
        self, blueprint: DbTableId, new_table: DbTableId
    ) -> Cmd[None]:
        stm = """
            CREATE TABLE {new_schema}.{new_table} (
                LIKE {blueprint_schema}.{blueprint_table}
            )
        """
        identifiers: Dict[str, str] = {
            "blueprint_schema": blueprint.schema.name.to_str(),
            "blueprint_table": blueprint.table.name.to_str(),
            "new_schema": new_table.schema.name.to_str(),
            "new_table": new_table.table.name.to_str(),
        }
        return self._db_client.execute(
            dynamic_query(stm, FrozenDict(identifiers)), None
        )

    def move_data(self, source: DbTableId, target: DbTableId) -> Cmd[None]:
        """
        This method moves data from source to target.
        - After the operation source will be empty.
        - Both tables must exists.
        """
        stm = """
            ALTER TABLE {target_schema}.{target_table}
            APPEND FROM {source_schema}.{source_table}
        """
        identifiers: Dict[str, str] = {
            "source_schema": source.schema.name.to_str(),
            "source_table": source.table.name.to_str(),
            "target_schema": target.schema.name.to_str(),
            "target_table": target.table.name.to_str(),
        }
        return self._db_client.execute(
            dynamic_query(stm, FrozenDict(identifiers)), None
        )

    def move(self, source: DbTableId, target: DbTableId) -> Cmd[None]:
        """
        - create target if not exist
        - move_data (append) data from source into target
        - delete source table (that will be empty)
        """
        nothing = Cmd.from_cmd(lambda: None)
        create = self.exist(target).bind(
            lambda b: self.create_like(source, target) if not b else nothing
        )
        return (
            create
            + self.move_data(source, target)
            + self.delete_cascade(source)
        )

    def migrate(self, source: DbTableId, target: DbTableId) -> Cmd[None]:
        """
        - delete target if exist
        - move source into target (see move method)
        """
        nothing = Cmd.from_cmd(lambda: None)
        delete = self.exist(target).bind(
            lambda b: self.delete_cascade(target) if b else nothing
        )
        return delete + self.move(source, target)
