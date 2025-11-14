"""
Unit tests for SQLAlchemy database models.

Testing Strategy (TDD):
1. Write test first (Red)
2. Implement model (Green)
3. Refactor if needed (Refactor)
"""

import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from app.models.project import Project
from app.models.account_group import AccountGroup
from app.models.work_category import WorkCategory
from app.models.time_entry import TimeEntry
from app.models.work_template import WorkTemplate
from app.models.setting import Setting


class TestProjectModel:
    """Test cases for Project model."""

    def test_create_project_with_required_fields(self, db_session):
        """
        Test creating a project with all required fields.

        Required fields:
        - code: Project code (e.g., 需2025單001)
        - requirement_code: Requirement code (e.g., R202511146001)
        - name: Project name
        """
        project = Project(
            code="需2025單001",
            requirement_code="R202511146001",
            name="AI系統"
        )
        db_session.add(project)
        db_session.commit()

        # Verify project was created
        assert project.id is not None
        assert project.code == "需2025單001"
        assert project.requirement_code == "R202511146001"
        assert project.name == "AI系統"
        assert project.status == "active"  # Default value

    def test_create_project_with_approved_man_days(self, db_session):
        """
        Test creating a project with approved man-days.

        Business rule: 1 man-day = 7.5 hours
        """
        project = Project(
            code="需2025單002",
            requirement_code="R202511146002",
            name="數據平台",
            approved_man_days=20.0  # 20 man-days = 150 hours
        )
        db_session.add(project)
        db_session.commit()

        assert project.approved_man_days == 20.0

    def test_project_code_must_be_unique(self, db_session):
        """
        Test that project code must be unique.

        Should raise IntegrityError when duplicate code is inserted.
        """
        # Create first project
        project1 = Project(
            code="需2025單001",
            requirement_code="R202511146001",
            name="AI系統"
        )
        db_session.add(project1)
        db_session.commit()

        # Try to create second project with same code
        project2 = Project(
            code="需2025單001",  # Duplicate code
            requirement_code="R202511146003",
            name="其他系統"
        )
        db_session.add(project2)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_project_default_values(self, db_session):
        """Test that default values are set correctly."""
        project = Project(
            code="需2025單003",
            requirement_code="R202511146003",
            name="測試專案"
        )
        db_session.add(project)
        db_session.commit()

        assert project.status == "active"
        assert project.color == "#409EFF"
        assert project.created_at is not None
        assert project.updated_at is not None
        assert project.deleted_at is None

    def test_project_timestamps(self, db_session):
        """Test that timestamps are set automatically."""
        project = Project(
            code="需2025單004",
            requirement_code="R202511146004",
            name="時間戳記測試"
        )
        db_session.add(project)
        db_session.commit()

        # Check created_at and updated_at are set
        assert isinstance(project.created_at, datetime)
        assert isinstance(project.updated_at, datetime)

    def test_project_soft_delete(self, db_session):
        """Test soft delete functionality using deleted_at."""
        project = Project(
            code="需2025單005",
            requirement_code="R202511146005",
            name="軟刪除測試"
        )
        db_session.add(project)
        db_session.commit()

        # Mark as deleted
        project.deleted_at = datetime.utcnow()
        db_session.commit()

        assert project.deleted_at is not None

    def test_project_relationships_with_account_group(self, db_session):
        """Test relationship between Project and AccountGroup."""
        # Create account group
        account_group = AccountGroup(
            code="A00",
            name="中概全權",
            is_default=True
        )
        db_session.add(account_group)
        db_session.commit()

        # Create project with default account group
        project = Project(
            code="需2025單006",
            requirement_code="R202511146006",
            name="關聯測試",
            default_account_group_id=account_group.id
        )
        db_session.add(project)
        db_session.commit()

        assert project.default_account_group_id == account_group.id

    def test_project_relationships_with_work_category(self, db_session):
        """Test relationship between Project and WorkCategory."""
        # Create work category
        work_category = WorkCategory(
            code="A07",
            name="其它",
            deduct_approved_hours=True,
            is_default=True
        )
        db_session.add(work_category)
        db_session.commit()

        # Create project with default work category
        project = Project(
            code="需2025單007",
            requirement_code="R202511146007",
            name="工作類別關聯測試",
            default_work_category_id=work_category.id
        )
        db_session.add(project)
        db_session.commit()

        assert project.default_work_category_id == work_category.id

    def test_project_optional_fields(self, db_session):
        """Test that optional fields can be null."""
        project = Project(
            code="需2025單008",
            requirement_code="R202511146008",
            name="選填欄位測試"
            # Optional fields not provided
        )
        db_session.add(project)
        db_session.commit()

        assert project.approved_man_days is None
        assert project.default_account_group_id is None
        assert project.default_work_category_id is None
        assert project.description is None


