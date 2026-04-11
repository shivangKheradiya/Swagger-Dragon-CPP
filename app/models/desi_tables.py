from .jsonb_base import JSONBBase


class TreeDESI(JSONBBase):
    """
    Dynamic JSONB table for tree-related data.
    """
    __tablename__ = "tree_desi"


class AssetDESI(JSONBBase):
    """
    Dynamic JSONB table for asset-related data.
    """
    __tablename__ = "asset_desi"


class NodeDESI(JSONBBase):
    """
    Dynamic JSONB table for generic node-related data.
    """
    __tablename__ = "node_desi"