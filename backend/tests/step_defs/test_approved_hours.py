"""
Step definitions for approved hours tracking feature.

Implements BDD scenarios for tracking and deducting approved project hours.
"""

from decimal import Decimal
from datetime import datetime
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from sqlalchemy.orm import Session

from app.models import Project, WorkCategory, TimeEntry, AccountGroup
from app.services.stats_service import calculate_project_stats

# Load scenarios from the feature file
scenarios("../features/approved_hours.feature")


# ============================================================================
# Given Steps - Setup initial state
# ============================================================================


@given(parsers.parse('存在以下專案\n{table}'), target_fixture="projects")
def given_projects(db: Session, table: str):
    """Create projects from table data."""
    projects = {}
    lines = [line.strip() for line in table.strip().split("\n") if line.strip()]

    # Skip header row
    for line in lines[1:]:
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 4:
            code = parts[0]
            name = parts[1]
            approved_days = Decimal(parts[2])
            # approved_hours is parts[3], but we don't store it directly
            # It's calculated as approved_man_days * 7.5

            project = Project(
                code=code,
                requirement_code=f"R{code}",  # Generate requirement code
                name=name,
                approved_man_days=approved_days,
                status="進行中",
            )
            db.add(project)
            db.commit()
            db.refresh(project)
            projects[code] = project

    return projects


@given(parsers.parse('存在以下工作類別\n{table}'), target_fixture="work_categories")
def given_work_categories(db: Session, table: str):
    """Create work categories from table data."""
    categories = {}
    lines = [line.strip() for line in table.strip().split("\n") if line.strip()]

    # Skip header row
    for line in lines[1:]:
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 3:
            code = parts[0]
            name = parts[1]
            deduct = parts[2] == "是"

            category = WorkCategory(
                code=code,
                name=name,
                deduct_approved_hours=deduct,
                is_default=True,
            )
            db.add(category)
            db.commit()
            db.refresh(category)
            categories[f"{code} {name}"] = category

    return categories


@given(parsers.parse('專案 "{project_code}" 的核定工時為 {hours:f} 小時'))
def given_project_approved_hours(projects: dict, project_code: str, hours: float):
    """Verify project has specified approved hours (calculated from man-days)."""
    project = projects[project_code]
    # approved_hours = approved_man_days * 7.5
    calculated_hours = float(project.approved_man_days * Decimal("7.5"))
    assert calculated_hours == hours, \
        f"Expected {hours} hours, got {calculated_hours} hours"


@given(parsers.re(r"已使用工時為 (?P<hours>\d+\.?\d*) 小時"), target_fixture="existing_hours")
def given_used_hours(db: Session, projects: dict, work_categories: dict, hours: str):
    """Create existing time entries to reach specified used hours."""
    hours_float = float(hours)
    if hours_float == 0:
        return []

    # Create a dummy account group for existing entries
    account_group = db.query(AccountGroup).first()
    if not account_group:
        account_group = AccountGroup(code="A00", name="中概全權", is_default=True)
        db.add(account_group)
        db.commit()
        db.refresh(account_group)

    # Get first project and deductible category
    project = list(projects.values())[0]
    category = None
    for cat in work_categories.values():
        if cat.deduct_approved_hours:
            category = cat
            break

    # Create time entry with the specified hours
    entry = TimeEntry(
        project_id=project.id,
        work_category_id=category.id,
        account_group_id=account_group.id,
        date=datetime.strptime("2025-11-01", "%Y-%m-%d").date(),
        hours=Decimal(str(hours)),
        description="Existing work",
    )
    db.add(entry)
    db.commit()

    return [entry]


# ============================================================================
# When Steps - Actions
# ============================================================================


@when(parsers.parse('我記錄以下工時\n{table}'), target_fixture="new_entries")
def when_record_hours(db: Session, projects: dict, work_categories: dict, table: str):
    """Record new time entries from table data."""
    entries = []
    lines = [line.strip() for line in table.strip().split("\n") if line.strip()]

    # Get or create account group
    account_group = db.query(AccountGroup).first()
    if not account_group:
        account_group = AccountGroup(code="A00", name="中概全權", is_default=True)
        db.add(account_group)
        db.commit()
        db.refresh(account_group)

    # Skip header row
    for line in lines[1:]:
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 3:
            project_code = parts[0]
            work_cat = parts[1]
            hours = Decimal(parts[2])

            project = projects[project_code]
            category = work_categories[work_cat]

            entry = TimeEntry(
                project_id=project.id,
                work_category_id=category.id,
                account_group_id=account_group.id,
                date=datetime.strptime("2025-11-12", "%Y-%m-%d").date(),
                hours=hours,
                description="Test work",
            )
            db.add(entry)
            entries.append(entry)

    db.commit()
    return entries


