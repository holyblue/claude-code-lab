# TCS 自動化填寫使用手冊

## 📋 目錄

- [概述](#概述)
- [環境需求](#環境需求)
- [安全使用指南](#安全使用指南)
- [使用方式](#使用方式)
- [TCS 表單欄位對應](#tcs-表單欄位對應)
- [常見問題排除](#常見問題排除)
- [技術細節](#技術細節)

## 概述

TCS 自動化填寫功能使用 Playwright 實現瀏覽器自動化，可自動將本系統的工時記錄填寫到 TCS 系統中。

### 特色

- ✅ **一鍵同步**: 將當日工時記錄自動填寫到 TCS
- ✅ **Windows 整合驗證**: 自動使用當前使用者身份登入
- ✅ **資料驗證**: 自動驗證專案代碼、模組、工作類別
- ✅ **錯誤檢測**: 即時捕捉並回報 TCS 系統錯誤
- ✅ **安全預設**: 預設 dry_run 模式，避免誤操作
- ✅ **自動截圖**: 填寫完畢後自動截取 TCS 畫面，方便確認與記錄

## 環境需求

### 必要條件

1. **Python 3.10+**
2. **Playwright 1.51.0**
3. **Chromium 瀏覽器驅動**
4. **內網連接**: 必須能夠訪問 `http://cfcgpap01/tcs/`
5. **Windows 整合驗證**: 已登入的 Windows 帳戶需有 TCS 系統權限

### 安裝步驟

```bash
# 1. 安裝 Playwright（已包含在 requirements.txt）
pip install playwright==1.51.0
# 或使用 uv (推薦)
uv pip install playwright==1.51.0

# 2. 安裝瀏覽器驅動
playwright install chromium

# 3. 驗證安裝
playwright --version
```

## 安全使用指南

### ⚠️ 重要警告

**在測試或開發期間，請務必使用 dry_run 模式！**

### 安全機制

1. **預設保護**
   - API 預設 `dry_run=True`
   - 手動腳本預設 `dry_run=True`
   - 需明確指定 `--no-dry-run` 才會真正寫入

2. **確認機制**
   - 真實寫入前會顯示警告訊息
   - 需要輸入 `YES` 才會繼續
   - 顯示將要填寫的資料摘要

3. **測試隔離**
   - 所有 pytest 測試使用 Mock
   - 不會啟動真實瀏覽器
   - 不會連接 TCS 系統

### 如何避免誤寫入資料

✅ **安全做法**:
```bash
# 使用 API（預設 dry_run）
curl -X POST "http://localhost:8000/api/tcs/auto-fill" \
  -H "Content-Type: application/json" \
  -d '{"date": "2025-11-24"}'

# 使用手動腳本（預設 dry_run）
python test_manual.py --date 2025-11-24
```

❌ **危險做法** (僅在確認資料正確時使用):
```bash
# API 真實寫入
curl -X POST "http://localhost:8000/api/tcs/auto-fill" \
  -H "Content-Type: application/json" \
  -d '{"date": "2025-11-24", "dry_run": false}'

# 手動腳本真實寫入（需確認）
python test_manual.py --date 2025-11-24 --no-dry-run
```

## 使用方式

### 方式 1: API 端點（推薦）

適合前端整合使用。

#### DRY RUN 模式（預設）

```bash
POST /api/tcs/auto-fill
Content-Type: application/json

{
  "date": "2025-11-24"
}
```

**響應範例**:
```json
{
  "success": true,
  "message": "[DRY RUN] 已模擬填寫 2 筆工時記錄（未真正儲存）",
  "filled_count": 2,
  "dry_run": true,
  "total_hours": "7.5"
}
```

#### 真實寫入模式

```bash
POST /api/tcs/auto-fill
Content-Type: application/json

{
  "date": "2025-11-24",
  "dry_run": false
}
```

### 方式 2: 手動測試腳本

適合開發測試使用。

#### 基本用法

```bash
cd backend/tcs_automation

# 安全模式（預設）
# 填寫完畢後會自動截圖，儲存在 backend/screenshots/ 目錄
python test_manual.py --date 2025-11-24

# 使用無頭模式
python test_manual.py --date 2025-11-24 --headless

# 真正寫入（會要求確認）
python test_manual.py --date 2025-11-24 --no-dry-run
```

#### 參數說明

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `--date` | 日期 (YYYYMMDD) | 今天 |
| `--no-dry-run` | 關閉 dry_run 模式 | 開啟 (安全) |
| `--headless` | 使用無頭模式 | 關閉 (可視) |

### 方式 3: 程式碼整合

```python
from tcs_automation.tcs_automation import TCSAutomation

# 準備資料
entries = [
    {
        'project_code': '商2025智001',
        'account_group': 'A00',
        'work_category': 'A07',
        'hours': 7.5,
        'description': '- [x] 系統開發\n- [x] 單元測試',
        'requirement_no': '',
        'progress_rate': 0
    }
]

# 執行自動填寫（dry_run 模式）
tcs = TCSAutomation()
try:
    tcs.start(headless=False, dry_run=True)
    tcs.fill_time_entries('20251124', entries)
    
    # 填寫完畢後截圖（推薦：只截取 frame，表單部分）
    screenshot_path = tcs.screenshot(frame_only=True, full_page=True)
    print(f"截圖已儲存: {screenshot_path}")
    
    tcs.preview_before_save()
    tcs.save()
finally:
    tcs.close()
```

#### 截圖功能說明

**自動截圖**:
- 使用 `test_manual.py` 時，填寫完畢後會自動截圖
- 截圖儲存在 `backend/screenshots/` 目錄
- 檔名格式: `tcs_screenshot_YYYYMMDD_HHMMSS.png`

**手動截圖**:
```python
# 只截取 frame（mainFrame，表單部分）- 推薦
screenshot_path = tcs.screenshot(frame_only=True, full_page=True)

# 截取整個頁面
screenshot_path = tcs.screenshot(frame_only=False, full_page=True)

# 指定自訂路徑
screenshot_path = tcs.screenshot(path='my_screenshot.png', frame_only=True)
```

**參數說明**:
- `path`: 截圖儲存路徑（可選，預設自動產生檔名）
- `full_page`: 是否截取完整頁面（包含需要滾動的部分），預設 `True`
- `frame_only`: 是否只截取 frame（mainFrame），預設 `False`（截整個頁面）

## TCS 表單欄位對應

### 資料庫欄位 → TCS 欄位

| 本系統欄位 | TCS 欄位 | 選擇器 | 必填 | 說明 |
|-----------|---------|--------|------|------|
| date | 日期 | `#txtDate` | ✅ | 格式: YYYYMMDD |
| project.code | 專案代碼 | `#txtPROJ_CD{idx}` | ✅ | 會觸發 AJAX 查詢專案名稱 |
| account_group.code | 帳組/模組 | `#txtMODULE_CD{idx}` | ✅ | 會觸發 AJAX 查詢模組名稱 |
| work_category.code | 工作類別 | `#txtWORK_ITEM_CD{idx}` | ✅ | 會觸發 AJAX 查詢類別名稱 |
| - | 需求單號 | `#txtREQ_CD{idx}` | ❌ | 選填 |
| hours | 實際工時 | `#txtWORK_HR{idx}` | ✅ | 單位: 小時 |
| description | 工作說明 | `#txtWROK_DESC` (nth) | ✅ | 多行文字 |
| - | 完成百分比 | `#txtPRGRS_RATE{idx}` | ❌ | 0-100 |

### 注意事項

1. **索引從 0 開始**: 第一筆記錄使用 `{idx}=0`
2. **工作說明特殊處理**: 所有 textarea 共用同一個 ID，需使用 `nth(idx)` 選擇
3. **AJAX 驗證**: 每個欄位 blur 後會觸發驗證，需等待完成
4. **最多 5 筆**: 預設只有 5 行，超過需點擊「新增一列」按鈕

## 常見問題排除

### Q1: 無法連接 TCS 系統

**症狀**: 錯誤訊息 "找不到 mainFrame"

**可能原因**:
1. 不在內網環境
2. TCS 系統維護中
3. 沒有 TCS 系統權限

**解決方法**:
```bash
# 測試連接
curl -I http://cfcgpap01/tcs/

# 使用 Windows 整合驗證
Invoke-WebRequest -Uri "http://cfcgpap01/tcs/" -UseDefaultCredentials
```

### Q2: 專案代碼無效

**症狀**: 警告訊息 "專案代碼 XXX 可能無效"

**可能原因**:
1. 專案代碼拼寫錯誤
2. 專案在 TCS 中不存在或已關閉
3. 沒有該專案的填寫權限

**解決方法**:
1. 登入 TCS 系統手動確認專案代碼
2. 更新本系統中的專案代碼
3. 聯繫 TCS 管理員確認權限

### Q3: 總工時超過限制

**症狀**: 錯誤訊息 "總工時超過 TCS 限制（18 小時）"

**解決方法**:
1. 檢查當日工時記錄是否正確
2. 將工時分配到不同日期
3. TCS 系統限制每日最多 18 小時

### Q4: Playwright 未安裝

**症狀**: `ImportError: No module named 'playwright'`

**解決方法**:
```bash
pip install playwright==1.51.0
playwright install chromium
```

### Q5: 測試時誤寫入資料

**預防措施**:
1. **永遠使用 dry_run 模式測試**
2. 確認資料正確後才關閉 dry_run
3. 定期備份 TCS 資料（如可能）

**如果已誤寫入**:
1. 立即登入 TCS 系統
2. 手動刪除或修正錯誤記錄
3. 聯繫 TCS 管理員協助

## 技術細節

### 架構設計

```
┌─────────────┐
│   Frontend  │
└──────┬──────┘
       │ HTTP POST /api/tcs/auto-fill
       ▼
┌─────────────────┐
│  FastAPI Backend│
│  (tcs.py)       │
└──────┬──────────┘
       │ 1. get_date_entries()
       │ 2. convert_entries_to_tcs_format()
       │ 3. validate_tcs_data()
       ▼
┌──────────────────────┐
│  TCSAutomation       │
│  (Playwright)        │
└──────┬───────────────┘
       │ start(dry_run=True)
       │ fill_time_entries()
       │ save()
       │ close()
       ▼
┌──────────────────────┐
│  TCS System          │
│  (cfcgpap01/tcs)     │
└──────────────────────┘
```

### 關鍵技術點

1. **Frame 切換**
   - TCS 使用 frameset 結構
   - 需切換到 `mainFrame` 才能操作表單

2. **AJAX 驗證**
   - 每個輸入欄位 onblur 會觸發 AJAX
   - 使用 `blur()` + `time.sleep()` 等待

3. **動態行數**
   - 預設 5 行
   - 使用 `#btnAddLine` 新增行

4. **BIG-5 編碼**
   - TCS 系統使用 BIG-5
   - Playwright 自動處理編碼

5. **Windows 認證**
   - 使用 NTLM/Kerberos
   - 瀏覽器自動傳遞當前使用者憑證

### 選擇器配置

所有選擇器定義在 `selectors.json`:

```json
{
  "date_input": "txtDate",
  "save_button": "btnSave",
  "project_code": "txtPROJ_CD",
  "module_code": "txtMODULE_CD",
  "work_item_code": "txtWORK_ITEM_CD",
  "work_hours": "txtWORK_HR",
  "work_description": "txtWROK_DESC",
  "add_row_button": "btnAddLine"
}
```

### 測試策略

#### 單元測試 (Mock)
- 測試資料轉換邏輯
- 測試資料驗證邏輯
- **不啟動瀏覽器**

#### 整合測試 (Mock)
- 測試 API 端點
- Mock 整個 TCSAutomation
- **不連接 TCS**

#### 手動測試 (真實)
- 僅在確認資料正確時執行
- 使用 dry_run 預覽
- 需明確確認才寫入

## 開發指南

### 修改自動化邏輯

```python
# backend/tcs_automation/tcs_automation.py
class TCSAutomation:
    def _fill_single_entry(self, row_idx: int, entry: Dict):
        # 在這裡修改欄位填寫邏輯
        pass
```

### 更新選擇器

如果 TCS 系統更新，需要更新選擇器:

```json
// backend/tcs_automation/selectors.json
{
  "new_field": "新欄位的 ID"
}
```

### 新增驗證邏輯

```python
# backend/app/services/tcs_service.py
def validate_tcs_data(tcs_entries: List[Dict]) -> tuple[bool, List[str]]:
    # 在這裡新增驗證規則
    pass
```

## 參考資源

- [Playwright Python 文檔](https://playwright.dev/python/)
- [FastAPI 文檔](https://fastapi.tiangolo.com/)
- [TCS 系統說明](http://cfcgpap01/tcs/) (內網)

## 授權與貢獻

此自動化工具僅供內部使用，請勿外傳。

如有問題或建議，請聯繫開發團隊。
