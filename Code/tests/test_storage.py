"""Unit tests for the Storage module (TP-3.1.1).

Traces to: TP-3.1.1 → BP-3.1.1 → ES-3.1 → PVD-1, PVD-2, PVD-3
Coverage target: 95%
"""

import json
import os

import pytest

from storage import TaskStorage


@pytest.fixture
def storage(tmp_path):
    """Provide a TaskStorage instance using a temp directory."""
    path = str(tmp_path / "tasks.json")
    return TaskStorage(path=path)


@pytest.fixture
def sample_tasks():
    """Standard sample tasks for testing."""
    return [
        {"id": 1, "title": "Buy groceries", "status": "pending"},
        {"id": 2, "title": "Walk the dog", "status": "done"},
        {"id": 3, "title": "Write report", "status": "pending"},
    ]


# --- Happy Path ---


class TestLoadExistingFile:
    """TP-3.1.1: Load from existing file returns correct tasks."""

    def test_load_returns_correct_tasks(self, storage, sample_tasks):
        with open(storage._path, "w", encoding="utf-8") as f:
            json.dump(sample_tasks, f)

        result = storage.load()

        assert result == sample_tasks

    def test_load_preserves_all_fields(self, storage):
        tasks = [{"id": 1, "title": "Test", "status": "pending"}]
        with open(storage._path, "w", encoding="utf-8") as f:
            json.dump(tasks, f)

        result = storage.load()

        assert result[0]["id"] == 1
        assert result[0]["title"] == "Test"
        assert result[0]["status"] == "pending"


class TestSaveWritesValidJSON:
    """TP-3.1.1: Save writes valid JSON."""

    def test_save_creates_valid_json_file(self, storage, sample_tasks):
        storage.save(sample_tasks)

        with open(storage._path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data == sample_tasks

    def test_save_file_is_readable_json(self, storage, sample_tasks):
        storage.save(sample_tasks)

        with open(storage._path, "r", encoding="utf-8") as f:
            raw = f.read()

        parsed = json.loads(raw)
        assert isinstance(parsed, list)


class TestRoundTrip:
    """TP-3.1.1: Round-trip (save → load) preserves data."""

    def test_round_trip_preserves_data(self, storage, sample_tasks):
        storage.save(sample_tasks)
        result = storage.load()

        assert result == sample_tasks

    def test_round_trip_multiple_cycles(self, storage, sample_tasks):
        for _ in range(3):
            storage.save(sample_tasks)
            result = storage.load()
            assert result == sample_tasks


# --- Edge Cases ---


class TestLoadMissingFile:
    """TP-3.1.1: Load from missing file returns empty list."""

    def test_load_missing_file_returns_empty_list(self, storage):
        assert not os.path.exists(storage._path)
        result = storage.load()
        assert result == []

    def test_load_missing_file_returns_list_type(self, storage):
        result = storage.load()
        assert isinstance(result, list)


class TestEmptyTaskList:
    """TP-3.1.1: Empty task list saves/loads correctly."""

    def test_save_empty_list(self, storage):
        storage.save([])

        with open(storage._path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data == []

    def test_round_trip_empty_list(self, storage):
        storage.save([])
        result = storage.load()
        assert result == []


# --- Error Cases ---


class TestCorruptedFile:
    """TP-3.1.1: Load from corrupted file raises appropriate error."""

    def test_load_corrupted_json_raises_ioerror(self, storage):
        with open(storage._path, "w", encoding="utf-8") as f:
            f.write("{not valid json[[[")

        with pytest.raises(IOError, match="Corrupted task file"):
            storage.load()

    def test_load_non_array_json_raises_ioerror(self, storage):
        with open(storage._path, "w", encoding="utf-8") as f:
            json.dump({"not": "a list"}, f)

        with pytest.raises(IOError, match="expected a JSON array"):
            storage.load()


# --- Boundary ---


class TestLargeTaskList:
    """TP-3.1.1: Large task list (100+ items) works."""

    def test_large_list_round_trip(self, storage):
        large_tasks = [
            {"id": i, "title": f"Task {i}", "status": "pending"}
            for i in range(200)
        ]

        storage.save(large_tasks)
        result = storage.load()

        assert result == large_tasks
        assert len(result) == 200


# --- Atomic Write Verification ---


class TestAtomicWrite:
    """BP-3.1.1: save() uses atomic write (temp file + rename)."""

    def test_no_tmp_file_remains_after_save(self, storage, sample_tasks):
        storage.save(sample_tasks)
        tmp_path = storage._path + ".tmp"
        assert not os.path.exists(tmp_path)

    def test_save_overwrites_existing_file(self, storage):
        original = [{"id": 1, "title": "Original", "status": "pending"}]
        updated = [{"id": 1, "title": "Updated", "status": "done"}]

        storage.save(original)
        storage.save(updated)
        result = storage.load()

        assert result == updated
