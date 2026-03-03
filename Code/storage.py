"""Storage module for GovernanceTestApp task persistence.

Traces to: ES-3.1 → PVD-1, PVD-2, PVD-3
Implements: BP-3.1.1 (TaskStorage class with JSON file persistence)
"""

import json
import os


class TaskStorage:
    """Reads and writes tasks to a JSON file.

    Uses atomic writes (temp file + os.replace) to prevent data corruption.
    Handles missing files gracefully by returning an empty list.
    """

    def __init__(self, path: str = "tasks.json") -> None:
        self._path = path

    def load(self) -> list[dict]:
        """Load tasks from the JSON file.

        Returns an empty list if the file does not exist.
        Raises IOError if the file exists but cannot be read or parsed.
        """
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            raise IOError(f"Corrupted task file '{self._path}': {e}") from e
        except OSError as e:
            raise IOError(f"Cannot read task file '{self._path}': {e}") from e

        if not isinstance(data, list):
            raise IOError(
                f"Invalid task file '{self._path}': expected a JSON array"
            )
        return data

    def save(self, tasks: list[dict]) -> None:
        """Save tasks to the JSON file using atomic write.

        Writes to a temporary file first, then atomically replaces the target
        to prevent data loss on crash or power failure.
        """
        tmp_path = self._path + ".tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
                f.write("\n")
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, self._path)
        except OSError as e:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            raise IOError(f"Cannot write task file '{self._path}': {e}") from e
