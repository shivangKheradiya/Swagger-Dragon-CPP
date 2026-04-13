from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.session_history import SessionHistoryBase

# ✅ NEW: commit logic
from app.crud.session_commit_crud import commit_session
from app.crud.session_abort_crud import abort_session
from app.crud.session_query_crud import (
    get_active_session,
    list_sessions,
)

router = APIRouter(prefix="/{code}/session", tags=["Session Management"])


# ---------------------------------------------------------
# START NEW SESSION
# ---------------------------------------------------------
@router.post("/start", summary="Start a new user session")
def start_session(
    code: str,
    username: str | None = None,
    hostname: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Start a new active session.

    Rules:
    - Only ONE active session per code
    - Existing active session is deactivated
    """

    db.query(SessionHistoryBase).filter(
        SessionHistoryBase.IsActive == True
    ).update(
        {"IsActive": False}
    )

    session = SessionHistoryBase(
        UserName=username,
        HostName=hostname,
        IsActive=True,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "session_uuid": session.SessionUUID,
        "status": "active",
    }


# ---------------------------------------------------------
# COMMIT SESSION ✅ NEW
# ---------------------------------------------------------
@router.post(
    "/{session_uuid}/commit",
    summary="Commit all staged changes and start a new session",
)
def commit_active_session(
    code: str,
    session_uuid: UUID,
    table: str,
    db: Session = Depends(get_db),
):
    """
    Commit session changes.

    Steps:
    - Apply overlay → live
    - Write history
    - Close session
    - Clear overlay
    - Create new active session
    """

    result = commit_session(
        db=db,
        table_code=table,
        session_uuid=session_uuid,
    )
    return result

# ---------------------------------------------------------
# ABORT SESSION (DISCARD CHANGES)
# ---------------------------------------------------------
@router.post(
    "/{session_uuid}/abort",
    summary="Abort a session and discard all staged changes",
)
def abort_active_session(
    code: str,
    session_uuid: UUID,
    db: Session = Depends(get_db),
):
    """
    Abort a session.

    TOOL / WORKFLOW RESPONSIBILITY:
    - Discards all staged overlay changes
    - Does NOT affect live data
    - Does NOT write history
    """

    return abort_session(
        db=db,
        session_uuid=session_uuid,
    )


# ---------------------------------------------------------
# GET ACTIVE SESSION
# ---------------------------------------------------------
@router.get(
    "/active",
    summary="Get active session for a user",
)
def get_active_user_session(
    code: str,
    username: str | None = None,
    hostname: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Returns the currently active session for a user, if any.
    """

    session = get_active_session(
        db=db,
        username=username,
        hostname=hostname,
    )

    if not session:
        return {
            "active": False,
            "session_uuid": None,
        }

    return {
        "active": True,
        "session_uuid": session.SessionUUID,
        "username": session.UserName,
        "hostname": session.HostName,
        "started_at": session.DateTime,
    }


# ---------------------------------------------------------
# LIST SESSIONS
# ---------------------------------------------------------
@router.get(
    "",
    summary="List sessions",
)
def list_user_sessions(
    code: str,
    username: str | None = None,
    hostname: str | None = None,
    active_only: bool = False,
    db: Session = Depends(get_db),
):
    """
    List all sessions for a user.
    """

    sessions = list_sessions(
        db=db,
        username=username,
        hostname=hostname,
        active_only=active_only,
    )

    return {
        "count": len(sessions),
        "sessions": [
            {
                "session_uuid": s.SessionUUID,
                "username": s.UserName,
                "hostname": s.HostName,
                "started_at": s.DateTime,
                "active": s.IsActive,
            }
            for s in sessions
        ],
    }