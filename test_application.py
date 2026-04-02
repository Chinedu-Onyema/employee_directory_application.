"""
Test suite for the Flask Employee Directory application.
Uses pytest with unittest.mock to isolate external dependencies
(AWS S3, DynamoDB, EC2 metadata, database, subprocess).
"""

import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def app():
    """Create and configure a test instance of the Flask application."""
    # Patch all external dependencies before importing the application module
    with patch("requests.get") as mock_get, patch("requests.put"), patch(
        "boto3.client"
    ), patch.dict("os.environ", {}, clear=False):
        # Make the EC2 instance-identity call return a fake document
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "availabilityZone": "us-east-1a",
            "instanceId": "i-1234567890abcdef0",
        }
        mock_get.return_value = mock_response

        # Provide a minimal config before importing the app
        import sys

        config_mock = MagicMock()
        config_mock.FLASK_SECRET = "test-secret-key"
        config_mock.PHOTOS_BUCKET = "test-bucket"
        sys.modules.setdefault("config", config_mock)
        sys.modules.setdefault("util", MagicMock())

        # Use a fresh in-memory database stub for every test
        db_mock = MagicMock()
        sys.modules["database"] = db_mock

        # Remove application from cache to force fresh import with mocked database
        if "application" in sys.modules:
            del sys.modules["application"]

        import importlib
        import application as app_module

        importlib.reload(app_module)

        flask_app = app_module.application
        flask_app.config["TESTING"] = True
        flask_app.config["WTF_CSRF_ENABLED"] = False

        yield flask_app, db_mock


@pytest.fixture
def client(app):
    flask_app, db_mock = app
    with flask_app.test_client() as c:
        yield c, db_mock


# ---------------------------------------------------------------------------
# Helper builders
# ---------------------------------------------------------------------------


def make_employee(**kwargs):
    """Return a minimal employee dict, with defaults that can be overridden."""
    defaults = {
        "id": "1",
        "full_name": "Jane Doe",
        "location": "Seattle",
        "job_title": "Engineer",
        "badges": "coffee,bug",
        "object_key": None,
        "signed_url": None,
    }
    defaults.update(kwargs)
    return defaults


# ---------------------------------------------------------------------------
# get_instance_document
# ---------------------------------------------------------------------------


class TestGetInstanceDocument:
    """Unit tests for the EC2 metadata helper."""

    def test_returns_json_on_success(self):
        with patch("requests.get") as mock_get, patch.dict(
            "os.environ", {"PHOTOS_BUCKET": "test-bucket"}
        ):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {
                "availabilityZone": "us-west-2a",
                "instanceId": "i-abc",
            }
            mock_get.return_value = mock_resp

            # Import fresh to exercise the function in isolation
            import importlib
            import application as app_module

            result = app_module.get_instance_document()
            assert result["instanceId"] == "i-abc"

    def test_falls_back_on_exception(self):
        with patch("requests.get", side_effect=Exception("no network")), patch.dict(
            "os.environ", {"PHOTOS_BUCKET": "test-bucket"}
        ):
            import application as app_module

            result = app_module.get_instance_document()
            assert "instanceId" in result
            assert result["availabilityZone"] == "us-fake-1a"

    def test_handles_401_with_token_refresh(self):
        """When metadata returns 401, a token should be fetched and retried."""
        with patch("requests.get") as mock_get, patch(
            "requests.put"
        ) as mock_put, patch.dict("os.environ", {"PHOTOS_BUCKET": "test-bucket"}):
            token_resp = MagicMock()
            token_resp.text = "fake-token"
            mock_put.return_value = token_resp

            unauth_resp = MagicMock()
            unauth_resp.status_code = 401

            auth_resp = MagicMock()
            auth_resp.status_code = 200
            auth_resp.json.return_value = {
                "availabilityZone": "eu-west-1a",
                "instanceId": "i-eu",
            }
            auth_resp.raise_for_status = MagicMock()

            mock_get.side_effect = [unauth_resp, auth_resp]

            import application as app_module

            result = app_module.get_instance_document()
            assert result["instanceId"] == "i-eu"
            # Token endpoint should have been called once
            mock_put.assert_called_once()


# ---------------------------------------------------------------------------
# Home route  /
# ---------------------------------------------------------------------------


