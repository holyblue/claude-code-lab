# Time Tracking System - Backend

FastAPI backend for the time tracking system.

## 技術棧

### 核心框架
- **Web 框架**: FastAPI 0.121.2 ⬆️
- **ASGI 伺服器**: Uvicorn 0.38.0 ⬆️ (with uvloop for high performance)
- **資料庫**: SQLite (via SQLAlchemy 2.0.44 ⬆️)
- **ORM**: SQLAlchemy 2.0.44 + aiosqlite 0.20.0 ⬆️
- **資料驗證**: Pydantic 2.12.4 ⬆️ + pydantic-settings 2.6.1 ⬆️

### 測試框架
- **測試執行**: pytest 7.4.4
- **BDD 測試**: pytest-bdd 7.0.1 (Gherkin support)
- **測試覆蓋率**: pytest-cov 6.0.0 ⬆️ (目標 ≥80%)
- **非同步測試**: pytest-asyncio 0.23.8 ⬆️
- **HTTP 測試**: httpx 0.28.1 ⬆️

### 程式碼品質
- **格式化**: black 25.11.0 ⬆️ (2025 stable style)
- **Import 排序**: isort 5.13.2
- **程式碼檢查**: flake8 7.1.1 ⬆️

### 工具函式庫
- **日期處理**: python-dateutil 2.8.2
- **時區支援**: pytz 2024.1
- **檔案上傳**: python-multipart 0.0.20 ⬆️
- **瀏覽器自動化**: Playwright 1.51.0 (用於 TCS 自動填寫)

### 依賴管理 ⚡
- **推薦**: **uv** (10-100x faster than pip)
- **備選**: pip + requirements.txt (傳統方式)

## 專案結構

```
backend/
├── app/
│   ├── models/          # SQLAlchemy 資料庫模型
│   ├── schemas/         # Pydantic 驗證模型
│   ├── api/             # API 端點
│   ├── services/        # 業務邏輯層
│   ├── utils/           # 工具函數
│   ├── config.py        # 配置管理
│   ├── database.py      # 資料庫連接
│   └── main.py          # FastAPI 應用入口
├── tests/
│   ├── features/        # Gherkin feature 檔案
│   ├── step_defs/       # BDD step definitions
│   ├── unit/            # 單元測試
│   ├── integration/     # 整合測試
│   └── conftest.py      # pytest 配置
├── data/                # SQLite 資料庫檔案
├── requirements.txt     # Python 套件依賴
├── pytest.ini           # pytest 配置
└── .env.example         # 環境變數範例

```

## 開發規範

### 測試驅動開發 (TDD)

**所有功能開發前必須先撰寫測試**

1. **Red** - 先寫測試，確認測試失敗
2. **Green** - 實作功能，讓測試通過
3. **Refactor** - 重構程式碼，確保測試仍然通過

### 測試類型

- **單元測試** (`tests/unit/`) - 測試單一函數或類別
- **整合測試** (`tests/integration/`) - 測試 API 端點
- **BDD 測試** (`tests/features/`) - 驗證業務邏輯（Gherkin）

## 安裝與設定

### 方法 1: 使用 uv（推薦 ⚡ 極速）

**為什麼選擇 uv？**
- ⚡ 速度：比 pip 快 10-100 倍
- 🎯 簡單：語法與 pip 完全相同
- 🔒 可靠：自動鎖定依賴版本

**安裝 uv：**
```bash
# 使用 pip 安裝 uv
pip install uv

# 或使用官方腳本（可能需要網絡權限）
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**設定專案：**
```bash
# 1. 創建虛擬環境（0.2 秒完成）
uv venv

