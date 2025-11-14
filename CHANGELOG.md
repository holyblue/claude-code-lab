# Changelog

本檔案記錄專案的所有重要變更，遵循 [claude.md](./claude.md) 規範。

## 格式說明
- **日期** - 功能名稱
- ✅ 已完成 - 實作內容
- 📊 測試成果 - 測試數量、覆蓋率
- 🔑 關鍵業務規則驗證 - 驗證的業務邏輯
- 📁 變更檔案 - 新增/修改的檔案列表
- 📝 備註 - 相關說明

---

## [2025-11-14] - 升級依賴管理工具至 uv（極速版）

### ✅ 已完成

**依賴管理工具升級：**
- ✅ 安裝 uv 0.8.17（Rust 實作的高速套件管理工具）
- ✅ 使用 uv 創建虛擬環境（`.venv/`）
- ✅ 使用 uv 安裝所有依賴（50 個套件）
- ✅ 驗證測試環境正常運作

**文件更新：**
- 更新 `backend/README.md`：
  - 新增「技術棧」章節（完整列出所有依賴及版本）
  - 新增 uv 安裝方法與效能數據
  - 更新開發進度狀態
- 更新 `agent.md` (claude.md)：
  - 新增依賴管理規範
  - 明確使用 uv 作為標準工具

### 📊 效能數據

**uv vs pip 速度對比：**
| 操作 | uv | pip (傳統) | 速度提升 |
|------|-----|-----------|---------|
| 創建虛擬環境 | 0.2 秒 | 2-3 秒 | **10-15x** |
| 安裝 50 個套件 | 5.2 秒 | 30-60 秒 | **6-12x** |
| 總體體驗 | ⚡ 極速 | 🐢 緩慢 | **顯著提升** |

### 🔑 關鍵優勢

**為什麼選擇 uv？**
1. ⚡ **極致速度** - Rust 實作，比 pip 快 10-100 倍
2. 🎯 **零學習成本** - 語法與 pip 完全相同
3. 🔒 **依賴鎖定** - 自動生成 lock 檔案
4. 📦 **統一工具** - 管理 Python 版本 + 虛擬環境 + 依賴
5. 💾 **全域快取** - 跨專案共享依賴，節省空間

### 📊 測試成果
- ✅ 所有 30 個單元測試通過
- ✅ 測試執行時間：1.6 秒
- ✅ 虛擬環境正常運作
- ✅ 所有依賴正確安裝

### 📁 變更檔案
- `backend/.venv/` - 新增虛擬環境（使用 uv 創建）
- `backend/README.md` - 新增技術棧章節，更新安裝方式
- `agent.md` (claude.md) - 新增依賴管理規範
- 系統全域 - 安裝 uv 0.8.17

### 📝 備註
- uv 已成為專案標準依賴管理工具
- 保留 requirements.txt 以確保向後兼容
- CI/CD 流程將來也可使用 uv 大幅加速
- 下次開發環境設定只需：`uv venv && uv pip install -r requirements.txt`

**安裝指令：**
```bash
# 快速設定開發環境
pip install uv                      # 安裝 uv
cd backend                          # 進入後端目錄
uv venv                            # 創建虛擬環境（0.2秒）
source .venv/bin/activate          # 啟動環境
uv pip install -r requirements.txt # 安裝依賴（5秒）
pytest -v                          # 運行測試
```

---

## [2025-11-14] - 完成全部 6 個資料庫模型（TDD）

### ✅ 已完成

**TDD Cycle 2 完成：**
- ✅ Red: 撰寫 TimeEntry, WorkTemplate, Setting 測試
- ✅ Green: 實作全部 3 個模型（13 個新測試，全部通過）
- ✅ Total: 30 個測試通過，82% 覆蓋率（超過 80% 目標）

**模型實作完成（6/6）：**

1. **Project** (專案) - 9 個測試，95% 覆蓋率
   - 核心欄位：code, requirement_code, name, approved_man_days
   - 業務邏輯：軟刪除、代碼唯一性、外鍵關聯

