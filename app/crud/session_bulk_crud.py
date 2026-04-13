from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.jsonb_bulk import (
    JSONBBulkRequest,
    JSONBBulkResponse,
    BulkFailure,
    BulkOperationSummary,
)
from app.crud.session_overlay_crud import (
    push_create,
    push_update,
    push_delete,
)


# ---------------------------------------------------------
# BULK STAGING ENGINE
# ---------------------------------------------------------
def bulk_stage_operations(
    db: Session,
    table_code: str,
    payload: JSONBBulkRequest,
) -> JSONBBulkResponse:
    """
    Stage bulk operations in strict order:
    CREATE → UPDATE → DELETE

    - Each item is committed independently
    - Failures do NOT stop the batch
    - Failures are reported with exact index + reason
    """

    failures = {
        "create": [],
        "update": [],
        "delete": [],
    }

    summary = {
        "create": BulkOperationSummary(
            total=len(payload.operations.create),
            success=0,
            failed=0,
        ),
        "update": BulkOperationSummary(
            total=len(payload.operations.update),
            success=0,
            failed=0,
        ),
        "delete": BulkOperationSummary(
            total=len(payload.operations.delete),
            success=0,
            failed=0,
        ),
    }

    session_uuid = payload.session_uuid


    # -----------------------------------------------------
    # CREATE PHASE
    # -----------------------------------------------------
    for idx, item in enumerate(payload.operations.create):
        try:
            push_create(
                db=db,
                table_code=table_code,
                payload=type(
                    "Payload",
                    (),
                    {
                        "session_uuid": session_uuid,
                        "node_uuid": item.node_uuid,
                        "attribute_id": item.attribute_id,
                        "value": item.value,
                    },
                )(),
            )
            summary["create"].success += 1

        except Exception as exc:
            db.rollback()
            summary["create"].failed += 1
            failures["create"].append(
                BulkFailure(
                    index=idx,
                    reason=str(exc),
                )
            )


    # -----------------------------------------------------
    # UPDATE PHASE
    # -----------------------------------------------------
    for idx, item in enumerate(payload.operations.update):
        try:
            push_update(
                db=db,
                table_code=table_code,
                attribute_uuid=item.uuid,
                payload=type(
                    "Payload",
                    (),
                    {
                        "session_uuid": session_uuid,
                        "value": item.value,
                    },
                )(),
            )
            summary["update"].success += 1

        except Exception as exc:
            db.rollback()
            summary["update"].failed += 1
            failures["update"].append(
                BulkFailure(
                    index=idx,
                    reason=str(exc),
                )
            )


    # -----------------------------------------------------
    # DELETE PHASE
    # -----------------------------------------------------
    for idx, item in enumerate(payload.operations.delete):
        try:
            push_delete(
                db=db,
                table_code=table_code,
                attribute_uuid=item.uuid,
                session_uuid=session_uuid,
            )
            summary["delete"].success += 1

        except Exception as exc:
            db.rollback()
            summary["delete"].failed += 1
            failures["delete"].append(
                BulkFailure(
                    index=idx,
                    reason=str(exc),
                )
            )


    # -----------------------------------------------------
    # RESPONSE STATUS
    # -----------------------------------------------------
    total_failed = (
        summary["create"].failed
        + summary["update"].failed
        + summary["delete"].failed
    )

    if total_failed == 0:
        status = "success"
    elif total_failed == (
        summary["create"].total
        + summary["update"].total
        + summary["delete"].total
    ):
        status = "failed"
    else:
        status = "partial_success"

    return JSONBBulkResponse(
        status=status,
        summary=summary,
        failures={k: v for k, v in failures.items() if v},
    )