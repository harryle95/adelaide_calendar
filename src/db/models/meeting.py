from sqlalchemy import String, ForeignKey, Time
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

__all__ = ("Meeting",)

# creatae a base class (can't use DeclarativeBase directly)
class Base(DeclarativeBase):
    pass

class Meeting(Base):

    __tablename__ = "Meetings"

    meeting_id: Mapped[int] = mapped_column(primary_key=True)
    class_nbr: Mapped[int] = mapped_column(ForeignKey("ClassInfo.class_nbr"))
    dates: Mapped[str] = mapped_column(String(15))
    days: Mapped[str] = mapped_column(String(9))
    start_time: Mapped[str] = mapped_column(Time)
    end_time: Mapped[str] = mapped_column(Time)
    location: Mapped[str] = mapped_column(String(100))
    
    #  relationship to ClassInfo
    class_info: Mapped["ClassInfo"] = relationship("ClassInfo", back_populates="meetings") # type: ignore

    # Lazy importing to avoid circular importing
    def get_course(self):
        from src.db.models.course import Course
        return Course

    def get_group(self):
        from src.db.models.group import Group
        return Group
    
    def get_classinfo(self):
        from src.db.models.classinfo import ClassInfo
        return ClassInfo

