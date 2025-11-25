"""
整合測試：TCS 自動填寫 API 端點
使用 Mock 完全模擬 Playwright，絕不連接真實 TCS 系統
"""
import pytest
from datetime import date
from decimal import Decimal
from unittest.mock import patch, Mock, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from tests.mocks.tcs_mock import (
    get_standard_test_data,
    create_mock_db_session,
    create_mock_tcs_automation,
    get_expected_tcs_entries,
)

client = TestClient(app)


@pytest.mark.mock
class TestTCSAutoFillAPI:
    """測試 TCS 自動填寫 API（完全使用 Mock）"""

    @patch('app.api.endpoints.tcs.get_date_entries')
    @patch('app.api.endpoints.tcs.convert_entries_to_tcs_format')
    @patch('app.api.endpoints.tcs.validate_tcs_data')
    @patch('tcs_automation.tcs_automation.TCSAutomation')
    def test_auto_fill_success_dry_run(
        self,
        mock_tcs_class,
        mock_validate,
        mock_convert,
        mock_get_entries,
    ):
        """測試成功的自動填寫（dry_run 模式）"""
        # 準備測試資料
        test_data = get_standard_test_data()
        expected_entries = get_expected_tcs_entries()

        # Mock 資料庫查詢
        mock_get_entries.return_value = test_data["time_entries"]

        # Mock 資料轉換
        mock_convert.return_value = expected_entries

        # Mock 資料驗證
        mock_validate.return_value = (True, [])

        # Mock TCSAutomation
        mock_tcs_instance = create_mock_tcs_automation()
        mock_tcs_class.return_value = mock_tcs_instance

        # 發送請求（預設 dry_run=True）
        response = client.post(
            "/api/tcs/auto-fill",
            json={"date": "2025-11-24"},
        )

        # 驗證響應
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["filled_count"] == 2
        assert data["dry_run"] is True
        assert "DRY RUN" in data["message"]
        assert data["total_hours"] == "7.5"

        # 驗證 TCSAutomation 被正確呼叫
        mock_tcs_instance.start.assert_called_once_with(headless=True, dry_run=True)
        mock_tcs_instance.fill_time_entries.assert_called_once()
        mock_tcs_instance.save.assert_called_once()
        mock_tcs_instance.close.assert_called_once()

    @patch('app.api.endpoints.tcs.get_date_entries')
    @patch('app.api.endpoints.tcs.convert_entries_to_tcs_format')
    @patch('app.api.endpoints.tcs.validate_tcs_data')
    @patch('tcs_automation.tcs_automation.TCSAutomation')
    def test_auto_fill_success_real_mode(
        self,
        mock_tcs_class,
        mock_validate,
        mock_convert,
        mock_get_entries,
    ):
        """測試成功的自動填寫（真實模式，但仍使用 Mock）"""
        # 準備測試資料
        test_data = get_standard_test_data()
        expected_entries = get_expected_tcs_entries()

        mock_get_entries.return_value = test_data["time_entries"]
        mock_convert.return_value = expected_entries
        mock_validate.return_value = (True, [])

        mock_tcs_instance = create_mock_tcs_automation()
        mock_tcs_class.return_value = mock_tcs_instance

        # 發送請求（明確指定 dry_run=False）
        response = client.post(
            "/api/tcs/auto-fill",
            json={"date": "2025-11-24", "dry_run": False},
        )

        # 驗證響應
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["filled_count"] == 2
        assert data["dry_run"] is False
        assert "成功自動填寫" in data["message"]

        # 驗證 dry_run=False 被傳遞
        mock_tcs_instance.start.assert_called_once_with(headless=True, dry_run=False)
        mock_tcs_instance.preview_before_save.assert_called_once()

    @patch('app.api.endpoints.tcs.get_date_entries')
    def test_auto_fill_no_entries_found(self, mock_get_entries):
        """測試找不到工時記錄"""
        mock_get_entries.return_value = []

        response = client.post(
            "/api/tcs/auto-fill",
            json={"date": "2025-11-24"},
        )

        assert response.status_code == 404
        assert "找不到" in response.json()["detail"]

    @patch('app.api.endpoints.tcs.get_date_entries')
    @patch('app.api.endpoints.tcs.convert_entries_to_tcs_format')
    @patch('app.api.endpoints.tcs.validate_tcs_data')
    def test_auto_fill_validation_failed(
        self,
        mock_validate,
        mock_convert,
        mock_get_entries,
    ):
        """測試資料驗證失敗"""
        test_data = get_standard_test_data()
        mock_get_entries.return_value = test_data["time_entries"]
        mock_convert.return_value = get_expected_tcs_entries()

        # Mock 驗證失敗
        mock_validate.return_value = (False, ["專案代碼為必填", "工時必須大於 0"])

        response = client.post(
            "/api/tcs/auto-fill",
            json={"date": "2025-11-24"},
        )

        assert response.status_code == 400
        assert "資料驗證失敗" in response.json()["detail"]

    @patch('app.api.endpoints.tcs.get_date_entries')
    @patch('app.api.endpoints.tcs.convert_entries_to_tcs_format')
    @patch('app.api.endpoints.tcs.validate_tcs_data')
    @patch('tcs_automation.tcs_automation.TCSAutomation')
    def test_auto_fill_playwright_error(
        self,
        mock_tcs_class,
        mock_validate,
        mock_convert,
        mock_get_entries,
    ):
        """測試 Playwright 執行失敗"""
        test_data = get_standard_test_data()
        mock_get_entries.return_value = test_data["time_entries"]
        mock_convert.return_value = get_expected_tcs_entries()
        mock_validate.return_value = (True, [])

        # Mock Playwright 拋出錯誤
        mock_tcs_instance = create_mock_tcs_automation()
        mock_tcs_instance.start.side_effect = Exception("無法連接瀏覽器")
        mock_tcs_class.return_value = mock_tcs_instance

        response = client.post(
            "/api/tcs/auto-fill",
            json={"date": "2025-11-24"},
        )

        assert response.status_code == 500
        assert "Playwright 執行失敗" in response.json()["detail"]

    @patch('app.api.endpoints.tcs.get_date_entries')
    @patch('app.api.endpoints.tcs.convert_entries_to_tcs_format')
    def test_auto_fill_data_conversion_error(
        self,
        mock_convert,
        mock_get_entries,
    ):
        """測試資料轉換錯誤"""
        test_data = get_standard_test_data()
        mock_get_entries.return_value = test_data["time_entries"]

        # Mock 轉換拋出 ValueError
        mock_convert.side_effect = ValueError("找不到專案 ID: 999")

        response = client.post(
            "/api/tcs/auto-fill",
            json={"date": "2025-11-24"},
        )

        assert response.status_code == 400
        assert "資料錯誤" in response.json()["detail"]

    @patch('app.api.endpoints.tcs.get_date_entries')
    @patch('app.api.endpoints.tcs.convert_entries_to_tcs_format')
    @patch('app.api.endpoints.tcs.validate_tcs_data')
    @patch('tcs_automation.tcs_automation.TCSAutomation')
    def test_auto_fill_correct_date_format(
        self,
        mock_tcs_class,
        mock_validate,
        mock_convert,
        mock_get_entries,
    ):
        """測試日期格式正確轉換為 YYYYMMDD"""
        test_data = get_standard_test_data()
        expected_entries = get_expected_tcs_entries()

        mock_get_entries.return_value = test_data["time_entries"]
        mock_convert.return_value = expected_entries
        mock_validate.return_value = (True, [])

        mock_tcs_instance = create_mock_tcs_automation()
        mock_tcs_class.return_value = mock_tcs_instance

        response = client.post(
            "/api/tcs/auto-fill",
            json={"date": "2025-11-24"},
        )

        assert response.status_code == 200

        # 驗證傳給 fill_time_entries 的日期格式是 YYYYMMDD
        call_args = mock_tcs_instance.fill_time_entries.call_args
        assert call_args[0][0] == "20251124"  # 第一個參數應該是 YYYYMMDD 格式


