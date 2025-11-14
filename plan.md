# 專案管理系統 - 開發計劃

## 專案概述

一個適合個人使用的公司內部專案管理工具，提供專案追蹤、任務管理、進度監控等功能。本地運行，無需網路連接，支援中英文雙語介面。

## 技術棧

### 前端
- **框架**: Vue 3 (Composition API)
- **UI 框架**: Element Plus / Ant Design Vue (待確認)
- **狀態管理**: Pinia
- **路由**: Vue Router
- **HTTP 客戶端**: Axios
- **構建工具**: Vite
- **國際化**: Vue I18n

### 後端
- **框架**: FastAPI
- **ORM**: SQLAlchemy
- **資料庫**: SQLite
- **資料驗證**: Pydantic
- **CORS**: FastAPI CORS Middleware

### 開發工具
- **API 文檔**: Swagger UI (FastAPI 自動生成)
- **代碼格式化**:
  - 前端: ESLint + Prettier
  - 後端: Black + isort
- **版本控制**: Git

## 核心功能規劃

### 1. 專案管理模組

#### 1.1 專案 CRUD
- 創建專案（名稱、描述、開始/結束日期）
- 查看專案列表（卡片視圖、列表視圖）
- 編輯專案資訊
- 刪除專案（軟刪除，可恢復）
- 專案歸檔功能

#### 1.2 專案屬性
- 專案狀態：規劃中、進行中、已暫停、已完成、已取消
- 優先級：低、中、高、緊急
- 專案類型/分類（自定義標籤）
- 進度百分比（自動計算或手動設定）
- 預算管理（可選）

### 2. 任務管理模組

#### 2.1 任務 CRUD
- 創建任務（標題、描述、所屬專案）
- 任務列表查看（看板視圖、列表視圖）
- 編輯任務
- 刪除任務

#### 2.2 任務屬性
- 任務狀態：待辦、進行中、測試中、已完成、已取消
- 優先級：低、中、高、緊急
- 截止日期
- 預估工時 vs 實際工時
- 任務標籤（多標籤支援）

#### 2.3 子任務支援
- 任務可包含多個子任務
- 子任務完成度影響父任務進度
- 最多支援 2-3 層嵌套

#### 2.4 任務依賴關係（可選，Phase 2）
- 設定任務之間的依賴關係
- 前置任務完成後才能開始後續任務

### 3. 時程規劃模組

#### 3.1 里程碑管理
- 創建里程碑（名稱、日期、所屬專案）
- 里程碑完成狀態
- 里程碑與任務關聯

#### 3.2 視圖功能
- 日曆視圖（顯示任務、里程碑、截止日期）
- 時間軸視圖（專案進度展示）
- 甘特圖（簡化版，Phase 2）

### 4. 儀表板模組

#### 4.1 總覽統計
- 進行中的專案數量
- 待完成任務數量
- 本週到期任務
- 逾期任務提醒

#### 4.2 數據視覺化
- 專案狀態分佈（圓餅圖）
- 任務完成趨勢（折線圖）
- 優先級分佈
- 每月完成任務統計

#### 4.3 快速操作
- 快速創建任務
- 快速創建專案
- 最近訪問的專案

### 5. 資源管理模組

#### 5.1 文件管理
- 上傳附件（與專案/任務關聯）
- 支援常見文件格式（文檔、圖片、PDF 等）
- 檔案大小限制（建議 10MB）
- 檔案預覽（圖片）
- 下載功能

#### 5.2 連結管理
- 保存相關連結（文檔、參考資料等）
- 連結分類

#### 5.3 標籤系統
- 自定義標籤
- 標籤顏色
- 標籤統計

### 6. 搜尋與篩選

#### 6.1 全局搜尋
- 搜尋專案（名稱、描述）
- 搜尋任務（標題、描述）
- 搜尋標籤

#### 6.2 進階篩選
- 按狀態篩選
- 按優先級篩選
- 按日期範圍篩選
- 按標籤篩選
- 組合篩選

### 7. 活動記錄

#### 7.1 歷史記錄
- 記錄所有變更（創建、更新、刪除）
- 時間戳記
- 變更內容詳情

#### 7.2 活動時間軸
- 專案活動時間軸
- 任務活動時間軸

### 8. 設定模組

#### 8.1 系統設定
- 語言切換（中文/英文）
- 主題設定（淺色/深色）
- 預設視圖設定

#### 8.2 資料管理
- 匯出資料（JSON/CSV）
- 匯入資料
- 資料備份
- 清理歸檔資料

### 9. 報表功能（Phase 2）

#### 9.1 報表生成
- 專案完成報告
- 任務統計報告
- 時間追蹤報告

