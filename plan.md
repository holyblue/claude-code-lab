# 工時記錄系統 - 開發計劃

## 專案概述

一個以**工時記錄為核心**的個人工具，主要用於追蹤每日工時並同步到公司內部 TCS 系統。本地運行，無需網路連接，支援中英文雙語介面。

### 核心目標
- 快速記錄每日工時（專案、類別、時數、說明）
- 便於整理和查詢工時資料
- 簡化填入 TCS 系統的流程（初期複製貼上，後期自動化）

## 技術棧

### 前端
- **框架**: Vue 3 (Composition API)
- **UI 框架**: Element Plus
- **狀態管理**: Pinia
- **路由**: Vue Router
- **HTTP 客戶端**: Axios
- **構建工具**: Vite
- **國際化**: Vue I18n
- **Markdown 支援**: marked.js 或 markdown-it

### 後端
- **框架**: FastAPI
- **ORM**: SQLAlchemy
- **資料庫**: SQLite
- **資料驗證**: Pydantic
- **CORS**: FastAPI CORS Middleware

### 自動化工具（Phase 2）
- **瀏覽器自動化**: Playwright

### 開發工具
- **API 文檔**: Swagger UI (FastAPI 自動生成)
- **代碼格式化**:
  - 前端: ESLint + Prettier
  - 後端: Black + isort
- **版本控制**: Git

## 核心功能規劃

### 1. 專案管理模組（簡化版）

#### 1.1 專案 CRUD
- 創建專案（專案代碼、名稱、預設帳組、預設工作類別）
- 查看專案列表（列表視圖、搜尋）
- 編輯專案資訊
- 刪除專案（軟刪除）
- 歸檔專案（已完成的專案）

#### 1.2 專案屬性
- 專案代碼（必填，如：需2025單001）
- 專案名稱（必填）
- 預設帳組（選填，可從固定清單選擇）
- 預設工作類別（選填，可從固定清單選擇）
- 備註說明
- 狀態（進行中/已完成/已歸檔）
- 顏色標籤（用於視覺化區分）

### 2. 工時記錄模組（核心功能）

#### 2.1 工時記錄 CRUD
- 創建工時記錄
- 查看工時記錄（按日期、專案篩選）
- 編輯工時記錄
- 刪除工時記錄
- 複製工時記錄（快速創建相似記錄）

#### 2.2 工時記錄屬性
- 日期（必填）
- 專案（必填，從專案清單選擇，自動帶入預設帳組和工作類別）
- 帳組（必填，可修改）
- 工作類別（必填，可修改）
- 實際工時（必填，數字，如：1.5、4、2）
- 工作說明（必填，支援 Markdown 格式）
- 帳項選擇（選填，文字輸入）

#### 2.3 快速操作
- 快速新增工時（當日日期預設）
- 從範本創建（常做的工作可儲存為範本）
- 批次編輯（修改多筆記錄的日期或專案）
- 檢查每日工時總和（提示是否達到標準工時 7.5 小時）

### 3. 每日工時視圖

#### 3.1 當日工時清單
- 顯示選定日期的所有工時記錄
- 顯示當日工時總和
- 快速編輯（inline editing）
- 拖曳排序
- 一鍵清除全部

#### 3.2 日期導航
- 日期選擇器
- 前一天/後一天快速切換
- 快速跳到今天

#### 3.3 工時驗證
- 檢查當日工時總和是否符合標準（7.5 小時）
- 提示遺漏欄位
- 提示重複記錄

### 4. 日曆視圖

#### 4.1 月曆展示
- 顯示每日工時總和
- 以顏色標示工時狀態：
  - 綠色：工時 = 7.5 小時
  - 黃色：工時不足 7.5 小時
  - 紅色：尚未填寫工時
  - 灰色：週末/假日
- 點擊日期查看/編輯當日工時

#### 4.2 假日管理（可選）
- 標記 DAYOFF（休假、病假、事假等）
- 自動填入休假工時記錄

### 5. 統計與報表模組

#### 5.1 工時統計
- 本週工時總計（週一至週日）
- 本月工時總計
- 按專案統計（顯示各專案累計工時）
- 按工作類別統計
- 自訂日期範圍統計

#### 5.2 視覺化圖表
- 專案工時分佈（圓餅圖）
- 每週工時趨勢（折線圖）
- 工作類別分佈（長條圖）

#### 5.3 匯出功能
- 匯出為 CSV（方便用 Excel 處理）
- 匯出為 JSON（備份用）
- 複製到剪貼簿（格式化文字，方便貼到其他地方）

