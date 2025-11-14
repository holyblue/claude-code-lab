"""
WorkTemplate model for time tracking system.

Work templates allow users to save commonly used work entries as templates
for quick creation of time entries.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class WorkTemplate(Base):
    """
    WorkTemplate model for storing reusable work entry templates.

    Templates help users quickly create time entries for repetitive tasks
    (e.g., daily standup meetings, code reviews).

    Attributes:
        id: Primary key
        name: Template name (e.g., "每日站會", "代碼審查")
        project_id: Optional default project
        account_group_id: Optional default account group
        work_category_id: Optional default work category
        default_hours: Optional default hours (e.g., 0.5 for standup)
        description_template: Template text for work description
        created_at: Timestamp when template was created
        updated_at: Timestamp when template was last updated
    """

    __tablename__ = "work_templates"

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Required Fields
    name = Column(String(200), nullable=False)

    # Optional Fields (for template defaults)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    account_group_id = Column(Integer, ForeignKey("account_groups.id"), nullable=True)
    work_category_id = Column(Integer, ForeignKey("work_categories.id"), nullable=True)
    default_hours = Column(Numeric(5, 2), nullable=True)
    description_template = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships (will be populated when needed)
    # project = relationship("Project")
    # account_group = relationship("AccountGroup")
    # work_category = relationship("WorkCategory")

    def __repr__(self):
        return f"<WorkTemplate(id={self.id}, name='{self.name}')>"
