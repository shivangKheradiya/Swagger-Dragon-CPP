# app/crud/search_crud.py

from sqlalchemy import text
from app.registry import (
    LIVE_TABLE_REGISTRY,
    SESSION_OVERLAY_REGISTRY,
    SEARCHABLE_COLUMN_REGISTRY,
)

# ---------------------------------------------------------
# Operator mapping (strict allow-list)
# ---------------------------------------------------------

OPERATOR_SQL_MAP = {
    "eq": "=",
    "ne": "!=",
    "gt": ">",
    "gte": ">=",
    "lt": "<",
    "lte": "<=",
    "like": "LIKE",
    "ilike": "ILIKE",
    "in": "IN",
}

# ---------------------------------------------------------
# Compile a single condition
# ---------------------------------------------------------

def compile_condition(condition, allowed_columns, params, index: int) -> str:
    if condition.field not in allowed_columns:
        raise ValueError(f"Search on column not allowed: {condition.field}")

    sql_op = OPERATOR_SQL_MAP[condition.operator]
    param_name = f"p{index}"

    if condition.operator == "in":
        params[param_name] = condition.value
        return f"{condition.field} = ANY(:{param_name})"

    params[param_name] = condition.value
    return f"{condition.field} {sql_op} :{param_name}"

# ---------------------------------------------------------
# Compile AND / OR cascaded WHERE clause
# ---------------------------------------------------------

def compile_where_clause(search_request, allowed_columns):
    params = {}
    param_index = 0
    groups = []

    for group in search_request.where:
        expressions = []

        for cond in group.conditions:
            expressions.append( compile_condition( condition=cond, allowed_columns=allowed_columns, params=params, index=param_index ) )
            param_index += 1

        joined = f" {group.logic} ".join(expressions)
        groups.append(f"({joined})")

    return " AND ".join(groups), params

# ---------------------------------------------------------
# Resolve FROM clause (live / overlay / merged)
# ---------------------------------------------------------

def resolve_from_clause(table_code, scope, session_uuid):
    live_table = LIVE_TABLE_REGISTRY[table_code].__tablename__
    overlay_table = SESSION_OVERLAY_REGISTRY[table_code].__tablename__

    if scope == "live":
        return live_table, {}

    if scope == "overlay":
        return overlay_table, {}

    if scope == "merged":
        if not session_uuid:
            raise ValueError("session_uuid is required for merged scope")

        return (
            f"""
            (
                SELECT *
                FROM {overlay_table}
                WHERE session_uuid = :session_uuid

                UNION ALL

                SELECT l.*
                FROM {live_table} l
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM {overlay_table} o
                    WHERE o.session_uuid = :session_uuid
                      AND o.uuid = l.uuid
                )
            ) AS merged_view
            """,
            {"session_uuid": session_uuid},
        )

    raise ValueError(f"Invalid scope: {scope}")

# ---------------------------------------------------------
# Execute search
# ---------------------------------------------------------

def execute_search(db, search_request):
    table_code = search_request.table
    allowed_columns = SEARCHABLE_COLUMN_REGISTRY[table_code]

    where_sql, where_params = compile_where_clause(
        search_request=search_request,
        allowed_columns=allowed_columns,
    )

    from_sql, from_params = resolve_from_clause(
        table_code=table_code,
        scope=search_request.scope,
        session_uuid=search_request.session_uuid,
    )

    sql = f"""
    SELECT *
    FROM {from_sql}
    WHERE {where_sql}
    LIMIT :limit OFFSET :offset
    """

    params = {
        **where_params,
        **from_params,
        "limit": search_request.limit,
        "offset": search_request.offset,
    }

    result = db.execute(text(sql), params)
    return [dict(row._mapping) for row in result]