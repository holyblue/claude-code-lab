"""
Pydantic schemas for Milestone model.

This module defines the data validation and serialization schemas
for milestone-related API requests and responses.
"""

from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional


class MilestoneBase(BaseModel):
    """Base schema for milestone with common fields."""

    name: str = Field(..., min_length=1, max_length=200, description="Milestone name")
    start_date: date = Field(..., description="Start date of the milestone")
    end_date: date = Field(..., description="End date of the milestone")
    description: Optional[str] = Field(None, description="Optional description")
    display_order: int = Field(default=0, description="Display order for sorting")

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, v: date, info) -> date:
        """Validate that end_date is not before start_date."""
        if "start_date" in info.data and v < info.data["start_date"]:
            raise ValueError("end_date must not be before start_date")
        return v


class MilestoneCreate(MilestoneBase):
    """Schema for creating a new milestone."""

    pass


class MilestoneUpdate(BaseModel):
    """Schema for updating an existing milestone."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    display_order: Optional[int] = None

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, v: Optional[date], info) -> Optional[date]:
        """Validate that end_date is not before start_date if both are provided."""
        if v is not None and "start_date" in info.data and info.data["start_date"] is not None:
            if v < info.data["start_date"]:
                raise ValueError("end_date must not be before start_date")
        return v


class MilestoneResponse(MilestoneBase):
    """Schema for milestone API response."""

    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

