# TCS 工時記錄系統

TCS 工時記錄系統 - 前端與後端整合開發環境

## 快速開始

### 一鍵啟動（推薦）

使用根目錄的 `package.json` 可以同時啟動前端和後端：

```bash
# 1. 安裝根目錄依賴（只需要執行一次）
npm install

# 2. 確保前端依賴已安裝
cd frontend && npm install && cd ..

# 3. 確保後端依賴已安裝（使用 uv 或 pip）
cd backend
# 使用 uv（推薦）
uv pip install -r requirements.txt
# 或使用 pip
# pip install -r requirements.txt
cd ..

# 4. 同時啟動前端和後端
npm run dev
```

啟動後：
- 前端: http://localhost:5173
- 後端: http://localhost:8000
- 後端 API 文檔: http://localhost:8000/docs

### 分別啟動

如果需要分別啟動：

**後端：**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**前端：**
```bash
cd frontend
npm run dev
```

## 專案結構

```
.
├── backend/          # FastAPI 後端
├── frontend/         # Vue 3 前端
└── package.json      # 合併啟動腳本
```

## 開發腳本

- `npm run dev` - 同時啟動前端和後端
- `npm run dev:backend` - 只啟動後端
- `npm run dev:frontend` - 只啟動前端
- `npm run install:all` - 安裝所有依賴（前端和根目錄）
- `npm run build` - 構建前端生產版本

## 詳細文檔

- [後端文檔](backend/README.md)
- [前端文檔](frontend/README.md)
