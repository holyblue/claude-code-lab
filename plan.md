# 工時記錄系統 - 開發計劃

## 專案概述

一個以**工時記錄為核心**的個人工具，主要用於追蹤每日工時並同步到公司內部 TCS 系統。本地運行，無需網路連接，支援中英文雙語介面。

### 核心目標
- 快速記錄每日工時（專案、類別、時數、說明）
- 便於整理和查詢工時資料
- 簡化填入 TCS 系統的流程（初期複製貼上，後期自動化）

### 業務規則
- **工作日**：週一至週五（週末為週六、週日）
- **時區**：UTC+8（台灣/中國標準時間）
- **每日工時範圍**：
  - 標準工時：7.5 小時
  - 最多：12 小時（超過會有警告提示）
- **工時計算規則**：
  - **平日（週一至週五）**：
    - 工時 ≤ 7.5 小時：計為正常工時
    - 工時 > 7.5 小時：7.5 小時為正常工時，超過部分計為加班
    - 工時 > 12 小時：會有超時警告
  - **週末（週六、週日）**：
    - 所有工時計為加班
- **工時驗證**：
  - 工作日工時不足 7.5 小時會提示
  - 工時超過 12 小時會警告

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

## 開發規範

### 測試驅動開發 (TDD)

**核心原則：在開發前先寫測試**

所有功能開發必須遵循以下流程：

1. **先寫測試（Red）**
   - 根據需求撰寫測試案例（單元測試、整合測試）
   - 執行測試，確認測試失敗（因為功能尚未實作）

2. **實作功能（Green）**
   - 撰寫最少的程式碼讓測試通過
   - 確保所有測試都通過

3. **重構優化（Refactor）**
   - 優化程式碼結構和可讀性
   - 確保重構後測試仍然通過

### 行為驅動開發 (BDD)

**使用 Gherkin 語言描述業務邏輯**

- 所有核心業務邏輯必須用 Gherkin 語言（Given-When-Then）表述
- Feature 檔案作為可執行的規格文件
- 實作完成後，必須驗證是否符合 Gherkin 規格

### 測試框架

#### 後端測試
- **測試框架**: pytest
- **BDD 框架**: pytest-bdd（執行 Gherkin feature 檔案）
- **測試覆蓋率**: pytest-cov
- **目標覆蓋率**: 最低 80%

#### 前端測試
- **測試框架**: Vitest
- **組件測試**: @vue/test-utils
- **E2E 測試**: Playwright (可選)

### 測試目錄結構

```
backend/
├── tests/
│   ├── features/              # Gherkin feature 檔案（BDD）
│   │   ├── work_hours.feature
│   │   ├── overtime.feature
│   │   ├── approved_hours.feature
│   │   └── project_management.feature
│   ├── step_defs/             # Gherkin step definitions
│   │   ├── test_work_hours_steps.py
│   │   ├── test_overtime_steps.py
│   │   └── test_approved_hours_steps.py
│   ├── unit/                  # 單元測試
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_utils.py
│   ├── integration/           # 整合測試
│   │   ├── test_api_projects.py
│   │   ├── test_api_time_entries.py
│   │   └── test_api_stats.py
│   ├── conftest.py            # pytest 配置與 fixtures
│   └── pytest.ini

frontend/
├── tests/
│   ├── unit/                  # 組件單元測試
│   │   ├── components/
│   │   └── utils/
│   └── integration/           # 整合測試
```

### 測試要求

1. **所有 API 端點**必須有整合測試
2. **所有業務邏輯**必須有對應的 Gherkin feature 和 step definitions
3. **所有 Service 層**必須有單元測試
4. **關鍵組件**必須有前端組件測試
5. 測試覆蓋率須達到 80% 以上
6. CI/CD 流程中必須執行所有測試並通過

## 業務邏輯規格（Gherkin）

以下使用 Gherkin 語言定義核心業務邏輯，作為開發與驗證的依據。

### Feature 1: 每日工時驗證

**檔案**: `tests/features/work_hours.feature`

