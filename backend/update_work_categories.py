"""
Update work categories script.

This script updates the work_categories table with the new comprehensive list.
"""

from app.database import SessionLocal
from app.models import WorkCategory


def update_work_categories():
    """Update work categories in the database."""
    db = SessionLocal()
    try:
        print("Updating work categories...")
        
        # Delete existing work categories
        deleted_count = db.query(WorkCategory).delete()
        print(f"  Deleted {deleted_count} existing work categories")
        
        # Insert new work categories
        work_categories = [
            # 專案管理
            WorkCategory(code="A02", name="進度追蹤", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="A03", name="工作溝通協調", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="A07", name="其它", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="A08", name="商模", deduct_approved_hours=False, is_default=True),  # 不扣抵
            WorkCategory(code="A09", name="工時審議", deduct_approved_hours=True, is_default=True),
            
            # 系統分析
            WorkCategory(code="B01", name="需求搜集、訪談", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="B02", name="需求分析", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="B03", name="需求規格撰寫、更新、確認", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="B04", name="其它", deduct_approved_hours=True, is_default=True),
            
            # 系統設計
            WorkCategory(code="C02", name="系統架構設計", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="C04", name="設計規格撰寫、更新、確認", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="C06", name="其它", deduct_approved_hours=True, is_default=True),
            
            # 程式開發
            WorkCategory(code="D01", name="程式規格設計與審查", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="D02", name="開發環境建置、維護", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="D03", name="程式撰寫", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="D04", name="除錯;測試", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="D05", name="其它", deduct_approved_hours=True, is_default=True),
            
            # 系統測試
            WorkCategory(code="E02", name="測試案例撰寫", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="E03", name="環境建置、維護", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="E07", name="除錯", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="E09", name="其它", deduct_approved_hours=True, is_default=True),
            
            # 使用者驗收測試
            WorkCategory(code="F01", name="測試計劃", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="F02", name="環境建置、維護", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="F07", name="除錯", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="F10", name="其它", deduct_approved_hours=True, is_default=True),
            
            # 一般行政事務
            WorkCategory(code="I01", name="出席會議", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="I04", name="教育訓練", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="I05", name="支援他人(含部門內及跨部門)", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="I06", name="臨時交辦事務", deduct_approved_hours=True, is_default=True),
            WorkCategory(code="I07", name="休假(年休、病假、事假)", deduct_approved_hours=False, is_default=True),  # 不扣抵
            WorkCategory(code="I08", name="其它", deduct_approved_hours=True, is_default=True),
        ]
        
        db.add_all(work_categories)
        db.commit()
        
        print(f"  ✓ Inserted {len(work_categories)} new work categories")
        
        # Display categories by group
        print("\n工作類別分組：")
        print("\n專案管理 (5):")
        for cat in work_categories[0:5]:
            deduct = "扣抵" if cat.deduct_approved_hours else "不扣抵"
            print(f"  {cat.code} - {cat.name} ({deduct})")
        
        print("\n系統分析 (4):")
        for cat in work_categories[5:9]:
            print(f"  {cat.code} - {cat.name}")
        
        print("\n系統設計 (3):")
        for cat in work_categories[9:12]:
            print(f"  {cat.code} - {cat.name}")
        
        print("\n程式開發 (5):")
        for cat in work_categories[12:17]:
            print(f"  {cat.code} - {cat.name}")
        
        print("\n系統測試 (4):")
        for cat in work_categories[17:21]:
            print(f"  {cat.code} - {cat.name}")
        
        print("\n使用者驗收測試 (4):")
        for cat in work_categories[21:25]:
            print(f"  {cat.code} - {cat.name}")
        
        print("\n一般行政事務 (6):")
        for cat in work_categories[25:31]:
            deduct = "扣抵" if cat.deduct_approved_hours else "不扣抵"
            print(f"  {cat.code} - {cat.name} ({deduct})")
        
        print(f"\n✅ 總計: {len(work_categories)} 個工作類別")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("更新工作類別")
    print("=" * 60)
    update_work_categories()
    print("=" * 60)

