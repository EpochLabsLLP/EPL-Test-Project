"""Unit tests for the Task Engine module (TP-2.1.1).

Traces to: TP-2.1.1 → BP-2.1.1 → ES-2.1 → PVD-1, PVD-2, PVD-3
Coverage target: 95%
"""

import pytest

from engine import TaskEngine
from storage import TaskStorage


@pytest.fixture
def engine(tmp_path):
    """Provide a TaskEngine instance backed by a temp-dir storage."""
    storage = TaskStorage(path=str(tmp_path / "tasks.json"))
    return TaskEngine(storage=storage)


# --- Happy Path ---


class TestAddTask:
    """TP-2.1.1: Add task returns task with correct ID and pending status."""

    def test_add_task_returns_correct_structure(self, engine):
        task = engine.add_task("Buy groceries")

        assert task["id"] == 1
        assert task["title"] == "Buy groceries"
        assert task["status"] == "pending"

    def test_add_task_persists_to_storage(self, engine):
        engine.add_task("Buy groceries")
        tasks = engine.list_tasks()

        assert len(tasks) == 1
        assert tasks[0]["title"] == "Buy groceries"


class TestListTasks:
    """TP-2.1.1: List tasks returns all tasks."""

    def test_list_empty(self, engine):
        assert engine.list_tasks() == []

    def test_list_returns_all_tasks(self, engine):
        engine.add_task("Task A")
        engine.add_task("Task B")
        engine.add_task("Task C")

        tasks = engine.list_tasks()

        assert len(tasks) == 3
        titles = [t["title"] for t in tasks]
        assert titles == ["Task A", "Task B", "Task C"]


class TestCompleteTask:
    """TP-2.1.1: Complete task changes status to done."""

    def test_complete_task_sets_status_done(self, engine):
        engine.add_task("Buy groceries")
        result = engine.complete_task(1)

        assert result["status"] == "done"
        assert result["id"] == 1

    def test_complete_task_persists(self, engine):
        engine.add_task("Buy groceries")
        engine.complete_task(1)

        tasks = engine.list_tasks()
        assert tasks[0]["status"] == "done"


# --- Edge Cases ---


class TestAutoIncrementingIDs:
    """TP-2.1.1: Add multiple tasks, IDs increment correctly."""

    def test_sequential_ids(self, engine):
        t1 = engine.add_task("First")
        t2 = engine.add_task("Second")
        t3 = engine.add_task("Third")

        assert t1["id"] == 1
        assert t2["id"] == 2
        assert t3["id"] == 3

    def test_first_task_gets_id_1(self, engine):
        """TP-2.1.1 Boundary: First task gets ID 1."""
        task = engine.add_task("First ever task")
        assert task["id"] == 1

    def test_add_to_non_empty_list_gets_max_plus_1(self, engine):
        """TP-2.1.1 Boundary: Add task to non-empty list gets max_id + 1."""
        engine.add_task("First")
        engine.add_task("Second")
        t3 = engine.add_task("Third")

        assert t3["id"] == 3


class TestCompleteAndList:
    """TP-2.1.1: Complete task then list shows updated status."""

    def test_list_reflects_completed_status(self, engine):
        engine.add_task("Task A")
        engine.add_task("Task B")
        engine.complete_task(1)

        tasks = engine.list_tasks()
        statuses = {t["id"]: t["status"] for t in tasks}

        assert statuses[1] == "done"
        assert statuses[2] == "pending"


# --- Error Cases ---


class TestCompleteInvalidID:
    """TP-2.1.1: Complete non-existent task ID raises ValueError."""

    def test_nonexistent_id_raises_valueerror(self, engine):
        engine.add_task("Only task")

        with pytest.raises(ValueError, match="not found"):
            engine.complete_task(999)

    def test_zero_id_raises_valueerror(self, engine):
        engine.add_task("Only task")

        with pytest.raises(ValueError, match="not found"):
            engine.complete_task(0)

    def test_negative_id_raises_valueerror(self, engine):
        engine.add_task("Only task")

        with pytest.raises(ValueError, match="not found"):
            engine.complete_task(-1)


class TestCompleteAlreadyDone:
    """TP-2.1.1: Complete already-done task raises ValueError."""

    def test_already_done_raises_valueerror(self, engine):
        engine.add_task("Buy groceries")
        engine.complete_task(1)

        with pytest.raises(ValueError, match="already complete"):
            engine.complete_task(1)