```gherkin
Feature: 每日工時記錄與驗證
  作為一個使用者
  我想要記錄每日工時
  以便追蹤我的工作時間並確保符合公司規範

  Background:
    Given 系統時區設定為 "UTC+8"
    And 標準工時設定為 7.5 小時
    And 最大工時設定為 12 小時

  # Scenario 1: 工作日標準工時
  Scenario: 工作日填寫標準 7.5 小時工時
    Given 今天是 "2025-11-12" (星期二，工作日)
    When 我記錄以下工時
      | 專案代碼    | 工時 |
      | 需2025單001 | 4.0  |
      | 需2025單002 | 3.5  |
    Then 當日工時總計應為 7.5 小時
    And 工時狀態應顯示為 "正常"
    And 正常工時應為 7.5 小時
    And 加班工時應為 0 小時

  # Scenario 2: 工作日不足 7.5 小時
  Scenario: 工作日工時不足 7.5 小時
    Given 今天是 "2025-11-13" (星期三，工作日)
    When 我記錄以下工時
      | 專案代碼    | 工時 |
      | 需2025單001 | 3.0  |
      | 需2025單002 | 2.0  |
    Then 當日工時總計應為 5.0 小時
    And 工時狀態應顯示為 "不足"
    And 應該顯示黃色警告
    And 警告訊息應為 "工時不足 7.5 小時"

  # Scenario 3: 工作日加班（7.5-12 小時）
  Scenario: 工作日加班 1.5 小時（總計 9 小時）
    Given 今天是 "2025-11-14" (星期四，工作日)
    When 我記錄以下工時
      | 專案代碼    | 工時 |
      | 需2025單001 | 5.0  |
      | 需2025單002 | 4.0  |
    Then 當日工時總計應為 9.0 小時
    And 工時狀態應顯示為 "正常+加班"
    And 正常工時應為 7.5 小時
    And 加班工時應為 1.5 小時
    And 應該顯示綠色狀態並標示加班時數

  # Scenario 4: 工作日超時（>12 小時）
  Scenario: 工作日工時超過 12 小時
    Given 今天是 "2025-11-15" (星期五，工作日)
    When 我記錄以下工時
      | 專案代碼    | 工時 |
      | 需2025單001 | 8.0  |
      | 需2025單002 | 5.5  |
    Then 當日工時總計應為 13.5 小時
    And 工時狀態應顯示為 "超時"
    And 應該顯示橘色警告
    And 警告訊息應為 "工時超過 12 小時，請檢查是否正確"

  # Scenario 5: 週末加班
  Scenario: 週末工作（全部計為加班）
    Given 今天是 "2025-11-16" (星期六，週末)
    When 我記錄以下工時
      | 專案代碼    | 工時 |
      | 需2025單001 | 6.0  |
    Then 當日工時總計應為 6.0 小時
    And 正常工時應為 0 小時
    And 加班工時應為 6.0 小時
    And 工時狀態應顯示為 "週末加班"
    And 應該顯示淺藍色狀態
```

### Feature 2: 加班工時計算

**檔案**: `tests/features/overtime.feature`

```gherkin
Feature: 加班工時計算
  作為一個使用者
  我想要系統自動計算加班工時
  以便準確追蹤加班時間

  Background:
    Given 系統時區設定為 "UTC+8"
    And 標準工時設定為 7.5 小時
    And 工作日為週一至週五
    And 週末為週六、週日

  # Scenario 1: 平日加班計算
  Scenario Outline: 平日不同工時的加班計算
    Given 今天是工作日
    When 我記錄總計 <總工時> 小時的工時
    Then 正常工時應為 <正常工時> 小時
    And 加班工時應為 <加班工時> 小時

    Examples:
      | 總工時 | 正常工時 | 加班工時 |
      | 5.0    | 5.0      | 0.0      |
      | 7.5    | 7.5      | 0.0      |
      | 8.0    | 7.5      | 0.5      |
      | 9.5    | 7.5      | 2.0      |
      | 12.0   | 7.5      | 4.5      |

  # Scenario 2: 週末加班計算
  Scenario Outline: 週末工時全部計為加班
    Given 今天是週末
    When 我記錄總計 <總工時> 小時的工時
    Then 正常工時應為 0 小時
    And 加班工時應為 <總工時> 小時

    Examples:
      | 總工時 |
      | 2.0    |
      | 4.5    |
      | 8.0    |

  # Scenario 3: 本週加班總計
  Scenario: 計算本週總加班時數
    Given 本週工時記錄如下
      | 日期       | 星期 | 工時 |
      | 2025-11-10 | 一   | 8.0  |
      | 2025-11-11 | 二   | 9.5  |
      | 2025-11-12 | 三   | 7.5  |
      | 2025-11-13 | 四   | 8.5  |
      | 2025-11-14 | 五   | 7.5  |
      | 2025-11-15 | 六   | 4.0  |
    Then 本週正常工時應為 37.5 小時
    And 本週平日加班應為 3.5 小時
      # (0.5 + 2.0 + 0 + 1.0 + 0)
    And 本週週末加班應為 4.0 小時
    And 本週總加班時數應為 7.5 小時
```

