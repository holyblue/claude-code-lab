"""
TCS formatting service.

Provides business logic for formatting time entries into TCS system format
and automation support.
"""

from datetime import date as DateType
from decimal import Decimal
from typing import List, Dict
from sqlalchemy.orm import Session

from app.models.time_entry import TimeEntry
from app.models.project import Project
from app.models.account_group import AccountGroup
from app.models.work_category import WorkCategory
from app.schemas import TCSFormatResponse, TCSEntryFormat, TCSEntryData


def format_date_for_tcs(date_entries: List[TimeEntry], target_date: DateType, db: Session) -> TCSFormatResponse:
    """
    Format time entries for a specific date into TCS format.

    Args:
        date_entries: List of TimeEntry objects for the target date
        target_date: The date to format
        db: Database session

    Returns:
        TCSFormatResponse with formatted text ready for copy-paste

    TCS Format:
        日期: YYYY/MM/DD
        專案名稱: {project_code}
        帳組: {code} {name}
        工作類別: {code} {name}
        實際工時: {hours}
        工作說明:
        {description}

        ---

        (repeat for each entry)
    """
    formatted_entries = []
    formatted_lines = [f"日期: {target_date.strftime('%Y/%m/%d')}"]
    total_hours = Decimal("0")

    for entry in date_entries:
        # Get related data
        project = db.query(Project).filter(Project.id == entry.project_id).first()
        account_group = db.query(AccountGroup).filter(AccountGroup.id == entry.account_group_id).first()
        work_category = db.query(WorkCategory).filter(WorkCategory.id == entry.work_category_id).first()

        if not all([project, account_group, work_category]):
            continue

        # Build entry format
        tcs_entry = TCSEntryFormat(
            project_name=project.code,
            account_group=account_group.full_name,
            work_category=work_category.full_name,
            hours=entry.hours,
            description=entry.description,
        )
        formatted_entries.append(tcs_entry)

        # Build formatted text
        formatted_lines.extend([
            f"專案名稱: {project.code}",
            f"帳組: {account_group.full_name}",
            f"工作類別: {work_category.full_name}",
            f"實際工時: {entry.hours}",
            "工作說明:",
            entry.description,
            "",
            "---",
            "",
        ])

        total_hours += entry.hours

    # Remove last separator
    if formatted_lines and formatted_lines[-1] == "" and formatted_lines[-2] == "---":
        formatted_lines = formatted_lines[:-2]

    formatted_text = "\n".join(formatted_lines)

    return TCSFormatResponse(
        date=target_date.strftime("%Y/%m/%d"),
        entries=formatted_entries,
        formatted_text=formatted_text,
        total_hours=total_hours,
    )


def get_date_entries(db: Session, target_date: DateType) -> List[TimeEntry]:
    """
    Get all time entries for a specific date, ordered by display_order.

    Args:
        db: Database session
        target_date: Date to query

    Returns:
        List of TimeEntry objects for the date
    """
    return (
        db.query(TimeEntry)
        .filter(TimeEntry.date == target_date)
        .order_by(TimeEntry.display_order.asc())
        .all()
    )


def convert_entries_to_tcs_format(date_entries: List[TimeEntry], db: Session) -> List[Dict]:
    """
    將資料庫 TimeEntry 轉換為 Playwright 需要的格式

    Args:
        date_entries: 時間記錄列表
        db: 資料庫 session

    Returns:
        TCS 自動化腳本需要的格式列表

    Raises:
        ValueError: 當資料不完整或無效時
    """
    tcs_entries = []

    for entry in date_entries:
        # 取得關聯資料
        project = db.query(Project).filter(Project.id == entry.project_id).first()
        
        # 模組是選填的，可能為 None
        account_group = None
        if entry.account_group_id:
            account_group = db.query(AccountGroup).filter(
                AccountGroup.id == entry.account_group_id
            ).first()
        
        work_category = db.query(WorkCategory).filter(
            WorkCategory.id == entry.work_category_id
        ).first()

        # 驗證必要資料
        if not project:
            raise ValueError(f"找不到專案 ID: {entry.project_id}")
        if not work_category:
            raise ValueError(f"找不到工作類別 ID: {entry.work_category_id}")
        
        # 如果有指定模組 ID 但找不到，則報錯
        if entry.account_group_id and not account_group:
            raise ValueError(f"找不到模組 ID: {entry.account_group_id}")

        # 建立 TCS 格式
        # 如果沒有指定模組（account_group_id 為 None），預設使用 "A00"
        account_group_code = account_group.code if account_group else "A00"
        
        tcs_entry = {
            "project_code": project.code,
            "account_group": account_group_code,
            "work_category": work_category.code,
            "hours": float(entry.hours),
            "description": entry.description or "",
            "requirement_no": "",  # 目前資料庫沒有這個欄位
            "progress_rate": 0,  # 目前資料庫沒有這個欄位
        }

        tcs_entries.append(tcs_entry)

    return tcs_entries


def validate_tcs_data(tcs_entries: List[Dict]) -> tuple[bool, List[str]]:
    """
    驗證 TCS 資料是否完整有效

    Args:
        tcs_entries: TCS 格式的記錄列表

    Returns:
        (is_valid, error_messages) tuple
        - is_valid: 是否全部驗證通過
        - error_messages: 錯誤訊息列表
    """
    errors = []

    if not tcs_entries:
        errors.append("沒有工時記錄")
        return False, errors

    # 計算總工時
    total_hours = sum(entry.get("hours", 0) for entry in tcs_entries)

    # 驗證總工時限制
    if total_hours > 18:
        errors.append(f"總工時 {total_hours} 小時超過 TCS 限制（18 小時）")

    if total_hours <= 0:
        errors.append("總工時必須大於 0")

    # 驗證每筆記錄
    for idx, entry in enumerate(tcs_entries, 1):
        # 必填欄位
        if not entry.get("project_code"):
            errors.append(f"第 {idx} 筆記錄：專案代碼為必填")

        # 模組是選填的，不檢查
        # if not entry.get("account_group"):
        #     errors.append(f"第 {idx} 筆記錄：模組為必填")

        if not entry.get("work_category"):
            errors.append(f"第 {idx} 筆記錄：工作類別為必填")

        # 工時驗證
        hours = entry.get("hours", 0)
        if hours <= 0:
            errors.append(f"第 {idx} 筆記錄：工時必須大於 0")
        if hours > 18:
            errors.append(f"第 {idx} 筆記錄：單筆工時不能超過 18 小時")

        # 工作說明
        if not entry.get("description"):
            errors.append(f"第 {idx} 筆記錄：工作說明為必填")

    is_valid = len(errors) == 0
    return is_valid, errors
