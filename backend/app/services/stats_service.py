"""
Statistics service for calculating project metrics.

Provides business logic for calculating project statistics, usage rates,
and approved hours tracking.
"""

from decimal import Decimal
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.time_entry import TimeEntry
from app.models.project import Project
from app.models.work_category import WorkCategory
from app.schemas import ProjectStats


def calculate_project_stats(db: Session, project_id: int) -> Optional[ProjectStats]:
    """
    Calculate statistics for a specific project.

    Args:
        db: Database session
        project_id: ID of the project to calculate stats for

    Returns:
        ProjectStats schema with calculated metrics, or None if project not found

    Business Rules:
        - used_hours: Sum of hours where deduct_approved_hours=True
        - non_deduct_hours: Sum of hours where deduct_approved_hours=False
        - total_hours: used_hours + non_deduct_hours
        - usage_rate: (used_hours / approved_hours) * 100
        - warning_level: none (<80%), warning (80-99%), danger (≥100%)
    """
    # Get project
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None

    # Calculate used hours (deduct_approved_hours=True)
    used_hours_query = (
        db.query(func.sum(TimeEntry.hours))
        .join(WorkCategory)
        .filter(
            TimeEntry.project_id == project_id,
            WorkCategory.deduct_approved_hours == True,
        )
        .scalar()
    )
    used_hours = Decimal(str(used_hours_query or 0))

    # Calculate non-deduct hours (deduct_approved_hours=False)
    non_deduct_hours_query = (
        db.query(func.sum(TimeEntry.hours))
        .join(WorkCategory)
        .filter(
            TimeEntry.project_id == project_id,
            WorkCategory.deduct_approved_hours == False,
        )
        .scalar()
    )
    non_deduct_hours = Decimal(str(non_deduct_hours_query or 0))

    # Calculate total hours
    total_hours = used_hours + non_deduct_hours

    # Calculate approved hours (man_days * 7.5)
    approved_hours = None
    if project.approved_man_days:
        approved_hours = project.approved_man_days * Decimal("7.5")

    # Calculate remaining hours and usage rate
    remaining_hours = None
    usage_rate = None
    if approved_hours:
        remaining_hours = approved_hours - used_hours
        usage_rate = (used_hours / approved_hours * 100).quantize(Decimal("0.1"))

    # Determine warning level
    warning_level = "none"
    warning_message = None
    if usage_rate:
        if usage_rate >= 100:
            warning_level = "danger"
            warning_message = "專案核定工時已用完，此記錄將超出預算"
        elif usage_rate >= 80:
            warning_level = "warning"
            warning_message = f"專案工時使用率已達 {usage_rate}%，請注意控制"

    return ProjectStats(
        project_id=project.id,
        project_code=project.code,
        project_name=project.name,
        approved_man_days=project.approved_man_days,
        approved_hours=approved_hours,
        used_hours=used_hours,
        non_deduct_hours=non_deduct_hours,
        total_hours=total_hours,
        remaining_hours=remaining_hours,
        usage_rate=usage_rate,
        warning_level=warning_level,
        warning_message=warning_message,
    )


def calculate_all_project_stats(db: Session) -> List[ProjectStats]:
    """
    Calculate statistics for all active projects.

    Args:
        db: Database session

    Returns:
        List of ProjectStats for all projects with time entries
    """
    # Get all projects with time entries
    projects = (
        db.query(Project)
        .join(TimeEntry)
        .filter(Project.deleted_at.is_(None))
        .distinct()
        .all()
    )

    stats_list = []
    for project in projects:
        stats = calculate_project_stats(db, project.id)
        if stats:
            stats_list.append(stats)

    return stats_list
