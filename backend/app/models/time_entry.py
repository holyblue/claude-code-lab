"""
TimeEntry model for time tracking system.

Time entries are the core records of work performed on projects.
Each entry tracks date, project, hours, and work description.
"""

from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.database import Base


class TimeEntry(Base):
    """
    TimeEntry model for recording daily work hours.

    This is the core model of the time tracking system. Each entry represents
    work performed on a specific date for a specific project.

    Attributes:
        id: Primary key
        date: Date when work was performed
        project_id: Foreign key to projects table
        account_group_id: Foreign key to account_groups table
        work_category_id: Foreign key to work_categories table
        hours: Hours worked (supports 0.5 increments, e.g., 0.5, 1.0, 4.5, 7.5)
        description: Work description (supports Markdown format)
        account_item: Optional account item description
        display_order: Order for displaying entries on the same date
        created_at: Timestamp when entry was created
        updated_at: Timestamp when entry was last updated
    """

    __tablename__ = "time_entries"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Required Fields
    date = Column(Date, nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    account_group_id = Column(Integer, ForeignKey("account_groups.id"), nullable=False)
    work_category_id = Column(Integer, ForeignKey("work_categories.id"), nullable=False)
    hours = Column(Numeric(5, 2), nullable=False)  # Max 99.99 hours, supports 0.5 increments
    description = Column(String, nullable=False)  # Supports Markdown

    # Optional Fields
    account_item = Column(String(200), nullable=True)
    display_order = Column(Integer, nullable=False, default=0)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships (will be populated when all models are created)
    # project = relationship("Project", back_populates="time_entries")
    # account_group = relationship("AccountGroup", back_populates="time_entries")
    # work_category = relationship("WorkCategory", back_populates="time_entries")

    # Additional indexes for common queries
    __table_args__ = (
        Index('idx_time_entry_date_project', 'date', 'project_id'),
    )

    def __repr__(self):
        return f"<TimeEntry(id={self.id}, date={self.date}, hours={self.hours})>"
