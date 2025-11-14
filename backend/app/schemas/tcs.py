"""
Pydantic schemas for TCS (Time Card System) integration.

These schemas define the data validation and serialization for formatting
time entries into TCS system format for copy-paste operations.
"""

from datetime import date as DateType
from decimal import Decimal

from pydantic import BaseModel, Field


class TCSEntryFormat(BaseModel):
    """Schema for a single TCS-formatted time entry."""

    project_name: str = Field(..., description="專案名稱")
    account_group: str = Field(..., description="帳組（代碼 + 名稱）")
    work_category: str = Field(..., description="工作類別（代碼 + 名稱）")
    hours: Decimal = Field(..., description="實際工時")
    description: str = Field(..., description="工作說明")


class TCSFormatRequest(BaseModel):
    """Schema for requesting TCS format for a specific date."""

    date: DateType = Field(
        ...,
        description="要格式化的日期",
        examples=["2025-11-12"],
    )


class TCSFormatResponse(BaseModel):
    """Schema for TCS formatted output response."""

    date: str = Field(
        ...,
        description="日期（YYYY/MM/DD 格式）",
        examples=["2025/11/12"],
    )
    entries: list[TCSEntryFormat] = Field(
        ...,
        description="該日期的所有時間記錄",
    )
    formatted_text: str = Field(
        ...,
        description="格式化後的文字（可直接複製到 TCS 系統）",
    )
    total_hours: Decimal = Field(
        ...,
        ge=0,
        description="當日總工時",
    )


class TCSDateRangeRequest(BaseModel):
    """Schema for requesting TCS format for a date range."""

    start_date: DateType = Field(..., description="開始日期")
    end_date: DateType = Field(..., description="結束日期")


class TCSDateRangeResponse(BaseModel):
    """Schema for TCS formatted output for multiple dates."""

    start_date: str = Field(..., description="開始日期（YYYY/MM/DD）")
    end_date: str = Field(..., description="結束日期（YYYY/MM/DD）")
    daily_formats: list[TCSFormatResponse] = Field(
        ...,
        description="每日的格式化記錄",
    )
    total_hours: Decimal = Field(
        ...,
        ge=0,
        description="期間總工時",
    )
    formatted_text: str = Field(
        ...,
        description="完整格式化文字（包含所有日期）",
    )
