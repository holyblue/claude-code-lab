"""
API endpoints for WorkCategory management.

Provides CRUD operations for work categories.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.work_category import WorkCategory
from app.schemas import (
    WorkCategoryCreate,
    WorkCategoryUpdate,
    WorkCategoryResponse,
    WorkCategoryList,
)

router = APIRouter()


@router.post(
    "/",
    response_model=WorkCategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create work category",
    description="Create a new work category",
)
def create_work_category(
    work_category: WorkCategoryCreate,
    db: Session = Depends(get_db),
) -> WorkCategoryResponse:
    """Create a new work category."""
    # Check if code+name combination already exists
    existing = (
        db.query(WorkCategory)
        .filter(
            WorkCategory.code == work_category.code,
            WorkCategory.name == work_category.name,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Work category '{work_category.code} {work_category.name}' already exists",
        )

    # Create new work category
    db_work_category = WorkCategory(**work_category.model_dump())
    db.add(db_work_category)
    db.commit()
    db.refresh(db_work_category)

    return WorkCategoryResponse.model_validate(db_work_category)


@router.get(
    "/",
    response_model=WorkCategoryList,
    summary="List work categories",
    description="Get all work categories",
)
def list_work_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> WorkCategoryList:
    """List all work categories with pagination."""
    query = db.query(WorkCategory)
    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return WorkCategoryList(
        items=[WorkCategoryResponse.model_validate(item) for item in items],
        total=total,
    )


@router.get(
    "/{work_category_id}",
    response_model=WorkCategoryResponse,
    summary="Get work category",
    description="Get a specific work category by ID",
)
def get_work_category(
    work_category_id: int,
    db: Session = Depends(get_db),
) -> WorkCategoryResponse:
    """Get a specific work category by ID."""
    work_category = db.query(WorkCategory).filter(WorkCategory.id == work_category_id).first()
    if not work_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work category with id {work_category_id} not found",
        )

    return WorkCategoryResponse.model_validate(work_category)


@router.patch(
    "/{work_category_id}",
    response_model=WorkCategoryResponse,
    summary="Update work category",
    description="Update an existing work category",
)
def update_work_category(
    work_category_id: int,
    work_category_update: WorkCategoryUpdate,
    db: Session = Depends(get_db),
) -> WorkCategoryResponse:
    """Update an existing work category."""
    work_category = db.query(WorkCategory).filter(WorkCategory.id == work_category_id).first()
    if not work_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work category with id {work_category_id} not found",
        )

    # Update only provided fields
    update_data = work_category_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(work_category, field, value)

    db.commit()
    db.refresh(work_category)

    return WorkCategoryResponse.model_validate(work_category)


@router.delete(
    "/{work_category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete work category",
    description="Delete a work category",
)
def delete_work_category(
    work_category_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a work category."""
    work_category = db.query(WorkCategory).filter(WorkCategory.id == work_category_id).first()
    if not work_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work category with id {work_category_id} not found",
        )

    db.delete(work_category)
    db.commit()