#### 9.2 匯出格式
- PDF
- Excel/CSV
- 列印友好格式

## 資料庫設計

### 主要資料表

#### 1. projects (專案表)
```
- id: INTEGER PRIMARY KEY
- name: VARCHAR(200) NOT NULL
- description: TEXT
- status: VARCHAR(50)
- priority: VARCHAR(20)
- start_date: DATE
- end_date: DATE
- progress: INTEGER (0-100)
- budget: DECIMAL(10,2)
- color: VARCHAR(7) (HEX color)
- is_archived: BOOLEAN
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
- deleted_at: TIMESTAMP (軟刪除)
```

#### 2. tasks (任務表)
```
- id: INTEGER PRIMARY KEY
- project_id: INTEGER FOREIGN KEY
- parent_task_id: INTEGER FOREIGN KEY (子任務)
- title: VARCHAR(200) NOT NULL
- description: TEXT
- status: VARCHAR(50)
- priority: VARCHAR(20)
- due_date: DATE
- estimated_hours: DECIMAL(5,2)
- actual_hours: DECIMAL(5,2)
- progress: INTEGER (0-100)
- order: INTEGER (排序)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
- deleted_at: TIMESTAMP
```

#### 3. milestones (里程碑表)
```
- id: INTEGER PRIMARY KEY
- project_id: INTEGER FOREIGN KEY
- name: VARCHAR(200) NOT NULL
- description: TEXT
- due_date: DATE
- is_completed: BOOLEAN
- completed_at: TIMESTAMP
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

#### 4. tags (標籤表)
```
- id: INTEGER PRIMARY KEY
- name: VARCHAR(50) NOT NULL UNIQUE
- color: VARCHAR(7)
- created_at: TIMESTAMP
```

#### 5. project_tags (專案標籤關聯表)
```
- id: INTEGER PRIMARY KEY
- project_id: INTEGER FOREIGN KEY
- tag_id: INTEGER FOREIGN KEY
- created_at: TIMESTAMP
```

#### 6. task_tags (任務標籤關聯表)
```
- id: INTEGER PRIMARY KEY
- task_id: INTEGER FOREIGN KEY
- tag_id: INTEGER FOREIGN KEY
- created_at: TIMESTAMP
```

#### 7. attachments (附件表)
```
- id: INTEGER PRIMARY KEY
- entity_type: VARCHAR(20) (project/task)
- entity_id: INTEGER
- filename: VARCHAR(255)
- original_filename: VARCHAR(255)
- file_path: VARCHAR(500)
- file_size: INTEGER (bytes)
- mime_type: VARCHAR(100)
- created_at: TIMESTAMP
```

#### 8. links (連結表)
```
- id: INTEGER PRIMARY KEY
- entity_type: VARCHAR(20)
- entity_id: INTEGER
- title: VARCHAR(200)
- url: VARCHAR(500)
- description: TEXT
- created_at: TIMESTAMP
```

#### 9. activity_logs (活動記錄表)
```
- id: INTEGER PRIMARY KEY
- entity_type: VARCHAR(20)
- entity_id: INTEGER
- action: VARCHAR(50) (created/updated/deleted)
- changes: JSON (記錄變更內容)
- created_at: TIMESTAMP
```

#### 10. settings (系統設定表)
```
- id: INTEGER PRIMARY KEY
- key: VARCHAR(100) UNIQUE
- value: TEXT
- updated_at: TIMESTAMP
```

### 資料表關係
- projects 1:N tasks
- projects 1:N milestones
- tasks 1:N tasks (子任務)
- projects N:M tags (through project_tags)
- tasks N:M tags (through task_tags)
- projects/tasks 1:N attachments
- projects/tasks 1:N links
- projects/tasks 1:N activity_logs

## API 設計

### RESTful API 端點

#### 專案 API
```
GET    /api/projects              - 獲取專案列表（支援篩選、排序、分頁）
POST   /api/projects              - 創建新專案
GET    /api/projects/{id}         - 獲取專案詳情
PUT    /api/projects/{id}         - 更新專案
DELETE /api/projects/{id}         - 刪除專案（軟刪除）
PATCH  /api/projects/{id}/archive - 歸檔/取消歸檔專案
GET    /api/projects/{id}/tasks   - 獲取專案下的所有任務
GET    /api/projects/{id}/stats   - 獲取專案統計資訊
```

#### 任務 API
```
GET    /api/tasks                 - 獲取任務列表
POST   /api/tasks                 - 創建新任務
GET    /api/tasks/{id}            - 獲取任務詳情
PUT    /api/tasks/{id}            - 更新任務
DELETE /api/tasks/{id}            - 刪除任務
GET    /api/tasks/{id}/subtasks   - 獲取子任務
PATCH  /api/tasks/{id}/status     - 更新任務狀態
```

#### 里程碑 API
```
GET    /api/milestones            - 獲取里程碑列表
POST   /api/milestones            - 創建里程碑
GET    /api/milestones/{id}       - 獲取里程碑詳情
PUT    /api/milestones/{id}       - 更新里程碑
DELETE /api/milestones/{id}       - 刪除里程碑
PATCH  /api/milestones/{id}/complete - 標記里程碑完成
```

#### 標籤 API
```
GET    /api/tags                  - 獲取所有標籤
POST   /api/tags                  - 創建標籤
PUT    /api/tags/{id}             - 更新標籤
DELETE /api/tags/{id}             - 刪除標籤
```

#### 附件 API
```
POST   /api/attachments           - 上傳附件
GET    /api/attachments/{id}      - 下載附件
DELETE /api/attachments/{id}      - 刪除附件
GET    /api/{entity_type}/{id}/attachments - 獲取實體的附件列表
```

#### 連結 API
```
GET    /api/links                 - 獲取連結列表
POST   /api/links                 - 創建連結
PUT    /api/links/{id}            - 更新連結
DELETE /api/links/{id}            - 刪除連結
```

#### 儀表板 API
```
GET    /api/dashboard/stats       - 獲取儀表板統計資訊
GET    /api/dashboard/recent      - 獲取最近活動
GET    /api/dashboard/upcoming    - 獲取即將到期的任務
```

#### 搜尋 API
```
GET    /api/search                - 全局搜尋
GET    /api/search/projects       - 搜尋專案
GET    /api/search/tasks          - 搜尋任務
```

#### 活動記錄 API
```
GET    /api/activities            - 獲取活動記錄
GET    /api/{entity_type}/{id}/activities - 獲取特定實體的活動記錄
```

#### 設定 API
```
GET    /api/settings              - 獲取系統設定
PUT    /api/settings              - 更新設定
POST   /api/export                - 匯出資料
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

