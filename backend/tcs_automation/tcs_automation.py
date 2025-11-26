"""
TCS 工時系統自動填寫腳本
使用 Playwright 自動化填寫工時記錄
"""
import json
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, Page, Frame, Browser, Playwright

# 嘗試設定終端編碼為 UTF-8（如果支援）
def _setup_terminal_encoding():
    """嘗試設定終端編碼為 UTF-8，以確保中文正確顯示"""
    try:
        # Python 3.7+ 支援 reconfigure
        if hasattr(sys.stdout, 'reconfigure'):
            try:
                # 嘗試設定為 UTF-8
                sys.stdout.reconfigure(encoding='utf-8', errors='replace')
                sys.stderr.reconfigure(encoding='utf-8', errors='replace')
                return True
            except Exception:
                pass  # 如果設定失敗，使用預設編碼
    except Exception:
        pass
    return False

# 在模組載入時嘗試設定編碼
_utf8_enabled = _setup_terminal_encoding()


def safe_print(*args, **kwargs):
    """
    安全的 print 函數，可以處理編碼錯誤（特別是 Windows cp950 無法編碼 emoji）
    並且確保中文文字能正確顯示在終端
    
    如果遇到編碼錯誤，會將 emoji 替換為文字標記，並正確處理中文編碼
    """
    # Emoji 到文字的對應表
    emoji_map = {
        '✅': '[OK]',
        '⚠️': '[WARN]',
        '❌': '[ERROR]',
        '📊': '[INFO]',
        '🔍': '[CHECK]',
        '🖱️': '[CLICK]',
        '📢': '[MSG]',
        '📸': '[SCREENSHOT]',
        '📋': '[TCS]',
        '⏳': '[WAIT]',
        '✓': '[OK]',
    }
    
    # 取得終端編碼
    terminal_encoding = sys.stdout.encoding
    if not terminal_encoding:
        # 如果無法取得終端編碼，嘗試使用系統預設編碼
        try:
            import locale
            terminal_encoding = locale.getpreferredencoding() or 'utf-8'
        except Exception:
            terminal_encoding = 'utf-8'
    
    # 將所有參數轉換為字串並替換 emoji
    safe_args = []
    for arg in args:
        if isinstance(arg, str):
            safe_str = arg
            # 先替換 emoji
            for emoji, replacement in emoji_map.items():
                safe_str = safe_str.replace(emoji, replacement)
            safe_args.append(safe_str)
        else:
            safe_args.append(arg)
    
    # 嘗試輸出，確保中文正確編碼
    try:
        # 如果已成功設定為 UTF-8，直接使用 print
        if _utf8_enabled:
            print(*safe_args, **kwargs)
        else:
            # 如果終端不是 UTF-8，需要手動進行編碼轉換
            # 將 UTF-8 字串轉換為終端編碼的 bytes，然後寫入
            output_parts = []
            for arg in safe_args:
                if isinstance(arg, str):
                    # 將 UTF-8 字串編碼為終端編碼的 bytes
                    output_parts.append(arg.encode(terminal_encoding, errors='replace'))
                else:
                    output_parts.append(str(arg).encode(terminal_encoding, errors='replace'))
            
            # 組合所有 bytes 並寫入
            sep = kwargs.get('sep', ' ').encode(terminal_encoding, errors='replace')
            end = kwargs.get('end', '\n').encode(terminal_encoding, errors='replace')
            message_bytes = sep.join(output_parts) + end
            sys.stdout.buffer.write(message_bytes)
            sys.stdout.buffer.flush()
    except (UnicodeEncodeError, UnicodeError):
        # 如果遇到編碼錯誤，使用更寬鬆的錯誤處理
        try:
            # 使用 errors='replace' 來處理無法編碼的字符
            output_parts = []
            for arg in safe_args:
                if isinstance(arg, str):
                    output_parts.append(arg.encode(terminal_encoding, errors='replace'))
                else:
                    output_parts.append(str(arg).encode(terminal_encoding, errors='replace'))
            
            sep = kwargs.get('sep', ' ').encode(terminal_encoding, errors='replace')
            end = kwargs.get('end', '\n').encode(terminal_encoding, errors='replace')
            message_bytes = sep.join(output_parts) + end
            sys.stdout.buffer.write(message_bytes)
            sys.stdout.buffer.flush()
        except Exception:
            # 最後的備選方案：只輸出 ASCII 字符
            text_only = ' '.join(
                str(arg).encode('ascii', errors='ignore').decode('ascii') 
                for arg in safe_args if arg
            )
            if text_only.strip():
                print(text_only, **kwargs)


