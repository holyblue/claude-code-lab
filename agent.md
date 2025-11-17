# AI Agent 開發規範

本文件定義 AI 開發助手在本專案中的執行規範和流程。

## 核心原則

### 1. 測試驅動開發 (TDD)
所有功能開發必須遵循 Red-Green-Refactor 循環：
1. **Red** - 先寫測試，確認測試失敗
2. **Green** - 實作功能，讓測試通過
3. **Refactor** - 重構程式碼，確保測試仍然通過

### 2. 行為驅動開發 (BDD)
核心業務邏輯必須用 Gherkin 語言描述（見 `plan.md`）

### 3. 測試覆蓋率要求
- 目標：最低 80% 覆蓋率
- 執行：`pytest --cov=app --cov-report=html`

### 4. 依賴管理 ⚡
- **工具**: uv (10-100x faster than pip)
- **虛擬環境**: `.venv/` (使用 `uv venv` 創建)
- **安裝依賴**: `uv pip install -r requirements.txt`
- **運行命令**: `source .venv/bin/activate` 或 `uv run <command>`

## 執行條件與檢查點

### ✅ 每次完成新功能後必須執行

#### 1. 運行所有測試
```bash
pytest -v
```
- 確保所有測試通過
- 檢查測試覆蓋率是否達標（≥80%）

#### 2. 程式碼品質檢查
```bash
black app/ tests/          # 格式化
isort app/ tests/          # import 排序
flake8 app/ tests/         # 程式碼檢查
```

#### 3. 更新 CHANGELOG.md（必須）

**格式範例：**
```markdown
## [日期] - 功能名稱

### ✅ 已完成
- 實作內容 1（檔案路徑）
- 實作內容 2（測試數量、覆蓋率）

### 📊 測試成果
- 測試數量：X 個測試通過
- 覆蓋率：XX%
- TDD 狀態：Red → Green → Refactor ✅

### 🔑 關鍵業務規則驗證
- 業務規則 1
- 業務規則 2

### 📁 變更檔案
- `app/models/xxx.py` - 新增模型
- `tests/unit/test_xxx.py` - 新增測試
- `app/api/endpoints/xxx.py` - 新增 API 端點

### 📝 備註
- 相關說明或需要注意的事項
```

#### 4. Git 提交規範

**提交訊息格式：**
```
<type>: <簡短描述>

<詳細說明>
- 詳細點 1
- 詳細點 2

測試狀態：X 個測試通過，覆蓋率 XX%
```

**Type 類型：**
- `feat`: 新功能
- `fix`: Bug 修復
- `test`: 新增或修改測試
- `refactor`: 重構
- `docs`: 文件更新
- `chore`: 建置或輔助工具變動

**範例：**
```
feat: Complete all 6 database models with TDD

TDD Cycle 2 Completed:
✅ Red: Write tests for TimeEntry, WorkTemplate, Setting
✅ Green: Implement all 3 models
✅ Total: 30 tests passing, 82% coverage

Models Implemented (6/6):
- Project, AccountGroup, WorkCategory
- TimeEntry, WorkTemplate, Setting

測試狀態：30 個測試通過，覆蓋率 82%
```

## 開發流程檢查清單

### 🔄 開始新功能前
- [ ] 閱讀 `plan.md` 確認需求
- [ ] 檢查相關 Gherkin feature 檔案
- [ ] 確認測試環境正常（`pytest --collect-only`）

### 🚀 實作過程中
- [ ] 先寫測試（Red）
- [ ] 實作功能（Green）
- [ ] 執行測試確認通過
- [ ] 重構優化（Refactor）
- [ ] 再次執行測試確認

### ✅ 完成功能後（強制執行）
1. [ ] 執行所有測試：`pytest -v`
2. [ ] 檢查覆蓋率：`pytest --cov=app --cov-report=term`
3. [ ] 程式碼格式化：`black app/ tests/`
4. [ ] Import 排序：`isort app/ tests/`
5. [ ] 程式碼檢查：`flake8 app/ tests/`
6. [ ] **更新 CHANGELOG.md**（必須）
7. [ ] Git commit（使用規範格式）
8. [ ] 如果是重大功能，更新 `README.md` 或 `plan.md`