### Feature 3: 專案核定工時追蹤

**檔案**: `tests/features/approved_hours.feature`

```gherkin
Feature: 專案核定工時追蹤與扣抵
  作為專案管理者
  我想要追蹤專案的核定工時使用情況
  以便控制專案成本並預警超支

  Background:
    Given 存在以下專案
      | 專案代碼    | 專案名稱 | 核定工時(人天) | 核定工時(小時) |
      | 需2025單001 | AI系統   | 20             | 150.0          |
    And 存在以下工作類別
      | 代碼 | 名稱 | 是否扣抵核定工時 |
      | A07  | 其它 | 是               |
      | A08  | 商模 | 否               |
      | B04  | 其它 | 是               |
      | I07  | 休假 | 否               |

  # Scenario 1: 一般工作類別扣抵核定工時
  Scenario: 填寫 A07 其它工作，應扣抵核定工時
    Given 專案 "需2025單001" 的核定工時為 150.0 小時
    And 已使用工時為 0 小時
    When 我記錄以下工時
      | 專案代碼    | 工作類別 | 工時 |
      | 需2025單001 | A07 其它 | 8.0  |
    Then 專案 "需2025單001" 的已使用工時應為 8.0 小時
    And 剩餘工時應為 142.0 小時
    And 使用率應為 5.3%

  # Scenario 2: A08 商模不扣抵核定工時
  Scenario: 填寫 A08 商模工作，不扣抵核定工時
    Given 專案 "需2025單001" 的核定工時為 150.0 小時
    And 已使用工時為 50.0 小時
    When 我記錄以下工時
      | 專案代碼    | 工作類別 | 工時 |
      | 需2025單001 | A08 商模 | 12.0 |
    Then 專案 "需2025單001" 的已使用工時應仍為 50.0 小時
    And 不扣抵工時應為 12.0 小時
    And 剩餘工時應為 100.0 小時
    And 使用率應為 33.3%

  # Scenario 3: 混合工作類別的工時計算
  Scenario: 同時填寫扣抵與不扣抵類別
    Given 專案 "需2025單001" 的核定工時為 150.0 小時
    And 已使用工時為 0 小時
    When 我記錄以下工時
      | 專案代碼    | 工作類別 | 工時 |
      | 需2025單001 | A07 其它 | 4.0  |
      | 需2025單001 | A08 商模 | 2.0  |
      | 需2025單001 | B04 其它 | 3.0  |
    Then 專案 "需2025單001" 的已使用工時應為 7.0 小時
      # (A07: 4.0 + B04: 3.0，A08 不計入)
    And 不扣抵工時應為 2.0 小時
    And 專案總工時應為 9.0 小時
    And 剩餘工時應為 143.0 小時
    And 使用率應為 4.7%

  # Scenario 4: 核定工時超過 80% 預警
  Scenario: 專案工時使用率超過 80% 應顯示警告
    Given 專案 "需2025單001" 的核定工時為 150.0 小時
    And 已使用工時為 120.0 小時
    When 我查看專案統計
    Then 使用率應為 80.0%
    And 應該顯示橘色預警
    And 警告訊息應為 "專案工時使用率已達 80%，請注意控制"

  # Scenario 5: 核定工時用完
  Scenario: 專案工時使用率達到或超過 100%
    Given 專案 "需2025單001" 的核定工時為 150.0 小時
    And 已使用工時為 150.0 小時
    When 我嘗試記錄以下工時
      | 專案代碼    | 工作類別 | 工時 |
      | 需2025單001 | A07 其它 | 5.0  |
    Then 系統應顯示紅色警告
    And 警告訊息應為 "專案核定工時已用完，此記錄將超出預算"
    And 應該允許記錄但標示為超支
```

