"""
TCS 工時系統自動填寫腳本
使用 Playwright 自動化填寫工時記錄
"""
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, Page, Frame, Browser, Playwright


class TCSAutomation:
    """TCS 自動填寫類別"""

    def __init__(self, tcs_url: str = "http://cfcgpap01/tcs/"):
        self.tcs_url = tcs_url
        self.page: Optional[Page] = None
        self.frame: Optional[Frame] = None
        self.browser: Optional[Browser] = None
        self.playwright: Optional[Playwright] = None
        self.dry_run = False

        # 載入選擇器配置
        selectors_path = Path(__file__).parent / "selectors.json"
        with open(selectors_path, 'r', encoding='utf-8') as f:
            self.selectors = json.load(f)

    def start(self, headless: bool = False, dry_run: bool = False):
        """
        啟動瀏覽器

        Args:
            headless: 是否使用無頭模式
            dry_run: 乾運行模式（不會真正儲存）
        """
        self.dry_run = dry_run
        self.playwright = sync_playwright().start()

        # 使用 Chromium，支援 Windows 整合驗證
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            slow_mo=300  # 每個操作延遲 300ms，方便觀察
        )

        # 建立新的頁面
        self.page = self.browser.new_page()

        # 前往 TCS 首頁
        print(f"正在連接 TCS 系統: {self.tcs_url}")
        self.page.goto(self.tcs_url, timeout=30000)
        self.page.wait_for_load_state('networkidle')

        # 切換到 mainFrame（工時輸入的 frame）
        main_frame = self.page.frame(name='mainFrame')
        if not main_frame:
            raise Exception('找不到 mainFrame，請確認 TCS 系統已正確載入')

        self.frame = main_frame
        print("✅ 成功連接 TCS 系統")

        if dry_run:
            print("⚠️  DRY RUN 模式：不會真正儲存資料")

    def fill_time_entries(self, date: str, entries: List[Dict]):
        """
        填寫多筆工時記錄

        Args:
            date: 日期，格式 YYYYMMDD (如: 20251124)
            entries: 工時記錄列表，每筆包含：
                - project_code: 專案代碼
                - account_group: 帳組/模組
                - work_category: 工作類別
                - hours: 工時
                - description: 工作說明
                - requirement_no: 需求單號（選填）
                - progress_rate: 完成百分比（選填，預設 0）
        """
        if not self.frame:
            raise Exception("瀏覽器未啟動，請先呼叫 start()")

        # 1. 填入日期
        self._fill_date(date)

        # 2. 點擊查詢按鈕（載入該日期的資料）
        print(f"查詢日期 {date} 的資料...")
        self.frame.click(f'#{self.selectors["query_button"]}')
        time.sleep(1)  # 等待查詢完成

        # 3. 清除現有資料（如果需要）
        self._clear_existing_data()

        # 4. 逐筆填寫工時記錄
        for idx, entry in enumerate(entries):
            if idx >= 5:
                # 如果超過 5 筆，需要新增行
                self._add_new_row()
                time.sleep(0.3)

            print(f"填寫第 {idx + 1} 筆記錄...")
            self._fill_single_entry(idx, entry)
            time.sleep(0.5)  # 每筆之間稍微延遲

        print(f"✅ 已填寫 {len(entries)} 筆工時記錄")

        # 5. 等待所有 AJAX 驗證完成
        print("⏳ 等待所有欄位驗證完成...")
        time.sleep(1)  # 確保所有 onblur 事件和 AJAX 請求都完成

        # 6. 驗證總工時
        self._validate_total_hours()

    def _fill_date(self, date: str):
        """填入日期"""
        date_input = f'#{self.selectors["date_input"]}'
        self.frame.fill(date_input, date)
        print(f"✅ 填入日期: {date}")

    def _clear_existing_data(self):
        """清除現有資料"""
        try:
            clear_button = self.frame.locator(self.selectors["clear_button"])
            if clear_button.count() > 0:
                clear_button.click()
                time.sleep(0.5)
                print("清除現有資料")
        except Exception:
            pass  # 沒有清除按鈕或資料，忽略

    def _fill_single_entry(self, row_idx: int, entry: Dict):
        """
        填寫單筆工時記錄

        Args:
            row_idx: 行索引（從 0 開始）
            entry: 工時記錄資料
                - account_group: 模組代碼，如果為空則預設填入 "A00"
        """
        # 專案代碼
        proj_input = f'#{self.selectors["project_code"]}{row_idx}'
        self.frame.fill(proj_input, entry['project_code'])
        self.frame.locator(proj_input).blur()  # 觸發 onblur 事件
        time.sleep(0.4)  # 等待自動查詢專案名稱

        # 驗證專案名稱是否正確載入
        proj_name_span = f'#{self.selectors["project_name_span"]}{row_idx}'
        proj_name = self.frame.locator(proj_name_span).text_content()
        if not proj_name or '錯誤' in proj_name:
            print(f"  ⚠️  警告: 專案代碼 {entry['project_code']} 可能無效")

        # 模組（如果為空則預設填入 "A00"）
        account_group_code = entry.get('account_group') or "A00"
        module_input = f'#{self.selectors["module_code"]}{row_idx}'
        self.frame.fill(module_input, account_group_code)
        self.frame.locator(module_input).blur()
        time.sleep(0.4)

        # 驗證模組名稱
        module_name_span = f'#{self.selectors["module_name_span"]}{row_idx}'
        module_name = self.frame.locator(module_name_span).text_content()
        if not module_name or '錯誤' in module_name:
            print(f"  ⚠️  警告: 模組代碼 {account_group_code} 可能無效")

        # 工作類別
        work_item_input = f'#{self.selectors["work_item_code"]}{row_idx}'
        self.frame.fill(work_item_input, entry['work_category'])
        self.frame.locator(work_item_input).blur()
        time.sleep(0.4)

        # 驗證工作類別名稱
        work_item_name_span = f'#{self.selectors["work_item_name_span"]}{row_idx}'
        work_item_name = self.frame.locator(work_item_name_span).text_content()
        if not work_item_name or '錯誤' in work_item_name:
            print(f"  ⚠️  警告: 工作類別 {entry['work_category']} 可能無效")

        # 需求單號（選填）
        if entry.get('requirement_no'):
            req_input = f'#{self.selectors["requirement_no"]}{row_idx}'
            self.frame.fill(req_input, entry['requirement_no'])

        # 實際工時
        hours_input = f'#{self.selectors["work_hours"]}{row_idx}'
        self.frame.fill(hours_input, str(entry['hours']))

        # 工作說明
        # 注意：所有 textarea 都用同樣的 ID，需要用 nth 選擇
        desc_textarea = self.frame.locator(f'#{self.selectors["work_description"]}').nth(row_idx)
        desc_textarea.fill(entry['description'])

        # 完成百分比（選填）
        progress_input = f'#{self.selectors["progress_rate"]}{row_idx}'
        progress_rate = str(entry.get('progress_rate', '0'))
        self.frame.fill(progress_input, progress_rate)

        print(f"  ✓ 第 {row_idx + 1} 筆: {entry['project_code']} - {entry['hours']}h")

    def _add_new_row(self):
        """新增一行"""
        add_button = self.frame.locator(f'#{self.selectors["add_row_button"]}')
        add_button.click()
        print("新增一列")

    def _validate_total_hours(self):
        """驗證總工時"""
        try:
            total_hours_label = self.frame.locator(f'#{self.selectors["actual_hours_label"]}')
            total_hours = total_hours_label.text_content()
            print(f"📊 總工時: {total_hours} 小時")

            total_float = float(total_hours)
            if total_float > 18:
                print("⚠️  警告: 總工時超過 18 小時，TCS 系統可能不接受")
        except Exception as e:
            print(f"無法驗證總工時: {e}")

    def preview_before_save(self, auto_confirm: bool = False):
        """
        儲存前預覽（讓使用者確認）
        
        Args:
            auto_confirm: 是否自動確認（不需要等待輸入），預設 False
        """
        print("\n" + "=" * 50)
        print("請確認填寫的資料是否正確")
        print("=" * 50)
        
        if self.dry_run:
            print("⚠️  DRY RUN 模式：將不會真正儲存")
            time.sleep(1)  # 稍微等待讓使用者看到訊息
        else:
            if auto_confirm:
                print("✅ 自動確認：繼續儲存")
                time.sleep(0.5)
            else:
                print("按 Enter 繼續儲存，或 Ctrl+C 取消")
                input()

    def save(self):
        """點擊儲存按鈕"""
        if self.dry_run:
            print("⚠️  DRY RUN 模式：跳過儲存")
            return

        # 儲存前驗證：確認至少有一筆資料已填入
        print("🔍 驗證資料是否已正確填入...")
        try:
            # 檢查第一筆專案代碼是否有值
            first_proj = self.frame.locator('#txtPROJ_CD0')
            if first_proj.count() > 0:
                proj_value = first_proj.input_value()
                if not proj_value or proj_value.strip() == "":
                    print("⚠️  警告: 第一筆專案代碼為空，可能資料未正確填入")
                else:
                    print(f"   ✓ 第一筆專案代碼: {proj_value}")
            
            # 檢查總工時
            try:
                total_hours = self.frame.locator('#lblACTL_HR').text_content()
                if total_hours and float(total_hours) > 0:
                    print(f"   ✓ 總工時: {total_hours} 小時")
                else:
                    print("⚠️  警告: 總工時為 0，可能資料未正確填入")
            except Exception:
                pass
        except Exception as e:
            print(f"⚠️  驗證過程中的警告: {e}")

        # 等待一下確保所有欄位都已正確填入
        time.sleep(0.5)

        # 在點擊前設定 dialog 監聽器（處理 confirm 和 alert）
        dialog_messages = []
        
        def handle_dialog(dialog):
            message = dialog.message
            dialog_messages.append(message)
            print(f"📢 TCS 訊息: {message}")
            
            # 如果是 confirm（非當日資料確認），自動接受
            if dialog.type == 'confirm':
                print("   ✓ 自動確認非當日資料儲存")
                dialog.accept()
            else:
                # alert 或其他類型的 dialog
                dialog.accept()

        # 設定 dialog 監聽器（必須在點擊前設定）
        self.page.on('dialog', handle_dialog)

        # 點擊儲存按鈕
        print("🖱️  點擊儲存按鈕...")
        save_button = self.frame.locator(f'#{self.selectors["save_button"]}')
        
        # 確保按鈕可見且可點擊
        save_button.wait_for(state='visible', timeout=3000)
        save_button.click()

        # 等待表單提交和可能的 dialog
        try:
            # 等待可能的 dialog 出現
            time.sleep(1)
            
            # 等待頁面導航或重新載入（如果是表單提交）
            try:
                # 等待 frame 重新載入或頁面導航
                self.frame.wait_for_load_state('networkidle', timeout=5000)
                print("✅ 頁面已重新載入")
            except Exception:
                # 如果沒有導航，至少等待一下讓表單提交完成
                time.sleep(2)
            
            # 檢查是否有錯誤訊息顯示在頁面上
            try:
                msg_span = self.frame.locator('#spanMSG')
                if msg_span.count() > 0:
                    msg_text = msg_span.text_content()
                    if msg_text and msg_text.strip():
                        print(f"📋 TCS 系統訊息: {msg_text}")
            except Exception:
                pass
            
            if dialog_messages:
                print(f"✅ 已處理 {len(dialog_messages)} 個對話框")
            else:
                print("✅ 已點擊儲存按鈕")
                
        except Exception as e:
            print(f"⚠️  儲存過程中的警告: {e}")
            # 即使有警告，也繼續執行

    def screenshot(self, path: Optional[str] = None, full_page: bool = True, frame_only: bool = False):
        """
        截取 TCS 畫面
        
        Args:
            path: 截圖儲存路徑，如果為 None 則自動產生檔名（格式：tcs_screenshot_YYYYMMDD_HHMMSS.png）
            full_page: 是否截取完整頁面（包含需要滾動的部分），預設 True
            frame_only: 是否只截取 frame（mainFrame），預設 False（截整個頁面）
        
        Returns:
            str: 截圖檔案路徑
        """
        if not self.page:
            raise Exception("瀏覽器未啟動，請先呼叫 start()")
        
        # 如果沒有指定路徑，自動產生檔名
        if path is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir = Path(__file__).parent.parent / "screenshots"
            screenshot_dir.mkdir(exist_ok=True)
            path = str(screenshot_dir / f"tcs_screenshot_{timestamp}.png")
        
        # 確保目錄存在
        screenshot_path = Path(path)
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if frame_only and self.frame:
                # 只截取 frame（mainFrame）
                # 注意：Locator.screenshot() 不支援 full_page 參數
                # 所以我們只能截取可見區域，或使用其他方法
                frame_body = self.frame.locator('body')
                
                if full_page:
                    # 嘗試截取完整 frame：先滾動到頂部，然後截取
                    # 由於 locator.screenshot() 不支援 full_page，我們使用替代方案
                    # 先取得 frame 的完整高度，然後滾動並截取
                    try:
                        # 取得 frame 的完整高度
                        total_height = self.frame.evaluate("""
                            () => Math.max(
                                document.documentElement.scrollHeight,
                                document.body.scrollHeight,
                                document.documentElement.offsetHeight,
                                document.body.offsetHeight
                            )
                        """)
                        
                        # 取得 viewport 高度
                        viewport_height = self.frame.evaluate("() => window.innerHeight")
                        
                        # 如果內容超過 viewport，需要滾動截圖
                        if total_height > viewport_height:
                            # 滾動到頂部
                            self.frame.evaluate("() => window.scrollTo(0, 0)")
                            # 截取可見區域（這是目前 locator.screenshot() 的限制）
                            frame_body.screenshot(path=path)
                            screenshot_type = "frame 畫面（可見區域，完整內容需手動滾動）"
                        else:
                            # 內容在 viewport 內，直接截取
                            frame_body.screenshot(path=path)
                            screenshot_type = "frame 畫面（完整內容）"
                    except Exception:
                        # 如果滾動失敗，至少截取可見區域
                        frame_body.screenshot(path=path)
                        screenshot_type = "frame 畫面（可見區域）"
                else:
                    # 只截取可見區域
                    frame_body.screenshot(path=path)
                    screenshot_type = "frame 畫面（可見區域）"
            else:
                # 截取整個頁面
                self.page.screenshot(path=path, full_page=full_page)
                screenshot_type = "完整頁面"
            
            # 轉換為絕對路徑以便顯示
            abs_path = Path(path).resolve()
            print(f"📸 已截取 {screenshot_type}")
            print(f"   檔案路徑: {abs_path}")
            
            return str(abs_path)
        except Exception as e:
            print(f"❌ 截圖失敗: {e}")
            import traceback
            traceback.print_exc()
            raise

    def close(self):
        """關閉瀏覽器"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("✅ 已關閉瀏覽器")


def main():
    """測試用主程式"""
    # 範例資料
    test_entries = [
        {
            'project_code': '商2025智001',
            'account_group': 'A00',
            'work_category': 'A07',
            'hours': 7.5,
            'description': '- [x] 語音質檢軟體架構規劃\n- [x] GC回撥功能討論',
            'requirement_no': '',
            'progress_rate': 0
        }
    ]

    # 執行自動填寫
    tcs = TCSAutomation()
    try:
        tcs.start(headless=False, dry_run=True)  # 預設 dry_run
        tcs.fill_time_entries('20251124', test_entries)
        
        # 填寫完畢後截圖
        screenshot_path = tcs.screenshot(frame_only=True, full_page=True)
        print(f"✅ 已儲存截圖: {screenshot_path}")
        
        tcs.preview_before_save()
        tcs.save()
        time.sleep(3)  # 等待儲存完成
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    finally:
        tcs.close()


if __name__ == '__main__':
    main()

