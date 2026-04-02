"""
Test suite for database.py — Database layer.
All tests mock mysql.connector and config to avoid
requiring a real database connection.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Setup - mock dependencies before importing database module
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_connect():
    """Mock mysql.connector and config before each test."""
    config_mock = MagicMock()
    config_mock.DATABASE_USER = "test_user"
    config_mock.DATABASE_PASSWORD = "test_password"
    config_mock.DATABASE_HOST = "localhost"
    config_mock.DATABASE_DB_NAME = "test_db"
    sys.modules["config"] = config_mock

    with patch("mysql.connector.connect") as mock_conn:
        yield mock_conn


def get_database_module():
    """Reload database module fresh for each test."""
    if "database" in sys.modules:
        del sys.modules["database"]
    import database

    return database


def make_mock_connection():
    """Build a reusable mock connection and cursor."""
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


# ---------------------------------------------------------------------------
# get_database_connection
# ---------------------------------------------------------------------------


class TestGetDatabaseConnection:

    def test_connects_with_correct_credentials(self, mock_connect):
        """Should connect using values from config."""
        mock_conn, _ = make_mock_connection()
        mock_connect.return_value = mock_conn

        database = get_database_module()
        database.get_database_connection()

        mock_connect.assert_called_once_with(
            user="test_user",
            password="test_password",
            host="localhost",
            database="test_db",
            use_pure=True,
        )

    def test_returns_connection_object(self, mock_connect):
        """Should return the connection object from mysql.connector."""
        mock_conn, _ = make_mock_connection()
        mock_connect.return_value = mock_conn

        database = get_database_module()
        result = database.get_database_connection()

        assert result == mock_conn


# ---------------------------------------------------------------------------
# list_employees
# ---------------------------------------------------------------------------


class TestListEmployees:

    def test_returns_all_employees(self, mock_connect):
        """Should return all rows fetched from the database."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn
        mock_cursor.fetchall.return_value = [
            {
                "id": 1,
                "full_name": "Alice",
                "location": "NYC",
                "job_title": "Engineer",
                "badges": "coffee",
                "object_key": None,
            },
            {
                "id": 2,
                "full_name": "Bob",
                "location": "LA",
                "job_title": "Designer",
                "badges": "",
                "object_key": None,
            },
        ]

        database = get_database_module()
        result = database.list_employees()

        assert len(result) == 2
        assert result[0]["full_name"] == "Alice"
        assert result[1]["full_name"] == "Bob"

    def test_executes_correct_sql(self, mock_connect):
        """Should execute a SELECT query with ORDER BY full_name."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn
        mock_cursor.fetchall.return_value = []

        database = get_database_module()
        database.list_employees()

        executed_sql = mock_cursor.execute.call_args[0][0]
        assert "SELECT" in executed_sql
        assert "employee" in executed_sql
        assert "ORDER BY full_name" in executed_sql

    def test_closes_cursor_and_connection(self, mock_connect):
        """Should always close the cursor and connection after use."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn
        mock_cursor.fetchall.return_value = []

        database = get_database_module()
        database.list_employees()

        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_returns_empty_list_when_no_employees(self, mock_connect):
        """Should return an empty list when the table is empty."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn
        mock_cursor.fetchall.return_value = []

        database = get_database_module()
        result = database.list_employees()

        assert result == []


# ---------------------------------------------------------------------------
# load_employee
# ---------------------------------------------------------------------------


class TestLoadEmployee:

    def test_returns_correct_employee(self, mock_connect):
        """Should return the employee matching the given ID."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn
        mock_cursor.fetchone.return_value = {
            "id": 1,
            "full_name": "Alice",
            "location": "NYC",
            "job_title": "Engineer",
            "badges": "coffee",
            "object_key": None,
        }

        database = get_database_module()
        result = database.load_employee(1)

        assert result["id"] == 1
        assert result["full_name"] == "Alice"

    def test_executes_correct_sql_with_employee_id(self, mock_connect):
        """Should execute a SELECT query filtered by the given employee ID."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn
        mock_cursor.fetchone.return_value = {}

        database = get_database_module()
        database.load_employee(42)

        executed_sql = mock_cursor.execute.call_args[0][0]
        executed_params = mock_cursor.execute.call_args[0][1]
        assert "WHERE id" in executed_sql
        assert executed_params == {"emp": 42}

    def test_returns_none_when_employee_not_found(self, mock_connect):
        """Should return None when no employee matches the ID."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn
        mock_cursor.fetchone.return_value = None

        database = get_database_module()
        result = database.load_employee(999)

        assert result is None

    def test_closes_cursor_and_connection(self, mock_connect):
        """Should always close the cursor and connection after use."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn
        mock_cursor.fetchone.return_value = {}

        database = get_database_module()
        database.load_employee(1)

        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


# ---------------------------------------------------------------------------
# add_employee
# ---------------------------------------------------------------------------


class TestAddEmployee:

    def test_inserts_employee_with_correct_values(self, mock_connect):
        """Should execute an INSERT with the correct employee values."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn

        database = get_database_module()
        database.add_employee("pic/abc.png", "Alice", "NYC", "Engineer", "coffee")

        executed_sql = mock_cursor.execute.call_args[0][0]
        executed_params = mock_cursor.execute.call_args[0][1]
        assert "INSERT INTO employee" in executed_sql
        assert executed_params == ("pic/abc.png", "Alice", "NYC", "Engineer", "coffee")

    def test_commits_after_insert(self, mock_connect):
        """Should commit the transaction after inserting."""
        mock_conn, _ = make_mock_connection()
        mock_connect.return_value = mock_conn

        database = get_database_module()
        database.add_employee(None, "Bob", "LA", "Designer", "")

        mock_conn.commit.assert_called_once()

    def test_closes_cursor_and_connection(self, mock_connect):
        """Should always close the cursor and connection after use."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn

        database = get_database_module()
        database.add_employee(None, "Bob", "LA", "Designer", "")

        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


# ---------------------------------------------------------------------------
# update_employee
# ---------------------------------------------------------------------------


class TestUpdateEmployee:

    def test_updates_employee_with_object_key(self, mock_connect):
        """Should include object_key in the UPDATE when it is provided."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn

        database = get_database_module()
        database.update_employee(1, "pic/new.png", "Alice", "NYC", "Engineer", "trophy")

        executed_sql = mock_cursor.execute.call_args[0][0]
        executed_params = mock_cursor.execute.call_args[0][1]
        assert "object_key" in executed_sql
        assert executed_params == (
            "pic/new.png",
            "Alice",
            "NYC",
            "Engineer",
            "trophy",
            1,
        )

    def test_updates_employee_without_object_key(self, mock_connect):
        """Should exclude object_key from the UPDATE when it is None."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn

        database = get_database_module()
        database.update_employee(1, None, "Alice", "NYC", "Engineer", "trophy")

        executed_sql = mock_cursor.execute.call_args[0][0]
        executed_params = mock_cursor.execute.call_args[0][1]
        assert "object_key" not in executed_sql
        assert executed_params == ("Alice", "NYC", "Engineer", "trophy", 1)

    def test_commits_after_update(self, mock_connect):
        """Should commit the transaction after updating."""
        mock_conn, _ = make_mock_connection()
        mock_connect.return_value = mock_conn

        database = get_database_module()
        database.update_employee(1, None, "Alice", "NYC", "Engineer", "")

        mock_conn.commit.assert_called_once()

    def test_closes_cursor_and_connection(self, mock_connect):
        """Should always close the cursor and connection after use."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn

        database = get_database_module()
        database.update_employee(1, None, "Alice", "NYC", "Engineer", "")

        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


# ---------------------------------------------------------------------------
# delete_employee
# ---------------------------------------------------------------------------


class TestDeleteEmployee:

    def test_deletes_correct_employee(self, mock_connect):
        """Should execute a DELETE query with the correct employee ID."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn

        database = get_database_module()
        database.delete_employee(5)

        executed_sql = mock_cursor.execute.call_args[0][0]
        executed_params = mock_cursor.execute.call_args[0][1]
        assert "DELETE FROM employee" in executed_sql
        assert executed_params == {"emp": 5}

    def test_commits_after_delete(self, mock_connect):
        """Should commit the transaction after deleting."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn

        database = get_database_module()
        database.delete_employee(5)

        mock_conn.commit.assert_called_once()

    def test_closes_cursor_and_connection(self, mock_connect):
        """Should always close the cursor and connection after use."""
        mock_conn, mock_cursor = make_mock_connection()
        mock_connect.return_value = mock_conn

        database = get_database_module()
        database.delete_employee(5)

        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