@when(parsers.parse('我嘗試記錄以下工時\n{table}'), target_fixture="new_entries")
def when_try_record_hours(db: Session, projects: dict, work_categories: dict, table: str):
    """Try to record new time entries (even if over budget)."""
    # Same implementation as when_record_hours
    return when_record_hours(db, projects, work_categories, table)


@when("我查看專案統計", target_fixture="project_stats")
def when_view_project_stats(db: Session, projects: dict):
    """Get project statistics."""
    project = list(projects.values())[0]
    stats = calculate_project_stats(db, project.id)
    return stats


# ============================================================================
# Then Steps - Assertions
# ============================================================================


@then(parsers.parse('專案 "{project_code}" 的已使用工時應為 {hours:f} 小時'))
def then_used_hours_should_be(db: Session, projects: dict, project_code: str, hours: float):
    """Verify project used hours."""
    project = projects[project_code]
    stats = calculate_project_stats(db, project.id)
    assert float(stats.used_hours) == hours, \
        f"Expected {hours}, got {stats.used_hours}"


@then(parsers.parse('專案 "{project_code}" 的已使用工時應仍為 {hours:f} 小時'))
def then_used_hours_should_remain(db: Session, projects: dict, project_code: str, hours: float):
    """Verify project used hours remained the same."""
    then_used_hours_should_be(db, projects, project_code, hours)


@then(parsers.parse("剩餘工時應為 {hours:f} 小時"))
def then_remaining_hours_should_be(db: Session, projects: dict, hours: float):
    """Verify remaining hours."""
    project = list(projects.values())[0]
    stats = calculate_project_stats(db, project.id)
    assert float(stats.remaining_hours) == hours, \
        f"Expected {hours}, got {stats.remaining_hours}"


@then(parsers.parse("使用率應為 {percentage:f}%"))
def then_usage_rate_should_be(db: Session, projects: dict, percentage: float):
    """Verify usage rate percentage."""
    project = list(projects.values())[0]
    stats = calculate_project_stats(db, project.id)
    assert abs(float(stats.usage_rate) - percentage) < 0.1, \
        f"Expected {percentage}%, got {stats.usage_rate}%"


@then(parsers.parse("不扣抵工時應為 {hours:f} 小時"))
def then_non_deductible_hours_should_be(db: Session, projects: dict, hours: float):
    """Verify non-deductible hours."""
    project = list(projects.values())[0]
    stats = calculate_project_stats(db, project.id)
    assert float(stats.non_deduct_hours) == hours, \
        f"Expected {hours}, got {stats.non_deduct_hours}"


@then(parsers.parse("專案總工時應為 {hours:f} 小時"))
def then_total_hours_should_be(db: Session, projects: dict, hours: float):
    """Verify total project hours (deductible + non-deductible)."""
    project = list(projects.values())[0]
    stats = calculate_project_stats(db, project.id)
    total = float(stats.used_hours) + float(stats.non_deduct_hours)
    assert total == hours, f"Expected {hours}, got {total}"


@then("應該顯示橘色預警")
def then_should_show_orange_warning(project_stats):
    """Verify orange warning is shown."""
    assert project_stats.warning_level == "warning", \
        f"Expected 'warning', got '{project_stats.warning_level}'"


@then(parsers.parse('警告訊息應為 "{message}"'))
def then_warning_message_should_be(db: Session, projects: dict, message: str, project_stats=None):
    """Verify warning message."""
    # If project_stats not provided as fixture, calculate it
    if project_stats is None:
        project = list(projects.values())[0]
        project_stats = calculate_project_stats(db, project.id)

    assert project_stats.warning_message == message, \
        f"Expected '{message}', got '{project_stats.warning_message}'"


@then("系統應顯示紅色警告")
def then_should_show_red_warning(db: Session, projects: dict, new_entries: list = None):
    """Verify red/critical warning is shown."""
    project = list(projects.values())[0]
    stats = calculate_project_stats(db, project.id)
    assert stats.warning_level == "danger", \
        f"Expected 'danger', got '{stats.warning_level}'"


@then("應該允許記錄但標示為超支")
def then_should_allow_but_mark_overbudget(db: Session, projects: dict, new_entries: list):
    """Verify entries are saved but marked as over budget."""
    assert len(new_entries) > 0, "No entries were created"
    project = list(projects.values())[0]
    stats = calculate_project_stats(db, project.id)
    assert float(stats.usage_rate) > 100, \
        "Usage rate should exceed 100%"