### 6. TCS 同步功能

#### 6.1 Phase 1: 半自動（複製貼上）

**功能：格式化輸出**
- 選擇日期範圍（如：本週、上週、本月）
- 按 TCS 格式排列資料：
  ```
  日期: 2025/11/12
  專案名稱: 需2025單001
  帳組: A00 中概全權
  工作類別: A07 其它
  實際工時: 1.5
  工作說明:
  - [x] 控股A1發展月會

  ---

  專案名稱: 需2025單002
  帳組: O18 數據智能應用科
  工作類別: B04 其它
  實際工時: 4
  工作說明:
  - [x] 串音頻檔導案業務
  - [x] 會談紀錄標寫與儲存
  - [x] SRS及WBS填案
  ```

**操作方式：**
1. 點擊「複製 TCS 格式」按鈕
2. 系統自動格式化並複製到剪貼簿
3. 手動貼到 TCS 系統對應欄位
4. 檢查並送出

#### 6.2 Phase 2: 全自動（Playwright）

**功能：自動填寫表單**
- 使用 Playwright 自動開啟 TCS 系統
- 自動填寫各欄位：
  - 日期選擇
  - 專案名稱（使用搜尋選擇器）
  - 帳組（使用搜尋選擇器）
  - 工作類別（使用搜尋選擇器）
  - 實際工時
  - 工作說明
- 多筆記錄自動依序填入
- 填寫完成後暫停，等待人工檢查
- 提供「送出」按鈕選項（需人工確認）

**技術考量：**
- TCS 系統需在內網可訪問
- 需要分析 TCS 表單的 HTML 結構（元素選擇器）
- 處理下拉選單、搜尋框等互動元素
- 錯誤處理（網路斷線、元素找不到等）

### 7. 基礎資料管理

#### 7.1 帳組管理
- 預設帳組清單（固定選項）：
  - A00 中概全權
  - O18 數據智能應用科
  - （其他可新增）
- 新增、編輯、刪除帳組
- 設定常用帳組

#### 7.2 工作類別管理
- 預設工作類別清單（固定選項）：
  - A07 其它
  - B04 其它
  - I07 休假（休假、病假、事假等）
  - （其他可新增）
- 新增、編輯、刪除工作類別
- 設定常用工作類別

#### 7.3 工作範本管理（可選）
- 儲存常做的工作為範本
- 範本內容：專案、帳組、工作類別、預設工時、工作說明
- 快速套用範本創建工時記錄

### 8. 設定模組

#### 8.1 系統設定
- 語言切換（中文/英文）
- 主題設定（淺色/深色模式）
- 預設工作時數（預設 7.5）
- 週末顯示/隱藏

#### 8.2 資料管理
- 匯出全部資料（JSON/CSV）
- 匯入資料
- 清除所有資料（需確認）
- 資料庫備份

#### 8.3 TCS 設定（Phase 2）
- TCS 網址設定
- 登入憑證管理（安全儲存）
- 自動化腳本設定

## 資料庫設計

### 主要資料表

#### 1. projects (專案表)
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) NOT NULL UNIQUE,          -- 專案代碼（如：需2025單001）
    name VARCHAR(200) NOT NULL,                -- 專案名稱
    default_account_group_id INTEGER,          -- 預設帳組 FK
    default_work_category_id INTEGER,          -- 預設工作類別 FK
    description TEXT,                          -- 備註
    status VARCHAR(20) DEFAULT 'active',       -- active/completed/archived
    color VARCHAR(7) DEFAULT '#409EFF',        -- 顏色標籤
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,                      -- 軟刪除
    FOREIGN KEY (default_account_group_id) REFERENCES account_groups(id),
    FOREIGN KEY (default_work_category_id) REFERENCES work_categories(id)
);
```

#### 2. account_groups (帳組表)
```sql
CREATE TABLE account_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) NOT NULL,                 -- 帳組代碼（如：A00）
    name VARCHAR(200) NOT NULL,                -- 帳組名稱（如：中概全權）
    full_name VARCHAR(250) GENERATED ALWAYS AS (code || ' ' || name) STORED,
    is_default BOOLEAN DEFAULT FALSE,          -- 是否為常用
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(code, name)
);
```

#### 3. work_categories (工作類別表)
```sql
CREATE TABLE work_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) NOT NULL,                 -- 類別代碼（如：A07）
    name VARCHAR(200) NOT NULL,                -- 類別名稱（如：其它）
    full_name VARCHAR(250) GENERATED ALWAYS AS (code || ' ' || name) STORED,
    is_default BOOLEAN DEFAULT FALSE,          -- 是否為常用
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(code, name)
);
```

#### 4. time_entries (工時記錄表)
```sql
CREATE TABLE time_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,                        -- 日期
    project_id INTEGER NOT NULL,               -- 專案 FK
    account_group_id INTEGER NOT NULL,         -- 帳組 FK
    work_category_id INTEGER NOT NULL,         -- 工作類別 FK
    hours DECIMAL(5,2) NOT NULL,               -- 實際工時
    description TEXT NOT NULL,                 -- 工作說明（支援 Markdown）
    account_item VARCHAR(200),                 -- 帳項選擇
    display_order INTEGER DEFAULT 0,           -- 排序
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (account_group_id) REFERENCES account_groups(id),
    FOREIGN KEY (work_category_id) REFERENCES work_categories(id)
);

