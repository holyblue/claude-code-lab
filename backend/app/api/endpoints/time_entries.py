"""
API endpoints for TimeEntry management.

Provides CRUD operations for time entries with advanced querying.
"""

from datetime import date as DateType
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.time_entry import TimeEntry
from app.schemas import (
    TimeEntryCreate,
    TimeEntryUpdate,
    TimeEntryResponse,
    TimeEntryList,
)

router = APIRouter()


@router.post(
    "/",
    response_model=TimeEntryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create time entry",
    description="Create a new time entry",
)
def create_time_entry(
    time_entry: TimeEntryCreate,
    db: Session = Depends(get_db),
) -> TimeEntryResponse:
    """Create a new time entry."""
    # Validate foreign keys exist
    from app.models.project import Project
    from app.models.account_group import AccountGroup
    from app.models.work_category import WorkCategory

    project = db.query(Project).filter(Project.id == time_entry.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {time_entry.project_id} not found",
        )

    # 模組改為選填，只有當提供時才驗證
    if time_entry.account_group_id is not None:
        account_group = (
            db.query(AccountGroup)
            .filter(AccountGroup.id == time_entry.account_group_id)
            .first()
        )
        if not account_group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Account group with id {time_entry.account_group_id} not found",
            )

    work_category = (
        db.query(WorkCategory)
        .filter(WorkCategory.id == time_entry.work_category_id)
        .first()
    )
    if not work_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work category with id {time_entry.work_category_id} not found",
        )

    # Create new time entry
    db_time_entry = TimeEntry(**time_entry.model_dump())
    db.add(db_time_entry)
    db.commit()
    db.refresh(db_time_entry)

    return TimeEntryResponse.model_validate(db_time_entry)


@router.get(
    "/",
    response_model=TimeEntryList,
    summary="List time entries",
    description="Get time entries with optional filtering by date range and project",
)
def list_time_entries(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[DateType] = Query(None, description="Filter by start date (inclusive)"),
    end_date: Optional[DateType] = Query(None, description="Filter by end date (inclusive)"),
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    account_group_id: Optional[int] = Query(None, description="Filter by account group ID"),
    work_category_id: Optional[int] = Query(None, description="Filter by work category ID"),
    db: Session = Depends(get_db),
) -> TimeEntryList:
    """List time entries with pagination and optional filtering."""
    query = db.query(TimeEntry)

    # Apply filters
    if start_date:
        query = query.filter(TimeEntry.date >= start_date)
    if end_date:
        query = query.filter(TimeEntry.date <= end_date)
    if project_id:
        query = query.filter(TimeEntry.project_id == project_id)
    if account_group_id:
        query = query.filter(TimeEntry.account_group_id == account_group_id)
    if work_category_id:
        query = query.filter(TimeEntry.work_category_id == work_category_id)

    # Order by date (descending) and display_order
    query = query.order_by(TimeEntry.date.desc(), TimeEntry.display_order.asc())

    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return TimeEntryList(
        items=[TimeEntryResponse.model_validate(item) for item in items],
        total=total,
    )


@router.get(
    "/{time_entry_id}",
    response_model=TimeEntryResponse,
    summary="Get time entry",
    description="Get a specific time entry by ID",
)
def get_time_entry(
    time_entry_id: int,
    db: Session = Depends(get_db),
) -> TimeEntryResponse:
    """Get a specific time entry by ID."""
    time_entry = db.query(TimeEntry).filter(TimeEntry.id == time_entry_id).first()
    if not time_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Time entry with id {time_entry_id} not found",
        )

    return TimeEntryResponse.model_validate(time_entry)


@router.patch(
    "/{time_entry_id}",
    response_model=TimeEntryResponse,
    summary="Update time entry",
    description="Update an existing time entry",
)
def update_time_entry(
    time_entry_id: int,
    time_entry_update: TimeEntryUpdate,
    db: Session = Depends(get_db),
) -> TimeEntryResponse:
    """Update an existing time entry."""
    time_entry = db.query(TimeEntry).filter(TimeEntry.id == time_entry_id).first()
    if not time_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Time entry with id {time_entry_id} not found",
        )

    # Update only provided fields
    update_data = time_entry_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(time_entry, field, value)

    db.commit()
    db.refresh(time_entry)

    return TimeEntryResponse.model_validate(time_entry)


@router.delete(
    "/{time_entry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete time entry",
    description="Delete a time entry",
)
def delete_time_entry(
    time_entry_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a time entry."""
    time_entry = db.query(TimeEntry).filter(TimeEntry.id == time_entry_id).first()
    if not time_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Time entry with id {time_entry_id} not found",
        )

    db.delete(time_entry)
    db.commit()