class TestAccountGroupModel:
    """Test cases for AccountGroup model."""

    def test_create_account_group(self, db_session):
        """Test creating an account group."""
        account_group = AccountGroup(
            code="A00",
            name="中概全權",
            is_default=True
        )
        db_session.add(account_group)
        db_session.commit()

        assert account_group.id is not None
        assert account_group.code == "A00"
        assert account_group.name == "中概全權"
        assert account_group.is_default is True

    def test_account_group_code_name_unique_together(self, db_session):
        """Test that combination of code and name must be unique."""
        # Create first account group
        ag1 = AccountGroup(code="A00", name="中概全權", is_default=True)
        db_session.add(ag1)
        db_session.commit()

        # Try to create duplicate
        ag2 = AccountGroup(code="A00", name="中概全權", is_default=False)
        db_session.add(ag2)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_account_group_timestamps(self, db_session):
        """Test that timestamps are set automatically."""
        account_group = AccountGroup(code="O18", name="數據智能應用科")
        db_session.add(account_group)
        db_session.commit()

        assert isinstance(account_group.created_at, datetime)
        assert isinstance(account_group.updated_at, datetime)


class TestWorkCategoryModel:
    """Test cases for WorkCategory model."""

    def test_create_work_category_with_deduct_true(self, db_session):
        """Test creating work category that deducts approved hours (A07)."""
        category = WorkCategory(
            code="A07",
            name="其它",
            deduct_approved_hours=True,
            is_default=True
        )
        db_session.add(category)
        db_session.commit()

        assert category.id is not None
        assert category.code == "A07"
        assert category.name == "其它"
        assert category.deduct_approved_hours is True

    def test_create_work_category_with_deduct_false(self, db_session):
        """
        Test creating work category that does NOT deduct approved hours (A08 商模).

        Business rule: A08 商模 work counts as project hours but doesn't
        consume approved budget.
        """
        category = WorkCategory(
            code="A08",
            name="商模",
            deduct_approved_hours=False,  # Does NOT deduct
            is_default=True
        )
        db_session.add(category)
        db_session.commit()

        assert category.code == "A08"
        assert category.name == "商模"
        assert category.deduct_approved_hours is False

    def test_work_category_default_deduct_value(self, db_session):
        """Test that deduct_approved_hours defaults to True."""
        category = WorkCategory(
            code="B04",
            name="其它"
            # deduct_approved_hours not specified
        )
        db_session.add(category)
        db_session.commit()

        assert category.deduct_approved_hours is True

    def test_work_category_code_name_unique_together(self, db_session):
        """Test that combination of code and name must be unique."""
        # Create first category
        cat1 = WorkCategory(code="A07", name="其它", deduct_approved_hours=True)
        db_session.add(cat1)
        db_session.commit()

        # Try to create duplicate
        cat2 = WorkCategory(code="A07", name="其它", deduct_approved_hours=False)
        db_session.add(cat2)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_work_category_vacation_type(self, db_session):
        """Test creating I07 休假 category (does not deduct)."""
        category = WorkCategory(
            code="I07",
            name="休假（休假、病假、事假等）",
            deduct_approved_hours=False,
            is_default=True
        )
        db_session.add(category)
        db_session.commit()

        assert category.code == "I07"
        assert category.deduct_approved_hours is False