CREATE INDEX idx_time_entries_date ON time_entries(date);
CREATE INDEX idx_time_entries_project ON time_entries(project_id);
```

#### 5. work_templates (工作範本表，可選)
```sql
CREATE TABLE work_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,                -- 範本名稱
    project_id INTEGER,                        -- 專案 FK
    account_group_id INTEGER,                  -- 帳組 FK
    work_category_id INTEGER,                  -- 工作類別 FK
    default_hours DECIMAL(5,2),                -- 預設工時
    description_template TEXT,                 -- 工作說明範本
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (account_group_id) REFERENCES account_groups(id),
    FOREIGN KEY (work_category_id) REFERENCES work_categories(id)
);
```

#### 6. settings (系統設定表)
```sql
CREATE TABLE settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 初始資料

系統啟動時自動插入常用的帳組和工作類別：

```sql
-- 帳組
INSERT INTO account_groups (code, name, is_default) VALUES
('A00', '中概全權', TRUE),
('O18', '數據智能應用科', TRUE);

-- 工作類別
INSERT INTO work_categories (code, name, is_default) VALUES
('A07', '其它', TRUE),
('B04', '其它', TRUE),
('I07', '休假（休假、病假、事假等）', TRUE);

-- 系統設定
INSERT INTO settings (key, value) VALUES
('language', 'zh-TW'),
('theme', 'light'),
('standard_work_hours', '7.5'),
('show_weekends', 'true');
```

## API 設計

### RESTful API 端點

#### 專案 API
```
GET    /api/projects              - 獲取專案列表（支援搜尋、篩選）
POST   /api/projects              - 創建新專案
GET    /api/projects/{id}         - 獲取專案詳情
PUT    /api/projects/{id}         - 更新專案
DELETE /api/projects/{id}         - 刪除專案（軟刪除）
PATCH  /api/projects/{id}/archive - 歸檔/取消歸檔專案
GET    /api/projects/{id}/stats   - 獲取專案工時統計
```

#### 工時記錄 API
```
GET    /api/time-entries          - 獲取工時記錄列表（支援日期範圍、專案篩選）
POST   /api/time-entries          - 創建新工時記錄
GET    /api/time-entries/{id}     - 獲取工時記錄詳情
PUT    /api/time-entries/{id}     - 更新工時記錄
DELETE /api/time-entries/{id}     - 刪除工時記錄
POST   /api/time-entries/{id}/duplicate - 複製工時記錄

GET    /api/time-entries/by-date  - 按日期獲取工時記錄
                                    ?date=2025-11-12
GET    /api/time-entries/daily-summary - 獲取每日工時總和
                                         ?start_date=2025-11-01&end_date=2025-11-30
POST   /api/time-entries/batch    - 批次更新工時記錄
```

#### 帳組 API
```
GET    /api/account-groups        - 獲取所有帳組
POST   /api/account-groups        - 創建新帳組
PUT    /api/account-groups/{id}   - 更新帳組
DELETE /api/account-groups/{id}   - 刪除帳組
```

#### 工作類別 API
```
GET    /api/work-categories       - 獲取所有工作類別
POST   /api/work-categories       - 創建新工作類別
PUT    /api/work-categories/{id}  - 更新工作類別
DELETE /api/work-categories/{id}  - 刪除工作類別
```

#### 工作範本 API（可選）
```
GET    /api/templates             - 獲取所有範本
POST   /api/templates             - 創建新範本
PUT    /api/templates/{id}        - 更新範本
DELETE /api/templates/{id}        - 刪除範本
POST   /api/templates/{id}/apply  - 套用範本創建工時記錄
```

