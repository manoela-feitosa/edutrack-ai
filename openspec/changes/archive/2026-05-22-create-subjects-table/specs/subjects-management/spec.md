## ADDED Requirements

### Requirement: Subjects database table structure
The subjects database table SHALL define the schema to store school subject details. It MUST contain the following fields:
- `id`: An integer primary key.
- `name`: A text field representing the name of the subject. It SHALL be trimmed.
- `teacher`: An optional text field representing the teacher's name. It SHALL be trimmed.
- `hours`: An optional integer field representing the hours/workload of the subject.
- `user_id`: An integer field that references the `id` of the `user` table.

#### Scenario: Verify subjects table schema structure
- **WHEN** the schema for the subjects table is verified
- **THEN** it contains the primary key `id`, the required `name` field, the optional `teacher` and `hours` fields, and the `user_id` field referencing the authenticated user.

### Requirement: Subjects database table indexing
The subjects database table SHALL define indexes to ensure efficient query execution. It MUST contain a primary key index on `id`. It SHALL also define a standard index on the `created_at` field sorted in descending order to allow sorting subjects by creation date.

#### Scenario: Verify subjects table indexes
- **WHEN** the indexes for the subjects table are verified
- **THEN** the primary key index on the `id` field exists and a standard btree index on the `created_at` field exists with descending order.
