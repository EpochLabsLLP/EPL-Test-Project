"""Unit tests for the CLI module (TP-1.1.1).

Traces to: TP-1.1.1 → BP-1.1.1 → ES-1.1 → PVD-1, PVD-2, PVD-3
Coverage target: 85%
"""

import os

import pytest

from cli import main


@pytest.fixture
def task_file(tmp_path, monkeypatch):
    """Set up a temp tasks.json and run CLI from the temp directory."""
    monkeypatch.chdir(tmp_path)
    return str(tmp_path / "tasks.json")


# --- Happy Path ---


class TestAddCommand:
    """TP-1.1.1: `add "title"` returns exit code 0, task created."""

    def test_add_returns_exit_code_0(self, task_file, capsys):
        result = main(["add", "Buy groceries"])

        assert result == 0

    def test_add_prints_confirmation(self, task_file, capsys):
        main(["add", "Buy groceries"])
        output = capsys.readouterr().out

        assert "Added task 1" in output
        assert "Buy groceries" in output

    def test_add_creates_file(self, task_file):
        main(["add", "Buy groceries"])

        assert os.path.exists("tasks.json")


class TestListCommand:
    """TP-1.1.1: `list` returns exit code 0, output contains task."""

    def test_list_returns_exit_code_0(self, task_file):
        main(["add", "Buy groceries"])
        result = main(["list"])

        assert result == 0

    def test_list_shows_task(self, task_file, capsys):
        main(["add", "Buy groceries"])
        capsys.readouterr()  # clear add output
        main(["list"])
        output = capsys.readouterr().out

        assert "Buy groceries" in output
        assert "pending" in output

    def test_list_shows_formatted_header(self, task_file, capsys):
        main(["add", "Test task"])
        capsys.readouterr()
        main(["list"])
        output = capsys.readouterr().out

        assert "ID" in output
        assert "Status" in output
        assert "Title" in output


class TestDoneCommand:
    """TP-1.1.1: `done <id>` returns exit code 0, task updated."""

    def test_done_returns_exit_code_0(self, task_file):
        main(["add", "Buy groceries"])
        result = main(["done", "1"])

        assert result == 0

    def test_done_prints_confirmation(self, task_file, capsys):
        main(["add", "Buy groceries"])
        capsys.readouterr()
        main(["done", "1"])
        output = capsys.readouterr().out

        assert "Completed task 1" in output
        assert "Buy groceries" in output


# --- Edge Cases ---


class TestListEmpty:
    """TP-1.1.1: `list` with no tasks shows 'No tasks found.'."""

    def test_list_empty_shows_message(self, task_file, capsys):
        result = main(["list"])
        output = capsys.readouterr().out

        assert result == 0
        assert "No tasks found." in output


# --- Error Cases ---


class TestNoSubcommand:
    """TP-1.1.1: No subcommand returns exit code 1."""

    def test_no_args_returns_exit_code_1(self, task_file):
        result = main([])

        assert result == 1


class TestDoneInvalidID:
    """TP-1.1.1: `done` with invalid ID returns exit code 1."""

    def test_nonexistent_id_returns_exit_code_1(self, task_file, capsys):
        main(["add", "A task"])
        result = main(["done", "999"])

        assert result == 1

    def test_nonexistent_id_shows_error(self, task_file, capsys):
        main(["add", "A task"])
        capsys.readouterr()
        main(["done", "999"])
        output = capsys.readouterr().out

        assert "Error" in output


class TestDoneNonNumericID:
    """TP-1.1.1: `done` with non-numeric ID returns exit code 1."""

    def test_non_numeric_id_returns_exit_code_1(self, task_file):
        result = main(["done", "abc"])

        assert result == 1

    def test_non_numeric_id_shows_error(self, task_file, capsys):
        main(["done", "abc"])
        output = capsys.readouterr().out

        assert "Error" in output
        assert "abc" in output


# --- Boundary ---


class TestLongTitle:
    """TP-1.1.1: Very long task title is handled."""

    def test_long_title_round_trip(self, task_file, capsys):
        long_title = "A" * 500
        result = main(["add", long_title])

        assert result == 0

        capsys.readouterr()
        main(["list"])
        output = capsys.readouterr().out

        assert long_title in output
