from .history_base import JSONBHistoryBase


class TreeHistoryDESI(JSONBHistoryBase):
    """
    Dynamic JSONB table for tree-related data.
    """
    __tablename__ = "treehistorydesi"


class TreeHistoryCATA(JSONBHistoryBase):
    """
    Dynamic JSONB table for asset-related data.
    """
    __tablename__ = "treehistorycata"


class TreeHistoryDICT(JSONBHistoryBase):
    """
    Dynamic JSONB table for generic node-related data.
    """
    __tablename__ = "treehistorydict"

class TreeHistoryENGG(JSONBHistoryBase):
    """
    Dynamic JSONB table for generic node-related data.
    """
    __tablename__ = "treehistoryengg"

class TreeHistorySCHE(JSONBHistoryBase):
    """
    Dynamic JSONB table for generic node-related data.
    """
    __tablename__ = "treehistorysche"

class TreeHistorySKET(JSONBHistoryBase):
    """
    Dynamic JSONB table for generic node-related data.
    """
    __tablename__ = "treehistorysket"