### Feature 4: 專案與需求單管理

**檔案**: `tests/features/project_management.feature`

```gherkin
Feature: 專案與需求單管理
  作為使用者
  我想要管理專案和需求單代碼
  以便正確追蹤工時歸屬

  # Scenario 1: 創建專案（必填欄位）
  Scenario: 成功創建專案
    When 我創建專案並填寫以下資訊
      | 專案代碼    | 需求單代碼     | 專案名稱 |
      | 需2025單001 | R202511146001  | AI系統   |
    Then 專案應該成功創建
    And 專案代碼應為 "需2025單001"
    And 需求單代碼應為 "R202511146001"
    And 專案名稱應為 "AI系統"

  # Scenario 2: 專案代碼唯一性
  Scenario: 專案代碼重複應拒絕創建
    Given 已存在專案代碼為 "需2025單001" 的專案
    When 我嘗試創建專案代碼為 "需2025單001" 的新專案
    Then 應該返回錯誤
    And 錯誤訊息應為 "專案代碼已存在"

  # Scenario 3: 需求單代碼格式驗證
  Scenario Outline: 需求單代碼格式驗證
    When 我嘗試創建專案並使用需求單代碼 "<需求單代碼>"
    Then 驗證結果應為 <是否有效>

    Examples:
      | 需求單代碼     | 是否有效 |
      | R202511146001  | 通過     |
      | R202507236423  | 通過     |
      | 202511146001   | 失敗     |
      | R20251114      | 失敗     |
      | A202511146001  | 失敗     |

  # Scenario 4: 專案核定工時轉換
  Scenario: 核定人天自動轉換為小時
    When 我創建專案並設定核定工時為 20 人天
    Then 核定工時（小時）應自動計算為 150.0 小時
      # 20 * 7.5 = 150.0
```

### Feature 5: TCS 格式化輸出

**檔案**: `tests/features/tcs_sync.feature`

```gherkin
Feature: TCS 格式化輸出
  作為使用者
  我想要將工時記錄格式化為 TCS 格式
  以便複製貼上到 TCS 系統

  Background:
    Given 存在以下專案
      | 專案代碼    | 專案名稱 |
      | 需2025單001 | AI系統   |
      | 需2025單002 | 數據平台 |
    And 存在以下模組
      | 代碼 | 名稱         |
      | A00  | 中概全權     |
      | O18  | 數據智能應用科 |
    And 存在以下工作類別
      | 代碼 | 名稱 |
      | A07  | 其它 |
      | B04  | 其它 |

  Scenario: 格式化單日多筆工時記錄
    Given 日期 "2025-11-12" 有以下工時記錄
      | 專案代碼    | 模組 | 工作類別 | 工時 | 工作說明                              |
      | 需2025單001 | A00  | A07      | 4.0  | - [x] 需求分析\n- [x] 系統設計        |
      | 需2025單002 | O18  | B04      | 3.5  | - [x] 資料庫優化                      |
    When 我請求格式化日期 "2025-11-12" 的工時記錄
    Then 應該返回以下格式的文字
      """
      日期: 2025/11/12
      專案名稱: 需2025單001
      模組: A00 中概全權
      工作類別: A07 其它
      實際工時: 4.0
      工作說明:
      - [x] 需求分析
      - [x] 系統設計

      ---

      專案名稱: 需2025單002
      模組: O18 數據智能應用科
      工作類別: B04 其它
      實際工時: 3.5
      工作說明:
      - [x] 資料庫優化
      """
```

## 核心功能規劃

### 1. 專案管理模組（簡化版）

