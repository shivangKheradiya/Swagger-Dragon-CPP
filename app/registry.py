"""
Registry of allowed JSONB-based dynamic tables.

This file acts as a security and routing layer:
- Only tables listed here can be accessed via dynamic APIs
- Prevents arbitrary table access or SQL injection
"""

from .models.desi_tables import (
    TreeDESI,
    AssetDESI,
    NodeDESI,
)


# ------------------------------------------------------------------
# JSONB dynamic table registry
# ------------------------------------------------------------------
# Key   -> table name used in API
# Value -> SQLAlchemy model class
# ------------------------------------------------------------------

DESI_TABLE_REGISTRY = {
    "tree_desi": TreeDESI,
    "asset_desi": AssetDESI,
    "node_desi": NodeDESI,
}


def get_desi_model(table_name: str):
    """
    Resolve table name to SQLAlchemy model.

    Raises KeyError if table is not registered.
    """
    return DESI_TABLE_REGISTRY[table_name]