class TestHomeRoute:

    def test_home_empty_directory(self, client):
        c, db_mock = client
        db_mock.list_employees.return_value = 0  # falsy sentinel used in the app
        resp = c.get("/")
        assert resp.status_code == 200

    def test_home_with_employees(self, client):
        c, db_mock = client
        employees = [
            make_employee(id="1", full_name="Alice"),
            make_employee(id="2", full_name="Bob"),
        ]
        db_mock.list_employees.return_value = employees

        with patch("boto3.client") as mock_boto:
            s3 = MagicMock()
            s3.generate_presigned_url.return_value = "https://s3.example.com/photo.png"
            mock_boto.return_value = s3

            resp = c.get("/")
            assert resp.status_code == 200
            assert b"Alice" in resp.data
            assert b"Bob" in resp.data

    def test_home_employee_with_photo(self, client):
        c, db_mock = client
        employee = make_employee(object_key="employee_pic/abc.png")
        db_mock.list_employees.return_value = [employee]

        with patch("boto3.client") as mock_boto:
            s3 = MagicMock()
            s3.generate_presigned_url.return_value = "https://s3.example.com/abc.png"
            mock_boto.return_value = s3

            resp = c.get("/")
            assert resp.status_code == 200
            assert b"https://s3.example.com/abc.png" in resp.data

    def test_home_presigned_url_failure_is_silent(self, client):
        """A broken S3 call should not crash the page."""
        c, db_mock = client
        employee = make_employee(object_key="employee_pic/bad.png")
        db_mock.list_employees.return_value = [employee]

        with patch("boto3.client") as mock_boto:
            s3 = MagicMock()
            s3.generate_presigned_url.side_effect = Exception("S3 error")
            mock_boto.return_value = s3

            resp = c.get("/")
            assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Add route  /add
# ---------------------------------------------------------------------------


class TestAddRoute:

    def test_add_page_loads(self, client):
        c, _ = client
        resp = c.get("/add")
        assert resp.status_code == 200

    def test_add_page_contains_form(self, client):
        c, _ = client
        resp = c.get("/add")
        assert b"Full Name" in resp.data or b"full_name" in resp.data


# ---------------------------------------------------------------------------
# Edit route  /edit/<employee_id>
# ---------------------------------------------------------------------------


class TestEditRoute:

    def test_edit_existing_employee(self, client):
        c, db_mock = client
        db_mock.load_employee.return_value = make_employee(id="42")

        with patch("boto3.client") as mock_boto:
            s3 = MagicMock()
            s3.generate_presigned_url.return_value = "https://s3.example.com/photo.png"
            mock_boto.return_value = s3

            resp = c.get("/edit/42")
            assert resp.status_code == 200
            db_mock.load_employee.assert_called_once_with("42")

    def test_edit_employee_without_photo(self, client):
        c, db_mock = client
        db_mock.load_employee.return_value = make_employee(id="7", object_key=None)

        with patch("boto3.client"):
            resp = c.get("/edit/7")
            assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Save route  /save  (POST)
# ---------------------------------------------------------------------------


class TestSaveRoute:

    def _post_form(self, client, data):
        c, db_mock = client
        with patch("boto3.client") as mock_boto:
            s3 = MagicMock()
            mock_boto.return_value = s3
            resp = c.post("/save", data=data, follow_redirects=True)
        return resp, db_mock, s3

    def test_save_new_employee_no_photo(self, client):
        data = {
            "full_name": "Charlie",
            "location": "Portland",
            "job_title": "Designer",
            "badges": "",
            "employee_id": "",
        }
        resp, db_mock, _ = self._post_form(client, data)
        assert resp.status_code == 200
        db_mock.add_employee.assert_called_once()

    def test_save_existing_employee(self, client):
        data = {
            "full_name": "Dana",
            "location": "Austin",
            "job_title": "PM",
            "badges": "trophy",
            "employee_id": "99",
        }
        resp, db_mock, _ = self._post_form(client, data)
        assert resp.status_code == 200
        db_mock.update_employee.assert_called_once()

    def test_save_with_photo_upload(self, client):
        import sys

        util_mock = sys.modules["util"]
        util_mock.resize_image.return_value = b"fake-image-bytes"
        util_mock.random_hex_bytes.return_value = "deadbeef"

        data = {
            "full_name": "Eve",
            "location": "NYC",
            "job_title": "Artist",
            "badges": "camera",
            "employee_id": "",
            "photo": (BytesIO(b"fake-image-content"), "photo.png"),
        }
        c, db_mock = client
        with patch("boto3.client") as mock_boto:
            s3 = MagicMock()
            mock_boto.return_value = s3
            resp = c.post(
                "/save",
                data=data,
                content_type="multipart/form-data",
                follow_redirects=True,
            )

        assert resp.status_code == 200
        db_mock.add_employee.assert_called_once()

    def test_save_invalid_form_returns_error(self, client):
        """Missing required fields should not call database helpers."""
        c, db_mock = client
        _ = c.post("/save", data={"full_name": ""}, follow_redirects=True)
        db_mock.add_employee.assert_not_called()
        db_mock.update_employee.assert_not_called()


