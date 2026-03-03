# GovernanceTestApp — Engineering Spec

| Field | Value |
|-------|-------|
| **Version** | 1 |
| **Status** | FROZEN |
| **Date** | 2026-03-03 |
| **Implements PVD** | GTA_PVD_v1.md |
| **Governed by** | CLAUDE.md, SDD Framework |

---

## 1. System Architecture Overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  CLI Module  │────▶│  Task Engine  │────▶│  Storage    │
│  (ES-1.1)   │     │  (ES-2.1)    │     │  (ES-3.1)   │
└─────────────┘     └──────────────┘     └─────────────┘
     argv               CRUD ops           tasks.json
```

Single-process Python CLI. No network, no database, no external dependencies.

## 2. Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Language | Python 3.10+ | Available everywhere, fast to prototype |
| CLI parsing | argparse (stdlib) | No external deps needed |
| Storage | JSON file | Simplest possible persistence |
| Testing | pytest | Standard Python testing |

## 3. Module Dependency Graph

```
CLI (ES-1.1) ──▶ TaskEngine (ES-2.1) ──▶ Storage (ES-3.1)
```

## 4. Module Specifications

### ES-1.1: CLI Module
- **Implements:** PVD-1, PVD-2, PVD-3
- **Purpose:** Parse command-line arguments and dispatch to TaskEngine
- **Responsibilities:**
  - Parse `add`, `list`, `done` subcommands
  - Format and print output
  - Handle user-facing error messages
- **Dependencies:** ES-2.1 (TaskEngine)
- **Performance Budget:** < 100ms startup

### ES-2.1: Task Engine
- **Implements:** PVD-1, PVD-2, PVD-3
- **Purpose:** Business logic for task CRUD operations
- **Responsibilities:**
  - Create tasks with auto-incrementing IDs
  - Retrieve all tasks
  - Update task status
  - Validate task IDs exist
- **Dependencies:** ES-3.1 (Storage)
- **Performance Budget:** < 50ms per operation

### ES-3.1: Storage Module
- **Implements:** PVD-1, PVD-2, PVD-3
- **Purpose:** Read/write tasks to JSON file
- **Responsibilities:**
  - Load tasks from `tasks.json`
  - Save tasks to `tasks.json`
  - Handle missing file (initialize empty)
  - Atomic writes (write to temp, rename)
- **Dependencies:** None
- **Performance Budget:** < 20ms per read/write

## 5. Frozen Interface Contracts

```python
# ES-3.1: Storage
class TaskStorage:
    def __init__(self, path: str = "tasks.json") -> None: ...
    def load(self) -> list[dict]: ...
    def save(self, tasks: list[dict]) -> None: ...

# ES-2.1: Task Engine
class TaskEngine:
    def __init__(self, storage: TaskStorage) -> None: ...
    def add_task(self, title: str) -> dict: ...
    def list_tasks(self) -> list[dict]: ...
    def complete_task(self, task_id: int) -> dict: ...

# ES-1.1: CLI (entry point)
def main(argv: list[str] | None = None) -> int: ...
```

**Task dict structure:**
```python
{
    "id": int,
    "title": str,
    "status": "pending" | "done"
}
```

## 6. Error Handling

| Error | Module | Behavior |
|-------|--------|----------|
| Invalid task ID | ES-2.1 | Raise `ValueError` with message |
| Already complete | ES-2.1 | Raise `ValueError` with warning |
| File I/O error | ES-3.1 | Raise `IOError`, CLI prints user-friendly message |
| No subcommand | ES-1.1 | Print help, return exit code 1 |

## 7. Performance Budgets

| Module | Metric | Target | Measurement |
|--------|--------|--------|-------------|
| ES-1.1 | Startup time | < 100ms | `time` command |
| ES-2.1 | Operation time | < 50ms | pytest benchmark |
| ES-3.1 | File I/O | < 20ms | pytest benchmark |

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1 | 2026-03-03 | Initial Engineering Spec — 3 modules, pure Python |
