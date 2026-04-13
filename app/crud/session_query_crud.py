from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException

from app.models.session_history import SessionHistoryBase


# ---------------------------------------------------------
# GET ACTIVE SESSION
# ---------------------------------------------------------
def get_active_session(
    db: Session,
    username: Optional[str] = None,
    hostname: Optional[str] = None,
):
    """
    Return the active session for a user (if any).
    """

    query = db.query(SessionHistoryBase).filter(
        SessionHistoryBase.IsActive == True
    )

    if username:
        query = query.filter(SessionHistoryBase.UserName == username)

    if hostname:
        query = query.filter(SessionHistoryBase.HostName == hostname)

    return query.first()


# ---------------------------------------------------------
# LIST SESSIONS
# ---------------------------------------------------------
def list_sessions(
    db: Session,
    username: Optional[str] = None,
    hostname: Optional[str] = None,
    active_only: bool = False,
):
    """
    List sessions for a user.
    """

    query = db.query(SessionHistoryBase)

    if active_only:
        query = query.filter(SessionHistoryBase.IsActive == True)

    if username:
        query = query.filter(SessionHistoryBase.UserName == username)

    if hostname:
        query = query.filter(SessionHistoryBase.HostName == hostname)

    return query.order_by(SessionHistoryBase.DateTime.desc()).all()
