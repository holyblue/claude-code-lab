# TCS 自動化功能安裝指南

## 📦 安裝步驟

### 1. 安裝 Python 依賴

```bash
cd backend

# 方法 A: 使用 uv（推薦，速度快）
uv pip install -r requirements.txt

# 方法 B: 使用 pip
pip install -r requirements.txt
```

### 2. 安裝 Playwright 瀏覽器驅動

```bash
# 安裝 Chromium 驅動（必須）
playwright install chromium

# 或安裝所有瀏覽器（可選）
playwright install
```

### 3. 驗證安裝

```bash
# 檢查 Playwright 版本
playwright --version
# 應顯示: Version 1.51.0

# 檢查 Python 環境
python -c "import playwright; print(playwright.__version__)"
# 應顯示: 1.51.0
```

## 🧪 執行測試

### 單元測試（完全安全，使用 Mock）

```bash
# 測試 TCS 資料轉換和驗證邏輯
pytest tests/unit/test_tcs_automation.py -v

# 輸出範例：
# tests/unit/test_tcs_automation.py::TestTCSSchemas::test_tcs_entry_data_valid PASSED
# tests/unit/test_tcs_automation.py::TestConvertEntriesToTCSFormat::test_convert_valid_entries PASSED
# tests/unit/test_tcs_automation.py::TestValidateTCSData::test_validate_valid_data PASSED
```

### 整合測試（完全安全，使用 Mock）

```bash
# 測試 API 端點（不會連接真實 TCS）
pytest tests/integration/test_tcs_auto_fill.py -v

# 輸出範例：
# tests/integration/test_tcs_auto_fill.py::TestTCSAutoFillAPI::test_auto_fill_success_dry_run PASSED
# tests/integration/test_tcs_auto_fill.py::TestTCSAutoFillAPI::test_auto_fill_validation_failed PASSED
```

### 執行所有 Mock 測試

```bash
# 只執行標記為 mock 的測試（推薦）
pytest -m mock -v

# 執行所有測試（包含其他功能）
pytest -v
```

## 🚀 啟動服務

### 1. 初始化資料庫（如果還沒有）

```bash
python app/init_db.py
```

### 2. 啟動 FastAPI 服務

```bash
# 開發模式（自動重載）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生產模式
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. 訪問 API 文檔

開啟瀏覽器訪問：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 手動測試（可選）

**⚠️ 注意**: 手動測試會啟動真實瀏覽器，但預設使用 dry_run 模式（不會真正寫入 TCS）

```bash
cd playwright

# 安全模式測試（預設，不會寫入）
python test_manual.py --date 2025-11-24

# 視覺化模式（可看到瀏覽器操作）
python test_manual.py --date 2025-11-24

# 無頭模式
python test_manual.py --date 2025-11-24 --headless
```

## 📋 API 使用範例

### Dry Run 模式（預設，安全）

```bash
curl -X POST "http://localhost:8000/api/tcs/auto-fill" \
  -H "Content-Type: application/json" \
  -d '{"date": "2025-11-24"}'
```

### 真實寫入模式（謹慎使用）

```bash
curl -X POST "http://localhost:8000/api/tcs/auto-fill" \
  -H "Content-Type: application/json" \
  -d '{"date": "2025-11-24", "dry_run": false}'
```

## ⚠️ 重要提醒

1. **測試環境**: 所有 pytest 測試使用 Mock，絕對安全
2. **手動測試**: 預設 dry_run 模式，不會真正寫入
3. **真實寫入**: 需要明確指定 `dry_run: false` 並確認資料正確
4. **內網需求**: TCS 自動化需要在內網環境執行（能訪問 http://cfcgpap01/tcs/）

## 🔧 疑難排解

### 問題 1: playwright 命令找不到

```bash
# 確保 playwright 已安裝
pip show playwright

# 重新安裝
pip uninstall playwright
pip install playwright==1.51.0
playwright install chromium
```

### 問題 2: 測試失敗 "No module named 'playwright'"

```bash
# 檢查當前環境
which python
python -m pip list | grep playwright

# 在正確的環境中安裝
pip install -r requirements.txt
```

### 問題 3: 無法連接 TCS

確認：
1. 在內網環境
2. 可以訪問 http://cfcgpap01/tcs/
3. 有 TCS 系統權限

```bash
# 測試連接
curl -I http://cfcgpap01/tcs/
```

## 📚 相關文檔

- [Backend README](./README.md) - 完整開發指南
- [TCS 自動化使用手冊](./tcs_automation/README.md) - 詳細使用說明
- [TCS 自動化計畫](../tcs.plan.md) - 實作計畫

## ✅ 完成檢查清單

安裝完成後，請確認：

- [ ] Python 依賴已安裝（`pip list | grep playwright`）
- [ ] Playwright 驅動已安裝（`playwright --version`）
- [ ] 單元測試通過（`pytest tests/unit/test_tcs_automation.py`）
- [ ] 整合測試通過（`pytest tests/integration/test_tcs_auto_fill.py`）
- [ ] FastAPI 服務可啟動（`uvicorn app.main:app`）
- [ ] API 文檔可訪問（http://localhost:8000/docs）
- [ ] （可選）手動測試可執行（`python tcs_automation/test_manual.py`）

全部完成後，TCS 自動化功能即可使用！
