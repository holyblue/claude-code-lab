"""
Mock utilities for TCS automation testing.
提供可重用的 Mock fixtures 和測試資料
"""
from datetime import date
from decimal import Decimal
from unittest.mock import MagicMock, Mock
from typing import List

from app.models.time_entry import TimeEntry
from app.models.project import Project
from app.models.account_group import AccountGroup
from app.models.work_category import WorkCategory


def create_mock_project(
    id: int = 1,
    code: str = "商2025智001",
    name: str = "語音質檢系統"
) -> Project:
    """建立模擬 Project"""
    project = Mock(spec=Project)
    project.id = id
    project.code = code
    project.name = name
    return project


def create_mock_account_group(
    id: int = 1,
    code: str = "A00",
    name: str = "中概全權",
) -> AccountGroup:
    """建立模擬 AccountGroup"""
    ag = Mock(spec=AccountGroup)
    ag.id = id
    ag.code = code
    ag.name = name
    ag.full_name = f"{code} {name}"
    return ag


def create_mock_work_category(
    id: int = 1,
    code: str = "A07",
    name: str = "其它",
) -> WorkCategory:
    """建立模擬 WorkCategory"""
    wc = Mock(spec=WorkCategory)
    wc.id = id
    wc.code = code
    wc.name = name
    wc.full_name = f"{code} {name}"
    return wc


def create_mock_time_entry(
    id: int = 1,
    date_val: date = date(2025, 11, 24),
    project_id: int = 1,
    account_group_id: int = 1,
    work_category_id: int = 1,
    hours: Decimal = Decimal("7.5"),
    description: str = "測試工作說明",
    display_order: int = 1,
) -> TimeEntry:
    """建立模擬 TimeEntry"""
    entry = Mock(spec=TimeEntry)
    entry.id = id
    entry.date = date_val
    entry.project_id = project_id
    entry.account_group_id = account_group_id
    entry.work_category_id = work_category_id
    entry.hours = hours
    entry.description = description
    entry.display_order = display_order
    return entry


def get_standard_test_data() -> dict:
    """
    取得標準測試資料集
    
    Returns:
        包含 project, account_group, work_category, time_entries 的字典
    """
    project = create_mock_project()
    account_group = create_mock_account_group()
    work_category = create_mock_work_category()
    
    time_entries = [
        create_mock_time_entry(
            id=1,
            hours=Decimal("4.0"),
            description="- [x] 系統架構設計\n- [x] 資料庫設計",
            display_order=1,
        ),
        create_mock_time_entry(
            id=2,
            hours=Decimal("3.5"),
            description="- [x] API 開發\n- [x] 單元測試",
            display_order=2,
        ),
    ]
    
    return {
        "project": project,
        "account_group": account_group,
        "work_category": work_category,
        "time_entries": time_entries,
    }


def create_mock_db_session(test_data: dict = None) -> Mock:
    """
    建立模擬資料庫 session
    
    Args:
        test_data: 測試資料字典（來自 get_standard_test_data）
    
    Returns:
        Mock DB session
    """
    if test_data is None:
        test_data = get_standard_test_data()
    
    db = Mock()
    
    # 模擬 query 方法
    def mock_query(model):
        query_mock = Mock()
        
        if model == Project:
            query_mock.filter.return_value.first.return_value = test_data["project"]
        elif model == AccountGroup:
            query_mock.filter.return_value.first.return_value = test_data["account_group"]
        elif model == WorkCategory:
            query_mock.filter.return_value.first.return_value = test_data["work_category"]
        elif model == TimeEntry:
            # 支援鏈式呼叫
            filter_mock = Mock()
            filter_mock.order_by.return_value.all.return_value = test_data["time_entries"]
            query_mock.filter.return_value = filter_mock
        
        return query_mock
    
    db.query = mock_query
    return db


def create_mock_tcs_automation():
    """
    建立模擬 TCSAutomation 實例
    
    Returns:
        Mock TCSAutomation instance
    """
    mock_tcs = Mock()
    mock_tcs.start = Mock()
    mock_tcs.fill_time_entries = Mock()
    mock_tcs.preview_before_save = Mock()
    mock_tcs.save = Mock()
    mock_tcs.close = Mock()
    return mock_tcs


def get_expected_tcs_entries() -> List[dict]:
    """
    取得預期的 TCS 格式資料（對應 standard_test_data）
    
    Returns:
        TCS 格式的記錄列表
    """
    return [
        {
            "project_code": "商2025智001",
            "account_group": "A00",
            "work_category": "A07",
            "hours": 4.0,
            "description": "- [x] 系統架構設計\n- [x] 資料庫設計",
            "requirement_no": "",
            "progress_rate": 0,
        },
        {
            "project_code": "商2025智001",
            "account_group": "A00",
            "work_category": "A07",
            "hours": 3.5,
            "description": "- [x] API 開發\n- [x] 單元測試",
            "requirement_no": "",
            "progress_rate": 0,
        },
    ]