#### 統計 API
```
GET    /api/stats/overview        - 總覽統計（本週、本月工時）
GET    /api/stats/by-project      - 按專案統計
                                    ?start_date=2025-11-01&end_date=2025-11-30
GET    /api/stats/by-category     - 按工作類別統計
GET    /api/stats/calendar        - 日曆資料（每日工時總和）
                                    ?year=2025&month=11
```

#### TCS 同步 API
```
POST   /api/tcs/format            - 格式化工時資料為 TCS 格式
                                    body: { start_date, end_date }
POST   /api/tcs/auto-fill         - 自動填寫 TCS（Phase 2）
                                    body: { date, time_entry_ids[] }
```

#### 設定 API
```
GET    /api/settings              - 獲取所有設定
PUT    /api/settings              - 更新設定
POST   /api/export                - 匯出資料（JSON/CSV）
POST   /api/import                - 匯入資料
```

### API 響應格式

#### 成功響應
```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功"
}
```

#### 錯誤響應
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "錯誤訊息",
    "details": { ... }
  }
}
```

## 前端架構

### 目錄結構
```
frontend/
├── src/
│   ├── assets/              # 靜態資源
│   ├── components/          # 可複用組件
│   │   ├── common/          # 通用組件
│   │   │   ├── DatePicker.vue
│   │   │   ├── MarkdownEditor.vue
│   │   │   └── ConfirmDialog.vue
│   │   ├── project/         # 專案相關組件
│   │   │   ├── ProjectSelect.vue
│   │   │   ├── ProjectForm.vue
│   │   │   └── ProjectList.vue
│   │   └── time-entry/      # 工時記錄組件
│   │       ├── TimeEntryForm.vue
│   │       ├── TimeEntryList.vue
│   │       ├── TimeEntryCard.vue
│   │       └── DailySummary.vue
│   ├── views/               # 頁面視圖
│   │   ├── Dashboard.vue            # 儀表板（工時總覽）
│   │   ├── DailyEntry.vue           # 每日工時記錄
│   │   ├── Calendar.vue             # 日曆視圖
│   │   ├── Projects.vue             # 專案管理
│   │   ├── Statistics.vue           # 統計報表
│   │   ├── TCSSync.vue              # TCS 同步
│   │   └── Settings.vue             # 設定
│   ├── router/              # 路由配置
│   │   └── index.js
│   ├── stores/              # Pinia stores
│   │   ├── project.js
│   │   ├── timeEntry.js
│   │   ├── accountGroup.js
│   │   ├── workCategory.js
│   │   ├── stats.js
│   │   └── app.js
│   ├── api/                 # API 請求封裝
│   │   ├── client.js
│   │   ├── project.js
│   │   ├── timeEntry.js
│   │   ├── stats.js
│   │   └── tcs.js
│   ├── i18n/                # 國際化
│   │   ├── index.js
│   │   ├── zh-TW.json
│   │   └── en-US.json
│   ├── utils/               # 工具函數
│   │   ├── date.js          # 日期處理
│   │   ├── format.js        # 格式化工具
│   │   ├── validators.js    # 驗證函數
│   │   └── markdown.js      # Markdown 處理
│   ├── styles/              # 全局樣式
│   ├── App.vue
│   └── main.js
├── package.json
├── vite.config.js
└── README.md
```

### 主要頁面

#### 1. 儀表板 (Dashboard)
- 本週工時總計（進度條顯示）
- 本月工時總計
- 快速操作：新增今日工時
- 最近使用的專案
- 本週工時趨勢圖
- 專案工時分佈圖

#### 2. 每日工時記錄 (DailyEntry)
- 日期選擇（預設今天）
- 當日工時記錄列表（可拖曳排序）
- 當日工時總和（顯示是否達到 7.5 小時）
- 快速新增按鈕
- Inline 編輯功能
- 複製記錄功能

#### 3. 日曆視圖 (Calendar)
- 月曆展示
- 每日工時總和
- 顏色標示（綠/黃/紅/灰）
- 點擊日期跳轉到每日工時記錄

#### 4. 專案管理 (Projects)
- 專案列表（搜尋、篩選）
- 新增/編輯專案表單
- 專案工時統計
- 歸檔專案管理

#### 5. 統計報表 (Statistics)
- 日期範圍選擇
- 專案工時統計表
- 工作類別統計表
- 視覺化圖表
- 匯出功能

#### 6. TCS 同步 (TCSSync)
- Phase 1: 複製格式化資料
  - 日期範圍選擇
  - 預覽格式化結果
  - 複製到剪貼簿
- Phase 2: 自動填寫（未來）
  - TCS 連線設定
  - 自動填寫按鈕
  - 執行日誌

#### 7. 設定 (Settings)
- 系統設定（語言、主題、工時標準）
- 帳組管理
- 工作類別管理
- 工作範本管理
- 資料管理（匯出/匯入/備份）
- TCS 設定（Phase 2）

## 後端架構

### 目錄結構
```
backend/
├── app/
│   ├── main.py                  # FastAPI 應用入口
│   ├── config.py                # 配置管理
│   ├── database.py              # 資料庫連接
│   ├── models/                  # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── account_group.py
│   │   ├── work_category.py
│   │   ├── time_entry.py
│   │   ├── work_template.py
│   │   └── setting.py
│   ├── schemas/                 # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── account_group.py
│   │   ├── work_category.py
│   │   ├── time_entry.py
│   │   ├── stats.py
│   │   └── tcs.py
│   ├── api/                     # API 路由
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── projects.py
│   │       ├── time_entries.py
│   │       ├── account_groups.py
│   │       ├── work_categories.py
│   │       ├── templates.py
│   │       ├── stats.py
│   │       ├── tcs.py
│   │       └── settings.py
│   ├── services/                # 業務邏輯層
│   │   ├── __init__.py
│   │   ├── project_service.py
│   │   ├── time_entry_service.py
│   │   ├── stats_service.py
│   │   └── tcs_service.py       # TCS 同步邏輯
│   ├── utils/                   # 工具函數
│   │   ├── __init__.py
│   │   ├── datetime.py
│   │   └── format.py
│   └── middleware/
│       └── error_handler.py
├── playwright/                  # Playwright 腳本（Phase 2）
│   ├── tcs_auto_fill.py
│   └── selectors.json          # TCS 元素選擇器配置
├── data/
│   └── app.db                  # SQLite 資料庫
├── requirements.txt
├── .env.example
└── README.md
```

### TCS 同步服務設計（Phase 2）

#### Playwright 腳本架構
```python
# playwright/tcs_auto_fill.py
from playwright.sync_api import sync_playwright

