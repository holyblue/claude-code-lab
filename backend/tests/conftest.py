"""
Pytest configuration and fixtures for time tracking system tests.

This module provides shared fixtures and configuration for all tests.
"""

import os
import sys
from datetime import datetime, timezone
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# ============================================================================
# Database Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def test_db_url() -> str:
    """Return test database URL (in-memory SQLite)."""
    return "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_engine(test_db_url: str):
    """
    Create a test database engine.

    Uses in-memory SQLite for fast test execution.
    Engine is created fresh for each test function.
    """
    engine = create_engine(
        test_db_url,
        connect_args={"check_same_thread": False},
        echo=False  # Set to True for SQL debugging
    )
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """
    Create a test database session.

    Creates all tables before test and drops them after.
    Provides a clean database state for each test.
    """
    from app.database import Base

    # Create all tables
    Base.metadata.create_all(bind=db_engine)

    # Create session
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=db_engine)


@pytest.fixture(scope="function")
def db(db_session) -> Generator[Session, None, None]:
    """
    Alias for db_session to support BDD step definitions.

    This provides a shorter fixture name for use in step definitions.
    """
    yield db_session


# ============================================================================
# Time & Timezone Fixtures
# ============================================================================

@pytest.fixture
def utc_tz():
    """Return UTC timezone object."""
    return timezone.utc


@pytest.fixture
def utc8_offset():
    """Return UTC+8 timezone offset in hours."""
    return 8


@pytest.fixture
def standard_work_hours() -> float:
    """Return standard work hours per day (7.5)."""
    return 7.5


@pytest.fixture
def max_work_hours() -> float:
    """Return maximum work hours per day (12)."""
    return 12.0


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_project_data():
    """Return sample project data for testing."""
    return {
        "code": "需2025單001",
        "requirement_code": "R202511146001",
        "name": "AI系統",
        "approved_man_days": 20.0,
        "status": "active",
    }


@pytest.fixture
def sample_account_groups():
    """Return sample account groups for testing."""
    return [
        {"code": "A00", "name": "中概全權", "is_default": True},
        {"code": "O18", "name": "數據智能應用科", "is_default": True},
    ]


@pytest.fixture
def sample_work_categories():
    """Return sample work categories for testing."""
    return [
        {"code": "A07", "name": "其它", "deduct_approved_hours": True, "is_default": True},
        {"code": "A08", "name": "商模", "deduct_approved_hours": False, "is_default": True},
        {"code": "B04", "name": "其它", "deduct_approved_hours": True, "is_default": True},
        {"code": "I07", "name": "休假（休假、病假、事假等）", "deduct_approved_hours": False, "is_default": True},
    ]


# ============================================================================
# BDD Context Fixture
# ============================================================================

@pytest.fixture
def bdd_context():
    """
    Provide a shared context dictionary for BDD step definitions.

    This allows steps to share data across Given/When/Then steps.
    """
    return {}


# ============================================================================
# Pytest Hooks
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "bdd: mark test as a BDD test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
