"""
Integration tests for API endpoints.

Tests the full API stack including routes, services, and database.
"""

import pytest
from datetime import date, datetime
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base
from app.api.dependencies import get_db
# Import all models to ensure Base.metadata knows about them
from app.models import (
    AccountGroup,
    WorkCategory,
    Project,
    TimeEntry,
    WorkTemplate,
    Setting,
)


# Create test database per function to avoid shared state
@pytest.fixture(scope="function")
def engine():
    """Create a fresh database engine for each test."""
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine):
    """Create database session for test data setup."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture(scope="function")
def client(engine):
    """Create test client with overridden database dependency."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        """Override database dependency for testing."""
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestAccountGroupAPI:
    """Test AccountGroup API endpoints."""

    def test_create_account_group(self, client):
        """Test creating account group via API."""
        response = client.post(
            "/api/account-groups/",
            json={
                "code": "A00",
                "name": "中概全權",
                "is_default": True,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == "A00"
        assert data["name"] == "中概全權"
        assert data["is_default"] is True
        assert "id" in data

    def test_list_account_groups(self, client, db_session):
        """Test listing account groups via API."""
        # Create test data
        db_session.add(AccountGroup(code="A00", name="中概全權"))
        db_session.add(AccountGroup(code="O18", name="數據智能應用科"))
        db_session.commit()

        response = client.get("/api/account-groups/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    def test_get_account_group(self, client, db_session):
        """Test getting specific account group via API."""
        ag = AccountGroup(code="A00", name="中概全權")
        db_session.add(ag)
        db_session.commit()
        db_session.refresh(ag)

        response = client.get(f"/api/account-groups/{ag.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "A00"

    def test_update_account_group(self, client, db_session):
        """Test updating account group via API."""
        ag = AccountGroup(code="A00", name="中概全權")
        db_session.add(ag)
        db_session.commit()
        db_session.refresh(ag)

        response = client.patch(
            f"/api/account-groups/{ag.id}",
            json={"name": "Updated Name"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"

    def test_delete_account_group(self, client, db_session):
        """Test deleting account group via API."""
        ag = AccountGroup(code="A00", name="中概全權")
        db_session.add(ag)
        db_session.commit()
        db_session.refresh(ag)

        response = client.delete(f"/api/account-groups/{ag.id}")
        assert response.status_code == 204


class TestProjectAPI:
    """Test Project API endpoints."""

    def test_create_project(self, client):
        """Test creating project via API."""
        response = client.post(
            "/api/projects/",
            json={
                "code": "需2025單001",
                "requirement_code": "R202511146001",
                "name": "AI系統開發",
                "approved_man_days": 20.5,
                "status": "active",
                "color": "#409EFF",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == "需2025單001"
        assert float(data["approved_man_days"]) == 20.5

    def test_list_projects_with_filter(self, client, db_session):
        """Test listing projects with status filter."""
        db_session.add(Project(code="P1", requirement_code="R1", name="Active", status="active"))
        db_session.add(Project(code="P2", requirement_code="R2", name="Completed", status="completed"))
        db_session.commit()

        response = client.get("/api/projects/?status=active")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["status"] == "active"


class TestTimeEntryAPI:
    """Test TimeEntry API endpoints."""

    def test_create_time_entry(self, client, db_session):
        """Test creating time entry via API."""
        # Setup required foreign key data
        ag = AccountGroup(code="A00", name="中概全權")
        wc = WorkCategory(code="A07", name="其它", deduct_approved_hours=True)
        proj = Project(code="需2025單001", requirement_code="R1", name="Test")
        db_session.add_all([ag, wc, proj])
        db_session.commit()
        db_session.refresh(ag)
        db_session.refresh(wc)
        db_session.refresh(proj)

        response = client.post(
            "/api/time-entries/",
            json={
                "date": "2025-11-14",
                "project_id": proj.id,
                "account_group_id": ag.id,
                "work_category_id": wc.id,
                "hours": 7.5,
                "description": "完成系統開發",
                "display_order": 0,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["date"] == "2025-11-14"
        assert float(data["hours"]) == 7.5

    def test_list_time_entries_by_date_range(self, client, db_session):
        """Test listing time entries with date range filter."""
        # Setup
        ag = AccountGroup(code="A00", name="Test")
        wc = WorkCategory(code="A07", name="Test")
        proj = Project(code="P1", requirement_code="R1", name="Test")
        db_session.add_all([ag, wc, proj])
        db_session.commit()

        # Add entries
        db_session.add(
            TimeEntry(
                date=date(2025, 11, 10),
                project_id=proj.id,
                account_group_id=ag.id,
                work_category_id=wc.id,
                hours=Decimal("4.0"),
                description="Day 1",
            )
        )
        db_session.add(
            TimeEntry(
                date=date(2025, 11, 15),
                project_id=proj.id,
                account_group_id=ag.id,
                work_category_id=wc.id,
                hours=Decimal("4.0"),
                description="Day 2",
            )
        )
        db_session.commit()

        response = client.get("/api/time-entries/?start_date=2025-11-12&end_date=2025-11-20")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1


class TestStatsAPI:
    """Test Statistics API endpoints."""

    def test_get_project_statistics(self, client, db_session):
        """Test getting project statistics."""
        # Setup
        ag = AccountGroup(code="A00", name="Test")
        wc_deduct = WorkCategory(code="A07", name="其它", deduct_approved_hours=True)
        wc_non_deduct = WorkCategory(code="A08", name="商模", deduct_approved_hours=False)
        proj = Project(
            code="需2025單001",
            requirement_code="R1",
            name="Test",
            approved_man_days=Decimal("20"),  # 150 hours
        )
        db_session.add_all([ag, wc_deduct, wc_non_deduct, proj])
        db_session.commit()

        # Add time entries
        db_session.add(
            TimeEntry(
                date=date(2025, 11, 14),
                project_id=proj.id,
                account_group_id=ag.id,
                work_category_id=wc_deduct.id,
                hours=Decimal("120.0"),  # 80% usage
                description="Deduct work",
            )
        )
        db_session.add(
            TimeEntry(
                date=date(2025, 11, 14),
                project_id=proj.id,
                account_group_id=ag.id,
                work_category_id=wc_non_deduct.id,
                hours=Decimal("10.0"),
                description="Non-deduct work",
            )
        )
        db_session.commit()

        response = client.get(f"/api/stats/projects/{proj.id}")
        assert response.status_code == 200
        data = response.json()
        assert float(data["used_hours"]) == 120.0
        assert float(data["non_deduct_hours"]) == 10.0
        assert float(data["total_hours"]) == 130.0
        assert float(data["usage_rate"]) == 80.0
        assert data["warning_level"] == "warning"


class TestTCSAPI:
    """Test TCS formatting API endpoints."""

    def test_format_single_date(self, client, db_session):
        """Test formatting time entries for TCS."""
        # Setup
        ag = AccountGroup(code="A00", name="中概全權")
        wc = WorkCategory(code="A07", name="其它")
        proj = Project(code="需2025單001", requirement_code="R1", name="AI系統")
        db_session.add_all([ag, wc, proj])
        db_session.commit()

        db_session.add(
            TimeEntry(
                date=date(2025, 11, 14),
                project_id=proj.id,
                account_group_id=ag.id,
                work_category_id=wc.id,
                hours=Decimal("4.0"),
                description="完成開發",
                display_order=0,
            )
        )
        db_session.commit()

        response = client.post(
            "/api/tcs/format",
            json={"date": "2025-11-14"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["date"] == "2025/11/14"
        assert float(data["total_hours"]) == 4.0
        assert "formatted_text" in data
        assert "需2025單001" in data["formatted_text"]