## CHANGELOG.md 編寫規則

### 🎯 核心原則
**每次完成重要功能後，必須立即更新 CHANGELOG.md**

CHANGELOG.md 是專案的開發日誌，記錄所有重要變更。新的記錄必須**加在檔案最上方**（在格式說明之後），保持時間倒序排列。

### 📋 必須記錄的資訊

#### 1. 標題格式
```markdown
## [日期] - Phase X 完成：簡短描述
```
**範例：**
- `## [2025-11-14] - Phase 2 完成：BDD Step Definitions 實作與測試覆蓋率提升`
- `## [2025-11-14] - Phase 1 完成：API 端點與業務邏輯層`

#### 2. 已完成內容（✅ 已完成）
**必須包含：**
- 功能分類清單（用數字編號）
- 每個功能的完成狀態（用 ✅ 標記）
- BDD 場景數量（例如：5/5 場景 ✅）
- 測試修復記錄（例如：0/11 → 32/32）

**範例：**
```markdown
### ✅ 已完成

**BDD Step Definitions 實作（10/11 測試通過）：**

1. **Approved Hours Tracking 核定工時追蹤（5/5 場景 ✅）**
   - ✅ A07 其它工作扣抵核定工時
   - ✅ A08 商模工作不扣抵核定工時
   - ✅ 混合工作類別計算

**測試修復與改進：**
- ✅ 修復整合測試資料庫初始化問題（0/11 → 32/32 通過）
- ✅ 新增 18 個整合測試
```

#### 3. 測試成果（📊 測試成果）
**必須包含：**
- 總測試數與成功率
- 測試分類統計（單元/整合/BDD）
- 覆蓋率百分比（標示是否達標）
- 覆蓋率分層細節（API/Service/Model/Schema）

**範例：**
```markdown
### 📊 測試成果

**總測試統計：**
- **總測試數**：93 個（92 通過，1 待修復）
- **成功率**：98.9%
- **覆蓋率**：89.97%（超過 80% 目標 ✅）

**測試分類：**
- 單元測試：50/50 通過 ✅
- 整合測試：32/32 通過 ✅
- BDD 測試：10/11 通過 ✅

**覆蓋率詳細：**
- API 端點層：88-100%
- Service 層：95-100%
```

#### 4. 關鍵業務規則驗證（🔑 關鍵業務規則驗證）
**必須列出：**
- 已驗證的業務邏輯（用 ✅ 標記）
- 關鍵計算規則（例如：使用率計算公式）
- 預警機制（例如：80% 橘色、100% 紅色）
- 資料完整性檢查

**範例：**
```markdown
### 🔑 關鍵業務規則驗證

**核定工時追蹤與扣抵：**
- ✅ 扣抵類別（A07 其它、B04 其它）正確減少核定工時
- ✅ 不扣抵類別（A08 商模、I07 休假）獨立追蹤
- ✅ 使用率計算準確（used_hours / approved_hours * 100）
- ✅ 預警機制：80% 橘色警告、100% 紅色危險
```

#### 5. 變更檔案（📁 變更檔案）
**分為兩類：**
- **新增檔案**：列出完整路徑與行數
- **修改檔案**：說明修改內容

**範例：**
```markdown
### 📁 變更檔案

**新增檔案：**
- `backend/tests/step_defs/test_approved_hours.py` - 核定工時 BDD（290 行）
- `backend/tests/step_defs/test_work_hours.py` - 每日工時 BDD（240 行）

**修改檔案：**
- `backend/tests/conftest.py` - 新增 `db` fixture 別名、BDD marker
- `backend/tests/integration/test_api.py` - 完整重寫（14 → 32 測試）
```

