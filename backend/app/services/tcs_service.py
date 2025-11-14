"""
TCS formatting service.

Provides business logic for formatting time entries into TCS system format.
"""

from datetime import date as DateType
from decimal import Decimal
from typing import List
from sqlalchemy.orm import Session

from app.models.time_entry import TimeEntry
from app.models.project import Project
from app.models.account_group import AccountGroup
from app.models.work_category import WorkCategory
from app.schemas import TCSFormatResponse, TCSEntryFormat


def format_date_for_tcs(date_entries: List[TimeEntry], target_date: DateType, db: Session) -> TCSFormatResponse:
    """
    Format time entries for a specific date into TCS format.

    Args:
        date_entries: List of TimeEntry objects for the target date
        target_date: The date to format
        db: Database session

    Returns:
        TCSFormatResponse with formatted text ready for copy-paste

    TCS Format:
        日期: YYYY/MM/DD
        專案名稱: {project_code}
        帳組: {code} {name}
        工作類別: {code} {name}
        實際工時: {hours}
        工作說明:
        {description}

        ---

        (repeat for each entry)
    """
    formatted_entries = []
    formatted_lines = [f"日期: {target_date.strftime('%Y/%m/%d')}"]
    total_hours = Decimal("0")

    for entry in date_entries:
        # Get related data
        project = db.query(Project).filter(Project.id == entry.project_id).first()
        account_group = db.query(AccountGroup).filter(AccountGroup.id == entry.account_group_id).first()
        work_category = db.query(WorkCategory).filter(WorkCategory.id == entry.work_category_id).first()

        if not all([project, account_group, work_category]):
            continue

        # Build entry format
        tcs_entry = TCSEntryFormat(
            project_name=project.code,
            account_group=account_group.full_name,
            work_category=work_category.full_name,
            hours=entry.hours,
            description=entry.description,
        )
        formatted_entries.append(tcs_entry)

        # Build formatted text
        formatted_lines.extend([
            f"專案名稱: {project.code}",
            f"帳組: {account_group.full_name}",
            f"工作類別: {work_category.full_name}",
            f"實際工時: {entry.hours}",
            "工作說明:",
            entry.description,
            "",
            "---",
            "",
        ])

        total_hours += entry.hours

    # Remove last separator
    if formatted_lines and formatted_lines[-1] == "" and formatted_lines[-2] == "---":
        formatted_lines = formatted_lines[:-2]

    formatted_text = "\n".join(formatted_lines)

    return TCSFormatResponse(
        date=target_date.strftime("%Y/%m/%d"),
        entries=formatted_entries,
        formatted_text=formatted_text,
        total_hours=total_hours,
    )


def get_date_entries(db: Session, target_date: DateType) -> List[TimeEntry]:
    """
    Get all time entries for a specific date, ordered by display_order.

    Args:
        db: Database session
        target_date: Date to query

    Returns:
        List of TimeEntry objects for the date
    """
    return (
        db.query(TimeEntry)
        .filter(TimeEntry.date == target_date)
        .order_by(TimeEntry.display_order.asc())
        .all()
    )
