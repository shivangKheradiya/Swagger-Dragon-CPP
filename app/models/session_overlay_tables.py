from app.models.session_overlay import SessionJSONBBase


class SessionTreeDESI(SessionJSONBBase):
    """
    Session overlay for DESI domain.
    """
    __tablename__ = "sessionoverlay_desi"


class SessionTreeCATA(SessionJSONBBase):
    """
    Session overlay for CATA domain.
    """
    __tablename__ = "sessionoverlay_cata"


class SessionTreeDICT(SessionJSONBBase):
    """
    Session overlay for DICT domain.
    """
    __tablename__ = "sessionoverlay_dict"


class SessionTreeENGG(SessionJSONBBase):
    """
    Session overlay for ENGG domain.
    """
    __tablename__ = "sessionoverlay_engg"


class SessionTreeSCHE(SessionJSONBBase):
    """
    Session overlay for SCHE domain.
    """
    __tablename__ = "sessionoverlay_sche"


class SessionTreeSKET(SessionJSONBBase):
    """
    Session overlay for SKET domain.
    """
    __tablename__ = "sessionoverlay_sket"