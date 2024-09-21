from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from src.db.models.classinfo import ClassInfo
from typing import List



__all__ = ("Group",)


# creatae a base class (can't use DeclarativeBase directly)
class Base(DeclarativeBase):
    pass

class Group(Base):

    __tablename__ = "Groups"

    group_id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[str] = mapped_column(ForeignKey("Courses.course_id"))
    group_type:  Mapped[str] = mapped_column(String(9))

    # Relationship with ClassInfo
    classes: Mapped[List["ClassInfo"]] = relationship("ClassInfo", back_populates="group")
    # Relationship with Course
    course: Mapped["Course"] = relationship("Course", back_populates="groups") # type: ignore

    # Lazy importing to avoid circular importing
    def get_course(self):
        from src.db.models.course import Course
        return Course

