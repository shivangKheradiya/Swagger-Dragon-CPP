***

# 📘 Attribute‑Driven Tree & Metadata Model

### Scalable, Auditable, and Extensible Design Data Architecture

***

## 🧩 Overview

This design implements a **generic, attribute‑driven data model** to represent:

*   Hierarchical tree structures
*   Rich metadata attached to nodes
*   Multiple independent domains of design data
*   Full historical tracking of changes

The core idea is:

> **Everything (structure + metadata) is represented as attributes, and history is tracked centrally and immutably.**

***

## 🎯 Key Goals

*   ✅ Avoid rigid table schemas for evolving design data
*   ✅ Scale across multiple design domains (Designs, Catalogues, Dictionaries, Tags, etc.)
*   ✅ Keep live queries fast and simple
*   ✅ Preserve full audit history with minimal assumptions
*   ✅ Support future claim‑based and compliance needs

***

## 🧠 Core Concept

Instead of hard‑coding structure and metadata into schemas:

*   **Tree nodes are identified by UUIDs**
*   **All properties (including parent/child relations) are modeled as attributes**
*   **Different data domains use different attribute tables**
*   **Each attribute table has its own history table**

This allows **n independent design models** to coexist without schema conflicts.

***

## 🌳 Attribute‑Based Tree Model

Tree hierarchy is represented by a **special attribute**, not a dedicated column.

Example:

*   Attribute: `Parent`
*   Value: `<ParentTreeNodeUUID>`

This makes parent–child relationships:

*   versionable
*   auditable
*   replaceable
*   domain‑specific if needed

***

## 🧱 Core Tables (per Domain)

Each **design domain** has its own attribute table.

Examples:

*   `TreeNodeAttributes_Design`
*   `TreeNodeAttributes_Catalogue`
*   `TreeNodeAttributes_Dictionary`
*   `TreeNodeAttributes_Tags`
*   `TreeNodeAttributes_T1 ... Tn`

All follow the **same structure and rules**.

***

## **TreeNodeAttributes\_<Domain>**

This table stores the **current (live) state** of attributes for tree nodes within a specific domain.

### Schema

| Column                   | Type      | Description                          |
| ------------------------ | --------- | ------------------------------------ |
| `UUID`                   | TEXT (PK) | Unique attribute instance identifier |
| `TreeNodeUUID`           | TEXT      | Tree node identifier                 |
| `ElementTypeAttributeID` | INTEGER   | Attribute definition for this domain |
| `Value`                  | TEXT      | Current attribute value              |

### Notes

*   This table is always **current state only**
*   No historical data is stored here
*   Optimized for fast reads and updates
*   Attribute meaning is resolved via the domain’s attribute definition table

***

## 📚 Attribute Definitions (per Domain)

Each domain has its own **ElementTypeAttributes** table.

Examples:

*   `ElementTypeAttributes_Design`
*   `ElementTypeAttributes_Catalogue`
*   `ElementTypeAttributes_Dictionary`

These tables define:

*   Attribute name
*   Data type
*   Default value
*   Semantic meaning

This allows each domain to:

*   evolve independently
*   define its own vocabulary
*   avoid cross‑domain coupling

***

## 🕰 History & Audit Model

Every attribute table has a corresponding **history table**.

History is:

*   append‑only
*   immutable
*   self‑contained
*   schema‑resilient

***

## **TreeNodeAttributes\_<Domain>\_History**

This table records **every change** made to attributes in a domain.

### Schema

| Column          | Type        | Description                        |
| --------------- | ----------- | ---------------------------------- |
| `TNHAUUID`      | TEXT (PK)   | Unique history record              |
| `TNAUUID`       | TEXT        | Reference to live attribute row    |
| `OperationType` | INT         | `1=CREATE`, `2=UPDATE`, `3=DELETE` |
| `ChangedAt`     | TIMESTAMPTZ | Time of change                     |
| `OldValue`      | JSONB       | Value before the change            |
| `NewValue`      | JSONB       | Value after the change             |

***

### History Semantics

| Operation | OldValue       | NewValue      |
| --------- | -------------- | ------------- |
| CREATE    | `NULL`         | Initial value |
| UPDATE    | Previous value | Updated value |
| DELETE    | Last value     | `NULL`        |

Each history row is a **complete fact**:

> It fully explains the change without relying on other rows.

***

## 🧪 Why JSONB in History?

*   History must survive schema and meaning changes
*   JSONB is compressed and efficient
*   Old records remain valid forever
*   History is cold data and read rarely

> **Live tables remain lightweight; only history carries context.**

***

## 🔍 Typical Use Cases

This architecture supports:

*   ✅ Dynamic tree structures
*   ✅ Metadata‑driven designs
*   ✅ Domain‑specific vocabularies
*   ✅ Full change audit and rollback
*   ✅ Long‑lived design repositories
*   ✅ Multi‑tenant or multi‑model systems

Examples:

*   Engineering designs
*   Product catalogues
*   Classification dictionaries
*   Tagging systems
*   Configuration trees

***

## 🧠 Scalability Strategy

*   Add a new domain → create a new attribute table + history table
*   No schema changes required elsewhere
*   Domains evolve independently
*   History storage can be archived or partitioned by domain

This avoids:

*   giant polymorphic tables
*   massive NULL columns
*   complex conditional logic

***

## ✅ Design Summary

**Live data**

*   Attribute‑centric
*   Fast, compact
*   Domain‑specific

**History**

*   Append‑only
*   Self‑contained
*   Auditable
*   Space‑efficient over time

***

## 🏁 Final Philosophy

> **Structure is data.  
> Metadata is data.  
> History is truth.**

By modeling everything as attributes and treating history as immutable facts, this design achieves flexibility **without sacrificing correctness or auditability**.

***