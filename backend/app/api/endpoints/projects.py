"""
API endpoints for Project management.

Provides CRUD operations for projects.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.project import Project
from app.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectList,
)

router = APIRouter()


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create project",
    description="Create a new project",
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    """Create a new project."""
    # Check if code already exists
    existing = (
        db.query(Project)
        .filter(Project.code == project.code, Project.deleted_at.is_(None))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project with code '{project.code}' already exists",
        )

    # Create new project
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return ProjectResponse.model_validate(db_project)


@router.get(
    "/",
    response_model=ProjectList,
    summary="List projects",
    description="Get all projects (optionally filter by status)",
)
def list_projects(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    include_deleted: bool = Query(False, description="Include soft-deleted projects"),
    db: Session = Depends(get_db),
) -> ProjectList:
    """List all projects with pagination and optional filtering."""
    query = db.query(Project)

    # Filter by status
    if status_filter:
        query = query.filter(Project.status == status_filter)

    # Exclude soft-deleted by default
    if not include_deleted:
        query = query.filter(Project.deleted_at.is_(None))

    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return ProjectList(
        items=[ProjectResponse.model_validate(item) for item in items],
        total=total,
    )


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get project",
    description="Get a specific project by ID",
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    """Get a specific project by ID."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )

    return ProjectResponse.model_validate(project)


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update project",
    description="Update an existing project",
)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    """Update an existing project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )

    # Update only provided fields
    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return ProjectResponse.model_validate(project)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete project",
    description="Soft delete a project",
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Soft delete a project by setting deleted_at timestamp."""
    from datetime import datetime

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found",
        )

    project.deleted_at = datetime.utcnow()
    db.commit()
