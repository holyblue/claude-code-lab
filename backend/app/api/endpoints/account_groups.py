"""
API endpoints for AccountGroup management.

Provides CRUD operations for account groups.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.account_group import AccountGroup
from app.schemas import (
    AccountGroupCreate,
    AccountGroupUpdate,
    AccountGroupResponse,
    AccountGroupList,
)

router = APIRouter()


@router.post(
    "/",
    response_model=AccountGroupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create account group",
    description="Create a new account group",
)
def create_account_group(
    account_group: AccountGroupCreate,
    db: Session = Depends(get_db),
) -> AccountGroupResponse:
    """Create a new account group."""
    # Check if code already exists
    existing = (
        db.query(AccountGroup)
        .filter(AccountGroup.code == account_group.code)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Account group with code '{account_group.code}' already exists",
        )

    # Create new account group
    db_account_group = AccountGroup(**account_group.model_dump())
    db.add(db_account_group)
    db.commit()
    db.refresh(db_account_group)

    return AccountGroupResponse.model_validate(db_account_group)


@router.get(
    "/",
    response_model=AccountGroupList,
    summary="List account groups",
    description="Get all account groups",
)
def list_account_groups(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> AccountGroupList:
    """List all account groups with pagination."""
    query = db.query(AccountGroup)
    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return AccountGroupList(
        items=[AccountGroupResponse.model_validate(item) for item in items],
        total=total,
    )


@router.get(
    "/{account_group_id}",
    response_model=AccountGroupResponse,
    summary="Get account group",
    description="Get a specific account group by ID",
)
def get_account_group(
    account_group_id: int,
    db: Session = Depends(get_db),
) -> AccountGroupResponse:
    """Get a specific account group by ID."""
    account_group = db.query(AccountGroup).filter(AccountGroup.id == account_group_id).first()
    if not account_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account group with id {account_group_id} not found",
        )

    return AccountGroupResponse.model_validate(account_group)


@router.patch(
    "/{account_group_id}",
    response_model=AccountGroupResponse,
    summary="Update account group",
    description="Update an existing account group",
)
def update_account_group(
    account_group_id: int,
    account_group_update: AccountGroupUpdate,
    db: Session = Depends(get_db),
) -> AccountGroupResponse:
    """Update an existing account group."""
    account_group = db.query(AccountGroup).filter(AccountGroup.id == account_group_id).first()
    if not account_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account group with id {account_group_id} not found",
        )

    # Update only provided fields
    update_data = account_group_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(account_group, field, value)

    db.commit()
    db.refresh(account_group)

    return AccountGroupResponse.model_validate(account_group)


@router.delete(
    "/{account_group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete account group",
    description="Delete an account group",
)
def delete_account_group(
    account_group_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete an account group."""
    account_group = db.query(AccountGroup).filter(AccountGroup.id == account_group_id).first()
    if not account_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account group with id {account_group_id} not found",
        )

    db.delete(account_group)
    db.commit()
