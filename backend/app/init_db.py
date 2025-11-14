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
        # A07: 其它 - 扣抵核定工時
        WorkCategory(code="A07", name="其它", deduct_approved_hours=True, is_default=True),
        # A08: 商模 - 不扣抵核定工時（重要業務規則）
        WorkCategory(code="A08", name="商模", deduct_approved_hours=False, is_default=True),
        # B04: 其它 - 扣抵核定工時
        WorkCategory(code="B04", name="其它", deduct_approved_hours=True, is_default=True),
        # I07: 休假 - 不扣抵核定工時
        WorkCategory(
            code="I07",
            name="休假（休假、病假、事假等）",
            deduct_approved_hours=False,
            is_default=True
        ),
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