#### 列表響應（含分頁）
```json
{
  "success": true,
  "data": {
    "items": [ ... ],
    "total": 100,
    "page": 1,
    "page_size": 20
  }
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
│   ├── assets/          # 靜態資源（圖片、字體等）
│   ├── components/      # 可複用組件
│   │   ├── common/      # 通用組件（Button、Modal、Card 等）
│   │   ├── project/     # 專案相關組件
│   │   ├── task/        # 任務相關組件
│   │   └── dashboard/   # 儀表板組件
│   ├── views/           # 頁面視圖
│   │   ├── Dashboard.vue
│   │   ├── Projects/
│   │   │   ├── ProjectList.vue
│   │   │   ├── ProjectDetail.vue
│   │   │   └── ProjectCreate.vue
│   │   ├── Tasks/
│   │   │   ├── TaskList.vue
│   │   │   ├── TaskBoard.vue
│   │   │   └── TaskDetail.vue
│   │   ├── Calendar.vue
│   │   └── Settings.vue
│   ├── router/          # 路由配置
│   │   └── index.js
│   ├── stores/          # Pinia stores
│   │   ├── project.js
│   │   ├── task.js
│   │   ├── tag.js
│   │   ├── dashboard.js
│   │   └── app.js
│   ├── api/             # API 請求封裝
│   │   ├── client.js    # Axios 實例
│   │   ├── project.js
│   │   ├── task.js
│   │   └── ...
│   ├── i18n/            # 國際化
│   │   ├── index.js
│   │   ├── zh-TW.json
│   │   └── en-US.json
│   ├── utils/           # 工具函數
│   │   ├── date.js
│   │   ├── format.js
│   │   └── validators.js
│   ├── styles/          # 全局樣式
│   │   ├── variables.scss
│   │   ├── mixins.scss
│   │   └── global.scss
│   ├── App.vue
│   └── main.js
├── public/
├── package.json
├── vite.config.js
└── README.md
```

### 主要頁面

1. **儀表板 (Dashboard)**
   - 統計卡片
   - 快速操作
   - 最近專案
   - 待辦任務列表
   - 圖表視覺化

2. **專案列表 (Project List)**
   - 卡片視圖 / 列表視圖切換
   - 篩選與搜尋
   - 排序功能
   - 創建新專案

3. **專案詳情 (Project Detail)**
   - 專案資訊展示與編輯
   - 任務列表（看板/列表視圖）
   - 里程碑時間軸
   - 附件與連結
   - 活動記錄

