# Time Tracking System - Backend

FastAPI backend for the time tracking system.

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

### 1. 創建虛擬環境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 2. 安裝相依套件

```bash
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

- [x] 專案結構建立
- [x] 測試框架設定 (pytest + pytest-bdd)
- [x] 基礎配置 (config.py, database.py)
- [x] Gherkin feature 檔案 (5 個)
- [ ] 資料庫模型 (6 個表)
- [ ] Pydantic Schemas
- [ ] API 端點 (專案、工時記錄、統計等)
- [ ] 業務邏輯層
- [ ] TCS 同步功能

## 參考文件

- [FastAPI 官方文檔](https://fastapi.tiangolo.com/)
- [SQLAlchemy 官方文檔](https://docs.sqlalchemy.org/)
- [pytest-bdd 官方文檔](https://pytest-bdd.readthedocs.io/)
- [Gherkin 語法參考](https://cucumber.io/docs/gherkin/reference/)
