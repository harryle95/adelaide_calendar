from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from src.db.models.meeting import Meeting

__all__ = ("ClassInfo",)

# creatae a base class (can't use DeclarativeBase directly)
class Base(DeclarativeBase):
    pass

class ClassInfo(Base):

    __tablename__ = "ClassInfo"

    class_nbr: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("Groups.group_id"))
    # section = SE01/SE02/WR01...
    section: Mapped[str] = mapped_column(String(4))
    size: Mapped[int] = mapped_column()
    enrolled: Mapped[int] = mapped_column()
    available: Mapped[int] = mapped_column()
    institution: Mapped[str] = mapped_column(String(30))
    component: Mapped[str] = mapped_column(String(50))

    # Relationship with Group
    group: Mapped["Group"] = relationship("Group", back_populates="classes") # type: ignore
    
    # Relationship with Meeting
    meetings: Mapped[list['Meeting']] = relationship('Meeting', back_populates='class_info')

    # Lazy importing to avoid circular importing
    def get_group(self):
        from src.db.models.group import Group
        return Group
    