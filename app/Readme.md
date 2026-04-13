***

# 📘 API Testing Guide (cURL)

This document provides **complete cURL examples** to test the **Session‑based JSONB editing workflow**.

***

## 🔧 Assumptions

*   FastAPI server running at:
        http://127.0.0.1:8000
*   Project code: `XYZ`
*   Domain table code: `DESI`
*   UUIDs below are examples — replace as needed
*   Database and tables are auto‑created

***

## 1️⃣ Start a New Session

Starts a new editing session.  
Sessions are **explicit** and tool‑controlled.

### Endpoint

    POST /{code}/session/start

### cURL

```bash
curl -X POST \
"http://127.0.0.1:8000/XYZ/session/start?username=atul&hostname=dev-machine"
```

### ✅ Response

```json
{
  "status": "active",
  "session_uuid": "01973fd2-bad0-4f13-9dd1-d1907c6ad5a1"
}
```

***

## 2️⃣ Stage CREATE (Session Overlay)

Stages a **new attribute** in the session overlay.  
**No live data is modified** yet.

### Endpoint

    POST /{code}/{table}

### cURL

```bash
curl -X POST \
"http://127.0.0.1:8000/XYZ/DESI" \
-H "Content-Type: application/json" \
-d '{
  "session_uuid": "01973fd2-bad0-4f13-9dd1-d1907c6ad5a1",
  "node_uuid": "11111111-2222-3333-4444-555555555555",
  "attribute_id": 1,
  "value": "Pump-Alpha"
}'
```

### ✅ Response

```json
{
  "status": "staged",
  "operation": "CREATE",
  "uuid": "3a9f8e12-5c41-4c36-a1bb-77f93fc55aaa",
  "session_uuid": "01973fd2-bad0-4f13-9dd1-d1907c6ad5a1"
}
```

***

## 3️⃣ Read Live Data (No Overlay)

Shows **only committed** (live) data.

### Endpoint

    GET /{code}/{table}

### cURL

```bash
curl \
"http://127.0.0.1:8000/XYZ/DESI"
```

✅ The staged record **will NOT appear** here.

***

## 4️⃣ Preview Session Overlay (All Staged Changes)

Returns **only staged changes** for a session.

### Endpoint

    GET /{code}/{table}/session/{session_uuid}

### cURL

```bash
curl \
"http://127.0.0.1:8000/XYZ/DESI/session/01973fd2-bad0-4f13-9dd1-d1907c6ad5a1"
```

### ✅ Response (example)

```json
[
  {
    "uuid": "3a9f8e12-5c41-4c36-a1bb-77f93fc55aaa",
    "node_uuid": "11111111-2222-3333-4444-555555555555",
    "attribute_id": 1,
    "OperationType": 1,
    "SessionUUID": "01973fd2-bad0-4f13-9dd1-d1907c6ad5a1",
    "OldValue": null,
    "NewValue": "Pump-Alpha"
  }
]
```

***

## 5️⃣ Stage UPDATE (Session Overlay)

Updates an existing attribute **within the same session**.

### Endpoint

    PUT /{code}/{table}/{uuid}

### cURL

```bash
curl -X PUT \
"http://127.0.0.1:8000/XYZ/DESI/3a9f8e12-5c41-4c36-a1bb-77f93fc55aaa" \
-H "Content-Type: application/json" \
-d '{
  "session_uuid": "01973fd2-bad0-4f13-9dd1-d1907c6ad5a1",
  "node_uuid": "11111111-2222-3333-4444-555555555555",
  "attribute_id": 1,
  "value": "Pump-Beta"
}'
```

✅ Overlay row is **overwritten**, not duplicated.

***

## 6️⃣ Stage DELETE (Session Overlay)

Stages deletion of an attribute.

### Endpoint

    DELETE /{code}/{table}/{uuid}?session_uuid=...

### cURL

```bash
curl -X DELETE \
"http://127.0.0.1:8000/XYZ/DESI/3a9f8e12-5c41-4c36-a1bb-77f93fc55aaa?session_uuid=01973fd2-bad0-4f13-9dd1-d1907c6ad5a1"
```

✅ If the attribute was **created in the same session**, it is removed from overlay entirely.

***

## 7️⃣ Commit Session (Persist Changes)

Persists all staged changes:

*   Applies overlay → live tables
*   Writes immutable history
*   Clears overlay
*   Marks session inactive

⚠️ **Does NOT create a new session**

### Endpoint

    POST /{code}/session/{session_uuid}/commit?table={table}

### cURL

```bash
curl -X POST \
"http://127.0.0.1:8000/XYZ/session/01973fd2-bad0-4f13-9dd1-d1907c6ad5a1/commit?table=DESI"
```

### ✅ Response

```json
{
  "status": "committed",
  "session_uuid": "01973fd2-bad0-4f13-9dd1-d1907c6ad5a1"
}
```

***

## 8️⃣ Verify Live Data After Commit

### Endpoint

    GET /{code}/{table}

### cURL

```bash
curl \
"http://127.0.0.1:8000/XYZ/DESI"
```

✅ Changes are now visible in live table.

***

## 9️⃣ Verify History Table (Database)

History records are written automatically on commit.

Example SQL (PostgreSQL):

```sql
SELECT *
FROM xyz.treehistorydesi
ORDER BY "HistoryUUID";
```

Each record includes:

*   `uuid` (live attribute UUID)
*   `OperationType`
*   `SessionUUID`
*   `OldValue`
*   `NewValue`

***

## 🔟 Start a New Session (Optional)

If the tool/user wants to continue editing:

```bash
curl -X POST \
"http://127.0.0.1:8000/XYZ/session/start"
```

***

## ✅ Summary of Workflow

    START SESSION
        ↓
    STAGE CREATE / UPDATE / DELETE
        ↓
    PREVIEW SESSION
        ↓
    COMMIT SESSION
        ↓
    (OPTIONAL) START NEW SESSION

This architecture matches **professional CAD / PLM / versioned configuration systems**.

***

✅ **End of README cURL section**

If you want next, I can:

*   add a **one‑page architecture diagram (ASCII or Mermaid)**
*   add **error case cURLs**
*   add **CI smoke test with curl**
*   add **Postman collection export**

Just tell me.
