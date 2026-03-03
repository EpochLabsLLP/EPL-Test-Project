"""Task Engine module for GovernanceTestApp business logic.

Traces to: ES-2.1 → PVD-1, PVD-2, PVD-3
Implements: BP-2.1.1 (TaskEngine class with task CRUD operations)
"""

from storage import TaskStorage


class TaskEngine:
    """Business logic for task CRUD operations.

    Delegates persistence to a TaskStorage instance. Manages auto-incrementing
    IDs, task creation, listing, and status updates.
    """

    def __init__(self, storage: TaskStorage) -> None:
        self._storage = storage

    def add_task(self, title: str) -> dict:
        """Create a new task with an auto-incrementing ID.

        The new task gets status "pending" and an ID one greater than the
        current maximum (or 1 if no tasks exist).

        Returns the created task dict.
        """
        tasks = self._storage.load()
        next_id = max((t["id"] for t in tasks), default=0) + 1
        task = {"id": next_id, "title": title, "status": "pending"}
        tasks.append(task)
        self._storage.save(tasks)
        return task

    def list_tasks(self) -> list[dict]:
        """Return all tasks from storage."""
        return self._storage.load()

    def complete_task(self, task_id: int) -> dict:
        """Mark a task as done by its ID.

        Raises ValueError if the task ID does not exist or if the task
        is already marked as done.

        Returns the updated task dict.
        """
        tasks = self._storage.load()

        target = None
        for task in tasks:
            if task["id"] == task_id:
                target = task
                break

        if target is None:
            raise ValueError(f"Task with ID {task_id} not found")

        if target["status"] == "done":
            raise ValueError(f"Task with ID {task_id} is already complete")

        target["status"] = "done"
        self._storage.save(tasks)
        return target
