"""
API endpoints for milestone management.

This module provides CRUD operations for project milestones.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.models import Milestone, Project
from app.schemas.milestone import (
    MilestoneCreate,
    MilestoneUpdate,
    MilestoneResponse,
)

router = APIRouter()


@router.post(
    "/projects/{project_id}/milestones/",
    response_model=MilestoneResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new milestone",
    description="Create a new milestone for a specific project",
)
async def create_milestone(
    project_id: int,
    milestone: MilestoneCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new milestone for a project.

    Args:
        project_id: ID of the project
        milestone: Milestone data to create
        db: Database session

    Returns:
        Created milestone

    Raises:
        HTTPException: 404 if project not found
    """
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )

    # Create milestone
    db_milestone = Milestone(
        project_id=project_id,
        name=milestone.name,
        start_date=milestone.start_date,
        end_date=milestone.end_date,
        description=milestone.description,
        display_order=milestone.display_order,
    )

    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)

    return db_milestone


@router.get(
    "/projects/{project_id}/milestones/",
    response_model=List[MilestoneResponse],
    summary="Get project milestones",
    description="Get all milestones for a specific project",
)
async def get_project_milestones(
    project_id: int,
    db: Session = Depends(get_db),
):
    """
    Get all milestones for a specific project.

    Args:
        project_id: ID of the project
        db: Database session

    Returns:
        List of milestones ordered by start_date and display_order

    Raises:
        HTTPException: 404 if project not found
    """
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )

    # Get milestones ordered by start_date and display_order
    milestones = (
        db.query(Milestone)
        .filter(Milestone.project_id == project_id)
        .order_by(Milestone.start_date, Milestone.display_order)
        .all()
    )

    return milestones


@router.get(
    "/milestones/{id}",
    response_model=MilestoneResponse,
    summary="Get a milestone",
    description="Get a specific milestone by ID",
)
async def get_milestone(
    id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific milestone by ID.

    Args:
        id: Milestone ID
        db: Database session

    Returns:
        Milestone details

    Raises:
        HTTPException: 404 if milestone not found
    """
    milestone = db.query(Milestone).filter(Milestone.id == id).first()
    if not milestone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Milestone with id {id} not found",
        )

    return milestone


@router.patch(
    "/milestones/{id}",
    response_model=MilestoneResponse,
    summary="Update a milestone",
    description="Update an existing milestone",
)
async def update_milestone(
    id: int,
    milestone_update: MilestoneUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing milestone.

    Args:
        id: Milestone ID
        milestone_update: Milestone data to update
        db: Database session

    Returns:
        Updated milestone

    Raises:
        HTTPException: 404 if milestone not found
        HTTPException: 400 if validation fails
    """
    # Get existing milestone
    db_milestone = db.query(Milestone).filter(Milestone.id == id).first()
    if not db_milestone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Milestone with id {id} not found",
        )

    # Update fields
    update_data = milestone_update.model_dump(exclude_unset=True)
    
    # If both dates are being updated, validate them together
    if "start_date" in update_data and "end_date" in update_data:
        if update_data["end_date"] < update_data["start_date"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="end_date must not be before start_date",
            )
    # If only end_date is being updated, validate against existing start_date
    elif "end_date" in update_data:
        if update_data["end_date"] < db_milestone.start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="end_date must not be before start_date",
            )
    # If only start_date is being updated, validate against existing end_date
    elif "start_date" in update_data:
        if update_data["start_date"] > db_milestone.end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="start_date must not be after end_date",
            )

    for field, value in update_data.items():
        setattr(db_milestone, field, value)

    db.commit()
    db.refresh(db_milestone)

    return db_milestone


@router.delete(
    "/milestones/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a milestone",
    description="Delete an existing milestone",
)
async def delete_milestone(
    id: int,
    db: Session = Depends(get_db),
):
    """
    Delete an existing milestone.

    Args:
        id: Milestone ID
        db: Database session

    Raises:
        HTTPException: 404 if milestone not found
    """
    # Get existing milestone
    db_milestone = db.query(Milestone).filter(Milestone.id == id).first()
    if not db_milestone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Milestone with id {id} not found",
        )

    db.delete(db_milestone)
    db.commit()

    return None