4. **任務看板 (Task Board)**
   - 拖拽式看板（待辦、進行中、已完成）
   - 任務卡片
   - 快速編輯

5. **日曆視圖 (Calendar)**
   - 月曆視圖
   - 顯示任務、里程碑
   - 點擊日期創建任務

6. **設定頁面 (Settings)**
   - 語言切換
   - 主題切換
   - 資料備份/匯出
   - 標籤管理

### 狀態管理

使用 Pinia 管理全局狀態：
- `projectStore`: 專案資料與操作
- `taskStore`: 任務資料與操作
- `tagStore`: 標籤資料
- `dashboardStore`: 儀表板統計資訊
- `appStore`: 應用設定（語言、主題等）

### 組件設計原則

1. **原子化設計**：從小組件組合成大組件
2. **可複用性**：通用組件獨立於業務邏輯
3. **Props 向下，Events 向上**：遵循 Vue 資料流
4. **組合式 API**：使用 Composition API 提高程式碼可維護性

## 後端架構

### 目錄結構
```
backend/
├── app/
│   ├── main.py              # FastAPI 應用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 資料庫連接與會話
│   ├── models/              # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── task.py
│   │   ├── milestone.py
│   │   ├── tag.py
│   │   ├── attachment.py
│   │   ├── link.py
│   │   ├── activity_log.py
│   │   └── setting.py
│   ├── schemas/             # Pydantic schemas（請求/響應模型）
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── task.py
│   │   ├── milestone.py
│   │   └── ...
│   ├── api/                 # API 路由
│   │   ├── __init__.py
│   │   ├── deps.py          # 依賴注入
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── projects.py
│   │   │   ├── tasks.py
│   │   │   ├── milestones.py
│   │   │   ├── tags.py
│   │   │   ├── attachments.py
│   │   │   ├── dashboard.py
│   │   │   ├── search.py
│   │   │   └── settings.py
│   ├── services/            # 業務邏輯層
│   │   ├── __init__.py
│   │   ├── project_service.py
│   │   ├── task_service.py
│   │   └── ...
│   ├── repositories/        # 資料訪問層（可選）
│   │   └── ...
│   ├── utils/               # 工具函數
│   │   ├── __init__.py
│   │   ├── datetime.py
│   │   └── file.py
│   └── middleware/          # 中間件
│       └── error_handler.py
├── uploads/                 # 上傳文件存儲
├── data/                    # SQLite 資料庫文件
│   └── app.db
├── tests/                   # 測試
├── requirements.txt
├── .env.example
└── README.md
```

### 分層架構

1. **路由層 (API Routes)**
   - 定義 API 端點
   - 請求驗證
   - 響應格式化

2. **服務層 (Services)**
   - 業務邏輯處理
   - 資料驗證
   - 跨資料表操作

3. **模型層 (Models)**
   - SQLAlchemy ORM 模型
   - 資料庫表映射

4. **Schema 層 (Schemas)**
   - Pydantic 資料驗證
   - 請求/響應序列化

### 關鍵設計

1. **資料庫連接管理**
   - 使用 SQLAlchemy 連接池
   - 每個請求獨立的資料庫會話

2. **錯誤處理**
   - 統一的錯誤響應格式
   - 自定義異常類別
   - 全局異常處理器

3. **檔案上傳**
   - 檔案大小限制
   - 檔案類型驗證
   - 安全的檔名處理
   - 儲存在本地 uploads/ 目錄

4. **活動記錄**
   - 使用裝飾器或中間件自動記錄
   - 記錄變更前後的資料

## 開發階段規劃

### Phase 1: 基礎架構與核心功能 (週 1-2)

#### 後端
- [x] 專案結構建立
- [ ] FastAPI 基礎設定
- [ ] SQLAlchemy 模型定義
- [ ] 資料庫初始化與遷移
- [ ] 基礎 API 端點
  - [ ] 專案 CRUD
  - [ ] 任務 CRUD
  - [ ] 標籤 CRUD

#### 前端
- [ ] Vue 3 專案建立（Vite）
- [ ] 安裝 UI 框架與基礎套件
- [ ] 路由設定
- [ ] Pinia stores 建立
- [ ] API 客戶端封裝
- [ ] 基礎 Layout 與導航

### Phase 2: 功能實作 (週 3-5)

#### 專案與任務管理
- [ ] 專案列表頁面（卡片/列表視圖）
- [ ] 專案創建/編輯表單
- [ ] 專案詳情頁面
- [ ] 任務列表與看板視圖
- [ ] 任務創建/編輯功能
- [ ] 任務拖拽功能
- [ ] 子任務支援

