"""
API endpoints for TCS formatting.

Provides endpoints for formatting time entries into TCS system format.
"""

from datetime import date as DateType
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.tcs_service import format_date_for_tcs, get_date_entries
from app.schemas import TCSFormatRequest, TCSFormatResponse, TCSDateRangeRequest, TCSDateRangeResponse

router = APIRouter()


@router.post(
    "/format",
    response_model=TCSFormatResponse,
    summary="Format time entries for TCS",
    description="Format time entries for a specific date into TCS system format",
)
def format_tcs_for_date(
    request: TCSFormatRequest,
    db: Session = Depends(get_db),
) -> TCSFormatResponse:
    """
    Format all time entries for a specific date into TCS format.

    Returns formatted text that can be copied and pasted directly into TCS system.

    Format example:
        日期: 2025/11/12
        專案名稱: 需2025單001
        帳組: A00 中概全權
        工作類別: A07 其它
        實際工時: 4.0
        工作說明:
        - [x] 需求分析
        - [x] 系統設計
    """
    entries = get_date_entries(db, request.date)

    if not entries:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No time entries found for date {request.date}",
        )

    return format_date_for_tcs(entries, request.date, db)


@router.post(
    "/format/range",
    response_model=TCSDateRangeResponse,
    summary="Format time entries for date range",
    description="Format time entries for a date range into TCS system format",
)
def format_tcs_for_date_range(
    request: TCSDateRangeRequest,
    db: Session = Depends(get_db),
) -> TCSDateRangeResponse:
    """
    Format all time entries for a date range into TCS format.

    Returns formatted text for multiple dates.
    """
    from datetime import timedelta
    from decimal import Decimal

    daily_formats = []
    total_hours = Decimal("0")

    # Iterate through date range
    current_date = request.start_date
    while current_date <= request.end_date:
        entries = get_date_entries(db, current_date)

        if entries:
            daily_format = format_date_for_tcs(entries, current_date, db)
            daily_formats.append(daily_format)
            total_hours += daily_format.total_hours

        current_date += timedelta(days=1)

    if not daily_formats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No time entries found between {request.start_date} and {request.end_date}",
        )

    # Combine all daily formats
    combined_text = "\n\n==========\n\n".join([df.formatted_text for df in daily_formats])

    return TCSDateRangeResponse(
        start_date=request.start_date.strftime("%Y/%m/%d"),
        end_date=request.end_date.strftime("%Y/%m/%d"),
        daily_formats=daily_formats,
        total_hours=total_hours,
        formatted_text=combined_text,
    )
