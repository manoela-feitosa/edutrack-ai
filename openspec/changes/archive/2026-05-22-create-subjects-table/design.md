## Context

EduTrack AI needs a database table structure to record academic subjects. Using the XanoScript syntax as described in `@AGENTS.md` and `docs/table_guideline.md`, we will define the `subjects` table schema.

## Goals / Non-Goals

**Goals:**
- Create a new XanoScript database table definition for the `subjects` table inside the `tables/` directory.
- Define appropriate fields, filters, descriptions, and indexes.
- Establish a relationship from `subjects` to the built-in `user` authentication table.

**Non-Goals:**
- Creating CRUD endpoints for the `subjects` table.
- Creating tasks, scheduled tasks, or other business logic associated with the subjects table.

## Decisions

### 1. Table File Location and Name
We will create `tables/subjects.xs` to define the schema of the `subjects` table.
- *Rationale*: Storing it in the `tables/` directory matches the standard structure of the project.

### 2. Fields and Types
The table `subjects` will be defined with:
- `int id`: Standard primary key.
- `timestamp created_at?=now`: Tracking creation time (internal/private, consistent with existing tables like `disciplinas`).
- `text name`: Non-empty subject name with `trim` filter.
- `text teacher?`: Optional teacher name with `trim` filter.
- `int hours?`: Optional weekly hours or total workload workload.
- `int user_id?`: Reference to the `user` table for ownership/authentication context.

### 3. Relationships and Constraints
- The `user_id` field will include `table = "user"` to establish a foreign key relationship to the standard authentication table.

### 4. Indexes
- A `primary` index on `id`.
- A `btree` index on `created_at` sorted in descending order for default listing sort.

## Risks / Trade-offs

- **Risk**: Deleting or replacing existing French/Portuguese tables.
  - *Mitigation*: We are adding a new English `subjects` table specifically without modifying the Portuguese tables `disciplinas` and `tarefas` unless requested.