#### 里程碑與時程
- [ ] 里程碑 API 與前端
- [ ] 日曆視圖
- [ ] 時間軸展示

#### 標籤與篩選
- [ ] 標籤管理介面
- [ ] 標籤選擇器組件
- [ ] 進階篩選功能
- [ ] 全局搜尋

### Phase 3: 進階功能 (週 6-7)

#### 儀表板與統計
- [ ] 儀表板 API
- [ ] 統計卡片組件
- [ ] 圖表整合（Chart.js 或 ECharts）
- [ ] 資料視覺化

#### 資源管理
- [ ] 檔案上傳 API
- [ ] 附件管理介面
- [ ] 連結管理功能
- [ ] 圖片預覽

#### 活動記錄
- [ ] 活動記錄 API
- [ ] 時間軸組件
- [ ] 活動篩選與搜尋

### Phase 4: 優化與完善 (週 8-9)

#### 國際化
- [ ] i18n 設定與配置
- [ ] 中文翻譯
- [ ] 英文翻譯
- [ ] 語言切換功能

#### UI/UX 優化
- [ ] 深色模式支援
- [ ] 響應式設計優化
- [ ] 載入狀態與錯誤處理
- [ ] 確認對話框
- [ ] 通知提示（Toast）

#### 資料管理
- [ ] 資料匯出功能（JSON/CSV）
- [ ] 資料匯入功能
- [ ] 資料備份
- [ ] 軟刪除與恢復功能

### Phase 5: 測試與部署 (週 10)

#### 測試
- [ ] 後端 API 測試
- [ ] 前端單元測試（可選）
- [ ] E2E 測試（可選）
- [ ] 手動測試與 Bug 修復

#### 文檔
- [ ] API 文檔（Swagger）
- [ ] 使用者文檔
- [ ] 部署指南
- [ ] README 更新

#### 部署準備
- [ ] Docker 配置（可選）
- [ ] 啟動腳本
- [ ] 環境變數設定
- [ ] 本地安裝指南

## 未來擴展功能（Phase 6+）

以下功能可在基礎系統完成後逐步添加：

### 1. 進階圖表
- 甘特圖（使用 Gantt Chart 庫）
- 燃盡圖
- 工時統計圖

### 2. 任務依賴
- 任務依賴關係設定
- 關鍵路徑分析

### 3. 自動化
- 任務自動分配規則
- 狀態自動轉換
- 定期提醒通知

### 4. 報表功能
- PDF 報表生成
- Excel 匯出
- 自定義報表範本

### 5. 協作功能（如需多人使用）
- 用戶管理
- 權限控制
- 評論與討論
- 通知系統

### 6. 整合功能
- Git 整合（顯示 commit）
- 日曆同步（Google Calendar）
- Webhook 支援

### 7. 行動優化
- PWA 支援
- 行動裝置優化

## 技術考量

### 效能優化
- 前端：虛擬滾動（大量資料列表）
- 後端：查詢優化、索引建立
- 圖片壓縮與快取
- 延遲載入

### 資料安全
- 定期自動備份
- 軟刪除機制
- 資料驗證與清理
- SQL 注入防護（SQLAlchemy ORM）

### 程式碼品質
- ESLint + Prettier（前端）
- Black + isort（後端）
- 類型提示（Python Type Hints）
- 程式碼註解與文檔

### 錯誤處理
- 前端：全局錯誤處理、API 錯誤提示
- 後端：異常捕獲、日誌記錄
- 友善的錯誤訊息

## 開發環境需求

### 必需軟體
- Node.js 18+ 與 npm/pnpm
- Python 3.10+
- Git

### 推薦 IDE/編輯器
- VS Code（推薦插件：Volar、Python、ESLint、Prettier）
- PyCharm（後端）
- WebStorm（前端）

## 專案里程碑

| 階段 | 目標 | 預計時間 |
|------|------|----------|
| Phase 1 | 完成基礎架構與核心 CRUD | 週 1-2 |
| Phase 2 | 完成主要功能模組 | 週 3-5 |
| Phase 3 | 完成進階功能 | 週 6-7 |
| Phase 4 | 優化與完善 | 週 8-9 |
| Phase 5 | 測試與部署 | 週 10 |
| Phase 6+ | 未來擴展功能 | 待定 |

## 下一步行動

在開始開發之前，請確認：

1. ✅ 功能需求是否完整且符合預期？
2. ✅ 技術棧選擇是否合適？
3. ✅ 是否需要調整或補充任何功能？
4. ✅ 開發時程是否合理？

確認無誤後，即可開始 **Phase 1: 基礎架構與核心功能** 的開發！

---

*本計劃書最後更新：2025-11-14*
