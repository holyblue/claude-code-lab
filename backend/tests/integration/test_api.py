"""
Integration tests for API endpoints.

Tests the full API stack including routes, services, and database.
"""

import pytest
from datetime import date, datetime
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Import app and database
from app.main import app
from app.database import Base
from app.api.dependencies import get_db

# Import all models to ensure they're registered with Base
from app.models import (
    AccountGroup,
    WorkCategory,
    Project,
    TimeEntry,
    WorkTemplate,
    Setting,
)


# Test database URL
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Override the get_db dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Create all tables before tests and drop after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    # Clean up test database file
    import os
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture(scope="function")
def db() -> Session:
    """Get a database session for test data setup."""
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function", autouse=True)
def clean_database(db):
    """Clean all data between tests."""
    yield
    # Clean up all tables in reverse order to avoid foreign key constraints
    db.query(TimeEntry).delete()
    db.query(Project).delete()
    db.query(WorkCategory).delete()
    db.query(AccountGroup).delete()
    db.query(WorkTemplate).delete()
    db.query(Setting).delete()
    db.commit()


@pytest.fixture(scope="module")
def client():
    """Create a test client."""
    return TestClient(app)


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

    def test_create_duplicate_account_group(self, client, db):
        """Test creating duplicate account group returns 400."""
        # Create first one
        ag = AccountGroup(code="A00", name="中概全權")
        db.add(ag)
        db.commit()

        # Try to create duplicate
        response = client.post(
            "/api/account-groups/",
            json={
                "code": "A00",
                "name": "中概全權",
                "is_default": False,
            },
        )
        assert response.status_code == 400

    def test_list_account_groups(self, client, db):
        """Test listing account groups via API."""
        # Create test data
        db.add(AccountGroup(code="A00", name="中概全權"))
        db.add(AccountGroup(code="O18", name="數據智能應用科"))
        db.commit()

        response = client.get("/api/account-groups/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    def test_get_account_group(self, client, db):
        """Test getting specific account group via API."""
        ag = AccountGroup(code="A00", name="中概全權")
        db.add(ag)
        db.commit()
        db.refresh(ag)

        response = client.get(f"/api/account-groups/{ag.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "A00"

    def test_get_nonexistent_account_group(self, client):
        """Test getting nonexistent account group returns 404."""
        response = client.get("/api/account-groups/99999")
        assert response.status_code == 404

    def test_update_account_group(self, client, db):
        """Test updating account group via API."""
        ag = AccountGroup(code="A00", name="中概全權")
        db.add(ag)
        db.commit()
        db.refresh(ag)

        response = client.patch(
            f"/api/account-groups/{ag.id}",
            json={"name": "Updated Name"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"

    def test_delete_account_group(self, client, db):
        """Test deleting account group via API."""
        ag = AccountGroup(code="A00", name="中概全權")
        db.add(ag)
        db.commit()
        db.refresh(ag)

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

    def test_create_duplicate_project(self, client, db):
        """Test creating duplicate project returns 400."""
        # Create first one
        db.add(Project(code="P1", requirement_code="R1", name="Test"))
        db.commit()

        # Try to create duplicate
        response = client.post(
            "/api/projects/",
            json={
                "code": "P1",
                "requirement_code": "R2",
                "name": "Duplicate",
            },
        )
        assert response.status_code == 400

    def test_list_projects_with_filter(self, client, db):
        """Test listing projects with status filter."""
        db.add(Project(code="P1", requirement_code="R1", name="Active", status="active"))
        db.add(Project(code="P2", requirement_code="R2", name="Completed", status="completed"))
        db.commit()

        response = client.get("/api/projects/?status=active")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["status"] == "active"

    def test_get_nonexistent_project(self, client):
        """Test getting nonexistent project returns 404."""
        response = client.get("/api/projects/99999")
        assert response.status_code == 404

    def test_update_project(self, client, db):
        """Test updating project."""
        proj = Project(code="P1", requirement_code="R1", name="Test")
        db.add(proj)
        db.commit()
        db.refresh(proj)

        response = client.patch(
            f"/api/projects/{proj.id}",
            json={"name": "Updated Name"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"

    def test_soft_delete_project(self, client, db):
        """Test soft deleting a project."""
        proj = Project(code="P1", requirement_code="R1", name="Test")
        db.add(proj)
        db.commit()
        db.refresh(proj)

        response = client.delete(f"/api/projects/{proj.id}")
        assert response.status_code == 204

        # Verify soft delete
        db.refresh(proj)
        assert proj.deleted_at is not None


class TestWorkCategoryAPI:
    """Test WorkCategory API endpoints."""

    def test_create_work_category(self, client):
        """Test creating work category."""
        response = client.post(
            "/api/work-categories/",
            json={
                "code": "A07",
                "name": "其它",
                "deduct_approved_hours": True,
                "is_default": True,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == "A07"
        assert data["deduct_approved_hours"] is True

    def test_create_duplicate_work_category(self, client, db):
        """Test creating duplicate work category returns 400."""
        db.add(WorkCategory(code="A07", name="其它"))
        db.commit()

        response = client.post(
            "/api/work-categories/",
            json={
                "code": "A07",
                "name": "其它",
                "deduct_approved_hours": False,
            },
        )
        assert response.status_code == 400

    def test_list_work_categories(self, client, db):
        """Test listing work categories."""
        db.add(WorkCategory(code="A07", name="其它", deduct_approved_hours=True))
        db.add(WorkCategory(code="A08", name="商模", deduct_approved_hours=False))
        db.commit()

        response = client.get("/api/work-categories/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2

    def test_get_work_category(self, client, db):
        """Test getting specific work category."""
        wc = WorkCategory(code="A07", name="其它")
        db.add(wc)
        db.commit()
        db.refresh(wc)

        response = client.get(f"/api/work-categories/{wc.id}")
        assert response.status_code == 200
        assert response.json()["code"] == "A07"

    def test_get_nonexistent_work_category(self, client):
        """Test getting nonexistent work category returns 404."""
        response = client.get("/api/work-categories/99999")
        assert response.status_code == 404

    def test_update_work_category(self, client, db):
        """Test updating work category."""
        wc = WorkCategory(code="A07", name="其它")
        db.add(wc)
        db.commit()
        db.refresh(wc)

        response = client.patch(
            f"/api/work-categories/{wc.id}",
            json={"deduct_approved_hours": False},
        )
        assert response.status_code == 200
        assert response.json()["deduct_approved_hours"] is False

    def test_delete_work_category(self, client, db):
        """Test deleting work category."""
        wc = WorkCategory(code="A07", name="其它")
        db.add(wc)
        db.commit()
        db.refresh(wc)

        response = client.delete(f"/api/work-categories/{wc.id}")
        assert response.status_code == 204


class TestTimeEntryAPI:
    """Test TimeEntry API endpoints."""

    def test_create_time_entry(self, client, db):
        """Test creating time entry via API."""
        # Setup required foreign key data
        ag = AccountGroup(code="A00", name="中概全權")
        wc = WorkCategory(code="A07", name="其它", deduct_approved_hours=True)
        proj = Project(code="需2025單001", requirement_code="R1", name="Test")
        db.add_all([ag, wc, proj])
        db.commit()
        db.refresh(ag)
        db.refresh(wc)
        db.refresh(proj)

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

    def test_create_time_entry_without_account_group(self, client, db):
        """Test creating time entry without account group (optional field)."""
        # Setup required foreign key data (without account group)
        wc = WorkCategory(code="A07", name="其它", deduct_approved_hours=True)
        proj = Project(code="需2025單001", requirement_code="R1", name="Test")
        db.add_all([wc, proj])
        db.commit()
        db.refresh(wc)
        db.refresh(proj)

        response = client.post(
            "/api/time-entries/",
            json={
                "date": "2025-11-24",
                "project_id": proj.id,
                "account_group_id": None,  # 模組為空（選填）
                "work_category_id": wc.id,
                "hours": 3.0,
                "description": "測試不選擇模組",
                "display_order": 0,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["date"] == "2025-11-24"
        assert float(data["hours"]) == 3.0
        assert data["account_group_id"] is None  # 驗證模組為 None
        assert data["description"] == "測試不選擇模組"

    def test_create_time_entry_invalid_project(self, client, db):
        """Test creating time entry with invalid project ID."""
        ag = AccountGroup(code="A00", name="Test")
        wc = WorkCategory(code="A07", name="Test")
        db.add_all([ag, wc])
        db.commit()

        response = client.post(
            "/api/time-entries/",
            json={
                "date": "2025-11-14",
                "project_id": 99999,  # Non-existent
                "account_group_id": ag.id,
                "work_category_id": wc.id,
                "hours": 7.5,
                "description": "Test",
                "display_order": 0,
            },
        )
        assert response.status_code == 404

    def test_list_time_entries_by_date_range(self, client, db):
        """Test listing time entries with date range filter."""
        # Setup
        ag = AccountGroup(code="A00", name="Test")
        wc = WorkCategory(code="A07", name="Test")
        proj = Project(code="P1", requirement_code="R1", name="Test")
        db.add_all([ag, wc, proj])
        db.commit()

        # Add entries
        db.add(
            TimeEntry(
                date=date(2025, 11, 10),
                project_id=proj.id,
                account_group_id=ag.id,
                work_category_id=wc.id,
                hours=Decimal("4.0"),
                description="Day 1",
            )
        )
        db.add(
            TimeEntry(
                date=date(2025, 11, 15),
                project_id=proj.id,
                account_group_id=ag.id,
                work_category_id=wc.id,
                hours=Decimal("4.0"),
                description="Day 2",
            )
        )
        db.commit()

        response = client.get("/api/time-entries/?start_date=2025-11-12&end_date=2025-11-20")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1

    def test_get_time_entry(self, client, db):
        """Test getting specific time entry."""
        ag = AccountGroup(code="A00", name="Test")
        wc = WorkCategory(code="A07", name="Test")
        proj = Project(code="P1", requirement_code="R1", name="Test")
        db.add_all([ag, wc, proj])
        db.commit()

        entry = TimeEntry(
            date=date(2025, 11, 14),
            project_id=proj.id,
            account_group_id=ag.id,
            work_category_id=wc.id,
            hours=Decimal("7.5"),
            description="Test",
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)

        response = client.get(f"/api/time-entries/{entry.id}")
        assert response.status_code == 200
        assert response.json()["id"] == entry.id

    def test_update_time_entry(self, client, db):
        """Test updating time entry."""
        ag = AccountGroup(code="A00", name="Test")
        wc = WorkCategory(code="A07", name="Test")
        proj = Project(code="P1", requirement_code="R1", name="Test")
        db.add_all([ag, wc, proj])
        db.commit()

        entry = TimeEntry(
            date=date(2025, 11, 14),
            project_id=proj.id,
            account_group_id=ag.id,
            work_category_id=wc.id,
            hours=Decimal("7.5"),
            description="Test",
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)

        response = client.patch(
            f"/api/time-entries/{entry.id}",
            json={"hours": 4.0, "description": "Updated"},
        )
        assert response.status_code == 200
        data = response.json()
        assert float(data["hours"]) == 4.0
        assert data["description"] == "Updated"

    def test_delete_time_entry(self, client, db):
        """Test deleting time entry."""
        ag = AccountGroup(code="A00", name="Test")
        wc = WorkCategory(code="A07", name="Test")
        proj = Project(code="P1", requirement_code="R1", name="Test")
        db.add_all([ag, wc, proj])
        db.commit()

        entry = TimeEntry(
            date=date(2025, 11, 14),
            project_id=proj.id,
            account_group_id=ag.id,
            work_category_id=wc.id,
            hours=Decimal("7.5"),
            description="Test",
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)

        response = client.delete(f"/api/time-entries/{entry.id}")
        assert response.status_code == 204


class TestStatsAPI:
    """Test Statistics API endpoints."""

    def test_get_project_statistics(self, client, db):
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
        db.add_all([ag, wc_deduct, wc_non_deduct, proj])
        db.commit()

        # Add time entries
        db.add(
            TimeEntry(
                date=date(2025, 11, 14),
                project_id=proj.id,
                account_group_id=ag.id,
                work_category_id=wc_deduct.id,
                hours=Decimal("120.0"),  # 80% usage
                description="Deduct work",
            )
        )
        db.add(
            TimeEntry(
                date=date(2025, 11, 14),
                project_id=proj.id,
                account_group_id=ag.id,
                work_category_id=wc_non_deduct.id,
                hours=Decimal("10.0"),
                description="Non-deduct work",
            )
        )
        db.commit()

        response = client.get(f"/api/stats/projects/{proj.id}")
        assert response.status_code == 200
        data = response.json()
        assert float(data["used_hours"]) == 120.0
        assert float(data["non_deduct_hours"]) == 10.0
        assert float(data["total_hours"]) == 130.0
        assert float(data["usage_rate"]) == 80.0
        assert data["warning_level"] == "warning"

    def test_get_nonexistent_project_statistics(self, client):
        """Test getting statistics for nonexistent project."""
        response = client.get("/api/stats/projects/99999")
        assert response.status_code == 404

    def test_get_all_project_statistics(self, client, db):
        """Test getting statistics for all projects."""
        # Setup
        ag = AccountGroup(code="A00", name="Test")
        wc = WorkCategory(code="A07", name="Test", deduct_approved_hours=True)
        proj1 = Project(code="P1", requirement_code="R1", name="Project 1")
        proj2 = Project(code="P2", requirement_code="R2", name="Project 2")
        db.add_all([ag, wc, proj1, proj2])
        db.commit()

        # Add entries for both projects
        db.add(
            TimeEntry(
                date=date(2025, 11, 14),
                project_id=proj1.id,
                account_group_id=ag.id,
                work_category_id=wc.id,
                hours=Decimal("10.0"),
                description="Test 1",
            )
        )
        db.add(
            TimeEntry(
                date=date(2025, 11, 14),
                project_id=proj2.id,
                account_group_id=ag.id,
                work_category_id=wc.id,
                hours=Decimal("20.0"),
                description="Test 2",
            )
        )
        db.commit()

        response = client.get("/api/stats/projects")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


class TestTCSAPI:
    """Test TCS formatting API endpoints."""

    def test_format_single_date(self, client, db):
        """Test formatting time entries for TCS."""
        # Setup
        ag = AccountGroup(code="A00", name="中概全權")
        wc = WorkCategory(code="A07", name="其它")
        proj = Project(code="需2025單001", requirement_code="R1", name="AI系統")
        db.add_all([ag, wc, proj])
        db.commit()

        db.add(
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
        db.commit()

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

    def test_format_nonexistent_date(self, client):
        """Test formatting nonexistent date returns 404."""
        response = client.post(
            "/api/tcs/format",
            json={"date": "2025-12-31"},
        )
        assert response.status_code == 404

    def test_format_date_range(self, client, db):
        """Test formatting date range for TCS."""
        # Setup
        ag = AccountGroup(code="A00", name="Test")
        wc = WorkCategory(code="A07", name="Test")
        proj = Project(code="P1", requirement_code="R1", name="Test")
        db.add_all([ag, wc, proj])
        db.commit()

        # Add entries for two dates
        db.add(
            TimeEntry(
                date=date(2025, 11, 14),
                project_id=proj.id,
                account_group_id=ag.id,
                work_category_id=wc.id,
                hours=Decimal("4.0"),
                description="Day 1",
            )
        )
        db.add(
            TimeEntry(
                date=date(2025, 11, 15),
                project_id=proj.id,
                account_group_id=ag.id,
                work_category_id=wc.id,
                hours=Decimal("3.5"),
                description="Day 2",
            )
        )
        db.commit()

        response = client.post(
            "/api/tcs/format/range",
            json={
                "start_date": "2025-11-14",
                "end_date": "2025-11-15",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["start_date"] == "2025/11/14"
        assert data["end_date"] == "2025/11/15"
        assert len(data["daily_formats"]) == 2
        assert float(data["total_hours"]) == 7.5
