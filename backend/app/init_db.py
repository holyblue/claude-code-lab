"""
Database initialization script.

This script creates all database tables and inserts initial seed data
for account groups, work categories, and system settings.
"""

from sqlalchemy.orm import Session

from app.database import engine, Base, SessionLocal
from app.models import (
    Project,
    AccountGroup,
    WorkCategory,
    TimeEntry,
    WorkTemplate,
    Setting,
)


def init_db():
    """
    Initialize database by creating all tables and inserting seed data.

    This function should be called when the application starts for the first time.
    """
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")

    # Insert seed data
    db = SessionLocal()
    try:
        insert_seed_data(db)
        print("✓ Seed data inserted")
    finally:
        db.close()


def insert_seed_data(db: Session):
    """
    Insert initial seed data into the database.

    Args:
        db: Database session
    """
    # Check if seed data already exists
    if db.query(AccountGroup).count() > 0:
        print("  Seed data already exists, skipping...")
        return

    print("  Inserting seed data...")

    # 1. Insert Account Groups
    account_groups = [
        AccountGroup(code="A00", name="中概全權", is_default=True),
        AccountGroup(code="O18", name="數據智能應用科", is_default=True),
    ]
    db.add_all(account_groups)
    db.commit()
    print(f"  ✓ Inserted {len(account_groups)} account groups")

    # 2. Insert Work Categories
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
    print(f"  ✓ Inserted {len(work_categories)} work categories")

    # 3. Insert System Settings
    settings = [
        Setting(key="language", value="zh-TW"),
        Setting(key="theme", value="light"),
        Setting(key="timezone", value="UTC+8"),
        Setting(key="standard_work_hours", value="7.5"),
        Setting(key="max_work_hours", value="12"),
        Setting(key="min_time_unit", value="0.5"),
        Setting(key="work_days", value="1,2,3,4,5"),  # Monday to Friday
        Setting(key="show_weekends", value="true"),
    ]
    db.add_all(settings)
    db.commit()
    print(f"  ✓ Inserted {len(settings)} system settings")

    print("  ✓ All seed data inserted successfully")


if __name__ == "__main__":
    """
    Run this script directly to initialize the database.

    Usage:
        python -m app.init_db
    """
    print("=" * 60)
    print("Time Tracking System - Database Initialization")
    print("=" * 60)
    init_db()
    print("\n✅ Database initialization completed!")
    print("=" * 60)
