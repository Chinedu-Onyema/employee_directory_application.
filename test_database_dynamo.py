"""
Test suite for database_dynamo.py — DynamoDB database layer.
All tests mock boto3 to avoid requiring real AWS credentials
or a live DynamoDB table.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Setup - mock boto3 before importing the module
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def mock_boto3():
    """Mock boto3.resource before each test."""
    with patch("boto3.resource") as mock_resource:
        yield mock_resource


def get_dynamo_module():
    """Reload database_dynamo fresh for each test."""
    if "database_dynamo" in sys.modules:
        del sys.modules["database_dynamo"]
    import database_dynamo

    return database_dynamo


def make_mock_table(mock_resource):
    """Build a reusable mock DynamoDB table."""
    mock_table = MagicMock()
    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = mock_table
    mock_resource.return_value = mock_dynamodb
    return mock_table


# ---------------------------------------------------------------------------
# list_employees
# ---------------------------------------------------------------------------


class TestListEmployees:

    def test_returns_all_employees(self, mock_boto3):
        """Should return all items from the DynamoDB scan."""
        mock_table = make_mock_table(mock_boto3)
        mock_table.scan.return_value = {
            "Items": [
                {
                    "id": "1",
                    "full_name": "Alice",
                    "location": "NYC",
                    "job_title": "Engineer",
                    "badges": ["coffee"],
                },
                {
                    "id": "2",
                    "full_name": "Bob",
                    "location": "LA",
                    "job_title": "Designer",
                    "badges": [],
                },
            ]
        }

        db = get_dynamo_module()
        result = db.list_employees()

        assert len(result) == 2
        assert result[0]["full_name"] == "Alice"
        assert result[1]["full_name"] == "Bob"

    def test_scans_correct_table(self, mock_boto3):
        """Should scan the Employees table."""
        mock_table = make_mock_table(mock_boto3)
        mock_table.scan.return_value = {"Items": []}

        db = get_dynamo_module()
        db.list_employees()

        mock_boto3.return_value.Table.assert_called_once_with("Employees")
        mock_table.scan.assert_called_once()

    def test_returns_zero_on_failure(self, mock_boto3):
        """Should return 0 when DynamoDB raises an exception."""
        mock_boto3.side_effect = Exception("AWS error")

        db = get_dynamo_module()
        result = db.list_employees()

        assert result == 0

    def test_returns_empty_list_when_no_employees(self, mock_boto3):
        """Should return an empty list when the table has no items."""
        mock_table = make_mock_table(mock_boto3)
        mock_table.scan.return_value = {"Items": []}

        db = get_dynamo_module()
        result = db.list_employees()

        assert result == []


# ---------------------------------------------------------------------------
# load_employee
# ---------------------------------------------------------------------------


class TestLoadEmployee:

    def test_returns_correct_employee(self, mock_boto3):
        """Should return the employee matching the given ID."""
        mock_table = make_mock_table(mock_boto3)
        mock_table.get_item.return_value = {
            "Item": {
                "id": "abc",
                "full_name": "Alice",
                "location": "NYC",
                "job_title": "Engineer",
                "badges": ["coffee"],
            }
        }

        db = get_dynamo_module()
        result = db.load_employee("abc")

        assert result["id"] == "abc"
        assert result["full_name"] == "Alice"

    def test_queries_with_correct_key(self, mock_boto3):
        """Should call get_item with the correct employee ID key."""
        mock_table = make_mock_table(mock_boto3)
        mock_table.get_item.return_value = {"Item": {"id": "abc"}}

        db = get_dynamo_module()
        db.load_employee("abc")

        mock_table.get_item.assert_called_once_with(Key={"id": "abc"})

    def test_returns_none_on_failure(self, mock_boto3):
        """Should return None silently when DynamoDB raises an exception."""
        mock_boto3.side_effect = Exception("AWS error")

        db = get_dynamo_module()
        result = db.load_employee("missing-id")

        assert result is None


# ---------------------------------------------------------------------------
# add_employee
# ---------------------------------------------------------------------------


class TestAddEmployee:

    def test_adds_employee_with_all_fields(self, mock_boto3):
        """Should call put_item with all provided employee fields."""
        mock_table = make_mock_table(mock_boto3)

        with patch("uuid.uuid4", return_value=MagicMock(hex="fake-uuid")):
            db = get_dynamo_module()
            db.add_employee("pic/abc.png", "Alice", "NYC", "Engineer", "coffee,trophy")

        put_item_call = mock_table.put_item.call_args[1]["Item"]
        assert put_item_call["full_name"] == "Alice"
        assert put_item_call["location"] == "NYC"
        assert put_item_call["job_title"] == "Engineer"
        assert put_item_call["object_key"] == "pic/abc.png"

    def test_splits_badges_into_list(self, mock_boto3):
        """Should split the badges string into a list before storing."""
        mock_table = make_mock_table(mock_boto3)

        db = get_dynamo_module()
        db.add_employee(None, "Alice", "NYC", "Engineer", "coffee,trophy,bug")

        put_item_call = mock_table.put_item.call_args[1]["Item"]
        assert put_item_call["badges"] == ["coffee", "trophy", "bug"]

    def test_excludes_object_key_when_none(self, mock_boto3):
        """Should not include object_key in the item when it is None."""
        mock_table = make_mock_table(mock_boto3)

        db = get_dynamo_module()
        db.add_employee(None, "Bob", "LA", "Designer", "")

        put_item_call = mock_table.put_item.call_args[1]["Item"]
        assert "object_key" not in put_item_call

    def test_excludes_badges_when_empty(self, mock_boto3):
        """Should not include badges in the item when badges is empty."""
        mock_table = make_mock_table(mock_boto3)

        db = get_dynamo_module()
        db.add_employee(None, "Bob", "LA", "Designer", "")

        put_item_call = mock_table.put_item.call_args[1]["Item"]
        assert "badges" not in put_item_call

    def test_generates_unique_id(self, mock_boto3):
        """Should generate a UUID as the employee ID."""
        mock_table = make_mock_table(mock_boto3)

        db = get_dynamo_module()
        db.add_employee(None, "Alice", "NYC", "Engineer", "")

        put_item_call = mock_table.put_item.call_args[1]["Item"]
        assert "id" in put_item_call
        assert len(put_item_call["id"]) > 0

    def test_silent_on_failure(self, mock_boto3):
        """Should not raise an exception when DynamoDB fails."""
        mock_boto3.side_effect = Exception("AWS error")

        db = get_dynamo_module()
        try:
            db.add_employee(None, "Alice", "NYC", "Engineer", "")
        except Exception:  # pylint: disable=broad-exception-caught
            pytest.fail("add_employee raised an exception unexpectedly")


# ---------------------------------------------------------------------------
# update_employee
# ---------------------------------------------------------------------------


class TestUpdateEmployee:

    def test_updates_employee_with_object_key(self, mock_boto3):
        """Should include object_key in the update when provided."""
        mock_table = make_mock_table(mock_boto3)

        db = get_dynamo_module()
        db.update_employee("1", "pic/new.png", "Alice", "NYC", "Engineer", "trophy")

        update_call = mock_table.update_item.call_args[1]
        assert update_call["Key"] == {"id": "1"}
        assert "object_key" in update_call["AttributeUpdates"]
        assert update_call["AttributeUpdates"]["object_key"]["Value"] == "pic/new.png"

    def test_updates_employee_without_object_key(self, mock_boto3):
        """Should exclude object_key from the update when it is None."""
        mock_table = make_mock_table(mock_boto3)

        db = get_dynamo_module()
        db.update_employee("1", None, "Alice", "NYC", "Engineer", "trophy")

        update_call = mock_table.update_item.call_args[1]
        assert "object_key" not in update_call["AttributeUpdates"]

    def test_splits_badges_into_list_on_update(self, mock_boto3):
        """Should split the badges string into a list on update."""
        mock_table = make_mock_table(mock_boto3)

        db = get_dynamo_module()
        db.update_employee("1", None, "Alice", "NYC", "Engineer", "coffee,trophy")

        update_call = mock_table.update_item.call_args[1]
        assert update_call["AttributeUpdates"]["badges"]["Value"] == [
            "coffee",
            "trophy",
        ]
        assert update_call["AttributeUpdates"]["badges"]["Action"] == "PUT"

    def test_deletes_badges_when_empty(self, mock_boto3):
        """Should set badges action to DELETE when badges is empty."""
        mock_table = make_mock_table(mock_boto3)

        db = get_dynamo_module()
        db.update_employee("1", None, "Alice", "NYC", "Engineer", "")

        update_call = mock_table.update_item.call_args[1]
        assert update_call["AttributeUpdates"]["badges"]["Action"] == "DELETE"

    def test_silent_on_failure(self, mock_boto3):
        """Should not raise an exception when DynamoDB fails."""
        mock_boto3.side_effect = Exception("AWS error")

        db = get_dynamo_module()
        try:
            db.update_employee("1", None, "Alice", "NYC", "Engineer", "")
        except Exception:  # pylint: disable=broad-exception-caught
            pytest.fail("update_employee raised an exception unexpectedly")


# ---------------------------------------------------------------------------
# delete_employee
# ---------------------------------------------------------------------------


class TestDeleteEmployee:

    def test_deletes_correct_employee(self, mock_boto3):
        """Should call delete_item with the correct employee ID key."""
        mock_table = make_mock_table(mock_boto3)

        db = get_dynamo_module()
        db.delete_employee("abc-123")

        mock_table.delete_item.assert_called_once_with(Key={"id": "abc-123"})

    def test_silent_on_failure(self, mock_boto3):
        """Should not raise an exception when DynamoDB fails."""
        mock_boto3.side_effect = Exception("AWS error")

        db = get_dynamo_module()
        try:
            db.delete_employee("abc-123")
        except Exception:  # pylint: disable=broad-exception-caught
            pytest.fail("delete_employee raised an exception unexpectedly")
