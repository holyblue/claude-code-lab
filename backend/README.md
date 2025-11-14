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

待實作後會列出所有可用的 API 端點。

## 開發進度

### Phase 1: 基礎架構 (Week 1)
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
- [ ] API 端點 (0/10+)
- [ ] 業務邏輯層 (0/5)
- [ ] TCS 同步功能

### 測試狀態
- ✅ 單元測試：50/50 通過 (30 模型 + 20 Schema)
- ✅ 模型測試覆蓋率：89-95%
- ✅ Schema 測試覆蓋率：97-100%
- ⚠️ 總體覆蓋率：49% (目標 80%，API 實作後會提升)
- 📝 BDD 測試：待實作 step definitions

## 參考文件

- [FastAPI 官方文檔](https://fastapi.tiangolo.com/)
- [SQLAlchemy 官方文檔](https://docs.sqlalchemy.org/)
- [pytest-bdd 官方文檔](https://pytest-bdd.readthedocs.io/)
- [Gherkin 語法參考](https://cucumber.io/docs/gherkin/reference/)
