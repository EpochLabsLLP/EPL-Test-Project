# GovernanceTestApp — Product Vision Document

| Field | Value |
|-------|-------|
| **Version** | 1 |
| **Status** | FROZEN |
| **Date** | 2026-03-03 |
| **Author** | Nathan (Test Fixture) |
| **Governed by** | CLAUDE.md, SDD Framework |

---

## Document Hierarchy

| # | Document | Status | Location |
|---|----------|--------|----------|
| 1 | **PVD** (this document) | FROZEN | `Specs/GTA_PVD_v1.md` |
| 2 | Engineering Spec | FROZEN | `Specs/GTA_Engineering_Spec_v1.md` |
| 3 | UX Spec | N/A | CLI app — no UI |
| 4 | Blueprint | FROZEN | `Specs/GTA_Blueprint_v1.md` |
| 5 | Testing Plans | FROZEN | `Testing/GTA_Testing_Plans_v1.md` |
| 6 | Gap Tracker | INITIALIZED | `Specs/gap_tracker.md` |
| 7 | Decision Record | LIVING | `Specs/GTA_Decision_Record.md` |

---

## 1. Executive Summary

GovernanceTestApp is a minimal CLI task tracker built to validate the EPL Project Template governance system. It demonstrates spec-driven development through a small but complete feature set: creating tasks, listing tasks, and marking tasks complete. The app itself is trivial — the value is in proving the governance framework works end-to-end.

## 2. Vision & Mission

**Vision:** Prove the governance system works by building a real (tiny) app through it.

**Mission:** Exercise every governance touchpoint — frozen specs, traceability chains, code-gate, commit-gate, Work Orders, and module completion — on a project small enough to complete in one session.

**Anti-Vision:** This is NOT a real product. It exists solely for template validation.

## 3. Problem Statement

We need a concrete project to test the EPL Project Template governance hooks and workflows. Without a real project to exercise them against, we can't validate that the system works as intended.

## 4. Target Users & Market

**Primary User:** Nathan and Claude agents testing the governance framework.

**Market Opportunity:** N/A — internal testing tool.

## 5. Product Overview

A Python CLI app that manages a simple task list stored in a JSON file. Three commands: `add`, `list`, `done`.

## 6. Feature Specifications

### PVD-1: Task Creation
- **Phase:** MVP
- **Description:** User can add a new task with a title via CLI command.
- **User Stories:**
  - As a user, I can run `task add "Buy groceries"` to create a new task.
- **Acceptance Criteria:**
  - [ ] `task add "<title>"` creates a new task with a unique ID
  - [ ] Task is persisted to `tasks.json`
  - [ ] New tasks default to status "pending"
  - [ ] Task ID is auto-incrementing integer

### PVD-2: Task Listing
- **Phase:** MVP
- **Description:** User can view all tasks with their status.
- **User Stories:**
  - As a user, I can run `task list` to see all my tasks.
- **Acceptance Criteria:**
  - [ ] `task list` displays all tasks with ID, title, and status
  - [ ] Output is formatted as a readable table
  - [ ] Empty list shows "No tasks found."

### PVD-3: Task Completion
- **Phase:** MVP
- **Description:** User can mark a task as complete by ID.
- **User Stories:**
  - As a user, I can run `task done 1` to mark task #1 as complete.
- **Acceptance Criteria:**
  - [ ] `task done <id>` changes task status to "done"
  - [ ] Invalid ID shows an error message
  - [ ] Already-completed tasks show a warning

## 7. User Flows

1. User runs `task add "Write tests"` → task created, confirmation printed
2. User runs `task list` → table of tasks displayed
3. User runs `task done 1` → task marked complete, confirmation printed

## 8. Economics & Business Model

N/A — internal testing tool.

## 9. Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| All governance gates exercised | 100% | Manual verification |
| Traceability chain complete | All IDs linked | `/trace-check` passes |
| Build clean | 0 warnings | Python lint |

## 10. Competitive Analysis

N/A — internal testing tool.

## 11. Risks & Mitigations

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Over-engineering the test app | Medium | High | Keep to 3 features max |

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1 | 2026-03-03 | Initial PVD — test fixture for governance validation |