class TestTimeEntryModel:
    """Test cases for TimeEntry model."""

    def test_create_time_entry_with_required_fields(self, db_session):
        """Test creating a time entry with all required fields."""
        # Setup: Create dependencies
        project = Project(code="需2025單001", requirement_code="R202511146001", name="AI系統")
        account_group = AccountGroup(code="A00", name="中概全權")
        work_category = WorkCategory(code="A07", name="其它", deduct_approved_hours=True)
        db_session.add_all([project, account_group, work_category])
        db_session.commit()

        # Create time entry
        from datetime import date
        time_entry = TimeEntry(
            date=date(2025, 11, 12),
            project_id=project.id,
            account_group_id=account_group.id,
            work_category_id=work_category.id,
            hours=4.0,
            description="完成需求分析與系統設計"
        )
        db_session.add(time_entry)
        db_session.commit()

        assert time_entry.id is not None
        assert time_entry.hours == 4.0
        assert time_entry.description == "完成需求分析與系統設計"

    def test_time_entry_with_markdown_description(self, db_session):
        """Test time entry with markdown formatted description."""
        # Setup
        project = Project(code="需2025單002", requirement_code="R202511146002", name="數據平台")
        account_group = AccountGroup(code="O18", name="數據智能應用科")
        work_category = WorkCategory(code="B04", name="其它")
        db_session.add_all([project, account_group, work_category])
        db_session.commit()

        # Create time entry with markdown
        from datetime import date
        time_entry = TimeEntry(
            date=date(2025, 11, 12),
            project_id=project.id,
            account_group_id=account_group.id,
            work_category_id=work_category.id,
            hours=3.5,
            description="- [x] 資料庫優化\n- [x] 索引建立\n- [ ] 效能測試"
        )
        db_session.add(time_entry)
        db_session.commit()

        assert "- [x]" in time_entry.description
        assert "資料庫優化" in time_entry.description

    def test_time_entry_hours_validation(self, db_session):
        """Test that hours can be decimal values (0.5 increments)."""
        # Setup
        project = Project(code="需2025單003", requirement_code="R202511146003", name="測試專案")
        account_group = AccountGroup(code="A00", name="中概全權")
        work_category = WorkCategory(code="A07", name="其它")
        db_session.add_all([project, account_group, work_category])
        db_session.commit()

        # Test various hour values
        from datetime import date
        test_hours = [0.5, 1.0, 1.5, 4.0, 7.5, 12.0]

        for hour_value in test_hours:
            time_entry = TimeEntry(
                date=date(2025, 11, 12),
                project_id=project.id,
                account_group_id=account_group.id,
                work_category_id=work_category.id,
                hours=hour_value,
                description=f"測試 {hour_value} 小時"
            )
            db_session.add(time_entry)

        db_session.commit()

        entries = db_session.query(TimeEntry).all()
        assert len(entries) == len(test_hours)

    def test_time_entry_with_optional_account_item(self, db_session):
        """Test time entry with optional account_item field."""
        # Setup
        project = Project(code="需2025單004", requirement_code="R202511146004", name="專案4")
        account_group = AccountGroup(code="A00", name="中概全權")
        work_category = WorkCategory(code="A07", name="其它")
        db_session.add_all([project, account_group, work_category])
        db_session.commit()

        # Create with account_item
        from datetime import date
        time_entry = TimeEntry(
            date=date(2025, 11, 12),
            project_id=project.id,
            account_group_id=account_group.id,
            work_category_id=work_category.id,
            hours=2.0,
            description="系統開發",
            account_item="開發人員薪資"
        )
        db_session.add(time_entry)
        db_session.commit()

        assert time_entry.account_item == "開發人員薪資"

    def test_time_entry_display_order(self, db_session):
        """Test time entry display order for sorting."""
        # Setup
        project = Project(code="需2025單005", requirement_code="R202511146005", name="專案5")
        account_group = AccountGroup(code="A00", name="中概全權")
        work_category = WorkCategory(code="A07", name="其它")
        db_session.add_all([project, account_group, work_category])
        db_session.commit()

        # Create entries with different display orders
        from datetime import date
        for i in range(3):
            time_entry = TimeEntry(
                date=date(2025, 11, 12),
                project_id=project.id,
                account_group_id=account_group.id,
                work_category_id=work_category.id,
                hours=1.0,
                description=f"任務 {i+1}",
                display_order=i
            )
            db_session.add(time_entry)

        db_session.commit()

        entries = db_session.query(TimeEntry).order_by(TimeEntry.display_order).all()
        assert entries[0].description == "任務 1"
        assert entries[2].description == "任務 3"

    def test_time_entry_timestamps(self, db_session):
        """Test that timestamps are set automatically."""
        # Setup
        project = Project(code="需2025單006", requirement_code="R202511146006", name="專案6")
        account_group = AccountGroup(code="A00", name="中概全權")
        work_category = WorkCategory(code="A07", name="其它")
        db_session.add_all([project, account_group, work_category])
        db_session.commit()

        # Create time entry
        from datetime import date
        time_entry = TimeEntry(
            date=date(2025, 11, 12),
            project_id=project.id,
            account_group_id=account_group.id,
            work_category_id=work_category.id,
            hours=4.0,
            description="測試時間戳記"
        )
        db_session.add(time_entry)
        db_session.commit()

        assert isinstance(time_entry.created_at, datetime)
        assert isinstance(time_entry.updated_at, datetime)


