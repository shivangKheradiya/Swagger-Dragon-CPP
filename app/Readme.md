***

# 📘 Session‑Based JSONB Editing API

This service provides a **session‑oriented, draft–commit workflow** for editing JSONB‑based attribute data.  
It supports **single‑row and bulk CRUD**, **preview**, **commit**, **abort**, **session discovery**, and **immutable history tracking**.

The design follows patterns used in **CAD / PLM / configuration management systems**, where edits are staged, reviewed, and explicitly persisted.

***

## 🧠 Core Concepts

### ✅ Project Code (`{code}`)

*   Identifies the project / schema / database
*   Appears in the URL path
*   Examples: `XYZ`, `DESI`, `CATA`

***

### ✅ Sessions

*   A **session** represents one unit of work
*   All edits are staged inside a session
*   Sessions are **explicitly started**
*   Sessions can be:
    *   committed (persist changes)
    *   aborted (discard changes)

***

### ✅ Overlay

*   Session overlay tables store **proposed state**
*   Live tables are **never modified directly**
*   Overlay rows are cleared on commit or abort

***

### ✅ History

*   On commit, immutable history rows are written
*   History captures:
    *   attribute UUID
    *   operation type
    *   session UUID
    *   old and new values

***

## 🔁 High‑Level Workflow

    START SESSION
        ↓
    STAGE CHANGES (single or bulk)
        ↓
    PREVIEW SESSION (optional)
        ↓
    COMMIT SESSION   OR   ABORT SESSION

***

## 🔧 Base URL

    http://127.0.0.1:8000

***

# 1️⃣ Session Lifecycle APIs

***

## Start Session

Creates a new active session.

    POST /{code}/session/start

### cURL

```bash
curl -X POST \
"http://127.0.0.1:8000/XYZ/session/start?username=atul&hostname=dev-machine"
```

### Response

```json
{
  "status": "active",
  "session_uuid": "25f37b21-9df8-4a75-820d-f3e474d717f6"
}
```

***

## Get Active Session

Find an existing active session for a user.

    GET /{code}/session/active

### cURL

```bash
curl \
"http://127.0.0.1:8000/XYZ/session/active?username=atul&hostname=dev-machine"
```

### Response (no active session)

```json
{
  "active": false,
  "session_uuid": null
}
```

### Response (active session exists)

```json
{
  "active": true,
  "session_uuid": "25f37b21-9df8-4a75-820d-f3e474d717f6",
  "username": "atul",
  "hostname": "dev-machine",
  "started_at": "2026-04-13T10:22:30Z"
}
```

***

## List Sessions

List sessions for a user.

    GET /{code}/session

### cURL

```bash
curl \
"http://127.0.0.1:8000/XYZ/session?username=atul"
```

### Response

```json
{
  "count": 2,
  "sessions": [
    {
      "session_uuid": "25f37b21-9df8-4a75-820d-f3e474d717f6",
      "username": "atul",
      "hostname": "dev-machine",
      "started_at": "2026-04-13T10:22:30Z",
      "active": true
    },
    {
      "session_uuid": "aabbccdd-1111-2222-3333-444444444444",
      "username": "atul",
      "hostname": "dev-machine",
      "started_at": "2026-04-10T09:05:00Z",
      "active": false
    }
  ]
}
```

***

# 2️⃣ Single‑Row CRUD (Session Overlay)

All CRUD operations below **stage changes inside the session overlay**.

***

## Create (Stage)

    POST /{code}/{table}

```bash
curl -X POST \
"http://127.0.0.1:8000/XYZ/DESI" \
-H "Content-Type: application/json" \
-d '{
  "session_uuid": "25f37b21-9df8-4a75-820d-f3e474d717f6",
  "node_uuid": "11111111-2222-3333-4444-555555555555",
  "attribute_id": 1,
  "value": "Pump-A"
}'
```

***

## Update (Stage)

    PUT /{code}/{table}/{uuid}

```bash
curl -X PUT \
"http://127.0.0.1:8000/XYZ/DESI/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee" \
-H "Content-Type: application/json" \
-d '{
  "session_uuid": "25f37b21-9df8-4a75-820d-f3e474d717f6",
  "value": "Pump-B"
}'
```

***

## Delete (Stage)

    DELETE /{code}/{table}/{uuid}?session_uuid=...