2. **AccountGroup** (帳組) - 3 個測試，89% 覆蓋率
   - 核心欄位：code, name, is_default
   - 唯一約束：(code, name) 組合

3. **WorkCategory** (工作類別) - 5 個測試，89% 覆蓋率
   - 核心欄位：code, name, deduct_approved_hours
   - 業務邏輯：A08 商模/I07 休假不扣抵核定工時

4. **TimeEntry** (工時記錄) - 6 個測試，95% 覆蓋率 ⭐ 核心模型
   - 核心欄位：date, project_id, hours, description
   - 功能：支援 Markdown、display_order、account_item
   - 驗證：支援 0.5 小時增量（0.5-12.0 小時）

5. **WorkTemplate** (工作範本) - 3 個測試，94% 覆蓋率
   - 核心欄位：name, default_hours, description_template
   - 用途：快速建立重複性工時記錄

6. **Setting** (系統設定) - 4 個測試，91% 覆蓋率
   - 核心欄位：key (唯一), value
   - 用途：系統配置（語言、時區、工時標準）

**資料庫初始化：**
- 創建 `init_db.py` 腳本
- 種子資料：2 個帳組、4 個工作類別、8 個系統設定
- 測試成功：所有表格創建，種子資料插入

### 📊 測試成果
- **總測試數**：30 個（全部通過 ✅）
- **覆蓋率**：82%（超過 80% 要求）
- **模型覆蓋率**：89-95%（優秀）
- **測試類型**：單元測試、關聯測試、約束測試

### 🔑 關鍵業務規則驗證
- ✅ 專案代碼唯一性
- ✅ 核定人天追蹤（1 人天 = 7.5 小時）
- ✅ A08 商模不扣抵核定工時（重要）
- ✅ I07 休假不扣抵核定工時
- ✅ 工時記錄支援 0.5 小時增量
- ✅ 設定 key 唯一性
- ✅ 軟刪除機制（deleted_at 時間戳記）
- ✅ 所有模型自動時間戳記

### 📁 變更檔案
- `backend/app/init_db.py` - 新增資料庫初始化腳本
- `backend/app/models/__init__.py` - 更新模型匯出
- `backend/app/models/setting.py` - 新增設定模型
- `backend/app/models/time_entry.py` - 新增工時記錄模型
- `backend/app/models/work_template.py` - 新增工作範本模型
- `backend/tests/unit/test_models.py` - 新增 270+ 行測試程式碼

### 📝 備註
- 資料庫架構完整：6 個表格，適當的關聯與索引
- 外鍵約束正確定義
- 必要的唯一約束
- 常查詢欄位建立索引（date, project_id）
- **下一階段**：Pydantic Schemas 與 API 端點

**Git Commit:** `c027af1` - Complete all 6 database models with TDD (30 tests passing, 82% coverage)

---

## [2025-11-14] - 實作前 3 個資料庫模型（TDD）

### ✅ 已完成

**TDD Cycle 1 完成：**
- ✅ Red: 撰寫 Project, AccountGroup, WorkCategory 測試
- ✅ Green: 實作全部 3 個模型
- ✅ Refactor: 優化程式碼結構

**模型實作（3/6）：**
1. **Project** - 專案模型（9 個測試）
2. **AccountGroup** - 帳組模型（3 個測試）
3. **WorkCategory** - 工作類別模型（5 個測試）

### 📊 測試成果
- **測試數量**：17 個測試通過
- **覆蓋率**：約 75%
- **TDD 狀態**：Red → Green → Refactor ✅

### 🔑 關鍵業務規則驗證
- ✅ 專案代碼唯一性
- ✅ 帳組 (code, name) 組合唯一性
- ✅ 工作類別扣抵核定工時邏輯

### 📁 變更檔案
- `backend/app/models/project.py` - 新增專案模型
- `backend/app/models/account_group.py` - 新增帳組模型
- `backend/app/models/work_category.py` - 新增工作類別模型
- `backend/tests/unit/test_models.py` - 新增模型測試（部分）

