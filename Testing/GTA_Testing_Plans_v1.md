# GovernanceTestApp — Testing Plans

| Field | Value |
|-------|-------|
| **Version** | 1 |
| **Status** | FROZEN |
| **Date** | 2026-03-03 |
| **Implements Blueprint** | GTA_Blueprint_v1.md |
| **Governed by** | CLAUDE.md, SDD Framework |

---

## 1. Testing Philosophy

- Unit tests for every public method
- Integration tests for module boundaries
- No mocking of our own code (only filesystem operations)
- Coverage target: 90%+

## 2. Test Infrastructure

| Type | Tool | Config |
|------|------|--------|
| Unit | pytest | `pytest.ini` or `pyproject.toml` |
| Coverage | pytest-cov | Target: 90% |

## 3. Per-Module Test Specs

### TP-3.1.1: Storage Module Tests
- **ES Module:** ES-3.1
- **Tests acceptance criteria from:** BP-3.1.1
- **Test Cases:**
  - **Happy Path:**
    - Load from existing file returns correct tasks
    - Save writes valid JSON
    - Round-trip (save → load) preserves data
  - **Edge Cases:**
    - Load from missing file returns empty list
    - Save to new directory (parent exists)
  - **Error Cases:**
    - Load from corrupted file raises appropriate error
  - **Boundary:**
    - Empty task list saves/loads correctly
    - Large task list (100+ items) works
- **Coverage Target:** 95%

### TP-2.1.1: Task Engine Tests
- **ES Module:** ES-2.1
- **Tests acceptance criteria from:** BP-2.1.1
- **Test Cases:**
  - **Happy Path:**
    - Add task returns task with correct ID and pending status
    - List tasks returns all tasks
    - Complete task changes status to done
  - **Edge Cases:**
    - Add multiple tasks, IDs increment correctly
    - Complete task then list shows updated status
  - **Error Cases:**
    - Complete non-existent task ID raises ValueError
    - Complete already-done task raises ValueError
  - **Boundary:**
    - First task gets ID 1
    - Add task to non-empty list gets max_id + 1
- **Coverage Target:** 95%

### TP-1.1.1: CLI Module Tests
- **ES Module:** ES-1.1
- **Tests acceptance criteria from:** BP-1.1.1
- **Test Cases:**
  - **Happy Path:**
    - `add "title"` returns exit code 0, task created
    - `list` returns exit code 0, output contains task
    - `done <id>` returns exit code 0, task updated
  - **Edge Cases:**
    - `list` with no tasks shows "No tasks found."
  - **Error Cases:**
    - No subcommand returns exit code 1
    - `done` with invalid ID returns exit code 1
    - `done` with non-numeric ID returns exit code 1
  - **Boundary:**
    - Very long task title is handled
- **Coverage Target:** 85%

## 4. Integration Test Scenarios

### CLI → Engine → Storage
- Add a task via CLI, verify it appears in `tasks.json`
- Add a task, list via CLI, verify output matches
- Add a task, complete via CLI, list via CLI, verify status

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1 | 2026-03-03 | Initial Testing Plans — mirrors Blueprint task cards |
