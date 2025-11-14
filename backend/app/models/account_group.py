"""
AccountGroup model for time tracking system.

Account groups represent organizational units or cost centers that time
entries are charged to (e.g., A00 中概全權, O18 數據智能應用科).
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class AccountGroup(Base):
    """
    AccountGroup model for organizing time entries by business unit.

    Attributes:
        id: Primary key
        code: Account group code (e.g., A00, O18)
        name: Account group name (e.g., 中概全權)
        is_default: Whether this is a commonly used account group
        created_at: Timestamp when account group was created
        updated_at: Timestamp when account group was last updated
    """

    __tablename__ = "account_groups"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Required Fields
    code = Column(String(50), nullable=False)
    name = Column(String(200), nullable=False)

    # Optional Fields
    is_default = Column(Boolean, nullable=False, default=False)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Unique constraint on combination of code and name
    __table_args__ = (
        UniqueConstraint('code', 'name', name='uq_account_group_code_name'),
    )

    # Relationships (will be populated when related models are created)
    # time_entries = relationship("TimeEntry", back_populates="account_group")

    def __repr__(self):
        return f"<AccountGroup(id={self.id}, code='{self.code}', name='{self.name}')>"

    @property
    def full_name(self):
        """Return full name as 'code name' (e.g., 'A00 中概全權')."""
        return f"{self.code} {self.name}"
