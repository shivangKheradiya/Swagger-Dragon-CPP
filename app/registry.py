"""
Registry of allowed JSONB-based dynamic tables.

This file acts as a security and routing layer:
- Only tables listed here can be accessed via dynamic APIs
- Prevents arbitrary table access or SQL injection
"""

from .models.tables import (
    TreeDESI,
    TreeCATA,
    TreeDICT,
    TreeENGG,
    TreeSCHE,
    TreeSKET
)

from app.models.tables_history import (
    TreeHistoryDESI,
    TreeHistoryCATA,
    TreeHistoryDICT,
    TreeHistoryENGG,
    TreeHistorySCHE,
    TreeHistorySKET,
)

from app.models.session_overlay_tables import (
    SessionTreeDESI,
    SessionTreeCATA,
    SessionTreeDICT,
    SessionTreeENGG,
    SessionTreeSCHE,
    SessionTreeSKET,
)

# ------------------------------------------------------------------
# JSONB dynamic table registry
# ------------------------------------------------------------------
# Key   -> table name used in API
# Value -> SQLAlchemy model class
# ------------------------------------------------------------------

LIVE_TABLE_REGISTRY = {
    "DESI": TreeDESI,
    "CATA": TreeCATA,
    "DICT": TreeDICT,
    "ENGG": TreeENGG,
    "SCHE": TreeSCHE,
    "SKET": TreeSKET,
}

HISTORY_TABLE_REGISTRY = {
    "DESI": TreeHistoryDESI,
    "CATA": TreeHistoryCATA,
    "DICT": TreeHistoryDICT,
    "ENGG": TreeHistoryENGG,
    "SCHE": TreeHistorySCHE,
    "SKET": TreeHistorySKET,
}

# ------------------------------------------------------------------
# SESSION OVERLAY TABLE REGISTRY
# ------------------------------------------------------------------

SESSION_OVERLAY_REGISTRY = {
    "DESI": SessionTreeDESI,
    "CATA": SessionTreeCATA,
    "DICT": SessionTreeDICT,
    "ENGG": SessionTreeENGG,
    "SCHE": SessionTreeSCHE,
    "SKET": SessionTreeSKET,
}