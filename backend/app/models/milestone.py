"""
Milestone model for time tracking system.

Milestones represent key project phases and deadlines.
Each milestone has a name, start date, and end date.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.database import Base


class Milestone(Base):
    """
    Milestone model for tracking project phases.

    Attributes:
        id: Primary key
        project_id: Foreign key to projects table
        name: Milestone name (e.g., "需求訪談", "系統分析 SA")
        start_date: Start date of the milestone
        end_date: End date of the milestone
        description: Optional description
        display_order: Order for displaying milestones (default: 0)
        created_at: Timestamp when milestone was created
        updated_at: Timestamp when milestone was last updated
    """

    __tablename__ = "milestones"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Required Fields
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # Optional Fields
    description = Column(String, nullable=True)
    display_order = Column(Integer, nullable=False, default=0)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="milestones")

    def __repr__(self):
        return f"<Milestone(id={self.id}, name='{self.name}', project_id={self.project_id})>"


# Create indexes
Index("idx_milestones_project", Milestone.project_id)
Index("idx_milestones_dates", Milestone.start_date, Milestone.end_date)

