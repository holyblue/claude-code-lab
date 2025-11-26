"""
Pydantic schemas for TimeEntry.

These schemas define the data validation and serialization for time entries
in API requests and responses.
"""

from datetime import datetime
from datetime import date as DateType
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TimeEntryBase(BaseModel):
    """Base schema with common TimeEntry attributes."""

    date: DateType = Field(
        ...,
        description="工作日期",
        examples=["2025-01-15"],
    )
    project_id: int = Field(
        ...,
        gt=0,
        description="專案 ID",
    )
    account_group_id: Optional[int] = Field(
        None,
        description="模組 ID（選填）",
    )
    work_category_id: int = Field(
        ...,
        gt=0,
        description="工作類別 ID",
    )
    hours: Decimal = Field(
        ...,
        gt=0,
        le=99.99,
        decimal_places=2,
        description="工作時數（支援 0.5 小時為單位，最大 99.99）",
        examples=[0.5, 4.0, 7.5],
    )
    description: str = Field(
        ...,
        min_length=1,
        description="工作內容描述（支援 Markdown 格式）",
        examples=["完成系統功能開發", "進行需求分析會議"],
    )
    account_item: Optional[str] = Field(
        None,
        max_length=200,
        description="帳務項目",
    )
    display_order: int = Field(
        default=0,
        ge=0,
        description="顯示順序",
    )


class TimeEntryCreate(TimeEntryBase):
    """Schema for creating a new time entry."""

    pass


class TimeEntryUpdate(BaseModel):
    """Schema for updating an existing time entry."""

    date: Optional[DateType] = Field(
        None,
        description="工作日期",
    )
    project_id: Optional[int] = Field(
        None,
        gt=0,
        description="專案 ID",
    )
    account_group_id: Optional[int] = Field(
        None,
        description="模組 ID（選填）",
    )
    work_category_id: Optional[int] = Field(
        None,
        gt=0,
        description="工作類別 ID",
    )
    hours: Optional[Decimal] = Field(
        None,
        gt=0,
        le=99.99,
        decimal_places=2,
        description="工作時數",
    )
    description: Optional[str] = Field(
        None,
        min_length=1,
        description="工作內容描述",
    )
    account_item: Optional[str] = Field(
        None,
        max_length=200,
        description="帳務項目",
    )
    display_order: Optional[int] = Field(
        None,
        ge=0,
        description="顯示順序",
    )


class TimeEntryResponse(TimeEntryBase):
    """Schema for time entry responses."""

    id: int = Field(..., description="時間紀錄 ID")
    created_at: datetime = Field(..., description="創建時間")
    updated_at: datetime = Field(..., description="更新時間")

    model_config = ConfigDict(from_attributes=True)


class TimeEntryList(BaseModel):
    """Schema for list of time entries."""

    items: list[TimeEntryResponse]
    total: int = Field(..., description="總數量")


class TimeEntryDateRange(BaseModel):
    """Schema for querying time entries by date range."""

    start_date: DateType = Field(..., description="開始日期")
    end_date: DateType = Field(..., description="結束日期")
    project_id: Optional[int] = Field(None, description="篩選專案 ID")
    account_group_id: Optional[int] = Field(None, description="篩選模組 ID")
    work_category_id: Optional[int] = Field(None, description="篩選工作類別 ID")