#### 6. 技術亮點（📝 技術亮點）
**記錄：**
- 重要的技術實作技巧
- 問題與解決方案
- 最佳實踐
- 已知問題與替代方案

**範例：**
```markdown
### 📝 技術亮點

**pytest-bdd 實作技巧：**
- 使用 `target_fixture` 在 Given/When 步驟間傳遞資料
- 實作 regex parser 處理整數匹配

**已知問題與解決方案：**
- ❌ 問題：pytest-bdd DocString 多行文字解析失敗
- ✅ 替代方案：TCS 服務已透過 32 個整合測試完整驗證
```

#### 7. Phase 完成度（🎯 Phase X 完成度）
**必須包含：**
- 已完成項目清單（用 ✅）
- 待完成項目（用 ⏸️ 或 📋）
- Git commit hash 記錄

**範例：**
```markdown
### 🎯 Phase 2 完成度：95%

**已完成：**
- ✅ 修復整合測試（0/11 → 32/32）
- ✅ 提升測試覆蓋率（44% → 89.97%）
- ✅ 實作 BDD Step Definitions（10/11 場景）

**待完成：**
- ⏸️ TCS DocString 測試（已有整合測試覆蓋）
- 📋 下一階段：Frontend Vue.js 專案初始化

**Git Commit:**
- `96fe991` - test: Fix integration tests and boost coverage to 89.70%
- `56ec058` - feat: Implement BDD step definitions for business logic testing
```

### ⏰ 更新時機

**必須立即更新的情況：**
- ✅ 完成一個 Phase 的主要功能
- ✅ 完成一組相關功能（如完成所有 BDD step definitions）
- ✅ 完成 API 端點實作
- ✅ 完成整合測試修復
- ✅ 測試覆蓋率有重大提升（>5%）
- ✅ 修復重大 Bug

**可以合併更新的情況：**
- 完成多個小功能後一起記錄
- 完成一天的工作後整理記錄

**不需要記錄的情況：**
- ❌ 純粹的文件修改（除非是重大文件更新）
- ❌ 臨時性的測試或除錯程式碼
- ❌ 微小的格式調整
- ❌ 僅修改註釋

### 📝 編寫規範

#### 排序規則
**新記錄永遠加在最上方**（在格式說明之後），保持時間倒序排列：
```markdown
# Changelog

## 格式說明
...

---
## [2025-11-14] - Phase 2 完成  ← 最新記錄（在這裡）
...

---
## [2025-11-14] - Phase 1 完成  ← 較舊記錄
...
```

#### Emoji 使用規範
- ✅ 已完成
- 📊 測試成果
- 🔑 關鍵業務規則驗證
- 📁 變更檔案
- 📝 技術亮點/備註
- 🎯 Phase 完成度
- ⚠️ 警告/已知問題
- ⏸️ 暫停/待處理
- 📋 待辦事項

#### 數字格式
- 測試數量：`93 個（92 通過，1 待修復）`
- 覆蓋率：`89.97%（超過 80% 目標 ✅）`
- 進度：`10/11 場景 ✅` 或 `5/5 通過 ✅`
- 提升：`44% → 89.97%`（使用箭頭）

### ✅ 檢查清單

更新 CHANGELOG.md 前，確認以下項目：
- [ ] 記錄已加在檔案最上方（格式說明之後）
- [ ] 日期格式正確：`[2025-11-14]`
- [ ] 包含 Phase 編號和簡短描述
- [ ] 已完成內容有明確的數量和狀態
- [ ] 測試成果包含總數、分類、覆蓋率
- [ ] 有列出關鍵業務規則驗證
- [ ] 變更檔案分為新增和修改兩類
- [ ] Phase 完成度有百分比和 Git commit
- [ ] 使用正確的 emoji 標記
- [ ] 數字格式統一（使用箭頭表示提升）

## 進度追蹤機制