class TestWorkTemplateModel:
    """Test cases for WorkTemplate model."""

    def test_create_work_template(self, db_session):
        """Test creating a work template."""
        # Setup
        project = Project(code="需2025單001", requirement_code="R202511146001", name="AI系統")
        account_group = AccountGroup(code="A00", name="中概全權")
        work_category = WorkCategory(code="A07", name="其它")
        db_session.add_all([project, account_group, work_category])
        db_session.commit()

        # Create template
        template = WorkTemplate(
            name="每日站會",
            project_id=project.id,
            account_group_id=account_group.id,
            work_category_id=work_category.id,
            default_hours=0.5,
            description_template="- [ ] 報告昨日進度\n- [ ] 今日計畫\n- [ ] 遇到的問題"
        )
        db_session.add(template)
        db_session.commit()

        assert template.id is not None
        assert template.name == "每日站會"
        assert template.default_hours == 0.5

    def test_work_template_minimal_fields(self, db_session):
        """Test creating template with only required fields."""
        template = WorkTemplate(name="簡單範本")
        db_session.add(template)
        db_session.commit()

        assert template.id is not None
        assert template.name == "簡單範本"
        assert template.project_id is None
        assert template.default_hours is None

    def test_work_template_timestamps(self, db_session):
        """Test that timestamps are set automatically."""
        template = WorkTemplate(name="測試範本")
        db_session.add(template)
        db_session.commit()

        assert isinstance(template.created_at, datetime)
        assert isinstance(template.updated_at, datetime)


class TestSettingModel:
    """Test cases for Setting model."""

    def test_create_setting(self, db_session):
        """Test creating a system setting."""
        setting = Setting(
            key="standard_work_hours",
            value="7.5"
        )
        db_session.add(setting)
        db_session.commit()

        assert setting.id is not None
        assert setting.key == "standard_work_hours"
        assert setting.value == "7.5"

    def test_setting_key_unique(self, db_session):
        """Test that setting key must be unique."""
        # Create first setting
        setting1 = Setting(key="timezone", value="UTC+8")
        db_session.add(setting1)
        db_session.commit()

        # Try to create duplicate
        setting2 = Setting(key="timezone", value="UTC+7")
        db_session.add(setting2)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_setting_multiple_keys(self, db_session):
        """Test creating multiple different settings."""
        settings = [
            Setting(key="language", value="zh-TW"),
            Setting(key="theme", value="light"),
            Setting(key="max_work_hours", value="12"),
        ]
        for setting in settings:
            db_session.add(setting)
        db_session.commit()

        all_settings = db_session.query(Setting).all()
        assert len(all_settings) == 3

    def test_setting_timestamps(self, db_session):
        """Test that timestamp is set automatically."""
        setting = Setting(key="test_key", value="test_value")
        db_session.add(setting)
        db_session.commit()

        assert isinstance(setting.updated_at, datetime)
