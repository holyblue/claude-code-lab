"""
API endpoints for Statistics.

Provides project statistics and usage tracking endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.stats_service import calculate_project_stats, calculate_all_project_stats
from app.schemas import ProjectStats

router = APIRouter()


@router.get(
    "/projects/{project_id}",
    response_model=ProjectStats,
    summary="Get project statistics",
    description="Get usage statistics for a specific project",
)
def get_project_statistics(
    project_id: int,
    db: Session = Depends(get_db),
) -> ProjectStats:
    """
    Get detailed statistics for a project.

    Returns:
        - used_hours: Hours from deductible work categories
        - non_deduct_hours: Hours from non-deductible work categories
        - total_hours: Sum of all hours
        - usage_rate: Percentage of approved hours used
        - warning_level: none, warning (80%+), or danger (100%+)
    """
    stats = calculate_project_stats(db, project_id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )

    return stats


@router.get(
    "/projects",
    response_model=List[ProjectStats],
    summary="Get all project statistics",
    description="Get usage statistics for all projects with time entries",
)
def get_all_project_statistics(
    db: Session = Depends(get_db),
) -> List[ProjectStats]:
    """
    Get statistics for all projects that have time entries.

    Useful for dashboard views and project portfolio tracking.
    """
    return calculate_all_project_stats(db)