### 查看進度的方法
1. **查看 CHANGELOG.md** - 完整的開發歷史
2. **查看 Git log** - `git log --oneline -10`
3. **查看測試覆蓋率報告** - `pytest --cov=app --cov-report=html`
4. **查看 plan.md 的開發進度** - 核對已完成項目

### AI Agent 自我檢查
每次開始新任務前，AI Agent 應該：
1. 讀取 `CHANGELOG.md` 了解最新進度
2. 執行 `pytest --collect-only` 確認測試狀態
3. 檢查 `plan.md` 的待辦事項
4. 確認 Git 狀態：`git status`, `git log --oneline -5`

## 特殊情況處理

### 當測試失敗時
1. 不要提交程式碼
2. 檢查錯誤訊息
3. 修復問題
4. 重新執行測試
5. 確認全部通過後才提交

### 當覆蓋率下降時
1. 檢查哪些程式碼未被測試
2. 補充測試案例
3. 確保覆蓋率回到 80% 以上

### 當需要重構時
1. 確保現有測試全部通過
2. 進行重構
3. 執行測試確認功能未改變
4. 在 CHANGELOG.md 記錄重構內容

## 範例工作流程

### 範例：實作專案 CRUD API

#### Step 1: TDD Red（寫測試）
```bash
# 創建測試檔案
vim tests/integration/test_api_projects.py

# 運行測試（預期失敗）
pytest tests/integration/test_api_projects.py -v
```

#### Step 2: TDD Green（實作功能）
```bash
# 實作 API 端點
vim app/api/endpoints/projects.py
vim app/schemas/project.py

# 運行測試（預期通過）
pytest tests/integration/test_api_projects.py -v
```

#### Step 3: TDD Refactor（重構）
```bash
# 優化程式碼
vim app/api/endpoints/projects.py

# 確認測試仍然通過
pytest tests/integration/test_api_projects.py -v
```

#### Step 4: 完成檢查
```bash
# 執行所有測試
pytest -v

# 檢查覆蓋率
pytest --cov=app --cov-report=term

# 程式碼品質
black app/ tests/
isort app/ tests/
flake8 app/ tests/
```

#### Step 5: 更新 CHANGELOG.md
```markdown
## 2025-11-14 - 專案 CRUD API 實作

### ✅ 已完成
- 實作專案 CRUD API 端點（GET, POST, PUT, DELETE）
- 實作 Pydantic schemas（ProjectCreate, ProjectUpdate, ProjectResponse）
- 整合測試（15 個測試案例）

### 📊 測試成果
- 測試數量：45 個測試通過（+15）
- 覆蓋率：85%（+3%）
- TDD 狀態：Red → Green → Refactor ✅

### 🔑 關鍵業務規則驗證
- ✅ 專案代碼唯一性驗證
- ✅ 需求單代碼格式驗證（R + 年月日 + 流水號）
- ✅ 核定工時計算（人天 × 7.5 = 小時）

### 📁 變更檔案
- `app/api/endpoints/projects.py` - 新增 API 端點
- `app/schemas/project.py` - 新增 Pydantic schemas
- `tests/integration/test_api_projects.py` - 新增整合測試

### 📝 備註
- API 文件自動生成：http://localhost:8000/docs
- 支援軟刪除（deleted_at）
```

#### Step 6: Git 提交
```bash
git add .
git commit -m "feat: Implement project CRUD API with TDD

Completed:
- GET /api/projects (list & detail)
- POST /api/projects (create)
- PUT /api/projects/{id} (update)
- DELETE /api/projects/{id} (soft delete)

Testing:
- 15 integration tests (all passing)
- Coverage: 85% (+3%)
- TDD cycle: Red → Green → Refactor ✅"
```

## 總結

遵循以上規範可以確保：
1. ✅ 程式碼品質穩定
2. ✅ 測試覆蓋率達標
3. ✅ 開發進度可追蹤
4. ✅ 團隊協作順暢
5. ✅ 下次接手時能快速了解進度

**記住：每次完成新功能後，CHANGELOG.md 是必須更新的！**