```bash
curl -X DELETE \
"http://127.0.0.1:8000/XYZ/DESI/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee?session_uuid=25f37b21-9df8-4a75-820d-f3e474d717f6"
```

***

# 3️⃣ BULK CRUD (Ordered, Fault‑Tolerant)

Bulk operations allow **large change sets** to be staged efficiently.

***

## Guarantees

*   Operations are executed in this strict order:
        CREATE → UPDATE → DELETE
*   Each item is committed independently
*   One failure does NOT stop the batch
*   Failed items are reported with **exact indices**

***

## Bulk Endpoint

    POST /{code}/{table}/bulk

***

## Bulk Payload Example

```json
{
  "session_uuid": "25f37b21-9df8-4a75-820d-f3e474d717f6",
  "operations": {
    "create": [
      {
        "node_uuid": "11111111-2222-3333-4444-555555555555",
        "attribute_id": 1,
        "value": "Pump-A"
      },
      {
        "node_uuid": "22222222-3333-4444-5555-666666666666",
        "attribute_id": 1,
        "value": "Pump-A1"
      }
    ],
    "update": [
      {
        "uuid": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
        "value": "Pump-B"
      }
    ],
    "delete": [
      {
        "uuid": "ffffffff-eeee-dddd-cccc-bbbbbbbbbbbb"
      }
    ]
  }
}
```

***

## Bulk cURL

```bash
curl -X POST \
"http://127.0.0.1:8000/XYZ/DESI/bulk" \
-H "Content-Type: application/json" \
-d @bulk.json
```

***

## Bulk Response (Partial Success)

```json
{
  "status": "partial_success",
  "summary": {
    "create": { "total": 2, "success": 1, "failed": 1 },
    "update": { "total": 1, "success": 1, "failed": 0 },
    "delete": { "total": 1, "success": 0, "failed": 1 }
  },
  "failures": {
    "create": [
      { "index": 1, "reason": "Duplicate attribute for node" }
    ],
    "delete": [
      { "index": 0, "reason": "UUID not found" }
    ]
  }
}
```

✅ Tools can retry **only the failed indices**.

***

# 4️⃣ Preview Session Changes

View all staged changes in a session.

    GET /{code}/{table}/session/{session_uuid}

```bash
curl \
"http://127.0.0.1:8000/XYZ/DESI/session/25f37b21-9df8-4a75-820d-f3e474d717f6"
```

***

# 5️⃣ Commit Session

Persists all staged changes:

*   applies overlay → live tables
*   writes history
*   clears overlay
*   marks session inactive

⚠️ Does NOT create a new session.

    POST /{code}/session/{session_uuid}/commit?table={table}

```bash
curl -X POST \
"http://127.0.0.1:8000/XYZ/session/25f37b21-9df8-4a75-820d-f3e474d717f6/commit?table=DESI"
```

Response:

```json
{
  "status": "committed",
  "session_uuid": "25f37b21-9df8-4a75-820d-f3e474d717f6"
}
```

***

# 6️⃣ Abort Session (Discard Changes)

Discards **all staged changes** for a session.

    POST /{code}/session/{session_uuid}/abort

```bash
curl -X POST \
"http://127.0.0.1:8000/XYZ/session/25f37b21-9df8-4a75-820d-f3e474d717f6/abort"
```

Response:

```json
{
  "status": "aborted",
  "session_uuid": "25f37b21-9df8-4a75-820d-f3e474d717f6"
}
```

✅ Live data untouched  
✅ No history written

***

# ✅ Design Guarantees

| Feature                 | Guarantee |
| ----------------------- | --------- |
| Explicit sessions       | ✅         |
| Live data safety        | ✅         |
| Ordered bulk execution  | ✅         |
| Partial success         | ✅         |
| Precise error reporting | ✅         |
| Retry‑friendly          | ✅         |
| Enterprise‑grade        | ✅         |

***

## ✅ Conclusion

This API provides a **complete, production‑ready editing workflow** with:

*   session discovery
*   overlay staging
*   ordered bulk mutation
*   fault‑tolerant batching
*   explicit commit & abort
*   immutable audit history

It is suitable for:

*   UI editors
*   CLI tools
*   automation pipelines
*   multi‑user environments

***