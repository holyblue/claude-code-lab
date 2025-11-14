"""
WorkCategory model for time tracking system.

Work categories classify the type of work performed (e.g., A07 其它, A08 商模).
Each category has a flag indicating whether it deducts from approved hours budget.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class WorkCategory(Base):
    """
    WorkCategory model for classifying types of work.

    Business Logic:
    - deduct_approved_hours=True: Time deducts from project approved hours (A07, B04)
    - deduct_approved_hours=False: Time counts but doesn't deduct from budget (A08 商模, I07 休假)

    Attributes:
        id: Primary key
        code: Work category code (e.g., A07, A08)
        name: Work category name (e.g., 其它, 商模)
        deduct_approved_hours: Whether this category deducts from approved hours budget
        is_default: Whether this is a commonly used category
        created_at: Timestamp when work category was created
        updated_at: Timestamp when work category was last updated
    """

    __tablename__ = "work_categories"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Required Fields
    code = Column(String(50), nullable=False)
    name = Column(String(200), nullable=False)

    # Business Logic Field
    deduct_approved_hours = Column(Boolean, nullable=False, default=True)

    # Optional Fields
    is_default = Column(Boolean, nullable=False, default=False)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Unique constraint on combination of code and name
    __table_args__ = (
        UniqueConstraint('code', 'name', name='uq_work_category_code_name'),
    )

    # Relationships (will be populated when related models are created)
    # time_entries = relationship("TimeEntry", back_populates="work_category")

    def __repr__(self):
        return f"<WorkCategory(id={self.id}, code='{self.code}', name='{self.name}', deduct={self.deduct_approved_hours})>"

    @property
    def full_name(self):
        """Return full name as 'code name' (e.g., 'A07 其它')."""
        return f"{self.code} {self.name}"
