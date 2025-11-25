"""
單元測試：TCS 自動化相關功能
不涉及任何瀏覽器操作，只測試資料轉換和驗證邏輯
"""
import pytest
from datetime import date
from decimal import Decimal

from app.services.tcs_service import (
    convert_entries_to_tcs_format,
    validate_tcs_data,
)
from app.schemas.tcs import (
    TCSAutoFillRequest,
    TCSAutoFillResponse,
    TCSEntryData,
)
from tests.mocks.tcs_mock import (
    get_standard_test_data,
    create_mock_db_session,
    get_expected_tcs_entries,
)


class TestTCSSchemas:
    """測試 TCS 相關的 Pydantic schemas"""

    def test_tcs_entry_data_valid(self):
        """測試有效的 TCS 記錄資料"""
        entry = TCSEntryData(
            project_code="商2025智001",
            account_group="A00",
            work_category="A07",
            hours=7.5,
            description="測試工作說明",
        )
        assert entry.project_code == "商2025智001"
        assert entry.hours == 7.5
        assert entry.requirement_no == ""  # 預設值
        assert entry.progress_rate == 0  # 預設值

    def test_tcs_entry_data_invalid_hours(self):
        """測試無效的工時（超過 18 小時）"""
        with pytest.raises(ValueError):
            TCSEntryData(
                project_code="商2025智001",
                account_group="A00",
                work_category="A07",
                hours=20.0,  # 超過限制
                description="測試",
            )

    def test_tcs_auto_fill_request_default_dry_run(self):
        """測試 auto-fill request 預設為 dry_run"""
        request = TCSAutoFillRequest(date=date(2025, 11, 24))
        assert request.dry_run is True  # 預設應為 True

    def test_tcs_auto_fill_response(self):
        """測試 auto-fill response"""
        response = TCSAutoFillResponse(
            success=True,
            message="測試成功",
            filled_count=2,
            dry_run=True,
            total_hours=Decimal("7.5"),
        )
        assert response.success is True
        assert response.filled_count == 2


class TestConvertEntriesToTCSFormat:
    """測試資料轉換函數"""

    def test_convert_valid_entries(self):
        """測試轉換有效的記錄"""
        test_data = get_standard_test_data()
        db = create_mock_db_session(test_data)

        result = convert_entries_to_tcs_format(test_data["time_entries"], db)

        assert len(result) == 2
        assert result[0]["project_code"] == "商2025智001"
        assert result[0]["account_group"] == "A00"
        assert result[0]["work_category"] == "A07"
        assert result[0]["hours"] == 4.0
        assert result[1]["hours"] == 3.5

    def test_convert_empty_entries(self):
        """測試空記錄列表"""
        db = create_mock_db_session()
        result = convert_entries_to_tcs_format([], db)
        assert result == []

    def test_convert_missing_project(self):
        """測試缺少專案資料時拋出錯誤"""
        test_data = get_standard_test_data()
        test_data["project"] = None
        db = create_mock_db_session(test_data)

        with pytest.raises(ValueError, match="找不到專案"):
            convert_entries_to_tcs_format(test_data["time_entries"], db)


class TestValidateTCSData:
    """測試 TCS 資料驗證"""

    def test_validate_valid_data(self):
        """測試驗證有效資料"""
        entries = get_expected_tcs_entries()
        is_valid, errors = validate_tcs_data(entries)

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_empty_entries(self):
        """測試空記錄列表"""
        is_valid, errors = validate_tcs_data([])

        assert is_valid is False
        assert "沒有工時記錄" in errors[0]

    def test_validate_total_hours_exceed_limit(self):
        """測試總工時超過限制"""
        entries = [
            {
                "project_code": "TEST001",
                "account_group": "A00",
                "work_category": "A07",
                "hours": 10.0,
                "description": "測試1",
            },
            {
                "project_code": "TEST001",
                "account_group": "A00",
                "work_category": "A07",
                "hours": 9.0,
                "description": "測試2",
            },
        ]

        is_valid, errors = validate_tcs_data(entries)

        assert is_valid is False
        assert any("超過 TCS 限制" in err for err in errors)

    def test_validate_missing_required_fields(self):
        """測試缺少必填欄位"""
        entries = [
            {
                "project_code": "",  # 缺少
                "account_group": "A00",
                "work_category": "",  # 缺少
                "hours": 5.0,
                "description": "",  # 缺少
            }
        ]

        is_valid, errors = validate_tcs_data(entries)

        assert is_valid is False
        assert len(errors) >= 3
        assert any("專案代碼為必填" in err for err in errors)
        assert any("工作類別為必填" in err for err in errors)
        assert any("工作說明為必填" in err for err in errors)

    def test_validate_zero_hours(self):
        """測試工時為 0"""
        entries = [
            {
                "project_code": "TEST001",
                "account_group": "A00",
                "work_category": "A07",
                "hours": 0,  # 無效
                "description": "測試",
            }
        ]

        is_valid, errors = validate_tcs_data(entries)

        assert is_valid is False
        assert any("必須大於 0" in err for err in errors)


@pytest.mark.mock
class TestTCSSelectors:
    """測試選擇器配置正確性"""

    def test_selectors_json_exists(self):
        """測試選擇器配置檔存在"""
        import json
        from pathlib import Path

        selectors_path = Path(__file__).parent.parent.parent / "playwright" / "selectors.json"
        assert selectors_path.exists()

        with open(selectors_path, 'r', encoding='utf-8') as f:
            selectors = json.load(f)

        # 驗證必要的選擇器
        required_selectors = [
            "date_input",
            "save_button",
            "project_code",
            "module_code",
            "work_item_code",
            "work_hours",
            "work_description",
        ]

        for selector in required_selectors:
            assert selector in selectors, f"缺少選擇器: {selector}"
