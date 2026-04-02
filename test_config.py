"""
Test suite for config.py — Central configuration module.
Tests that environment variables are correctly loaded,
optional variables default to None, and missing required
variables raise an appropriate error.
"""

import pytest
import sys


def reload_config(env_vars):
    """
    Helper to reload config.py with a controlled set of
    environment variables using patch.dict.
    """
    from unittest.mock import patch

    with patch.dict("os.environ", env_vars, clear=True):
        if "config" in sys.modules:
            del sys.modules["config"]
        import config

        return config


def test_photos_bucket_missing_raises_error():
    """PHOTOS_BUCKET is required — a missing value should raise KeyError."""
    with pytest.raises(KeyError):
        reload_config({})  # No PHOTOS_BUCKET set


def test_all_variables_loaded_correctly():
    """All environment variables should load correctly when fully set."""
    config = reload_config(
        {
            "PHOTOS_BUCKET": "my-test-bucket",
            "DATABASE_HOST": "db.example.com",
            "DATABASE_USER": "admin",
            "DATABASE_PASSWORD": "supersecret",
            "DATABASE_DB_NAME": "employees",
        }
    )
    assert config.PHOTOS_BUCKET == "my-test-bucket"
    assert config.DATABASE_HOST == "db.example.com"
    assert config.DATABASE_USER == "admin"
    assert config.DATABASE_PASSWORD == "supersecret"
    assert config.DATABASE_DB_NAME == "employees"


def test_optional_variables_all_default_to_none():
    """All optional variables should be None when not set."""
    config = reload_config({"PHOTOS_BUCKET": "my-test-bucket"})
    assert config.DATABASE_HOST is None
    assert config.DATABASE_USER is None
    assert config.DATABASE_PASSWORD is None
    assert config.DATABASE_DB_NAME is None
