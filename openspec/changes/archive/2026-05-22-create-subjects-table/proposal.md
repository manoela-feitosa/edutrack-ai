## Why

Currently, there is no generic/English subjects table for storing school subjects in the database. Defining the `subjects` table allows users to track and manage their subjects (name, teacher, hours) associated with their account in EduTrack AI.

## What Changes

A new XanoScript table definition for `subjects` will be created with the following fields:
- `id` (primary key, integer, auto-increment)
- `name` (text, non-empty)
- `teacher` (text)
- `hours` (integer)
- `user_id` (foreign key pointing to the `user` table)

## Capabilities

### New Capabilities
- `subjects-management`: Provides the schema definition and database structure to manage subjects, linking them to authenticated users.

### Modified Capabilities
<!-- No requirement changes to existing capabilities -->

## Impact

Adds a new XanoScript table file in the `tables/` directory (`tables/subjects.xs`). This new table can be referenced by future endpoints or other tables (e.g., tasks or schedules).