class TCSAutomation:
    """TCS 自動填寫類別"""

    def __init__(self, tcs_url: str = "http://cfcgpap01/tcs/"):
        self.tcs_url = tcs_url
        self.page: Optional[Page] = None
        self.frame: Optional[Frame] = None
        self.browser: Optional[Browser] = None
        self.playwright: Optional[Playwright] = None
        self.dry_run = False
        self.fast_mode = True  # 預設啟用快速模式

        # 載入選擇器配置
        selectors_path = Path(__file__).parent / "selectors.json"
        with open(selectors_path, 'r', encoding='utf-8') as f:
            self.selectors = json.load(f)

    def start(self, headless: bool = False, dry_run: bool = False, fast_mode: bool = True):
        """
        啟動瀏覽器

        Args:
            headless: 是否使用無頭模式
            dry_run: 乾運行模式（不會真正儲存）
            fast_mode: 快速模式（預設 True，移除 slow_mo 和減少等待時間）
        """
        self.dry_run = dry_run
        self.fast_mode = fast_mode
        self.playwright = sync_playwright().start()

        # 使用 Chromium，支援 Windows 整合驗證
        browser_options = {
            "headless": headless,
        }
        
        # 只在非快速模式下使用 slow_mo（用於調試）
        if not fast_mode:
            browser_options["slow_mo"] = 300
        
        self.browser = self.playwright.chromium.launch(**browser_options)

        # 建立新的頁面
        self.page = self.browser.new_page()

        # 前往 TCS 首頁
        safe_print(f"正在連接 TCS 系統: {self.tcs_url}")
        self.page.goto(self.tcs_url, timeout=30000)
        self.page.wait_for_load_state('networkidle')

        # 切換到 mainFrame（工時輸入的 frame）
        main_frame = self.page.frame(name='mainFrame')
        if not main_frame:
            raise Exception('找不到 mainFrame，請確認 TCS 系統已正確載入')

        self.frame = main_frame
        safe_print("✅ 成功連接 TCS 系統")

        if dry_run:
            safe_print("⚠️  DRY RUN 模式：不會真正儲存資料")

    def fill_time_entries(self, date: str, entries: List[Dict]):
        """
        填寫多筆工時記錄

        Args:
            date: 日期，格式 YYYYMMDD (如: 20251124)
            entries: 工時記錄列表，每筆包含：
                - project_code: 專案代碼
                - account_group: 模組/模組
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
        safe_print(f"查詢日期 {date} 的資料...")
        query_button = self.frame.locator(f'#{self.selectors["query_button"]}')
        query_button.click()
        
        # 智能等待查詢完成
        if self.fast_mode:
            try:
                # 等待 frame 載入完成或等待查詢結果出現
                self.frame.wait_for_load_state('networkidle', timeout=3000)
            except Exception:
                # 如果等待失敗，使用較短的固定等待
                time.sleep(0.5)
        else:
            time.sleep(1)  # 非快速模式：使用原始等待時間

        # 3. 清除現有資料（如果需要）
        self._clear_existing_data()

        # 4. 逐筆填寫工時記錄
        for idx, entry in enumerate(entries):
            if idx >= 5:
                # 如果超過 5 筆，需要新增行
                self._add_new_row()
                # 快速模式：減少等待時間
                wait_time = 0.1 if self.fast_mode else 0.3
                time.sleep(wait_time)

            safe_print(f"填寫第 {idx + 1} 筆記錄...")
            self._fill_single_entry(idx, entry)
            # 快速模式：減少記錄間延遲
            wait_time = 0.1 if self.fast_mode else 0.5
            time.sleep(wait_time)  # 每筆之間稍微延遲

        safe_print(f"✅ 已填寫 {len(entries)} 筆工時記錄")

        # 5. 等待所有 AJAX 驗證完成
        safe_print("⏳ 等待所有欄位驗證完成...")
        if self.fast_mode:
            # 快速模式：使用較短的等待時間
            time.sleep(0.3)
        else:
            time.sleep(1)  # 非快速模式：確保所有 onblur 事件和 AJAX 請求都完成

        # 6. 驗證總工時
        self._validate_total_hours()

    def _fill_date(self, date: str):
        """填入日期"""
        date_input = f'#{self.selectors["date_input"]}'
        self.frame.fill(date_input, date)
        safe_print(f"✅ 填入日期: {date}")

    def _clear_existing_data(self):
        """清除現有資料"""
        try:
            clear_button = self.frame.locator(self.selectors["clear_button"])
            if clear_button.count() > 0:
                clear_button.click()
                
                # 智能等待資料清除完成
                if self.fast_mode:
                    try:
                        # 等待第一筆專案代碼變為空（最多等待 1 秒）
                        first_proj = self.frame.locator('#txtPROJ_CD0')
                        start_time = time.time()
                        while time.time() - start_time < 1.0:
                            try:
                                value = first_proj.input_value()
                                if not value or value.strip() == "":
                                    break
                            except Exception:
                                pass
                            time.sleep(0.1)
                        # 額外等待 0.1 秒確保清除完成
                        time.sleep(0.1)
                    except Exception:
                        # 如果等待失敗，使用較短的固定等待
                        time.sleep(0.2)
                else:
                    time.sleep(0.5)  # 非快速模式：使用原始等待時間
                
                safe_print("清除現有資料")
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

        # 智能等待專案名稱驗證完成
        proj_name_span = self.frame.locator(f'#{self.selectors["project_name_span"]}{row_idx}')
        is_valid = self._wait_for_ajax_validation(proj_name_span, timeout=2000)
        
        # 驗證專案名稱是否正確載入
        proj_name = proj_name_span.text_content()
        if not proj_name or '錯誤' in proj_name:
            safe_print(f"  ⚠️  警告: 專案代碼 {entry['project_code']} 可能無效")

        # 模組（如果為空則預設填入 "A00"）
        account_group_code = entry.get('account_group') or "A00"
        module_input = f'#{self.selectors["module_code"]}{row_idx}'
        self.frame.fill(module_input, account_group_code)
        self.frame.locator(module_input).blur()
        
        # 智能等待模組名稱驗證完成
        module_name_span = self.frame.locator(f'#{self.selectors["module_name_span"]}{row_idx}')
        self._wait_for_ajax_validation(module_name_span, timeout=2000)

        # 驗證模組名稱
        module_name = module_name_span.text_content()
        if not module_name or '錯誤' in module_name:
            safe_print(f"  ⚠️  警告: 模組代碼 {account_group_code} 可能無效")

        # 工作類別
        work_item_input = f'#{self.selectors["work_item_code"]}{row_idx}'
        self.frame.fill(work_item_input, entry['work_category'])
        self.frame.locator(work_item_input).blur()
        
        # 智能等待工作類別名稱驗證完成
        work_item_name_span = self.frame.locator(f'#{self.selectors["work_item_name_span"]}{row_idx}')
        self._wait_for_ajax_validation(work_item_name_span, timeout=2000)

        # 驗證工作類別名稱
        work_item_name = work_item_name_span.text_content()
        if not work_item_name or '錯誤' in work_item_name:
            safe_print(f"  ⚠️  警告: 工作類別 {entry['work_category']} 可能無效")

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

        safe_print(f"  ✓ 第 {row_idx + 1} 筆: {entry['project_code']} - {entry['hours']}h")

    def _add_new_row(self):
        """新增一行"""
        add_button = self.frame.locator(f'#{self.selectors["add_row_button"]}')
        add_button.click()
        safe_print("新增一列")

    def _wait_for_ajax_validation(self, element_locator, timeout: int = 2000, error_keyword: str = "錯誤"):
        """
        智能等待 AJAX 驗證完成
        
        Args:
            element_locator: 要等待的元素 locator（通常是顯示驗證結果的 span）
            timeout: 超時時間（毫秒），預設 2000ms
            error_keyword: 錯誤關鍵字，預設 "錯誤"
        
        Returns:
            bool: 是否驗證成功（非空且非錯誤）
        """
        if not self.fast_mode:
            # 非快速模式：使用固定等待
            time.sleep(0.4)
            return True
        
        try:
            # 快速模式：智能等待元素內容改變
            # 等待元素文字內容非空且不包含錯誤關鍵字
            start_time = time.time()
            max_wait = timeout / 1000.0  # 轉換為秒
            
            while time.time() - start_time < max_wait:
                try:
                    text = element_locator.text_content()
                    if text and text.strip() != "":
                        # 檢查是否為錯誤訊息
                        if error_keyword not in text:
                            return True
                        else:
                            # 是錯誤訊息，但已經有內容了，可以返回
                            return False
                except Exception:
                    pass
                
                # 短暫等待後重試
                time.sleep(0.1)
            
            # 超時：回退到固定等待
            time.sleep(0.2)
            return True
        except Exception:
            # 發生錯誤：回退到固定等待
            time.sleep(0.3)
            return True

    def _validate_total_hours(self):
        """驗證總工時"""
        try:
            total_hours_label = self.frame.locator(f'#{self.selectors["actual_hours_label"]}')
            total_hours = total_hours_label.text_content()
            safe_print(f"📊 總工時: {total_hours} 小時")

            total_float = float(total_hours)
            if total_float > 18:
                safe_print("⚠️  警告: 總工時超過 18 小時，TCS 系統可能不接受")
        except Exception as e:
            safe_print(f"無法驗證總工時: {e}")

    def preview_before_save(self, auto_confirm: bool = False):
        """
        儲存前預覽（讓使用者確認）
        
        Args:
            auto_confirm: 是否自動確認（不需要等待輸入），預設 False
        """
        safe_print("\n" + "=" * 50)
        safe_print("請確認填寫的資料是否正確")
        safe_print("=" * 50)
        
        if self.dry_run:
            safe_print("⚠️  DRY RUN 模式：將不會真正儲存")
            # 快速模式：減少等待時間
            wait_time = 0.2 if self.fast_mode else 1.0
            time.sleep(wait_time)
        else:
            if auto_confirm:
                safe_print("✅ 自動確認：繼續儲存")
                wait_time = 0.2 if self.fast_mode else 0.5
                time.sleep(wait_time)
            else:
                safe_print("按 Enter 繼續儲存，或 Ctrl+C 取消")
                input()

    def save(self):
        """點擊儲存按鈕"""
        if self.dry_run:
            safe_print("⚠️  DRY RUN 模式：跳過儲存")
            return

        # 儲存前驗證：確認至少有一筆資料已填入
        safe_print("🔍 驗證資料是否已正確填入...")
        try:
            # 檢查第一筆專案代碼是否有值
            first_proj = self.frame.locator('#txtPROJ_CD0')
            if first_proj.count() > 0:
                proj_value = first_proj.input_value()
                if not proj_value or proj_value.strip() == "":
                    safe_print("⚠️  警告: 第一筆專案代碼為空，可能資料未正確填入")
                else:
                    safe_print(f"   ✓ 第一筆專案代碼: {proj_value}")
            
            # 檢查總工時
            try:
                total_hours = self.frame.locator('#lblACTL_HR').text_content()
                if total_hours and float(total_hours) > 0:
                    safe_print(f"   ✓ 總工時: {total_hours} 小時")
                else:
                    safe_print("⚠️  警告: 總工時為 0，可能資料未正確填入")
            except Exception:
                pass
        except Exception as e:
            safe_print(f"⚠️  驗證過程中的警告: {e}")

        # 等待一下確保所有欄位都已正確填入
        wait_time = 0.2 if self.fast_mode else 0.5
        time.sleep(wait_time)

        # 在點擊前設定 dialog 監聽器（處理 confirm 和 alert）
        dialog_messages = []
        
        def handle_dialog(dialog):
            message = dialog.message
            dialog_messages.append(message)
            safe_print(f"📢 TCS 訊息: {message}")
            
            # 如果是 confirm（非當日資料確認），自動接受
            if dialog.type == 'confirm':
                safe_print("   ✓ 自動確認非當日資料儲存")
                dialog.accept()
            else:
                # alert 或其他類型的 dialog
                dialog.accept()

        # 設定 dialog 監聽器（必須在點擊前設定）
        self.page.on('dialog', handle_dialog)

        # 點擊儲存按鈕
        safe_print("🖱️  點擊儲存按鈕...")
        save_button = self.frame.locator(f'#{self.selectors["save_button"]}')
        
        # 確保按鈕可見且可點擊
        save_button.wait_for(state='visible', timeout=3000)
        save_button.click()

        # 等待表單提交和可能的 dialog
        try:
            # 快速模式：減少初始等待時間
            if self.fast_mode:
                time.sleep(0.3)  # 短暫等待 dialog 出現
            else:
                time.sleep(1)
            
            # 等待頁面導航或重新載入（如果是表單提交）
            try:
                # 快速模式：使用較短的 timeout
                timeout = 3000 if self.fast_mode else 5000
                self.frame.wait_for_load_state('networkidle', timeout=timeout)
                safe_print("✅ 頁面已重新載入")
            except Exception:
                # 如果沒有導航，至少等待一下讓表單提交完成
                wait_time = 1.0 if self.fast_mode else 2.0
                time.sleep(wait_time)
            
            # 檢查是否有錯誤訊息顯示在頁面上
            try:
                msg_span = self.frame.locator('#spanMSG')
                if msg_span.count() > 0:
                    msg_text = msg_span.text_content()
                    if msg_text and msg_text.strip():
                        safe_print(f"📋 TCS 系統訊息: {msg_text}")
            except Exception:
                pass
            
            if dialog_messages:
                safe_print(f"✅ 已處理 {len(dialog_messages)} 個對話框")
            else:
                safe_print("✅ 已點擊儲存按鈕")
                
        except Exception as e:
            safe_print(f"⚠️  儲存過程中的警告: {e}")
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
            safe_print(f"📸 已截取 {screenshot_type}")
            safe_print(f"   檔案路徑: {abs_path}")
            
            return str(abs_path)
        except Exception as e:
            safe_print(f"❌ 截圖失敗: {e}")
            import traceback
            traceback.print_exc()
            raise

    def close(self):
        """關閉瀏覽器"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        safe_print("✅ 已關閉瀏覽器")


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
        tcs.start(headless=False, dry_run=True, fast_mode=True)  # 預設 dry_run，啟用快速模式
        tcs.fill_time_entries('20251124', test_entries)
        
        # 填寫完畢後截圖
        screenshot_path = tcs.screenshot(frame_only=True, full_page=True)
        safe_print(f"✅ 已儲存截圖: {screenshot_path}")
        
        tcs.preview_before_save()
        tcs.save()
        # 快速模式：減少等待時間
        wait_time = 1.0 if tcs.fast_mode else 3.0
        time.sleep(wait_time)  # 等待儲存完成
    except Exception as e:
        safe_print(f"❌ 錯誤: {e}")
    finally:
        tcs.close()


if __name__ == '__main__':
    main()

