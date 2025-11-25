# 專案開發規範與共通語言

> 本文件定義專案的術語、命名規範和開發標準，確保團隊成員和 AI 助手使用一致的語言進行開發。

## 📚 術語對照表 (Terminology)

### 核心業務術語

| 正確術語 | ❌ 錯誤/不使用 | 英文 | 說明 |
|---------|--------------|------|------|
| **模組** | 帳組、帳組/模組 | Account Group / Module | TCS 系統中的分類欄位，對應資料表 `account_groups` |
| **工作類別** | 類別 | Work Category | 工作項目分類，對應資料表 `work_categories` |
| **專案代碼** | 專案編號 | Project Code | 專案的唯一識別碼，如 `商2025智001` |
| **需求單代碼** | 需求編號 | Requirement Code | 需求單的識別碼 |
| **工時** | 時數、小時數 | Hours | 工作時間，單位為小時 |
| **工時記錄** | 時間記錄、工作記錄 | Time Entry | 單筆工時記錄 |
| **核定工時** | 預估工時、計畫工時 | Approved Hours | 專案核定的總工時（人天轉換為小時） |
| **實際工時** | 已用工時 | Used Hours | 實際使用的工時 |
| **剩餘工時** | 可用工時 | Remaining Hours | 尚未使用的工時 |

### TCS 相關術語

| 正確術語 | ❌ 錯誤/不使用 | 說明 |
|---------|--------------|------|
| **TCS 系統** | 工時系統、時間卡系統 | Time Card System，公司內部工時記錄系統 |
| **同步到 TCS** | 上傳到 TCS、匯出到 TCS | 將工時記錄同步到 TCS 系統 |
| **Dry Run 模式** | 測試模式、預覽模式 | 模擬執行但不實際寫入的模式 |
| **自動填寫** | 自動輸入、自動同步 | 使用 Playwright 自動填寫 TCS 表單 |

### 技術術語

| 正確術語 | ❌ 錯誤/不使用 | 說明 |
|---------|--------------|------|
| **前端** | Frontend、客戶端 | Vue 3 + TypeScript 前端應用 |
| **後端** | Backend、伺服器端 | FastAPI + Python 後端服務 |
| **API 端點** | 接口、API | RESTful API 端點 |
| **Store** | 狀態管理、Pinia | Pinia 狀態管理 Store |
| **Schema** | 模型、驗證 | Pydantic Schema 資料驗證模型 |
| **Model** | 資料模型 | SQLAlchemy ORM Model |

## 🏗️ 資料表命名規範

### 資料表名稱

| 資料表 | 說明 | 關鍵欄位 |
|--------|------|---------|
| `projects` | 專案 | `code`, `requirement_code`, `approved_man_days` |
| `account_groups` | 模組 | `code`, `name`, `full_name` |
| `work_categories` | 工作類別 | `code`, `name`, `deduct_approved_hours` |
| `time_entries` | 工時記錄 | `date`, `project_id`, `account_group_id`, `hours` |
| `work_templates` | 工作範本 | 用於快速建立常用工時記錄 |
| `milestones` | 里程碑 | 專案里程碑管理 |
| `settings` | 系統設定 | 全域設定 |

### 欄位命名規範

- 使用 **snake_case**（後端資料庫、Python）
- 使用 **camelCase**（前端 TypeScript）
- ID 欄位統一使用 `id`（主鍵）、`xxx_id`（外鍵）
- 時間戳記使用 `created_at`, `updated_at`, `deleted_at`
- 布林值使用 `is_xxx`, `has_xxx`, `deduct_xxx` 等前綴

## 📝 註釋與文檔規範

### Python (後端)

```python
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
    
    Note:
        模組（account_group）是選填的，可能為 None
    """
```

### TypeScript (前端)

```typescript
/**
 * 同步工時到 TCS 系統
 * @param date 日期 (YYYY-MM-DD)
 * @param dryRun 是否為 Dry Run 模式（預設 true）
 * @returns 同步結果
 * 
 * @note 模組是選填欄位，允許為 null
 */
async syncToTCS(date: string, dryRun: boolean = true): Promise<TCSAutoFillResponse>
```

## 🎯 業務規則

### 工時記錄規則

1. **必填欄位**
   - ✅ 日期 (`date`)
   - ✅ 專案 (`project_id`)
   - ✅ 工作類別 (`work_category_id`)
   - ✅ 工時 (`hours`)
   - ✅ 工作說明 (`description`)

2. **選填欄位**
   - ⭕ 模組 (`account_group_id`) - **重要：模組是選填的！**
   - ⭕ 需求單號 (`requirement_no`)
   - ⭕ 完成百分比 (`progress_rate`)

3. **工時限制**
   - 單筆工時：0.5 ~ 18 小時
   - 每日總工時：≤ 18 小時
   - 工時單位：0.5 小時（30 分鐘）

### TCS 同步規則

1. **同步範圍**
   - 一次同步一天的工時記錄
   - 同步會覆蓋 TCS 該日期的現有資料

2. **安全機制**
   - 預設使用 Dry Run 模式
   - 需明確關閉 Dry Run 才會真正寫入
   - 所有測試使用 Mock，不碰真實 TCS

