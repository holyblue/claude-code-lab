"""
Pydantic schemas for API request/response validation.

This package contains all Pydantic schemas used for validating
API requests and serializing responses in the FastAPI application.
"""

from .account_group import (
    AccountGroupBase,
    AccountGroupCreate,
    AccountGroupUpdate,
    AccountGroupResponse,
    AccountGroupList,
)
from .work_category import (
    WorkCategoryBase,
    WorkCategoryCreate,
    WorkCategoryUpdate,
    WorkCategoryResponse,
    WorkCategoryList,
)
from .project import (
    ProjectBase,
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectList,
)
from .time_entry import (
    TimeEntryBase,
    TimeEntryCreate,
    TimeEntryUpdate,
    TimeEntryResponse,
    TimeEntryList,
    TimeEntryDateRange,
)
from .stats import (
    ProjectStats,
    DailyStats,
    WeeklyStats,
    MonthlyStats,
)
from .tcs import (
    TCSEntryFormat,
    TCSFormatRequest,
    TCSFormatResponse,
    TCSDateRangeRequest,
    TCSDateRangeResponse,
)

__all__ = [
    # AccountGroup schemas
    "AccountGroupBase",
    "AccountGroupCreate",
    "AccountGroupUpdate",
    "AccountGroupResponse",
    "AccountGroupList",
    # WorkCategory schemas
    "WorkCategoryBase",
    "WorkCategoryCreate",
    "WorkCategoryUpdate",
    "WorkCategoryResponse",
    "WorkCategoryList",
    # Project schemas
    "ProjectBase",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "ProjectList",
    # TimeEntry schemas
    "TimeEntryBase",
    "TimeEntryCreate",
    "TimeEntryUpdate",
    "TimeEntryResponse",
    "TimeEntryList",
    "TimeEntryDateRange",
    # Stats schemas
    "ProjectStats",
    "DailyStats",
    "WeeklyStats",
    "MonthlyStats",
    # TCS schemas
    "TCSEntryFormat",
    "TCSFormatRequest",
    "TCSFormatResponse",
    "TCSDateRangeRequest",
    "TCSDateRangeResponse",
]
