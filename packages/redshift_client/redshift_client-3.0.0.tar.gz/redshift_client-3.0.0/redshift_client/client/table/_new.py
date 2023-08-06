from . import (
    _encode,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenDict,
)
from redshift_client.core.id_objs import (
    DbTableId,
)
from redshift_client.core.table import (
    Table,
)
from redshift_client.sql_client import (
    QueryValues,
    SqlClient,
)
from redshift_client.sql_client.query import (
    dynamic_query,
)
from typing import (
    Callable,
    Dict,
)


def new(
    db_client: SqlClient, table_id: DbTableId, table: Table, if_not_exist: bool
) -> Cmd[None]:
    enum_primary_keys = tuple(enumerate(table.primary_keys))
    enum_columns = tuple(
        enumerate(tuple((i, table.columns[i]) for i in table.order))
    )
    p_fields = ",".join([f"{{pkey_{i}}}" for i, _ in enum_primary_keys])
    pkeys_template = f",PRIMARY KEY({p_fields})" if table.primary_keys else ""
    not_exists = "" if not if_not_exist else "IF NOT EXISTS"
    encode_nullable: Callable[[bool], str] = (
        lambda b: "NULL" if b else "NOT NULL"
    )
    fields_template: str = ",".join(
        [
            f"""
                {{name_{n}}} {_encode.encode_data_type(c.data_type)}
                DEFAULT %(default_{n})s {encode_nullable(c.nullable)}
            """
            for n, (_, c) in enum_columns
        ]
    )
    stm = f"CREATE TABLE {not_exists} {{schema}}.{{table}} ({fields_template}{pkeys_template})"
    identifiers: Dict[str, str] = {
        "schema": table_id.schema.name.to_str(),
        "table": table_id.table.name.to_str(),
    }
    for index, cid in enum_primary_keys:
        identifiers[f"pkey_{index}"] = cid.name.to_str()
    for index, (cid, _) in enum_columns:
        identifiers[f"name_{index}"] = cid.name.to_str()
    values = FrozenDict(
        {f"default_{index}": c.default for index, (_, c) in enum_columns}
    )
    return db_client.execute(
        dynamic_query(stm, FrozenDict(identifiers)), QueryValues(values)
    )