class TCSAutoFiller:
    def __init__(self, tcs_url, selectors_config):
        self.tcs_url = tcs_url
        self.selectors = selectors_config

    def login(self, username, password):
        """登入 TCS 系統"""
        pass

    def fill_time_entry(self, entry_data):
        """填寫單筆工時記錄"""
        # 1. 選擇日期
        # 2. 點擊專案搜尋器，輸入專案代碼
        # 3. 點擊帳組搜尋器，選擇帳組
        # 4. 點擊工作類別搜尋器，選擇類別
        # 5. 輸入實際工時
        # 6. 輸入工作說明
        pass

    def fill_multiple_entries(self, entries):
        """批次填寫多筆工時記錄"""
        pass

    def verify_and_submit(self):
        """驗證並送出（需人工確認）"""
        pass
```

#### 元素選擇器配置
```json
// playwright/selectors.json
{
  "date_picker": "#date-input",
  "project_search": "input[name='project']",
  "project_dropdown": ".project-dropdown",
  "account_group_search": "input[name='account_group']",
  "work_category_search": "input[name='work_category']",
  "hours_input": "input[name='hours']",
  "description_textarea": "textarea[name='description']",
  "submit_button": "button[type='submit']"
}
```

## 開發階段規劃

### Phase 1: 基礎功能與手動同步（4-5 週）

#### Week 1: 後端基礎架構
- [x] 專案結構建立
- [ ] FastAPI 基礎設定
- [ ] SQLAlchemy 模型定義（6 個表）
- [ ] 資料庫初始化與遷移
- [ ] 初始資料插入（帳組、工作類別）
- [ ] 基礎 API 端點（CRUD）

#### Week 2: 前端基礎架構
- [ ] Vue 3 + Vite 專案建立
- [ ] 安裝 Element Plus 與基礎套件
- [ ] 路由設定（7 個主要頁面）
- [ ] Pinia stores 建立
- [ ] API 客戶端封裝
- [ ] 基礎 Layout 與導航選單

#### Week 3: 核心功能 - 專案與工時記錄
- [ ] 專案管理頁面
  - [ ] 專案列表（搜尋、篩選）
  - [ ] 新增/編輯專案表單
  - [ ] 專案刪除與歸檔
- [ ] 每日工時記錄頁面
  - [ ] 工時記錄表單（支援 Markdown）
  - [ ] 當日工時列表
  - [ ] Inline 編輯
  - [ ] 拖曳排序
  - [ ] 工時總和計算

#### Week 4: 日曆與統計
- [ ] 日曆視圖
  - [ ] 月曆組件
  - [ ] 每日工時顯示
  - [ ] 顏色標示
  - [ ] 點擊日期跳轉
- [ ] 統計報表頁面
  - [ ] 日期範圍選擇
  - [ ] 專案/類別統計表
  - [ ] 圖表視覺化（ECharts）
  - [ ] 匯出功能（CSV/JSON）

#### Week 5: TCS 同步（半自動）與完善
- [ ] TCS 同步頁面
  - [ ] 格式化輸出功能
  - [ ] 複製到剪貼簿
  - [ ] 預覽格式化結果
- [ ] 設定頁面
  - [ ] 帳組管理
  - [ ] 工作類別管理
  - [ ] 系統設定
  - [ ] 資料管理
- [ ] 國際化（中英文）
- [ ] UI/UX 優化
- [ ] 錯誤處理與驗證

### Phase 2: 自動化同步（2-3 週，未來擴展）

#### Week 6-7: Playwright 整合
- [ ] Playwright 環境建置
- [ ] TCS 頁面元素分析
- [ ] 自動填寫腳本開發
  - [ ] 登入功能
  - [ ] 表單填寫
  - [ ] 多筆記錄處理
- [ ] 錯誤處理與重試機制
- [ ] 執行日誌與反饋

#### Week 8: 測試與優化
- [ ] 功能測試
- [ ] 自動化腳本調試
- [ ] 效能優化
- [ ] 文檔撰寫

## 技術考量

### 資料安全
- 定期自動備份 SQLite 資料庫
- 軟刪除機制（可恢復誤刪資料）
- 資料驗證與清理
- TCS 登入憑證加密儲存（Phase 2）

### 使用者體驗
- 響應式設計（支援不同螢幕尺寸）
- 快捷鍵支援（如：Ctrl+S 儲存）
- 自動儲存草稿（避免資料遺失）
- 載入狀態提示
- 友善的錯誤訊息

### 效能優化
- 資料庫索引（date, project_id）
- 前端虛擬滾動（大量記錄）
- API 分頁（避免一次載入過多資料）
- 快取機制（專案、帳組、類別清單）

### 程式碼品質
- 類型提示（TypeScript for Vue, Python Type Hints）
- 程式碼格式化（ESLint + Prettier, Black + isort）
- 程式碼註解與文檔
- 單元測試（可選）

## 未來擴展功能

### Phase 3+（依需求增加）
- [ ] 工作範本系統（快速套用常用工作）
- [ ] 批次操作（批次修改日期、專案等）
- [ ] 進階圖表（燃盡圖、工時趨勢）
- [ ] 多人協作（如果需要）
- [ ] 手機 App 或 PWA
- [ ] 與其他系統整合（如 Slack 通知）
- [ ] AI 輔助（自動分類工作、預測工時）

## 開發環境需求

### 必需軟體
- Node.js 18+ 與 npm/pnpm
- Python 3.10+
- Git

### 推薦 IDE
- VS Code（推薦插件：Volar、Python、ESLint、Prettier）

## 專案里程碑

| 階段 | 目標 | 預計時間 |
|------|------|----------|
| Phase 1 | 完成核心功能與半自動 TCS 同步 | 週 1-5 |
| Phase 2 | 完成 Playwright 自動化同步 | 週 6-8 |
| Phase 3+ | 未來擴展功能 | 依需求 |

## 下一步行動

確認此計劃符合您的需求後，即可開始 **Phase 1: 基礎功能開發**！

主要變更：
1. ✅ 聚焦於**工時記錄**核心功能
2. ✅ 移除複雜的任務管理、里程碑、甘特圖等
3. ✅ 專案簡化為工時記錄的輔助資料
4. ✅ 新增 TCS 同步功能（Phase 1 半自動，Phase 2 全自動）
5. ✅ 支援 Markdown 工作說明
6. ✅ 每日最多 6 筆記錄的設計
7. ✅ 工時總和驗證（標準 7.5 小時）

---

*本計劃書最後更新：2025-11-14*