# ---------------------------------------------------------------------------
# View route  /employee/<employee_id>
# ---------------------------------------------------------------------------


class TestViewRoute:

    def test_view_employee(self, client):
        c, db_mock = client
        db_mock.load_employee.return_value = make_employee(id="5", full_name="Frank")

        with patch("boto3.client"):
            resp = c.get("/employee/5")
            assert resp.status_code == 200
            assert b"Frank" in resp.data

    def test_view_employee_with_photo(self, client):
        c, db_mock = client
        db_mock.load_employee.return_value = make_employee(
            id="6", object_key="employee_pic/x.png"
        )

        with patch("boto3.client") as mock_boto:
            s3 = MagicMock()
            s3.generate_presigned_url.return_value = "https://s3.example.com/x.png"
            mock_boto.return_value = s3

            resp = c.get("/employee/6")
            assert resp.status_code == 200
            assert b"https://s3.example.com/x.png" in resp.data

    def test_view_employee_s3_error_is_silent(self, client):
        c, db_mock = client
        db_mock.load_employee.return_value = make_employee(id="6", object_key="bad.png")

        with patch("boto3.client") as mock_boto:
            s3 = MagicMock()
            s3.generate_presigned_url.side_effect = Exception("boom")
            mock_boto.return_value = s3

            resp = c.get("/employee/6")
            assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Delete route  /delete/<employee_id>
# ---------------------------------------------------------------------------


class TestDeleteRoute:

    def test_delete_employee(self, client):
        c, db_mock = client
        db_mock.list_employees.return_value = []
        resp = c.get("/delete/3", follow_redirects=True)
        assert resp.status_code == 200
        db_mock.delete_employee.assert_called_once_with("3")

    def test_delete_redirects_to_home(self, client):
        c, db_mock = client
        db_mock.list_employees.return_value = []
        resp = c.get("/delete/3", follow_redirects=False)
        assert resp.status_code == 302
        assert "/" in resp.headers["Location"]


# ---------------------------------------------------------------------------
# Info route  /info
# ---------------------------------------------------------------------------


class TestInfoRoute:

    def test_info_page_loads(self, client):
        c, _ = client
        resp = c.get("/info")
        assert resp.status_code == 200

    def test_info_shows_instance_data(self, client):
        c, _ = client
        resp = c.get("/info")
        assert b"instance_id" in resp.data
        assert b"availability_zone" in resp.data


# ---------------------------------------------------------------------------
# Stress CPU route  /info/stress_cpu/<seconds>
# ---------------------------------------------------------------------------


class TestStressRoute:

    def test_stress_calls_subprocess(self, client):
        c, _ = client
        with patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value = MagicMock()
            resp = c.get("/info/stress_cpu/60", follow_redirects=True)
            assert resp.status_code == 200
            mock_popen.assert_called_once_with(
                ["stress", "--cpu", "8", "--timeout", "60"]
            )

    def test_stress_redirects_to_info(self, client):
        c, _ = client
        with patch("subprocess.Popen"):
            resp = c.get("/info/stress_cpu/300", follow_redirects=False)
            assert resp.status_code == 302
            assert "info" in resp.headers["Location"]


# ---------------------------------------------------------------------------
# Before-request globals
# ---------------------------------------------------------------------------


class TestBeforeRequest:

    def test_globals_are_set(self, client):
        """g.instance_id and g.availability_zone should be populated."""
        c, _ = client
        resp = c.get("/info")
        assert resp.status_code == 200
        # The rendered template echoes these values
        assert b"i-" in resp.data  # partial instance-id match


# ---------------------------------------------------------------------------
# Badge rendering
# ---------------------------------------------------------------------------


class TestBadges:

    def test_badges_appear_on_employee_view(self, client):
        c, db_mock = client
        db_mock.load_employee.return_value = make_employee(
            id="10", badges="coffee,trophy"
        )

        with patch("boto3.client"):
            resp = c.get("/employee/10")
            assert resp.status_code == 200
            assert b"coffee" in resp.data or b"Coffee" in resp.data

    def test_missing_badge_not_rendered(self, client):
        c, db_mock = client
        db_mock.load_employee.return_value = make_employee(id="11", badges="")

        with patch("boto3.client"):
            resp = c.get("/employee/11")
            assert resp.status_code == 200
            # Trophy icon should not appear when badge not assigned
            assert b"Employee of the Month" not in resp.data
