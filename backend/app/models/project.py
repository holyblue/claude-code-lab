"""
Project model for time tracking system.

Projects represent the work assignments that time entries are recorded against.
Each project has a code, requirement code, name, and optional approved man-days budget.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Project(Base):
    """
    Project model for tracking work projects.

    Attributes:
        id: Primary key
        code: Unique project code (e.g., 需2025單001)
        requirement_code: Requirement code (e.g., R202511146001)
        name: Project name
        approved_man_days: Approved budget in man-days (1 man-day = 7.5 hours)
        default_account_group_id: Default account group for time entries
        default_work_category_id: Default work category for time entries
        description: Optional project description
        status: Project status (active/completed/archived)
        color: Color code for UI display (hex format)
        created_at: Timestamp when project was created
        updated_at: Timestamp when project was last updated
        deleted_at: Timestamp for soft delete (null if not deleted)
    """

    __tablename__ = "projects"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Required Fields
    code = Column(String(50), nullable=False, unique=True, index=True)
    requirement_code = Column(String(50), nullable=False)
    name = Column(String(200), nullable=False)

    # Optional Fields
    approved_man_days = Column(Numeric(10, 2), nullable=True)
    default_account_group_id = Column(Integer, ForeignKey("account_groups.id"), nullable=True)
    default_work_category_id = Column(Integer, ForeignKey("work_categories.id"), nullable=True)
    description = Column(String, nullable=True)

    # Status and Display
    status = Column(String(20), nullable=False, default="active")
    color = Column(String(7), nullable=False, default="#409EFF")

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships (will be populated when related models are created)
    # default_account_group = relationship("AccountGroup", foreign_keys=[default_account_group_id])
    # default_work_category = relationship("WorkCategory", foreign_keys=[default_work_category_id])
    # time_entries = relationship("TimeEntry", back_populates="project")
    milestones = relationship("Milestone", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, code='{self.code}', name='{self.name}')>"
