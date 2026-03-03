"""CLI module for GovernanceTestApp.

Traces to: ES-1.1 → PVD-1, PVD-2, PVD-3
Implements: BP-1.1.1 (CLI entry point with argparse subcommands)
"""

import argparse
import sys

from engine import TaskEngine
from storage import TaskStorage


def main(argv: list[str] | None = None) -> int:
    """Parse command-line arguments and dispatch to TaskEngine.

    Returns 0 on success, 1 on error.
    """
    parser = argparse.ArgumentParser(
        prog="task",
        description="Simple task manager",
    )
    subparsers = parser.add_subparsers(dest="command")

    # add subcommand
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")

    # list subcommand
    subparsers.add_parser("list", help="List all tasks")

    # done subcommand
    done_parser = subparsers.add_parser("done", help="Mark a task as complete")
    done_parser.add_argument("id", help="Task ID to complete")

    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 1

    storage = TaskStorage()
    engine = TaskEngine(storage)

    if args.command == "add":
        task = engine.add_task(args.title)
        print(f"Added task {task['id']}: {task['title']}")
        return 0

    if args.command == "list":
        tasks = engine.list_tasks()
        if not tasks:
            print("No tasks found.")
            return 0
        print(f"{'ID':<6}{'Status':<10}{'Title'}")
        print("-" * 40)
        for task in tasks:
            status = task["status"]
            print(f"{task['id']:<6}{status:<10}{task['title']}")
        return 0

    if args.command == "done":
        try:
            task_id = int(args.id)
        except ValueError:
            print(f"Error: '{args.id}' is not a valid task ID")
            return 1
        try:
            task = engine.complete_task(task_id)
            print(f"Completed task {task['id']}: {task['title']}")
            return 0
        except ValueError as e:
            print(f"Error: {e}")
            return 1

    return 1


if __name__ == "__main__":
    sys.exit(main())
