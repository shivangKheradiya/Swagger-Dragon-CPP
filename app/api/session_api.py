from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.session_history import SessionHistoryBase

# ✅ NEW: commit logic
from app.crud.session_commit_crud import commit_session

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
        table_name=table,
        session_uuid=session_uuid,
    )

    return result