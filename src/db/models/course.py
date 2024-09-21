from src.db.models.group import Group
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

__all__ = ("Course",)


# creatae a base class (can't use DeclarativeBase directly)
class Base(DeclarativeBase):
    pass

# PRIMARY KEY: class_nbr because the same class on diff. sems has the same course_id
class Course(Base):

    __tablename__ = "Courses"

    course_id:Mapped[str] = mapped_column(String(10))
    course_offer_nbr:  Mapped[int] = mapped_column()
    year: Mapped[str] = mapped_column(String(4))
    term: Mapped[str] = mapped_column(String(5))
    term_descr: Mapped[str] = mapped_column(String(10))
    subject: Mapped[str] = mapped_column(String(10))
    catalogue_nbr: Mapped[str] = mapped_column(String(10))
    acad_career: Mapped[str] = mapped_column(String(10))
    acad_career_descr: Mapped[str] = mapped_column(String(15))
    course_title: Mapped[str] = mapped_column(String(200))
    units: Mapped[int] = mapped_column()
    campus: Mapped[str] = mapped_column(String(30))
    class_nbr: Mapped[int] = mapped_column(primary_key=True)

    # Relationship with Group
    groups: Mapped[List["Group"]] = relationship("Group", back_populates="course") 
