# 工時記錄系統 - 前端

基於 Vue 3 + TypeScript + Vite + Element Plus 的工時記錄系統前端應用。

## 技術棧

### 核心框架
- **Vue 3.5.24** - Composition API
- **TypeScript 5.9.3** - 類型安全
- **Vite 7.2.2** - 構建工具

### UI 框架
- **Element Plus 2.11.8** - UI 組件庫
- **@element-plus/icons-vue 2.3.2** - 圖標組件

### 狀態管理 & 路由
- **Pinia 3.0.4** - 狀態管理
- **Vue Router 4.6.3** - 路由管理

### HTTP & 國際化
- **Axios 1.13.2** - HTTP 客戶端
- **Vue I18n 11.1.12** - 國際化（中/英文）

### 開發工具
- **ESLint 9.39.1** - 代碼檢查
- **Prettier 3.6.2** - 代碼格式化
- **@typescript-eslint** - TypeScript 規則

## 專案結構

```
frontend/
├── src/
│   ├── api/              # API 客戶端
│   │   ├── client.ts     # Axios 封裝
│   │   ├── projects.ts   # 專案 API
│   │   ├── timeEntries.ts # 工時記錄 API
│   │   └── index.ts
│   ├── assets/           # 靜態資源
│   ├── components/       # 可重用組件
│   ├── composables/      # 組合式函數
│   ├── layouts/          # 布局組件
│   │   └── MainLayout.vue # 主布局
│   ├── locales/          # 國際化
│   │   ├── zh-TW.json    # 繁體中文
│   │   ├── en-US.json    # 英文
│   │   └── index.ts
│   ├── router/           # 路由配置
│   │   └── index.ts
│   ├── stores/           # Pinia 狀態管理
│   │   ├── project.ts    # 專案 store
│   │   ├── timeEntry.ts  # 工時記錄 store
│   │   └── index.ts
│   ├── types/            # TypeScript 類型定義
│   │   └── index.ts
│   ├── utils/            # 工具函數
│   ├── views/            # 頁面組件
│   │   ├── TimeEntries.vue  # 工時記錄
│   │   ├── Calendar.vue     # 日曆視圖
│   │   ├── Projects.vue     # 專案管理
│   │   ├── Statistics.vue   # 統計報表
│   │   └── Settings.vue     # 系統設定
│   ├── App.vue           # 根組件
│   └── main.ts           # 入口文件
├── .env                  # 環境變數
├── .prettierrc           # Prettier 配置
├── eslint.config.js      # ESLint 配置
├── vite.config.ts        # Vite 配置
├── tsconfig.json         # TypeScript 配置
└── package.json          # 依賴配置
```

## 快速開始

### 安裝依賴

```bash
npm install
```

### 開發模式

```bash
npm run dev
```

訪問 http://localhost:5173

### 構建生產版本

```bash
npm run build
```

### 預覽生產版本

```bash
npm run preview
```

### 代碼檢查

```bash
npm run lint
```

### 代碼格式化

```bash
npm run format
```

## 功能模組

### 1. 工時記錄 (Time Entries)
- 記錄每日工時
- 支援 Markdown 工作說明
- 快速輸入與編輯

### 2. 日曆視圖 (Calendar)
- 月曆視圖
- 顯示每日工時總計
- 點擊日期查看詳情

### 3. 專案管理 (Projects)
- 專案 CRUD 操作
- 核定工時追蹤
- 使用率預警

### 4. 統計報表 (Statistics)
- 專案工時統計
- 每日/週/月統計
- 圖表視覺化

### 5. 系統設定 (Settings)
- 語言切換（中文/英文）
- 主題切換（淺色/深色）
- 基礎資料管理

## 開發規範

### TypeScript
- 所有組件使用 `<script setup lang="ts">`
- API 響應使用類型定義
- 避免使用 `any` 類型

### 組件命名
- 組件文件使用 PascalCase（如：`TimeEntries.vue`）
- 組件名稱與文件名一致

### 代碼風格
- 使用 ESLint + Prettier 自動格式化
- 單引號、無分號
- 2 空格縮排

### Commit 規範
- `feat:` 新功能
- `fix:` 修復
- `docs:` 文檔
- `style:` 格式
- `refactor:` 重構
- `test:` 測試
- `chore:` 構建/工具

## API 配置

後端 API 地址配置在 `.env` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000
```

所有 API 請求會自動添加 `/api` 前綴並通過 Vite 代理轉發到後端。

## 狀態管理

使用 Pinia 管理全局狀態：

```typescript
import { useProjectStore } from '@/stores/project'

const projectStore = useProjectStore()
await projectStore.fetchProjects()
```

## 國際化

切換語言：

```typescript
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()
locale.value = 'zh-TW' // 或 'en-US'
```

## 瀏覽器支持

- Chrome >= 90
- Firefox >= 88
- Safari >= 14
- Edge >= 90

## 已知問題

無

## 下一步開發

- [ ] 實作工時記錄表單組件
- [ ] 實作專案管理完整功能
- [ ] 實作日曆視圖
- [ ] 實作統計報表與圖表
- [ ] 實作 TCS 格式化輸出
- [ ] 添加單元測試（Vitest）

## 授權

私有專案
