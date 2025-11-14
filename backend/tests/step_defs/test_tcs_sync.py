"""
Step definitions for TCS formatting feature.

Implements BDD scenarios for formatting time entries into TCS system format.
"""

from decimal import Decimal
from datetime import datetime
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from sqlalchemy.orm import Session

from app.models import Project, WorkCategory, TimeEntry, AccountGroup
from app.services.tcs_service import format_date_for_tcs, get_date_entries

# Load scenarios from the feature file
scenarios("../features/tcs_sync.feature")


# ============================================================================
# Given Steps - Setup initial state
# ============================================================================


@given(parsers.parse('存在以下專案\n{table}'), target_fixture="projects")
def given_projects_exist(db: Session, table: str):
    """Create projects from table data."""
    projects = {}
    lines = [line.strip() for line in table.strip().split("\n") if line.strip()]

    # Skip header row
    for line in lines[1:]:
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 2:
            code = parts[0]
            name = parts[1]

            project = Project(
                code=code,
                requirement_code=f"R{code}",
                name=name,
                approved_man_days=Decimal("20"),
                status="進行中",
            )
            db.add(project)
            db.commit()
            db.refresh(project)
            projects[code] = project

    return projects


@given(parsers.parse('存在以下帳組\n{table}'), target_fixture="account_groups")
def given_account_groups_exist(db: Session, table: str):
    """Create account groups from table data."""
    groups = {}
    lines = [line.strip() for line in table.strip().split("\n") if line.strip()]

    # Skip header row
    for line in lines[1:]:
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 2:
            code = parts[0]
            name = parts[1]

            group = AccountGroup(code=code, name=name, is_default=True)
            db.add(group)
            db.commit()
            db.refresh(group)
            groups[code] = group

    return groups


@given(parsers.parse('存在以下工作類別\n{table}'), target_fixture="work_categories")
def given_work_categories_exist(db: Session, table: str):
    """Create work categories from table data."""
    categories = {}
    lines = [line.strip() for line in table.strip().split("\n") if line.strip()]

    # Skip header row
    for line in lines[1:]:
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 2:
            code = parts[0]
            name = parts[1]

            category = WorkCategory(
                code=code,
                name=name,
                deduct_approved_hours=True,
                is_default=True,
            )
            db.add(category)
            db.commit()
            db.refresh(category)
            categories[code] = category

    return categories


@given(parsers.parse('日期 "{date_str}" 有以下工時記錄\n{table}'), target_fixture="date_entries")
def given_date_has_time_entries(
    db: Session,
    projects: dict,
    account_groups: dict,
    work_categories: dict,
    date_str: str,
    table: str,
):
    """Create time entries for a specific date from table data."""
    entries = []
    lines = [line.strip() for line in table.strip().split("\n") if line.strip()]

    # Skip header row
    for line in lines[1:]:
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 5:
            project_code = parts[0]
            account_code = parts[1]
            category_code = parts[2]
            hours = Decimal(parts[3])
            description = parts[4].replace("\\n", "\n")

            project = projects[project_code]
            account_group = account_groups[account_code]
            work_category = work_categories[category_code]

            entry = TimeEntry(
                project_id=project.id,
                work_category_id=work_category.id,
                account_group_id=account_group.id,
                date=datetime.strptime(date_str, "%Y-%m-%d").date(),
                hours=hours,
                description=description,
            )
            db.add(entry)
            entries.append(entry)

    db.commit()
    return {"date": date_str, "entries": entries}


# ============================================================================
# When Steps - Actions
# ============================================================================


@when(parsers.parse('我請求格式化日期 "{date_str}" 的工時記錄'), target_fixture="formatted_output")
def when_request_format_for_date(db: Session, date_str: str):
    """Request formatting for a specific date."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    entries = get_date_entries(db, date_obj)

    if not entries:
        return None

    result = format_date_for_tcs(entries, date_obj, db)
    return result


# ============================================================================
# Then Steps - Assertions
# ============================================================================


@then("應該返回以下格式的文字")
def then_should_return_formatted_text(formatted_output, docstring):
    """Verify the formatted output matches expected text (using Gherkin DocString)."""
    if formatted_output is None:
        pytest.fail("No formatted output was generated")

    actual_text = formatted_output.formatted_text.strip()
    expected = docstring.strip()

    # Normalize whitespace for comparison
    actual_lines = [line.strip() for line in actual_text.split("\n")]
    expected_lines = [line.strip() for line in expected.split("\n")]

    # Compare line by line for better error messages
    for i, (actual_line, expected_line) in enumerate(zip(actual_lines, expected_lines)):
        assert actual_line == expected_line, \
            f"Line {i+1} mismatch:\n  Expected: {expected_line}\n  Actual: {actual_line}"

    # Verify same number of lines
    assert len(actual_lines) == len(expected_lines), \
        f"Expected {len(expected_lines)} lines, got {len(actual_lines)}"


@then(parsers.parse("總工時應為 {hours:f} 小時"))
def then_total_hours_should_be(formatted_output, hours: float):
    """Verify total hours in formatted output."""
    if formatted_output is None:
        pytest.fail("No formatted output was generated")

    assert float(formatted_output.total_hours) == hours, \
        f"Expected {hours}, got {formatted_output.total_hours}"