#### 1.1 專案 CRUD
- 創建專案（專案代碼、名稱、預設模組、預設工作類別）
- 查看專案列表（列表視圖、搜尋）
- 編輯專案資訊
- 刪除專案（軟刪除）
- 歸檔專案（已完成的專案）

#### 1.2 專案屬性
- 專案代碼（必填，如：需2025單001）
- 需求單代碼（必填，如：R202507236423）
  - 格式：R + 年月日 + 流水號
  - 用於內部追蹤，填寫 TCS 時不需要
- 專案名稱（必填）
- **核定工時**（選填，單位：人天，如：20）
  - 專案核准的總工時額度
  - 用於追蹤專案工時使用情況
  - 換算：1 人天 = 7.5 小時
- 預設模組（選填，可從固定清單選擇）
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
- 專案（必填，從專案清單選擇，自動帶入預設模組和工作類別）
- 模組（必填，可修改）
- 工作類別（必填，可修改）
- 實際工時（必填，數字，如：1.5、4、2）
  - 單筆工時範圍：0.5 ~ 12 小時
  - 支援小數點（精度到 0.5 小時）
- 工作說明（必填，支援 Markdown 格式）
- 帳項選擇（選填，文字輸入）

#### 2.3 快速操作
- 快速新增工時（當日日期預設）
- 從範本創建（常做的工作可儲存為範本）
- 批次編輯（修改多筆記錄的日期或專案）
- 檢查每日工時總和（提示是否在 7.5~12 小時範圍內）

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

#### 3.3 工時驗證與顯示
- **平日工時顯示**（週一至週五）：
  - 顯示總工時、正常工時、加班工時
  - 例如：總計 8.5h（正常 7.5h + 加班 1h）
  - 工時狀態：
    - 🟢 正常：工時 = 7.5 小時
    - 🟢 正常+加班：7.5 < 工時 ≤ 12 小時（顯示加班小時數）
    - 🟡 不足：工時 < 7.5 小時（黃色警告）
    - 🟠 超時：工時 > 12 小時（橘色警告）
    - ⚪ 未填寫：工時 = 0（提示需要填寫）
- **週末工時顯示**（週六、週日）：
  - 顯示總工時（全部計為加班）
  - 例如：加班 8h
  - 不強制驗證，可選擇性記錄
- 提示遺漏欄位
- 提示重複記錄

### 4. 日曆視圖

#### 4.1 月曆展示
- 顯示每日工時總和與加班小時數
  - 工作日顯示：總工時（如：8.5h）+ 加班標記（如：+1h OT）
  - 週末顯示：加班工時（如：8h OT）
- 以顏色標示工時狀態：
  - **工作日（週一至週五）**：
    - 🟢 綠色：工時 = 7.5 小時（正常）
    - 🟢 綠色+角標：7.5 < 工時 ≤ 12 小時（正常+加班，顯示加班時數）
    - 🟡 黃色：0 < 工時 < 7.5 小時（不足）
    - 🟠 橘色：工時 > 12 小時（超時警告）
    - ⚪ 白色/紅框：工時 = 0（未填寫）
  - **週末（週六、週日）**：
    - 🔵 淺藍色：有記錄工時（全部為加班）
    - ⚫ 灰色：無工時記錄（正常休息）
- 點擊日期查看/編輯當日工時
- 顯示當月工作日總數與已填寫天數
- 顯示當月總加班時數

#### 4.2 假日管理（可選）
- 標記 DAYOFF（休假、病假、事假等）
- 自動填入休假工時記錄

### 5. 統計與報表模組

#### 5.1 工時統計
- 本週工時總計
  - 正常工時：週一至週五的 7.5 小時/天（最多 37.5 小時）
  - 平日加班：週一至週五超過 7.5 小時的部分
  - 週末加班：週六、週日的所有工時
  - 總加班時數：平日加班 + 週末加班
  - 平均每日工時
- 本月工時總計
  - 正常工時總計
  - 平日加班總計
  - 週末加班總計
  - 總加班時數
  - 應工作天數 vs 已填寫天數
