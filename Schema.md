TreeNodes
UUID, Parent, IsDeleted

TreeNodeAttributes
UUID, TreeNodeUUID, ElementTypeAttributeID, Value, ChangedFrom(UUID), IsDeleted

ElementTypes
IDNo, Name

ElementTypeAttributes
IDNo, ElementTypeID, Name, DataType, DefaultValue


Below is a clean, professional, production‑grade **README.md** section containing **API documentation** for your project.  
This matches the exact behavior of your multi‑DB FastAPI system with the four required tables.

You can copy/paste this as your actual `README.md` file.

***

# 📘 OPE‑DBSQLite — API Documentation

OPE‑DBSQLite is a multi‑database FastAPI service that dynamically manages multiple SQLite databases based on **3‑letter codes**.

Each database:

*   is created automatically on first access
*   contains 4 required tables
*   supports full CRUD operations
*   remains isolated per code (e.g., `ABC`, `XYZ`, `QWE` represent separate databases)

***

# 📚 Table of Contents

1.  \#overview
2.  \#database-selection
3.  \#required-tables
4.  \#api-endpoints
5.  \#crud-examples
6.  \#data-models
7.  \#notes

***

# 📌 Overview

This API provides CRUD operations for 4 internal tables:

1.  **TreeNodes**
2.  **TreeNodeAttributes**
3.  **ElementTypes**
4.  **ElementTypeAttributes**

Each 3‑letter code (e.g., `ABC`) represents a separate SQLite file:

    dbs/ABC.db
    dbs/XYZ.db
    dbs/QWE.db

Databases and required tables are created automatically on first request.

***

# 🗂 Database Selection

Every API route starts with:

    /{code}/{table}

Where:

*   `{code}` = **3‑letter uppercase identifier** (e.g., `ABC`)
*   `{table}` = One of:

    *   `TreeNodes`
    *   `TreeNodeAttributes`
    *   `ElementTypes`
    *   `ElementTypeAttributes`

Example:

    GET /ABC/TreeNodes

This means:

*   Use SQLite file `dbs/ABC.db`
*   Read from the table `TreeNodes`

***

# 🏛 Required Tables

When a new database is referenced (e.g., `/XYZ/...`), the system automatically creates the following schema.

***

## **TreeNodes**

| Column    | Type      | Default | Description       |
| --------- | --------- | ------- | ----------------- |
| UUID      | TEXT (PK) | —       | Unique identifier |
| Parent    | TEXT      | NULL    | Parent UUID       |
| IsDeleted | BOOLEAN   | 0       | Soft delete flag  |

***

## **TreeNodeAttributes**

| Column                 | Type      | Default | Description                |
| ---------------------- | --------- | ------- | -------------------------- |
| UUID                   | TEXT (PK) | —       | Unique                     |
| TreeNodeUUID           | TEXT      | —       | FK → TreeNodes             |
| ElementTypeAttributeID | INTEGER   | —       | FK → ElementTypeAttributes |
| Value                  | TEXT      | NULL    | Attribute value            |
| ChangedFrom            | TEXT      | NULL    | Previous UUID              |
| IsDeleted              | BOOLEAN   | 0       | Soft delete                |

***

## **ElementTypes**

| Column | Type                     | Default | Description       |
| ------ | ------------------------ | ------- | ----------------- |
| IDNo   | INTEGER PK AUTOINCREMENT | —       | Auto ID           |
| Name   | TEXT                     | NULL    | Element type name |

***

## **ElementTypeAttributes**

| Column        | Type                     | Default | Description       |
| ------------- | ------------------------ | ------- | ----------------- |
| IDNo          | INTEGER PK AUTOINCREMENT | —       | Auto ID           |
| ElementTypeID | INTEGER                  | —       | FK → ElementTypes |
| Name          | TEXT                     | —       | Attribute name    |
| DataType      | TEXT                     | —       | Attribute type    |
| DefaultValue  | TEXT                     | —       | Default value     |

***

# 🔌 API Endpoints

All endpoints follow this pattern:

| Method     | Path                    | Description       |
| ---------- | ----------------------- | ----------------- |
| **POST**   | `/{code}/{table}`       | Create new record |
| **GET**    | `/{code}/{table}`       | Read all records  |
| **GET**    | `/{code}/{table}/{key}` | Read one record   |
| **PUT**    | `/{code}/{table}/{key}` | Update one record |
| **DELETE** | `/{code}/{table}/{key}` | Delete one record |

***

# 🧪 CRUD Examples

Assuming database code: `ABC`

***

## 1️⃣ Create TreeNode

**POST /ABC/TreeNodes**

```json
{
  "UUID": "N1",
  "Parent": null,
  "IsDeleted": false
}
```

Response:

```json
{ "status": "created" }
```

***

## 2️⃣ Read All TreeNodes

**GET /ABC/TreeNodes**

Response:

```json
[
  {
    "UUID": "N1",
    "Parent": null,
    "IsDeleted": 0
  }
]
```

***

## 3️⃣ Read One TreeNode

**GET /ABC/TreeNodes/N1**

***

## 4️⃣ Update TreeNode

**PUT /ABC/TreeNodes/N1**

```json
{
  "IsDeleted": true
}
```

***

## 5️⃣ Delete TreeNode

**DELETE /ABC/TreeNodes/N1**

***

# 🧱 Operation Examples for All Tables

***

### Create ElementType

POST `/ABC/ElementTypes`

```json
{
  "Name": "Pipe"
}
```

***

### Create ElementTypeAttribute

POST `/ABC/ElementTypeAttributes`

```json
{
  "ElementTypeID": 1,
  "Name": "Diameter",
  "DataType": "float",
  "Default": "0.0"
}
```

***

### Create TreeNodeAttribute

POST `/ABC/TreeNodeAttributes`

```json
{
  "UUID": "A1",
  "TreeNodeUUID": "N1",
  "ElementTypeAttributeID": 1,
  "Value": "100",
  "ChangedFrom": null,
  "IsDeleted": false
}
```

***

# 📄 Data Model Rules

### 1. UUID‑based tables:

*   `TreeNodes`
*   `TreeNodeAttributes`

Use:

    key = UUID

### 2. Numeric auto‑ID tables:

*   `ElementTypes`
*   `ElementTypeAttributes`

Use:

    key = IDNo

The API automatically determines the correct primary key column.

***

# 📝 Notes

*   All 3‑letter DB codes are converted to uppercase.
*   All databases are stored in `dbs/` directory.
*   Boolean values are stored as integers (0/1) internally by SQLite.
*   Databases and tables self‑initialize automatically on first request.

***
