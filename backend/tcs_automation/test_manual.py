"""
TCS 手動測試腳本
預設為 DRY RUN 模式，需明確指定才會真正寫入資料
"""
import argparse
import sys
from datetime import datetime
from tcs_automation import TCSAutomation


def confirm_write():
    """確認是否真的要寫入 TCS 系統"""
    print("\n" + "=" * 60)
    print("⚠️  警告: 即將寫入真實 TCS 系統")
    print("=" * 60)
    print("這將會修改您的工時記錄！")
    print("=" * 60)
    
    response = input("\n請輸入 'YES' 確認繼續（其他任何輸入將取消）: ")
    return response.strip() == 'YES'


def main():
    parser = argparse.ArgumentParser(
        description='TCS 自動填寫測試腳本（預設 DRY RUN 模式）',
        epilog='⚠️  預設為安全模式，不會真正寫入資料'
    )
    parser.add_argument(
        '--date',
        type=str,
        default=datetime.now().strftime('%Y%m%d'),
        help='日期（格式: YYYYMMDD，預設今天）'
    )
    parser.add_argument(
        '--no-dry-run',
        action='store_true',
        help='關閉 DRY RUN 模式（將真正寫入資料）'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='使用無頭模式'
    )
    
    args = parser.parse_args()
    
    # 預設為 dry_run
    dry_run = not args.no_dry_run
    
    # 如果要真正寫入，需要確認
    if not dry_run:
        if not confirm_write():
            print("❌ 已取消操作")
            sys.exit(0)
    
    # 測試資料
    test_entries = [
        {
            'project_code': '商2025智001',
            'account_group': 'A00',
            'work_category': 'A07',
            'hours': 4.0,
            'description': '- [x] TCS 自動化測試\n- [x] 系統整合測試',
            'requirement_no': '',
            'progress_rate': 0
        },
        {
            'project_code': '商2025智001',
            'account_group': 'A00',
            'work_category': 'A07',
            'hours': 3.5,
            'description': '- [x] 文檔撰寫\n- [x] Code Review',
            'requirement_no': '',
            'progress_rate': 0
        }
    ]
    
    # 顯示將要填寫的資料摘要
    print("\n" + "=" * 60)
    print("資料摘要")
    print("=" * 60)
    print(f"日期: {args.date}")
    print(f"模式: {'DRY RUN (安全模式)' if dry_run else '真實寫入'}")
    print(f"工時記錄數: {len(test_entries)}")
    total_hours = sum(e['hours'] for e in test_entries)
    print(f"總工時: {total_hours} 小時")
    print("\n記錄明細:")
    for idx, entry in enumerate(test_entries, 1):
        print(f"  {idx}. {entry['project_code']} - {entry['hours']}h")
    print("=" * 60 + "\n")
    
    # 執行自動填寫
    tcs = TCSAutomation()
    try:
        print("啟動瀏覽器...")
        tcs.start(headless=args.headless, dry_run=dry_run)
        
        print(f"\n填寫 {args.date} 的工時記錄...")
        tcs.fill_time_entries(args.date, test_entries)
        
        # 填寫完畢後截圖
        print("\n📸 正在截取填寫完畢的畫面...")
        screenshot_path = tcs.screenshot(frame_only=True, full_page=True)
        print(f"✅ 截圖已儲存: {screenshot_path}")
        
        tcs.preview_before_save()
        tcs.save()
        
        import time
        time.sleep(3)  # 等待儲存完成
        
        if dry_run:
            print("\n✅ DRY RUN 完成：未真正儲存資料")
        else:
            print("\n✅ 完成：已儲存到 TCS 系統")
            
    except KeyboardInterrupt:
        print("\n\n❌ 使用者中斷操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        tcs.close()


if __name__ == '__main__':
    main()

