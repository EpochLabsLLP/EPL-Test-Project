# Work Order: WO-2.1.1-A

| Field | Value |
|-------|-------|
| **WO ID** | WO-2.1.1-A |
| **Status** | DONE |
| **Created** | 2026-03-03 |
| **Updated** | 2026-03-03 |
| **Assigned To** | Claude Agent |

---

## Traceability Chain

```
WO-2.1.1-A  →  BP-2.1.1  →  ES-2.1  →  PVD-1, PVD-2, PVD-3
"Implement Task Engine" → "Implement Task Engine" → "Task Engine" → "Task Creation, Task Listing, Task Completion"
```

---

## 1. Tasks

### From BP-2.1.1: Implement Task Engine

- **Description:** Implement `TaskEngine` class in `Code/engine.py` with task CRUD operations.
- **Interface Contracts:**
  ```python
  class TaskEngine:
      def __init__(self, storage: TaskStorage) -> None: ...
      def add_task(self, title: str) -> dict: ...
      def list_tasks(self) -> list[dict]: ...
      def complete_task(self, task_id: int) -> dict: ...
  ```
- **Implementation Notes:**
  - Depends on `TaskStorage` from ES-3.1 (WO-3.1.1-A DONE)
  - Auto-incrementing IDs: max existing ID + 1, or 1 if no tasks
  - `add_task` sets status to "pending"
  - `complete_task` raises `ValueError` for invalid ID or already-done task

---

## 2. Testing Requirements

### From TP-2.1.1: Task Engine Tests

Implement in `Code/tests/test_engine.py`:

- [x] Add task returns task with correct ID and pending status
- [x] List tasks returns all tasks
- [x] Complete task changes status to done
- [x] Add multiple tasks, IDs increment correctly
- [x] Complete task then list shows updated status
- [x] Complete non-existent task ID raises ValueError
- [x] Complete already-done task raises ValueError
- [x] First task gets ID 1
- [x] Add task to non-empty list gets max_id + 1

---

## 3. Acceptance Criteria

- [x] `add_task()` creates task with auto-incrementing ID
- [x] `add_task()` sets status to "pending"
- [x] `list_tasks()` returns all tasks
- [x] `complete_task()` sets status to "done"
- [x] `complete_task()` raises ValueError for invalid ID
- [x] `complete_task()` raises ValueError for already-done task

---

## 4. Dependencies

| Dependency | Status | Notes |
|-----------|--------|-------|
| WO-3.1.1-A (Storage Module) | DONE | TaskEngine depends on TaskStorage |

---

## 5. Validation Checklist

_Completed during VALIDATION phase:_

- [x] All acceptance criteria met
- [x] All test cases pass (14/14)
- [x] No TODO/FIXME comments in implemented code
- [x] No compiler/linter warnings
- [x] Interface contracts match Engineering Spec exactly
- [x] Traceability chain is valid (`/trace-check`)

---

## 6. Validation Result

| Field | Value |
|-------|-------|
| **Result** | PASS — All 7 quality gates passed |
| **Validated by** | Claude Agent (/code-review + /module-complete) |
| **Date** | 2026-03-03 |