# 2. 啟動虛擬環境
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. 安裝依賴（5 秒完成 50 個套件）
uv pip install -r requirements.txt
```

**效能數據：**
- 創建虛擬環境：0.2 秒 (vs pip: 2-3 秒)
- 安裝 50 個套件：5.2 秒 (vs pip: 30-60 秒)
- 速度提升：**6-12 倍** 🔥

### 方法 2: 使用傳統 pip

```bash
# 1. 創建虛擬環境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 2. 安裝相依套件
pip install -r requirements.txt
```

### 3. 配置環境變數

```bash
cp .env.example .env
# 編輯 .env 檔案根據需求調整設定
```

### 4. 運行測試

```bash
# 運行所有測試
pytest

# 運行單元測試
pytest tests/unit -m unit

# 運行整合測試
pytest tests/integration -m integration

# 運行 BDD 測試
pytest tests/features -m bdd

# 查看測試覆蓋率
pytest --cov=app --cov-report=html
```

### 5. 啟動開發伺服器

```bash
uvicorn app.main:app --reload --port 8000
```

API 文檔將在以下網址可用：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 程式碼品質

### 格式化程式碼

```bash
# Black - 程式碼格式化
black app/ tests/

# isort - import 排序
isort app/ tests/

# flake8 - 程式碼檢查
flake8 app/ tests/
```

## 資料庫

### 初始化資料庫

資料庫會在應用啟動時自動初始化。

### 查看資料庫

```bash
sqlite3 data/app.db
```

## API 端點

API 文檔可透過 Swagger UI 查看：啟動應用後訪問 `http://localhost:8000/docs`

### 已實作的 API 端點

**帳組管理 (Account Groups)**
- `POST /api/account-groups/` - 創建帳組
- `GET /api/account-groups/` - 列出所有帳組
- `GET /api/account-groups/{id}` - 獲取特定帳組
- `PATCH /api/account-groups/{id}` - 更新帳組
- `DELETE /api/account-groups/{id}` - 刪除帳組

**工作類別管理 (Work Categories)**
- `POST /api/work-categories/` - 創建工作類別
- `GET /api/work-categories/` - 列出所有工作類別
- `GET /api/work-categories/{id}` - 獲取特定工作類別
- `PATCH /api/work-categories/{id}` - 更新工作類別
- `DELETE /api/work-categories/{id}` - 刪除工作類別

**專案管理 (Projects)**
- `POST /api/projects/` - 創建專案
- `GET /api/projects/` - 列出專案（支援狀態篩選）
- `GET /api/projects/{id}` - 獲取特定專案
- `PATCH /api/projects/{id}` - 更新專案
- `DELETE /api/projects/{id}` - 軟刪除專案

**時間記錄管理 (Time Entries)**
- `POST /api/time-entries/` - 創建時間記錄
- `GET /api/time-entries/` - 列出時間記錄（支援日期範圍篩選）
- `GET /api/time-entries/{id}` - 獲取特定時間記錄
- `PATCH /api/time-entries/{id}` - 更新時間記錄
- `DELETE /api/time-entries/{id}` - 刪除時間記錄

**統計分析 (Statistics)**
- `GET /api/stats/projects/{id}` - 獲取專案統計（使用率、超支預警）
- `GET /api/stats/projects` - 獲取所有專案統計

**TCS 格式化與自動化 (TCS Format & Automation)**
- `POST /api/tcs/format` - 格式化單日時間記錄
- `POST /api/tcs/format/range` - 格式化日期範圍時間記錄
- `POST /api/tcs/auto-fill` - 自動填寫工時記錄到 TCS 系統（支援 dry_run）

## 開發進度

### Phase 1: 基礎架構 (Week 1) - ✅ 已完成
- [x] 專案結構建立
- [x] 測試框架設定 (pytest + pytest-bdd)
- [x] 基礎配置 (config.py, database.py)
- [x] Gherkin feature 檔案 (5 個)
- [x] **資料庫模型 (6/6 完成)** ✅
  - Project, AccountGroup, WorkCategory
  - TimeEntry, WorkTemplate, Setting
  - 30 個測試通過，模型覆蓋率 89-95%
