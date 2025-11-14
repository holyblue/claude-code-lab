"""
Setting model for time tracking system.

System settings store configuration values that can be modified at runtime
(e.g., language, theme, work hours standards).
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class Setting(Base):
    """
    Setting model for system configuration.

    Stores key-value pairs for system settings. Each setting has a unique key.

    Common settings:
    - language: zh-TW, en-US
    - theme: light, dark
    - timezone: UTC+8
    - standard_work_hours: 7.5
    - max_work_hours: 12
    - min_time_unit: 0.5
    - work_days: 1,2,3,4,5 (Monday to Friday)

    Attributes:
        id: Primary key
        key: Unique setting key
        value: Setting value (stored as string)
        updated_at: Timestamp when setting was last updated
    """

    __tablename__ = "settings"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Required Fields
    key = Column(String(100), nullable=False, unique=True, index=True)
    value = Column(String, nullable=True)

    # Timestamp
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Setting(key='{self.key}', value='{self.value}')>"