3. **模組處理**
   - 如果工時記錄沒有指定模組（`account_group_id` 為 `null`）
   - TCS 同步時會跳過模組欄位
   - 不會報錯，正常完成同步

## 🚫 常見錯誤與修正

### ❌ 錯誤用法

```python
# 錯誤：把模組當作必填
if not account_group:
    raise ValueError(f"找不到帳組 ID: {entry.account_group_id}")
```

```python
# 錯誤：使用不一致的術語
errors.append(f"帳組為必填")
```

### ✅ 正確用法

```python
# 正確：模組是選填的
if entry.account_group_id and not account_group:
    raise ValueError(f"找不到模組 ID: {entry.account_group_id}")
```

```python
# 正確：使用統一術語
# 模組是選填的，不檢查
```

## 🔄 API 設計規範

### RESTful 端點命名

- `GET /api/projects` - 列出專案
- `POST /api/projects` - 建立專案
- `GET /api/projects/{id}` - 取得單一專案
- `PATCH /api/projects/{id}` - 更新專案（部分更新）
- `DELETE /api/projects/{id}` - 刪除專案

### 請求/響應格式

```typescript
// 請求
{
  "date": "2025-11-25",
  "dry_run": true  // 使用 snake_case（API 層）
}

// 響應
{
  "success": true,
  "message": "成功同步 2 筆工時記錄",
  "filled_count": 2,
  "dry_run": true,
  "total_hours": "7.5"
}
```

## 📊 日期與時間格式

### 標準格式

| 用途 | 格式 | 範例 |
|------|------|------|
| API 傳輸 | `YYYY-MM-DD` | `2025-11-25` |
| TCS 系統 | `YYYYMMDD` | `20251125` |
| 顯示（完整） | `YYYY/MM/DD` | `2025/11/25` |
| 顯示（時間戳記） | `YYYY-MM-DD HH:mm:ss` | `2025-11-25 14:30:00` |

## 🎨 UI/UX 術語

### 按鈕文字

| 操作 | 正確用語 | ❌ 錯誤 |
|------|---------|--------|
| 同步 | 同步到 TCS | 上傳、匯出 |
| 預覽 | 預覽（不寫入） | 測試、模擬 |
| 確認 | 確認同步 | 送出、提交 |
| 取消 | 取消 | 返回、關閉 |

### 狀態訊息

```typescript
// ✅ 正確
"成功同步 2 筆工時記錄到 TCS 系統"
"[DRY RUN] 已模擬填寫 2 筆記錄（未真正寫入）"
"找不到模組 ID: 123"

// ❌ 錯誤
"成功上傳 2 筆時間記錄"
"測試模式完成"
"找不到帳組"
```

## 🔐 安全與測試規範

### 測試命名

- `test_convert_entries_with_optional_module()` - 測試選填模組
- `test_sync_without_module()` - 測試無模組同步
- `test_dry_run_mode()` - 測試 Dry Run 模式

### 錯誤訊息

```python
# ✅ 清晰且一致的錯誤訊息
raise ValueError(f"找不到模組 ID: {entry.account_group_id}")
raise ValueError(f"總工時 {total_hours} 小時超過 TCS 限制（18 小時）")
raise ValueError(f"第 {idx} 筆記錄：專案代碼為必填")

# ❌ 避免模糊或不一致的訊息
raise ValueError("ID not found")
raise ValueError("帳組錯誤")
```

## 📚 專案特定慣例

### 1. 模組（Account Group）特別說明

**重要**: `account_group` 在程式碼中保持原名（歷史原因），但在**所有註釋、文檔、UI 顯示**中統一使用「**模組**」。

```python
# 程式碼變數名稱
account_group_id: int | None  # 資料庫欄位名稱不變

# 但註釋和文檔中使用「模組」
"""
模組是選填的，可能為 None
If account_group_id is provided...
"""
```

### 2. Dry Run 命名

- 程式碼參數: `dry_run` (snake_case)
- API 欄位: `dry_run`
- UI 顯示: `DRY RUN` 或 `Dry Run 模式`
- 中文說明: 「乾運行模式」或「預覽模式（不寫入）」

### 3. 工時單位

- 資料庫儲存: `Decimal` 或 `float`
- 顯示格式: `X.X 小時` 或 `X.X h`
- 最小單位: `0.5` 小時

## ✅ 檢查清單

在提交程式碼前，請確認：

- [ ] 使用「模組」而非「帳組」
- [ ] 使用「工時記錄」而非「時間記錄」
- [ ] 使用「同步到 TCS」而非「上傳到 TCS」
- [ ] 註釋使用中文（或英文），保持一致
- [ ] API 使用 snake_case，前端使用 camelCase
- [ ] 錯誤訊息清晰且使用統一術語
- [ ] 模組（account_group）處理為選填欄位
- [ ] Dry Run 預設為 `true`

## 🔄 更新記錄

| 日期 | 版本 | 更新內容 | 更新者 |
|------|------|---------|--------|
| 2025-11-25 | 1.0.0 | 建立初始版本，統一「模組」術語 | Claude + User |

---

**注意**: 本文件是專案的核心規範文件，所有開發人員和 AI 助手都應遵循此規範。如有疑問或建議，請提出討論並更新此文件。

**Last Updated**: 2025-11-25  
**Maintained by**: 開發團隊
