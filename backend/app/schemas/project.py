"""
Pydantic schemas for Project.

These schemas define the data validation and serialization for projects
in API requests and responses.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProjectBase(BaseModel):
    """Base schema with common Project attributes."""

    code: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="專案代碼（如：需2025單001）",
        examples=["需2025單001", "需2024單999"],
    )
    requirement_code: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="需求單號（如：R202511146001）",
        examples=["R202511146001", "R202412010001"],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="專案名稱",
        examples=["系統功能開發", "資料分析需求"],
    )
    approved_man_days: Optional[Decimal] = Field(
        None,
        ge=0,
        decimal_places=2,
        description="核定工時（人天，1人天=7.5小時）",
        examples=[10.5, 20.0],
    )
    default_account_group_id: Optional[int] = Field(
        None,
        description="預設帳組 ID",
    )
    default_work_category_id: Optional[int] = Field(
        None,
        description="預設工作類別 ID",
    )
    description: Optional[str] = Field(
        None,
        description="專案描述",
    )
    status: str = Field(
        default="active",
        max_length=20,
        description="專案狀態（active/completed/archived）",
        examples=["active", "completed", "archived"],
    )
    color: str = Field(
        default="#409EFF",
        pattern=r"^#[0-9A-Fa-f]{6}$",
        description="顏色代碼（hex 格式）",
        examples=["#409EFF", "#67C23A", "#E6A23C"],
    )


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""

    pass


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project."""

    code: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="專案代碼",
    )
    requirement_code: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="需求單號",
    )
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="專案名稱",
    )
    approved_man_days: Optional[Decimal] = Field(
        None,
        ge=0,
        decimal_places=2,
        description="核定工時（人天）",
    )
    default_account_group_id: Optional[int] = Field(
        None,
        description="預設帳組 ID",
    )
    default_work_category_id: Optional[int] = Field(
        None,
        description="預設工作類別 ID",
    )
    description: Optional[str] = Field(
        None,
        description="專案描述",
    )
    status: Optional[str] = Field(
        None,
        max_length=20,
        description="專案狀態",
    )
    color: Optional[str] = Field(
        None,
        pattern=r"^#[0-9A-Fa-f]{6}$",
        description="顏色代碼",
    )


class ProjectResponse(ProjectBase):
    """Schema for project responses."""

    id: int = Field(..., description="專案 ID")
    created_at: datetime = Field(..., description="創建時間")
    updated_at: datetime = Field(..., description="更新時間")
    deleted_at: Optional[datetime] = Field(None, description="刪除時間（軟刪除）")

    model_config = ConfigDict(from_attributes=True)


class ProjectList(BaseModel):
    """Schema for list of projects."""

    items: list[ProjectResponse]
    total: int = Field(..., description="總數量")
