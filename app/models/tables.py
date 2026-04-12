from .jsonb_base import JSONBBase


class TreeDESI(JSONBBase):
    """
    Dynamic JSONB table for tree-related data.
    """
    __tablename__ = "treedesi"


class TreeCATA(JSONBBase):
    """
    Dynamic JSONB table for asset-related data.
    """
    __tablename__ = "treecata"


class TreeDICT(JSONBBase):
    """
    Dynamic JSONB table for generic node-related data.
    """
    __tablename__ = "treedict"

class TreeENGG(JSONBBase):
    """
    Dynamic JSONB table for generic node-related data.
    """
    __tablename__ = "treeengg"

class TreeSCHE(JSONBBase):
    """
    Dynamic JSONB table for generic node-related data.
    """
    __tablename__ = "treesche"

class TreeSKET(JSONBBase):
    """
    Dynamic JSONB table for generic node-related data.
    """
    __tablename__ = "treesket"

class TreeCLIM(JSONBBase):
    """
    Dynamic JSONB table for generic node-related data.
    """
    __tablename__ = "treeclim"