- 按專案統計
  - 各專案累計總工時
  - 各專案正常工時 vs 加班工時
  - **核定工時追蹤**：
    - 核定工時（人天 / 小時）
    - 已使用工時（僅計算扣抵類別）
    - 不扣抵工時（如 A08 商模）
    - 剩餘工時
    - 使用率（已使用 / 核定）
    - 預警提示（使用率 > 80% 顯示警告）
- 按工作類別統計
  - 各類別累計工時
  - 區分扣抵 vs 不扣抵工時
- 自訂日期範圍統計

#### 5.2 視覺化圖表
- 專案工時分佈（圓餅圖）
  - 顯示各專案佔比
  - 可選擇顯示：總工時 / 正常工時 / 加班工時
- 每週工時趨勢（折線圖或堆疊長條圖）
  - 每日正常工時（最多 7.5h）
  - 每日加班工時（堆疊顯示）
  - 標示週末加班
- 工作類別分佈（長條圖）
- 加班工時統計（長條圖）
  - 平日加班 vs 週末加班
  - 按週/月顯示加班趨勢

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
  模組: A00 中概全權
  工作類別: A07 其它
  實際工時: 1.5
  工作說明:
  - [x] 控股A1發展月會

  ---

  專案名稱: 需2025單002
  模組: O18 數據智能應用科
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
  - 模組（使用搜尋選擇器）
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

#### 7.1 模組管理
- 預設模組清單（固定選項）：
  - A00 中概全權
  - O18 數據智能應用科
  - （其他可新增）
- 新增、編輯、刪除模組
- 設定常用模組

#### 7.2 工作類別管理
- 預設工作類別清單（固定選項）：
  - A07 其它（扣抵核定工時）
  - A08 商模（**不扣抵**核定工時）
  - B04 其它（扣抵核定工時）
  - I07 休假（休假、病假、事假等）（不扣抵核定工時）
  - （其他可新增）
- 工作類別屬性：
  - 代碼與名稱
  - **是否扣抵核定工時**（預設：是）
  - 說明：A08 商模等特殊類別雖計入專案工時，但不消耗核定工時
- 新增、編輯、刪除工作類別
- 設定常用工作類別

#### 7.3 工作範本管理（可選）
- 儲存常做的工作為範本
- 範本內容：專案、模組、工作類別、預設工時、工作說明
- 快速套用範本創建工時記錄

### 8. 設定模組

#### 8.1 系統設定
- 語言切換（中文/英文）
- 主題設定（淺色/深色模式）
- 時區設定（預設 UTC+8）
- 工時設定：
  - 標準每日工時（預設 7.5）
  - 最大每日工時（預設 12）
  - 單筆工時最小單位（預設 0.5）
- 工作日設定：
  - 工作日：週一至週五（可自訂）
  - 週末：週六、週日
- 週末顯示/隱藏選項

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
    requirement_code VARCHAR(50) NOT NULL,     -- 需求單代碼（如：R202507236423）
    name VARCHAR(200) NOT NULL,                -- 專案名稱
    approved_man_days DECIMAL(10,2),           -- 核定工時（人天，如：20）
    default_account_group_id INTEGER,          -- 預設模組 FK
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

#### 2. account_groups (模組表)
```sql
CREATE TABLE account_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) NOT NULL,                 -- 模組代碼（如：A00）
    name VARCHAR(200) NOT NULL,                -- 模組名稱（如：中概全權）
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
    deduct_approved_hours BOOLEAN DEFAULT TRUE,-- 是否扣抵核定工時（A08商模=FALSE）
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
    account_group_id INTEGER NOT NULL,         -- 模組 FK
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
    account_group_id INTEGER,                  -- 模組 FK
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

系統啟動時自動插入常用的模組和工作類別：

```sql
-- 模組
INSERT INTO account_groups (code, name, is_default) VALUES
('A00', '中概全權', TRUE),
('O18', '數據智能應用科', TRUE);

-- 工作類別
INSERT INTO work_categories (code, name, deduct_approved_hours, is_default) VALUES
('A07', '其它', TRUE, TRUE),
('A08', '商模', FALSE, TRUE),  -- 不扣抵核定工時
('B04', '其它', TRUE, TRUE),
('I07', '休假（休假、病假、事假等）', FALSE, TRUE);  -- 休假不扣抵核定工時

