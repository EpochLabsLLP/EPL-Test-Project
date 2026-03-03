# GovernanceTestApp — Blueprint

| Field | Value |
|-------|-------|
| **Version** | 1 |
| **Status** | FROZEN |
| **Date** | 2026-03-03 |
| **Implements Engineering Spec** | GTA_Engineering_Spec_v1.md |
| **Governed by** | CLAUDE.md, SDD Framework |

---

## 1. Build Principles

1. Build bottom-up: Storage → Engine → CLI
2. Every module gets tests before moving to the next
3. No external dependencies — stdlib only (except pytest for testing)

## 2. Dependency Graph

```
Wave 1: [BP-3.1.1 Storage]
              │
Wave 2: [BP-2.1.1 Engine] ───▶ depends on Storage
              │
Wave 3: [BP-1.1.1 CLI] ───▶ depends on Engine
```

## 3. Wave Schedule

### Wave 1 — Foundation (Storage)
- **Objective:** Persistent storage layer
- **Prerequisites:** None
- **Tasks:** BP-3.1.1
- **Exit Criteria:** Storage module passes all unit tests

### Wave 2 — Core Logic (Task Engine)
- **Objective:** Business logic layer
- **Prerequisites:** Wave 1 complete
- **Tasks:** BP-2.1.1
- **Exit Criteria:** Engine module passes all unit tests

### Wave 3 — Interface (CLI)
- **Objective:** User-facing CLI
- **Prerequisites:** Wave 2 complete
- **Tasks:** BP-1.1.1
- **Exit Criteria:** CLI module passes all unit tests, end-to-end works

## 4. Task Cards

### BP-3.1.1: Implement Storage Module
- **Module:** ES-3.1 (Storage)
- **Wave:** 1
- **Complexity:** Low
- **Dependencies:** None
- **Description:** Implement `TaskStorage` class with JSON file persistence.
- **Interface Contracts:**
  ```python
  class TaskStorage:
      def __init__(self, path: str = "tasks.json") -> None: ...
      def load(self) -> list[dict]: ...
      def save(self, tasks: list[dict]) -> None: ...
  ```
- **Acceptance Criteria:**
  - [ ] `load()` returns empty list when file doesn't exist
  - [ ] `load()` returns tasks from existing file
  - [ ] `save()` writes tasks to JSON file
  - [ ] `save()` uses atomic write (temp file + rename)
  - [ ] Round-trip: save then load returns identical data

### BP-2.1.1: Implement Task Engine
- **Module:** ES-2.1 (Task Engine)
- **Wave:** 2
- **Complexity:** Low
- **Dependencies:** BP-3.1.1
- **Description:** Implement `TaskEngine` class with task CRUD operations.
- **Interface Contracts:**
  ```python
  class TaskEngine:
      def __init__(self, storage: TaskStorage) -> None: ...
      def add_task(self, title: str) -> dict: ...
      def list_tasks(self) -> list[dict]: ...
      def complete_task(self, task_id: int) -> dict: ...
  ```
- **Acceptance Criteria:**
  - [ ] `add_task()` creates task with auto-incrementing ID
  - [ ] `add_task()` sets status to "pending"
  - [ ] `list_tasks()` returns all tasks
  - [ ] `complete_task()` sets status to "done"
  - [ ] `complete_task()` raises ValueError for invalid ID
  - [ ] `complete_task()` raises ValueError for already-done task

### BP-1.1.1: Implement CLI Module
- **Module:** ES-1.1 (CLI)
- **Wave:** 3
- **Complexity:** Low
- **Dependencies:** BP-2.1.1
- **Description:** Implement CLI entry point with argparse subcommands.
- **Interface Contracts:**
  ```python
  def main(argv: list[str] | None = None) -> int: ...
  ```
- **Acceptance Criteria:**
  - [ ] `task add "<title>"` creates task, prints confirmation
  - [ ] `task list` displays formatted task table
  - [ ] `task done <id>` marks task complete, prints confirmation
  - [ ] No subcommand prints help, returns exit code 1
  - [ ] Invalid ID prints error message, returns exit code 1

## 5. Quality Gates Checklist

- [ ] All interface contracts implemented with real logic
- [ ] Unit tests cover all public methods
- [ ] No TODO/FIXME comments
- [ ] No GPL dependencies
- [ ] Builds/runs without warnings
- [ ] Performance meets targets

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1 | 2026-03-03 | Initial Blueprint — 3 tasks across 3 waves |