- [x] **依賴管理工具升級** (pip → uv) ⚡
- [x] **Pydantic Schemas (6/6 完成)** ✅
  - AccountGroup, WorkCategory, Project
  - TimeEntry, Stats, TCS
  - 20 個測試通過，Schema 覆蓋率 97-100%
- [x] **API 端點 (6 組 CRUD 完成)** ✅
  - AccountGroup, WorkCategory, Project CRUD
  - TimeEntry CRUD + 日期範圍查詢
  - Stats API (專案統計、使用率追蹤)
  - TCS API (格式化輸出、單日/多日)
- [x] **業務邏輯層 (2/2 完成)** ✅
  - Stats Service: 專案工時統計、超支預警
  - TCS Service: 時間記錄格式化
- [x] TCS 格式化功能

### 測試狀態
- ✅ 單元測試：50/50 通過 (30 模型 + 20 Schema)
- ✅ 模型測試覆蓋率：89-95%
- ✅ Schema 測試覆蓋率：97-100%
- ⚠️ 整合測試：需修復（資料庫初始化問題）
- ⚠️ 總體覆蓋率：44% (API 層未被整合測試覆蓋)
- 📝 BDD 測試：待實作 step definitions

## TCS 自動化填寫功能 🤖

### 安裝 Playwright

```bash
# 安裝 Playwright
pip install playwright
# 或使用 uv (推薦)
uv pip install playwright

# 安裝瀏覽器驅動
playwright install chromium
```

### 使用方式

#### 1. API 方式（推薦用於前端整合）

```bash
# DRY RUN 模式（預設，安全）- 不會真正儲存
curl -X POST "http://localhost:8000/api/tcs/auto-fill" \
  -H "Content-Type: application/json" \
  -d '{"date": "2025-11-24"}'

# 真正寫入模式（需明確指定）
curl -X POST "http://localhost:8000/api/tcs/auto-fill" \
  -H "Content-Type: application/json" \
  -d '{"date": "2025-11-24", "dry_run": false}'
```

#### 2. 手動測試腳本

```bash
cd backend/tcs_automation

# 安全模式（預設，只預覽不儲存）
python test_manual.py --date 2025-11-24

# 真正寫入（需明確指定並確認）
python test_manual.py --date 2025-11-24 --no-dry-run
```

### ⚠️ 重要安全提示

1. **測試絕不碰真實 TCS 系統**
   - 所有自動化測試（pytest）完全使用 Mock
   - 不會啟動真實瀏覽器
   - 不會連接 TCS 系統

2. **預設保護機制**
   - API 預設 `dry_run=true`
   - 手動腳本預設 `dry_run=true`
   - 需明確關閉才會真正寫入

3. **測試執行**
   ```bash
   # 安全測試（使用 Mock）
   pytest tests/unit/test_tcs_automation.py -v
   pytest tests/integration/test_tcs_auto_fill.py -v
   
   # 只執行 mock 測試（推薦）
   pytest -m mock
   
   # 手動測試需明確指定（不推薦在 CI 中執行）
   pytest -m manual
   ```

### 功能說明

- **自動連接**: 使用 Windows 整合驗證自動登入 TCS
- **Frame 處理**: 自動切換到正確的 frame（mainFrame）
- **資料驗證**: 自動驗證專案代碼、模組、工作類別
- **AJAX 等待**: 自動等待欄位驗證完成
- **錯誤處理**: 捕捉並回報 TCS 系統錯誤訊息
- **工時限制**: 自動檢查總工時不超過 18 小時

### 詳細文檔

請參閱 [`tcs_automation/README.md`](./tcs_automation/README.md) 獲取更多詳細資訊。

## 參考文件

- [FastAPI 官方文檔](https://fastapi.tiangolo.com/)
- [SQLAlchemy 官方文檔](https://docs.sqlalchemy.org/)
- [pytest-bdd 官方文檔](https://pytest-bdd.readthedocs.io/)
- [Gherkin 語法參考](https://cucumber.io/docs/gherkin/reference/)
- [Playwright Python 文檔](https://playwright.dev/python/)
