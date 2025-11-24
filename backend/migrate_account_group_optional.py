"""
Database migration: Make account_group_id optional in time_entries table.

This script modifies the time_entries table to allow NULL values for account_group_id.
"""

import sqlite3
import os

def migrate_database():
    """Make account_group_id nullable in time_entries table."""
    
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    print(f"📂 Database path: {db_path}")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # SQLite doesn't support ALTER COLUMN directly
        # We need to recreate the table
        
        print("1. Creating backup of time_entries table...")
        cursor.execute("""
            CREATE TABLE time_entries_backup AS 
            SELECT * FROM time_entries
        """)
        conn.commit()
        print("   ✓ Backup created")
        
        print("\n2. Dropping original time_entries table...")
        cursor.execute("DROP TABLE time_entries")
        conn.commit()
        print("   ✓ Original table dropped")
        
        print("\n3. Creating new time_entries table (account_group_id nullable)...")
        cursor.execute("""
            CREATE TABLE time_entries (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                project_id INTEGER NOT NULL,
                account_group_id INTEGER,
                work_category_id INTEGER NOT NULL,
                hours NUMERIC(5, 2) NOT NULL,
                description VARCHAR NOT NULL,
                account_item VARCHAR(200),
                display_order INTEGER NOT NULL DEFAULT 0,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                FOREIGN KEY(project_id) REFERENCES projects (id),
                FOREIGN KEY(account_group_id) REFERENCES account_groups (id),
                FOREIGN KEY(work_category_id) REFERENCES work_categories (id)
            )
        """)
        conn.commit()
        print("   ✓ New table created")
        
        print("\n4. Creating indexes...")
        cursor.execute("""
            CREATE INDEX idx_time_entries_date ON time_entries(date)
        """)
        cursor.execute("""
            CREATE INDEX idx_time_entries_project ON time_entries(project_id)
        """)
        cursor.execute("""
            CREATE INDEX idx_time_entry_date_project ON time_entries(date, project_id)
        """)
        conn.commit()
        print("   ✓ Indexes created")
        
        print("\n5. Restoring data from backup...")
        cursor.execute("""
            INSERT INTO time_entries 
            SELECT * FROM time_entries_backup
        """)
        conn.commit()
        
        # Check how many records were restored
        cursor.execute("SELECT COUNT(*) FROM time_entries")
        count = cursor.fetchone()[0]
        print(f"   ✓ Restored {count} records")
        
        print("\n6. Dropping backup table...")
        cursor.execute("DROP TABLE time_entries_backup")
        conn.commit()
        print("   ✓ Backup table dropped")
        
        print("\n7. Verifying schema...")
        cursor.execute("PRAGMA table_info(time_entries)")
        columns = cursor.fetchall()
        
        for col in columns:
            col_id, name, type_, notnull, default, pk = col
            if name == 'account_group_id':
                nullable = "NULL" if notnull == 0 else "NOT NULL"
                print(f"   account_group_id: {type_} {nullable}")
                if notnull == 0:
                    print("   ✅ account_group_id is now nullable!")
                else:
                    print("   ❌ Failed: account_group_id is still NOT NULL")
                    return False
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("\nRolling back...")
        try:
            cursor.execute("DROP TABLE IF EXISTS time_entries")
            cursor.execute("ALTER TABLE time_entries_backup RENAME TO time_entries")
            conn.commit()
            print("✓ Rollback completed")
        except:
            print("❌ Rollback failed - please restore from backup manually")
        finally:
            conn.close()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration: Make account_group_id Optional")
    print("=" * 60)
    print()
    
    success = migrate_database()
    
    if success:
        print("\n✅ 模組欄位已改為選填！")
        print("現在可以新增工時記錄而不選擇模組。")
    else:
        print("\n❌ Migration failed!")
        print("Please check the error messages above.")

