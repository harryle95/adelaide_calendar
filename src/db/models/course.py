from src.db.models.group import Group
from sqlalchemy import String, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

__all__ = ("Course",)


# creatae a base class (can't use DeclarativeBase directly)
class Base(DeclarativeBase):
    pass

# PRIMARY KEY: class_nbr because the same class on diff. sems has the same course_id
class Course(Base):

    __tablename__ = "Courses"

    # composite key columns: course_id, course_offer_nbr, term, year
    course_id:Mapped[str] = mapped_column(String(10), nullable=False)
    course_offer_nbr:  Mapped[int] = mapped_column(nullable=False)
    year: Mapped[str] = mapped_column(String(4), nullable=False)
    term: Mapped[str] = mapped_column(String(5), nullable=False)
    term_descr: Mapped[str] = mapped_column(String(10))
    subject: Mapped[str] = mapped_column(String(10))
    catalogue_nbr: Mapped[str] = mapped_column(String(10))
    acad_career: Mapped[str] = mapped_column(String(10))
    acad_career_descr: Mapped[str] = mapped_column(String(15))
    course_title: Mapped[str] = mapped_column(String(200))
    units: Mapped[int] = mapped_column(Integer)
    campus: Mapped[str] = mapped_column(String(30))
    class_nbr: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint('course_id', 'course_offer_nbr', 'year','term'),
    )
    # Relationship with Group
    groups: Mapped[List["Group"]] = relationship("Group", back_populates="course") 