**Git Commit:** `c655ce3` - Implement first 3 database models with TDD (Red-Green cycle)

---

## [2025-11-14] - 初始化後端專案與 TDD/BDD 框架

### ✅ 已完成

**專案結構：**
- 建立完整的 backend 目錄結構
- 配置 pytest 與 pytest-bdd 測試框架
- 創建 5 個 Gherkin feature 檔案
- 設定基礎配置檔案（config.py, database.py）

**測試框架：**
- pytest.ini 配置完成
- conftest.py fixture 設定
- 測試目錄結構：features/, step_defs/, unit/, integration/

**Gherkin Feature 檔案（5 個）：**
1. `work_hours.feature` - 每日工時記錄與驗證
2. `overtime.feature` - 加班工時計算
3. `approved_hours.feature` - 專案核定工時追蹤與扣抵
4. `project_management.feature` - 專案與需求單管理
5. `tcs_sync.feature` - TCS 格式化輸出

### 📊 測試成果
- 測試框架配置完成
- 可執行 `pytest --collect-only` 收集測試

### 📁 變更檔案
- `backend/app/config.py` - 應用配置
- `backend/app/database.py` - 資料庫連接設定
- `backend/app/main.py` - FastAPI 應用入口
- `backend/tests/conftest.py` - pytest fixtures
- `backend/tests/features/*.feature` - 5 個 Gherkin feature 檔案
- `backend/requirements.txt` - Python 依賴套件
- `backend/pytest.ini` - pytest 配置

### 📝 備註
- 測試驅動開發 (TDD) 流程已建立
- 行為驅動開發 (BDD) 規格已定義
- 下一步：實作資料庫模型

**Git Commit:** `56ede96` - Initialize backend project with TDD/BDD framework

---

## [2025-11-14] - 新增 TDD/BDD 開發標準與 Gherkin 業務邏輯規格 (v1.5)

### ✅ 已完成

**重大變更：新增開發規範與測試驅動開發流程**

1. **測試驅動開發 (TDD)**
   - 所有功能開發前必須先撰寫測試
   - Red-Green-Refactor 循環

2. **行為驅動開發 (BDD)**
   - 使用 Gherkin 語言描述業務邏輯

3. **測試框架設定**
   - 後端：pytest + pytest-bdd + pytest-cov（目標覆蓋率 80%）
   - 前端：Vitest + @vue/test-utils

4. **業務邏輯規格（Gherkin）**
   - Feature 1: 每日工時記錄與驗證（5 個場景）
   - Feature 2: 加班工時計算（3 個場景，含 Scenario Outline）
   - Feature 3: 專案核定工時追蹤與扣抵（5 個場景）
   - Feature 4: 專案與需求單管理（4 個場景）
   - Feature 5: TCS 格式化輸出（1 個場景）

5. **測試目錄結構**
   - features/：Gherkin feature 檔案
   - step_defs/：Step definitions
   - unit/：單元測試
   - integration/：整合測試

6. **測試要求**
   - 所有 API 端點必須有整合測試
   - 所有業務邏輯必須有 Gherkin 規格
   - 所有 Service 層必須有單元測試
   - 測試覆蓋率達 80% 以上

### 📁 變更檔案
- `plan.md` - 新增開發規範章節
- `plan.md` - 新增 Gherkin 業務邏輯規格（5 個 Features）

### 📝 備註
- 這是重要的開發標準設定，所有後續開發必須遵循
- 提供清晰的 BDD 規格，作為開發與驗證依據

---

## 更早的變更

詳見 `plan.md` 的「變更歷史」章節：
- 2025-11-14 - v1.4：核定工時追蹤與扣抵機制
- 2025-11-14 - v1.3：新增需求單代碼欄位
- 2025-11-14 - v1.2：明確加班計算規則
- 2025-11-14 - v1.1：工作日與時區業務規則
- 2025-11-14 - v1.0：初版計劃

---

**下次更新提醒：完成新功能後請在此檔案頂部新增記錄！**