-- 系統設定
INSERT INTO settings (key, value) VALUES
('language', 'zh-TW'),
('theme', 'light'),
('timezone', 'UTC+8'),
('standard_work_hours', '7.5'),
('max_work_hours', '12'),
('min_time_unit', '0.5'),
('work_days', '1,2,3,4,5'),  -- 1=Monday, 5=Friday
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
                                    返回：核定工時、已使用（扣抵）、不扣抵、
                                          剩餘工時、使用率、按類別分組明細
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

#### 模組 API
```
GET    /api/account-groups        - 獲取所有模組
POST   /api/account-groups        - 創建新模組
PUT    /api/account-groups/{id}   - 更新模組
DELETE /api/account-groups/{id}   - 刪除模組
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
                                    返回：正常工時、平日加班、週末加班、總加班
GET    /api/stats/by-project      - 按專案統計
                                    ?start_date=2025-11-01&end_date=2025-11-30
                                    返回：各專案總工時、正常工時、加班工時、
                                          核定工時、已使用工時（扣抵）、
                                          不扣抵工時、剩餘工時、使用率
GET    /api/stats/by-category     - 按工作類別統計
GET    /api/stats/overtime        - 加班統計
                                    ?start_date=2025-11-01&end_date=2025-11-30
                                    返回：平日加班、週末加班、每日明細
GET    /api/stats/calendar        - 日曆資料（每日工時總和與加班）
                                    ?year=2025&month=11
                                    返回：每日總工時、加班工時、狀態
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
- 本週工時總計
  - 正常工時（進度條顯示，目標 37.5 小時）
  - 平日加班工時
  - 週末加班工時
  - 總加班時數（醒目顯示）
  - 工時狀態提示（正常/不足/超時）
- 本月工時總計
  - 正常工時總計
  - 平日加班總計
  - 週末加班總計
  - 總加班時數
  - 已填寫天數 / 應工作天數
- 快速操作：新增今日工時
- 最近使用的專案
- 本週工時趨勢圖
  - 堆疊長條圖：正常工時（底部）+ 加班工時（堆疊）
  - 區分平日和週末
- 專案工時分佈圖
- 加班統計卡片（本週/本月總加班）

#### 2. 每日工時記錄 (DailyEntry)
- 日期選擇（預設今天）
- 工作日/週末標示
- 當日工時記錄列表（可拖曳排序）
- 當日工時總和與狀態提示：
  - 工作日：顯示 7.5~12 小時範圍驗證
  - 週末：顯示加班工時（無驗證）
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
  - 顯示：專案代碼、需求單代碼、專案名稱、狀態
  - 顯示核定工時與使用率（進度條）
  - 支援按專案代碼或需求單代碼搜尋
- 新增/編輯專案表單
  - 必填：專案代碼、需求單代碼、專案名稱
  - 選填：核定工時（人天）、預設模組、預設工作類別、備註、顏色
- 專案詳情
  - 顯示完整專案資訊（含需求單代碼、核定工時）
  - **核定工時使用情況**：
    - 核定：XX 人天（XX 小時）
    - 已使用：XX 小時（扣抵類別）
    - 不扣抵：XX 小時（如 A08 商模）
    - 剩餘：XX 小時
    - 進度條視覺化
  - 專案工時明細（按類別分組）
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
- 模組管理
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
        # 3. 點擊模組搜尋器，選擇模組
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
- [ ] 初始資料插入（模組、工作類別）
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
  - [ ] 模組管理
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
- 快取機制（專案、模組、類別清單）

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
7. ✅ 工時總和驗證（7.5~12 小時範圍）
8. ✅ 工作日設定（週一至週五）與週末區分
9. ✅ 時區支援（UTC+8）
10. ✅ 日曆視圖顏色編碼（綠/黃/橘/藍/灰）

## 變更歷史

### 2025-11-14 - v1.5
- **重大變更**：新增開發規範與測試驅動開發流程
  - **測試驅動開發 (TDD)**：所有功能開發前必須先撰寫測試
  - **行為驅動開發 (BDD)**：使用 Gherkin 語言描述業務邏輯
- **測試框架設定**：
  - 後端：pytest + pytest-bdd + pytest-cov（目標覆蓋率 80%）
  - 前端：Vitest + @vue/test-utils
- **業務邏輯規格（Gherkin）**：
  - Feature 1: 每日工時記錄與驗證（5 個場景）
  - Feature 2: 加班工時計算（3 個場景，含 Scenario Outline）
  - Feature 3: 專案核定工時追蹤與扣抵（5 個場景）
  - Feature 4: 專案與需求單管理（4 個場景）
  - Feature 5: TCS 格式化輸出（1 個場景）
- **測試目錄結構**：
  - features/：Gherkin feature 檔案
  - step_defs/：Step definitions
  - unit/：單元測試
  - integration/：整合測試
- **測試要求**：
  - 所有 API 端點必須有整合測試
  - 所有業務邏輯必須有 Gherkin 規格
  - 所有 Service 層必須有單元測試
  - 測試覆蓋率達 80% 以上

### 2025-11-14 - v1.4
- **重要業務邏輯**：核定工時追蹤與扣抵機制
  - 專案新增「核定工時」欄位（單位：人天，1人天=7.5小時）
  - 工作類別新增「是否扣抵核定工時」屬性
  - A08 商模、I07 休假：計入專案工時但**不扣抵**核定工時
  - 其他類別（A07、B04等）：計入且**扣抵**核定工時
- **資料庫更新**：
  - projects 表：新增 approved_man_days 欄位（核定人天）
  - work_categories 表：新增 deduct_approved_hours 欄位（布林值）
  - 初始資料：新增 A08 商模（不扣抵）
- **統計功能增強**：
  - 專案統計：顯示核定工時、已使用（扣抵）、不扣抵、剩餘、使用率
  - 使用率預警：超過 80% 顯示警告
  - 工作類別統計：區分扣抵 vs 不扣抵工時
- **專案詳情增強**：
  - 顯示核定工時使用情況（進度條視覺化）
  - 按類別分組顯示工時明細
  - 專案列表顯示使用率進度條
- **API 更新**：
  - /api/projects/{id}/stats：返回核定工時追蹤資訊
  - /api/stats/by-project：增加核定工時相關統計

### 2025-11-14 - v1.3
- **新增欄位**：專案增加「需求單代碼」欄位
  - 格式：R + 年月日 + 流水號（如：R202507236423）
  - 用於內部追蹤，填寫 TCS 時不需要此欄位
- 更新資料庫：projects 表新增 requirement_code 欄位（必填）
- 更新專案管理頁面：列表顯示需求單代碼，支援搜尋
- 更新專案表單：新增需求單代碼輸入欄位（必填）

### 2025-11-14 - v1.2
- **重要變更**：明確加班計算規則
  - 平日超過 7.5 小時即計為加班（7.5h 正常 + 超過部分為加班）
  - 週末所有工時計為加班
- 更新統計模組：分別顯示正常工時、平日加班、週末加班
- 更新儀表板：新增加班統計卡片與堆疊圖表
- 更新日曆視圖：顯示每日加班小時數（角標）
- 新增 API：加班統計 API（/api/stats/overtime）
- 更新每日工時視圖：顯示正常工時與加班工時拆分

### 2025-11-14 - v1.1
- 新增業務規則：工作日（週一至週五）、時區（UTC+8）
- 更新工時驗證：最少 7.5 小時，最多 12 小時
- 優化日曆視圖顏色標示邏輯（5 種狀態）
- 新增週末加班工時單獨統計
- 更新系統設定：時區、工作日、工時範圍設定

### 2025-11-14 - v1.0
- 初版計劃：聚焦工時記錄核心功能
- 確定技術棧：Vue 3 + Element Plus + FastAPI + SQLite
- 設計 6 個資料表與完整 API
- 規劃 Phase 1（5 週）與 Phase 2（2-3 週）開發時程

---

*本計劃書最後更新：2025-11-14 19:30 UTC+8 (v1.5)*
