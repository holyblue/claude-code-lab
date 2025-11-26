"""
API endpoints for TCS formatting and automation.

Provides endpoints for formatting time entries into TCS system format
and automatic filling using Playwright.
"""

from datetime import date as DateType
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.tcs_service import (
    format_date_for_tcs,
    get_date_entries,
    convert_entries_to_tcs_format,
    validate_tcs_data,
)
from app.schemas import (
    TCSFormatRequest,
    TCSFormatResponse,
    TCSDateRangeRequest,
    TCSDateRangeResponse,
    TCSAutoFillRequest,
    TCSAutoFillResponse,
)

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
        模組: A00 中概全權
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


@router.post(
    "/auto-fill",
    response_model=TCSAutoFillResponse,
    summary="Automatically fill TCS system",
    description=(
        "Automatically fill time entries into TCS system using browser automation. "
        "預設為 dry_run 模式（不會真正儲存）。"
    ),
)
def auto_fill_tcs(
    request: TCSAutoFillRequest,
    db: Session = Depends(get_db),
) -> TCSAutoFillResponse:
    """
    自動填寫工時記錄到 TCS 系統

    此端點會：
    1. 查詢指定日期的工時記錄
    2. 驗證資料完整性
    3. 使用 Playwright 自動填寫到 TCS 系統

    Args:
        request: 包含日期和 dry_run 參數
        db: 資料庫 session

    Returns:
        執行結果，包含成功/失敗訊息和填寫筆數

    Raises:
        HTTPException: 當找不到記錄或資料驗證失敗時
    """
    try:
        # 1. 查詢工時記錄
        entries = get_date_entries(db, request.date)

        if not entries:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"找不到 {request.date} 的工時記錄",
            )

        # 2. 轉換為 TCS 格式
        tcs_entries = convert_entries_to_tcs_format(entries, db)

        # 3. 驗證資料
        is_valid, errors = validate_tcs_data(tcs_entries)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"資料驗證失敗: {'; '.join(errors)}",
            )

        # 4. 計算總工時
        total_hours = Decimal(sum(e["hours"] for e in tcs_entries))

        # 5. 執行 Playwright 自動填寫
        # 注意：這裡使用延遲導入，避免在沒有 Playwright 的環境中出錯
        try:
            # Import here to avoid errors if playwright not installed
            import sys
            from pathlib import Path

            # Add backend to path to import tcs_automation module
            backend_path = Path(__file__).parent.parent.parent.parent
            if str(backend_path) not in sys.path:
                sys.path.insert(0, str(backend_path))

            from tcs_automation.tcs_automation import TCSAutomation

            # 建立自動化實例
            tcs = TCSAutomation()

            # 轉換日期格式為 YYYYMMDD
            date_str = request.date.strftime("%Y%m%d")

            # 執行自動填寫
            tcs.start(headless=True, dry_run=request.dry_run)
            tcs.fill_time_entries(date_str, tcs_entries)
            
            # 填寫完畢後截圖
            screenshot_path = None
            try:
                screenshot_path = tcs.screenshot(frame_only=True, full_page=True)
            except Exception as e:
                # 截圖失敗不影響主要流程，只記錄錯誤
                print(f"⚠️  截圖失敗（不影響主要流程）: {e}")
            
            # 儲存前預覽（自動確認模式，不需要等待輸入）
            tcs.preview_before_save(auto_confirm=True)
            
            tcs.save()
            tcs.close()

            # 成功訊息
            if request.dry_run:
                message = f"[DRY RUN] 已模擬填寫 {len(tcs_entries)} 筆工時記錄（未真正儲存）"
            else:
                message = f"成功自動填寫 {len(tcs_entries)} 筆工時記錄到 TCS 系統"

            return TCSAutoFillResponse(
                success=True,
                message=message,
                filled_count=len(tcs_entries),
                dry_run=request.dry_run,
                total_hours=total_hours,
                screenshot_path=screenshot_path,
            )

        except ImportError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Playwright 未安裝或配置錯誤: {str(e)}",
            )
        except Exception as playwright_error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Playwright 執行失敗: {str(playwright_error)}",
            )

    except HTTPException:
        # 重新拋出 HTTP 異常
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"資料錯誤: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"自動填寫失敗: {str(e)}",
        )
