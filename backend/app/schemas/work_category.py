"""
Pydantic schemas for WorkCategory.

These schemas define the data validation and serialization for work categories
in API requests and responses.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class WorkCategoryBase(BaseModel):
    """Base schema with common WorkCategory attributes."""

    code: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="工作類別代碼（如：A07）",
        examples=["A07", "A08", "B04"],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="工作類別名稱（如：其它）",
        examples=["其它", "商模", "休假"],
    )
    deduct_approved_hours: bool = Field(
        default=True,
        description="是否扣抵核定工時",
    )
    is_default: bool = Field(
        default=False,
        description="是否為常用類別",
    )


class WorkCategoryCreate(WorkCategoryBase):
    """Schema for creating a new work category."""

    pass


class WorkCategoryUpdate(BaseModel):
    """Schema for updating an existing work category."""

    code: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="工作類別代碼",
    )
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="工作類別名稱",
    )
    deduct_approved_hours: Optional[bool] = Field(
        None,
        description="是否扣抵核定工時",
    )
    is_default: Optional[bool] = Field(
        None,
        description="是否為常用類別",
    )


class WorkCategoryResponse(WorkCategoryBase):
    """Schema for work category responses."""

    id: int = Field(..., description="工作類別 ID")
    full_name: str = Field(..., description="完整名稱（代碼 + 名稱）")
    created_at: datetime = Field(..., description="創建時間")
    updated_at: datetime = Field(..., description="更新時間")

    model_config = ConfigDict(from_attributes=True)


class WorkCategoryList(BaseModel):
    """Schema for list of work categories."""

    items: list[WorkCategoryResponse]
    total: int = Field(..., description="總數量")