@pytest.mark.mock
class TestTCSAutoFillSafety:
    """測試安全機制"""

    def test_default_dry_run_is_true(self):
        """確認預設為 dry_run 模式"""
        from app.schemas.tcs import TCSAutoFillRequest

        request = TCSAutoFillRequest(date=date(2025, 11, 24))
        assert request.dry_run is True

    @patch('app.api.endpoints.tcs.get_date_entries')
    @patch('app.api.endpoints.tcs.convert_entries_to_tcs_format')
    @patch('app.api.endpoints.tcs.validate_tcs_data')
    @patch('tcs_automation.tcs_automation.TCSAutomation')
    def test_no_real_tcs_connection_in_tests(
        self,
        mock_tcs_class,
        mock_validate,
        mock_convert,
        mock_get_entries,
    ):
        """確認測試中絕不會連接真實 TCS"""
        test_data = get_standard_test_data()
        mock_get_entries.return_value = test_data["time_entries"]
        mock_convert.return_value = get_expected_tcs_entries()
        mock_validate.return_value = (True, [])

        mock_tcs_instance = create_mock_tcs_automation()
        mock_tcs_class.return_value = mock_tcs_instance

        # 執行測試
        response = client.post(
            "/api/tcs/auto-fill",
            json={"date": "2025-11-24", "dry_run": False},
        )

        # 驗證使用的是 Mock，不是真實的 TCSAutomation
        assert response.status_code == 200
        assert mock_tcs_class.called
        assert isinstance(mock_tcs_instance, Mock)

        # 確認沒有任何真實的網路請求
        # 因為所有操作都是 Mock，不會有實際的瀏覽器啟動或網路連接
