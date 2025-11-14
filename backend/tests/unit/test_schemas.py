"""
Unit tests for Pydantic schemas.

Tests validate that schemas properly validate input data and serialize responses.
"""

import pytest
from datetime import datetime, date
from decimal import Decimal
from pydantic import ValidationError

from app.schemas import (
    AccountGroupCreate,
    AccountGroupUpdate,
    AccountGroupResponse,
    WorkCategoryCreate,
    WorkCategoryUpdate,
    WorkCategoryResponse,
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    TimeEntryCreate,
    TimeEntryUpdate,
    TimeEntryResponse,
    ProjectStats,
    TCSFormatRequest,
)


class TestAccountGroupSchemas:
    """Test AccountGroup schemas."""

    def test_account_group_create_valid(self):
        """Test creating account group with valid data."""
        data = {
            "code": "A00",
            "name": "中概全權",
            "is_default": True,
        }
        schema = AccountGroupCreate(**data)
        assert schema.code == "A00"
        assert schema.name == "中概全權"
        assert schema.is_default is True

    def test_account_group_create_missing_required(self):
        """Test creating account group without required fields."""
        with pytest.raises(ValidationError) as exc_info:
            AccountGroupCreate(code="A00")
        assert "name" in str(exc_info.value)

    def test_account_group_create_invalid_length(self):
        """Test creating account group with invalid field length."""
        with pytest.raises(ValidationError):
            AccountGroupCreate(code="", name="Test")

    def test_account_group_update_partial(self):
        """Test updating account group with partial data."""
        data = {"name": "Updated Name"}
        schema = AccountGroupUpdate(**data)
        assert schema.name == "Updated Name"
        assert schema.code is None

    def test_account_group_response_from_orm(self):
        """Test account group response schema with ORM mode."""
        # Simulate ORM object
        class MockORM:
            id = 1
            code = "A00"
            name = "中概全權"
            is_default = True
            full_name = "A00 中概全權"
            created_at = datetime.now()
            updated_at = datetime.now()

        schema = AccountGroupResponse.model_validate(MockORM())
        assert schema.id == 1
        assert schema.full_name == "A00 中概全權"


class TestWorkCategorySchemas:
    """Test WorkCategory schemas."""

    def test_work_category_create_valid(self):
        """Test creating work category with valid data."""
        data = {
            "code": "A07",
            "name": "其它",
            "deduct_approved_hours": True,
            "is_default": True,
        }
        schema = WorkCategoryCreate(**data)
        assert schema.code == "A07"
        assert schema.deduct_approved_hours is True

    def test_work_category_create_defaults(self):
        """Test work category create with default values."""
        data = {"code": "A07", "name": "其它"}
        schema = WorkCategoryCreate(**data)
        assert schema.deduct_approved_hours is True
        assert schema.is_default is False

    def test_work_category_update_partial(self):
        """Test updating work category with partial data."""
        data = {"deduct_approved_hours": False}
        schema = WorkCategoryUpdate(**data)
        assert schema.deduct_approved_hours is False
        assert schema.code is None


class TestProjectSchemas:
    """Test Project schemas."""

    def test_project_create_valid(self):
        """Test creating project with valid data."""
        data = {
            "code": "需2025單001",
            "requirement_code": "R202511146001",
            "name": "AI系統開發",
            "approved_man_days": Decimal("20.5"),
            "status": "active",
            "color": "#409EFF",
        }
        schema = ProjectCreate(**data)
        assert schema.code == "需2025單001"
        assert schema.approved_man_days == Decimal("20.5")

    def test_project_create_invalid_color(self):
        """Test creating project with invalid color format."""
        with pytest.raises(ValidationError):
            ProjectCreate(
                code="需2025單001",
                requirement_code="R202511146001",
                name="Test",
                color="invalid",
            )

    def test_project_create_negative_man_days(self):
        """Test creating project with negative man days."""
        with pytest.raises(ValidationError):
            ProjectCreate(
                code="需2025單001",
                requirement_code="R202511146001",
                name="Test",
                approved_man_days=Decimal("-10"),
            )

    def test_project_update_partial(self):
        """Test updating project with partial data."""
        data = {"status": "completed"}
        schema = ProjectUpdate(**data)
        assert schema.status == "completed"
        assert schema.name is None


class TestTimeEntrySchemas:
    """Test TimeEntry schemas."""

    def test_time_entry_create_valid(self):
        """Test creating time entry with valid data."""
        data = {
            "date": date(2025, 11, 14),
            "project_id": 1,
            "account_group_id": 1,
            "work_category_id": 1,
            "hours": Decimal("7.5"),
            "description": "完成系統開發",
            "display_order": 0,
        }
        schema = TimeEntryCreate(**data)
        assert schema.hours == Decimal("7.5")
        assert schema.description == "完成系統開發"

    def test_time_entry_create_invalid_hours(self):
        """Test creating time entry with invalid hours."""
        with pytest.raises(ValidationError):
            TimeEntryCreate(
                date=date(2025, 11, 14),
                project_id=1,
                account_group_id=1,
                work_category_id=1,
                hours=Decimal("100"),  # Exceeds max 99.99
                description="Test",
            )

    def test_time_entry_create_negative_hours(self):
        """Test creating time entry with negative hours."""
        with pytest.raises(ValidationError):
            TimeEntryCreate(
                date=date(2025, 11, 14),
                project_id=1,
                account_group_id=1,
                work_category_id=1,
                hours=Decimal("-1"),
                description="Test",
            )

    def test_time_entry_update_partial(self):
        """Test updating time entry with partial data."""
        data = {"hours": Decimal("4.5")}
        schema = TimeEntryUpdate(**data)
        assert schema.hours == Decimal("4.5")
        assert schema.description is None


class TestStatsSchemas:
    """Test Stats schemas."""

    def test_project_stats_valid(self):
        """Test project stats with valid data."""
        data = {
            "project_id": 1,
            "project_code": "需2025單001",
            "project_name": "AI系統",
            "approved_hours": Decimal("150"),
            "used_hours": Decimal("120"),
            "non_deduct_hours": Decimal("10"),
            "total_hours": Decimal("130"),
            "remaining_hours": Decimal("30"),
            "usage_rate": Decimal("80.0"),
            "warning_level": "warning",
            "warning_message": "專案工時使用率已達 80%",
        }
        schema = ProjectStats(**data)
        assert schema.usage_rate == Decimal("80.0")
        assert schema.warning_level == "warning"
        assert schema.is_over_budget is False

    def test_project_stats_over_budget(self):
        """Test project stats when over budget."""
        data = {
            "project_id": 1,
            "project_code": "需2025單001",
            "project_name": "AI系統",
            "approved_hours": Decimal("100"),
            "used_hours": Decimal("120"),
            "non_deduct_hours": Decimal("0"),
            "total_hours": Decimal("120"),
            "remaining_hours": Decimal("-20"),
            "usage_rate": Decimal("120.0"),
            "warning_level": "danger",
        }
        schema = ProjectStats(**data)
        assert schema.is_over_budget is True


class TestTCSSchemas:
    """Test TCS schemas."""

    def test_tcs_format_request_valid(self):
        """Test TCS format request with valid data."""
        data = {"date": date(2025, 11, 14)}
        schema = TCSFormatRequest(**data)
        assert schema.date == date(2025, 11, 14)

    def test_tcs_format_request_invalid_date(self):
        """Test TCS format request with invalid date."""
        with pytest.raises(ValidationError):
            TCSFormatRequest(date="invalid-date")
