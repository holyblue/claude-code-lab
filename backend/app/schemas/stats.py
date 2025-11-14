"""
Pydantic schemas for Statistics and Reporting.

These schemas define the data validation and serialization for statistics
and project tracking metrics.
"""

from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, Field, computed_field


class ProjectStats(BaseModel):
    """Schema for project statistics and approved hours tracking."""

    project_id: int = Field(..., description="專案 ID")
    project_code: str = Field(..., description="專案代碼")
    project_name: str = Field(..., description="專案名稱")
    approved_man_days: Optional[Decimal] = Field(
        None,
        description="核定工時（人天）",
    )
    approved_hours: Optional[Decimal] = Field(
        None,
        description="核定工時（小時，1人天=7.5小時）",
    )
    used_hours: Decimal = Field(
        ...,
        ge=0,
        description="已使用工時（扣抵類別）",
    )
    non_deduct_hours: Decimal = Field(
        default=Decimal("0"),
        ge=0,
        description="不扣抵工時（如 A08 商模、I07 休假）",
    )
    total_hours: Decimal = Field(
        ...,
        ge=0,
        description="專案總工時（扣抵 + 不扣抵）",
    )
    remaining_hours: Optional[Decimal] = Field(
        None,
        description="剩餘工時（核定工時 - 已使用工時）",
    )
    usage_rate: Optional[Decimal] = Field(
        None,
        ge=0,
        decimal_places=1,
        description="使用率（%，可能超過 100% 表示超支）",
    )
    warning_level: Literal["none", "warning", "danger"] = Field(
        default="none",
        description="預警級別（none: <80%, warning: 80-99%, danger: ≥100%）",
    )
    warning_message: Optional[str] = Field(
        None,
        description="警告訊息",
    )

    @computed_field
    @property
    def is_over_budget(self) -> bool:
        """Check if project is over budget."""
        if self.approved_hours is None:
            return False
        return self.used_hours > self.approved_hours


class DailyStats(BaseModel):
    """Schema for daily work hours statistics."""

    date: str = Field(..., description="日期（YYYY-MM-DD）")
    total_hours: Decimal = Field(
        ...,
        ge=0,
        description="當日總工時",
    )
    entry_count: int = Field(
        ...,
        ge=0,
        description="當日記錄筆數",
    )
    project_count: int = Field(
        ...,
        ge=0,
        description="涉及專案數",
    )


class WeeklyStats(BaseModel):
    """Schema for weekly work hours statistics."""

    week_start: str = Field(..., description="週起始日期（YYYY-MM-DD）")
    week_end: str = Field(..., description="週結束日期（YYYY-MM-DD）")
    total_hours: Decimal = Field(
        ...,
        ge=0,
        description="本週總工時",
    )
    daily_breakdown: list[DailyStats] = Field(
        ...,
        description="每日明細",
    )


class MonthlyStats(BaseModel):
    """Schema for monthly work hours statistics."""

    year: int = Field(..., ge=2020, le=2100, description="年份")
    month: int = Field(..., ge=1, le=12, description="月份")
    total_hours: Decimal = Field(
        ...,
        ge=0,
        description="本月總工時",
    )
    working_days: int = Field(
        ...,
        ge=0,
        description="工作天數",
    )
    avg_hours_per_day: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="平均每日工時",
    )
    project_breakdown: list[ProjectStats] = Field(
        default_factory=list,
        description="專案分布",
    )
